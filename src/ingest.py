import sys
import os

sys.path.append(os.path.abspath('src'))

from ingestion.load import load_documents
from ingestion.embed import get_embedding_function
from ingestion.store import ingest_documents 

def main():
    print("🚀 Starting data ingestion pipeline...")
    
    # Step 1: Load documents
    documents = load_documents()
    
    # Step 2: Get embedding function
    embedding_function = get_embedding_function()
    
    # Step 3: Ingest (Splitting is now handled internally)
    ingest_documents(documents, embedding_function)
    
    print("✅ Pipeline finished successfully.")

if __name__ == "__main__":
    main()
