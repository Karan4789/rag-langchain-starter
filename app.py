import os
import shutil
import sys
import argparse

# Add src to path so we can import modules
sys.path.append(os.path.abspath('src'))

from ingest import main as run_ingestion
from src.retrieval.generate import main as run_generation

CHROMA_PATH = "db/"

def clear_database():
    """Force delete the database to ensure we don't have duplicate data."""
    if os.path.exists(CHROMA_PATH):
        print(f"🗑️  Clearing existing database at {CHROMA_PATH}...")
        shutil.rmtree(CHROMA_PATH)
    else:
        print("✨ Database is already empty.")

def run_full_pipeline(query):
    # 1. Clear old data (Optional: remove this if you want to keep adding data)
    clear_database()

    # 2. Run Ingestion (main.py)
    print("\n--- STEP 1: INGESTION ---")
    try:
        run_ingestion()
    except Exception as e:
        print(f"❌ Ingestion failed: {e}")
        return

    # 3. Run Generation (generate.py) with Reranking
    print("\n--- STEP 2: RETRIEVAL & GENERATION ---")
    # We need to simulate CLI arguments for generate.py
    sys.argv = ["generate.py", query]
    try:
        run_generation()
    except Exception as e:
        print(f"❌ Generation failed: {e}")

if __name__ == "__main__":

    if len(sys.argv) > 1:
        user_query = sys.argv[1]
    else:
        user_query = "What is the main topic of these documents?"
        
    run_full_pipeline(user_query)
