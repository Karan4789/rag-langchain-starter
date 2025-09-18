# src/main.py

import sys
import os

sys.path.append(os.path.abspath('src'))

from ingestion.load import load_documents
from ingestion.split import split_documents
from ingestion.embed import get_embedding_function
from ingestion.store import store_chunks

def main():
    """
    Main function to run the full data ingestion pipeline.
    """
    print("🚀 Starting data ingestion pipeline...")
    
    # Step 1: Load documents
    documents = load_documents()
    
    # Step 2: Split documents into chunks
    chunks = split_documents(documents)
    
    # Step 3: Get the embedding function
    embedding_function = get_embedding_function()
    
    # Step 4: Embed and store chunks in ChromaDB
    db = store_chunks(chunks, embedding_function)
    
    print("✅ Pipeline finished successfully.")

if __name__ == "__main__":
    main()
