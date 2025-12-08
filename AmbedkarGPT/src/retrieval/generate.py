import argparse
import os
import sys

# Add the parent directory of 'retrieval' (which is 'src') to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM as Ollama
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

from ingestion.embed import get_embedding_function

CHROMA_PATH = "db/"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {input}
"""

def start_qa_session():
    """
    Initializes the retrieval chain and enters an interactive Q&A loop.
    This function will be called by main.py.
    """
    print("\n🚀 Starting interactive Q&A session...")

    # Prepare the retriever and the model
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    retriever = db.as_retriever(search_kwargs={"k": 5})

    model = Ollama(model="mistral:latest")
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    document_chain = create_stuff_documents_chain(model, prompt)
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    # Start the interactive loop
    while True:
        try:
            query_text = input("\n> Enter your question (or type 'exit' to quit): ")
            if query_text.lower().strip() == 'exit':
                break
            if not query_text.strip():
                continue

            # Invoke the chain and print the answer
            response = retrieval_chain.invoke({"input": query_text})
            print("\n--- Answer ---\n")
            print(response["answer"])
            print("\n--------------\n")

        except KeyboardInterrupt:
            break
    print("\n✅ Q&A session ended.")


def main_cli():
    """
    The original command-line functionality of this script.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    
    # This part remains mostly the same for single-shot command line use
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    retriever = db.as_retriever(search_kwargs={"k": 5})
    model = Ollama(model="mistral:latest")
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    document_chain = create_stuff_documents_chain(model, prompt)
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    response = retrieval_chain.invoke({"input": query_text})
    print("--- RESPONSE ---")
    print(response["answer"])

if __name__ == "__main__":
    # This allows you to still run `python src/retrieval/generate.py "question"`
    main_cli()
