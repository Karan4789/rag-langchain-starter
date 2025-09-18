# src/ingestion/store.py

from langchain_community.vectorstores import Chroma


CHROMA_PATH = "db/"

def store_chunks(chunks, embedding_function):
    """
    Embeds the chunks and stores them in a ChromaDB vector store.

    Args:
        chunks: A list of document chunks from the splitting step.
        embedding_function: The embedding model to use.
    """
    # Create a new ChromaDB database from the documents
    db = Chroma.from_documents(
        chunks, 
        embedding_function, 
        persist_directory=CHROMA_PATH
    )
    
    print(f"Stored {len(chunks)} chunks in {CHROMA_PATH}.")
    return db
