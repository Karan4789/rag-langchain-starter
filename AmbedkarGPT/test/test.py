
#For testing the ingestion Pipeline


import sys
import os

# Add the project root to the Python path
# This allows us to import from the 'src' directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.ingestion.load import load_documents
from src.ingestion.split import split_documents
from src.ingestion.embed import get_embedding_function
from src.ingestion.store import store_chunks

def main():
    """
    Runs the complete data ingestion and processing pipeline.
    1. Loads documents from the data directory.
    2. Splits the documents into manageable chunks.
    3. Initializes the embedding model.
    4. Stores the document chunks and their embeddings in ChromaDB.
    """
    print("Starting the ingestion pipeline...")
    
    # 1. Load documents
    documents = load_documents()
    if not documents:
        print("No documents found. Exiting.")
        return

    # 2. Split documents into chunks
    chunks = split_documents(documents)
    if not chunks:
        print("No chunks were created. Exiting.")
        return

    # 3. Initialize the embedding function
    embedding_function = get_embedding_function()

    # 4. Store the chunks in ChromaDB
    store_chunks(chunks, embedding_function)
    
    print("Ingestion pipeline completed successfully.")

if __name__ == "__main__":
    main()