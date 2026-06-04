import os
import sys
import shutil

sys.path.append(os.path.abspath('src'))

from src.ingestion.load import load_documents
from src.ingestion.embed import get_embedding_function
from src.ingestion.store import ingest_documents
from src.retrieval.generate import query_rag 

def clear_database():
    if os.path.exists("db/"):
        shutil.rmtree("db/")

def run_cli_pipeline(query):
    # 1. Ingest
    # (Optional: comment this out if you don't want to re-ingest every time)
    clear_database()
    print("🚀 Ingesting...")
    docs = load_documents()
    embed_fn = get_embedding_function()
    ingest_documents(docs, embed_fn)
    
    # 2. Query
    print(f"\n❓ Question: {query}")
    result = query_rag(query)
    
    print("\n💡 Answer:")
    print(result["answer"])
    
    print("\n📚 Sources:")
    for src in result["sources"]:
        print(f"- {src[:100]}...")

if __name__ == "__main__":
    # Default query if none provided
    q = sys.argv[1] if len(sys.argv) > 1 else "What is this about?"
    run_cli_pipeline(q)
