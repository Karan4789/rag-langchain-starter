import argparse
import os
import sys
from dotenv import load_dotenv

# Add parent directory to path if running directly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_classic.retrievers.document_compressors import FlashrankRerank
from langchain_classic.storage import LocalFileStore
from langchain_classic.storage._lc_store import create_kv_docstore
from langchain_classic.retrievers import ParentDocumentRetriever
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from utils.skill_loader import load_skill

from ingestion.embed import get_embedding_function
from core.config import (
    DB_FOLDER,
    PARENT_DOCS_FOLDER,
    CHROMA_COLLECTION_NAME,     
    CHILD_CHUNK_SIZE,
    PARENT_CHUNK_SIZE,
    RAG_PROMPT_TEMPLATE,
    USE_RERANKING,
    RERANKING_MODEL,
    LLM_MODEL,
    GROQ_API_KEY
)

load_dotenv()

def query_rag(query_text: str):
    """
    Core RAG logic. Accepts a query string and returns a dictionary with the answer and sources.
    """
    # 1. Setup Stores
    embedding_function = get_embedding_function()
    
    vectorstore = Chroma(
        collection_name=CHROMA_COLLECTION_NAME,
        persist_directory=DB_FOLDER,
        embedding_function=embedding_function
    )
    
    fs = LocalFileStore(PARENT_DOCS_FOLDER)
    store = create_kv_docstore(fs)

    # 2. Setup Retrievers
    child_splitter = RecursiveCharacterTextSplitter(chunk_size=CHILD_CHUNK_SIZE)
    parent_splitter = RecursiveCharacterTextSplitter(chunk_size=PARENT_CHUNK_SIZE)

    base_retriever = ParentDocumentRetriever(
        vectorstore=vectorstore,
        docstore=store,
        child_splitter=child_splitter,
        parent_splitter=parent_splitter,
    )

    # 3. Add Reranking if enabled
    if USE_RERANKING:
        compressor = FlashrankRerank(model=RERANKING_MODEL)
        compression_retriever = ContextualCompressionRetriever(
            base_compressor=compressor, 
            base_retriever=base_retriever
        )
        results = compression_retriever.invoke(query_text)
    else:
        results = base_retriever.invoke(query_text)

    # 4. Search & Answer
    if not results:
        return {
            "answer": "No relevant context found.", 
            "sources": []
        }
        
    document_type = results[0].metadata.get(
    "document_type",
    "general"
)
    skill = load_skill(document_type)

    context_text = "\n\n---\n\n".join([doc.page_content for doc in results])
    prompt_template = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)
    prompt = prompt_template.format(skill=skill,context=context_text, question=query_text)
    
    model = ChatGroq(model=LLM_MODEL, temperature=0.7, api_key=GROQ_API_KEY)
    response = model.invoke(prompt)

    # 5. Return Structured Data
    return {
        "answer": response.content,
        "sources": [doc.page_content for doc in results]
    }

def main():
    # CLI Entry Point
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", help="The query text.")
    args = parser.parse_args()
    
    result = query_rag(args.query_text)

    print("\n--- RESPONSE ---")
    print(result["answer"])
    
    print("\n--- SOURCES (Parent Docs) ---")
    for i, src in enumerate(result["sources"]):
        print(f"{i+1}. Preview: {src[:100]}...")

if __name__ == "__main__":
    main()
