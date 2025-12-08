import argparse
import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import FlashrankRerank
from langchain.storage._lc_store import create_kv_docstore
from langchain.storage import LocalFileStore
from langchain.retrievers import ParentDocumentRetriever
from langchain.text_splitter import RecursiveCharacterTextSplitter

from ingestion.embed import get_embedding_function

load_dotenv()

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text

    # 1. Setup Same Stores as Ingestion
    embedding_function = get_embedding_function()
    
    vectorstore = Chroma(
        collection_name="split_parents",
        persist_directory="db/",
        embedding_function=embedding_function
    )
    fs = LocalFileStore("db/parent_docs")
    store = create_kv_docstore(fs)

    # 2. Re-initialize Parent Retriever
    # Use same splitters as ingestion to match the data structure
    child_splitter = RecursiveCharacterTextSplitter(chunk_size=400)
    parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000)

    base_retriever = ParentDocumentRetriever(
        vectorstore=vectorstore,
        docstore=store,
        child_splitter=child_splitter,
        parent_splitter=parent_splitter,
    )

    # 3. Add Reranking on top (Optional but recommended)
    # This reranks the PARENT chunks returned by the base retriever
    compressor = FlashrankRerank(model="ms-marco-MiniLM-L-12-v2")
    
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor, 
        base_retriever=base_retriever
    )

    # 4. Search
    results = compression_retriever.invoke(query_text)

    if not results:
        print("No relevant context found.")
        return

    context_text = "\n\n---\n\n".join([doc.page_content for doc in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    
    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
    response = model.invoke(prompt)

    print("\n--- RESPONSE ---")
    print(response.content)
    
    print("\n--- SOURCES (Parent Docs) ---")
    for i, doc in enumerate(results):
        print(f"{i+1}. Preview: {doc.page_content[:100]}...")

if __name__ == "__main__":
    main()
