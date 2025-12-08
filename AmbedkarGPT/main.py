import os
import sys

# Ensure the 'src' directory is in the Python path
sys.path.append(os.path.abspath('src'))

# --- Import your existing modules ---
from ingestion.load import load_documents
from ingestion.split import split_documents
from ingestion.embed import get_embedding_function
from ingestion.store import store_chunks
# Import the new Q&A session function from your generate script
from retrieval.generate import start_qa_session

CHROMA_PATH = "db/"

def run_ingestion_if_needed():
    """
    Checks if the database exists and runs the full ingestion pipeline if it doesn't.
    """
    if os.path.exists(CHROMA_PATH):
        print("✅ Database found. Skipping ingestion.")
        return

    print("🚀 Database not found. Starting data ingestion pipeline...")
    
    # Step 1: Load documents
    documents = load_documents()
    
    # Step 2: Split documents into chunks
    chunks = split_documents(documents)
    
    # Step 3: Get the embedding function
    embedding_function = get_embedding_function()
    
    # Step 4: Embed and store chunks in ChromaDB
    store_chunks(chunks, embedding_function)
    
    print("✅ Ingestion pipeline finished successfully.")


if __name__ == "__main__":
    # First, run the ingestion pipeline only if the DB doesn't exist.
    run_ingestion_if_needed()
    
    # Now, start the interactive Q&A session using the logic from generate.py.
    start_qa_session()
