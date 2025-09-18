# src/ingestion/load.py

import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DATA_PATH = "data/"

def load_documents():
    """
    Loads documents from the source documents directory.
    For now, it's configured to load PDF files.
    """
    # Initialize the DirectoryLoader to load .pdf files
    loader = DirectoryLoader(DATA_PATH, glob="**/*.pdf", loader_cls=PyPDFLoader)
    
    # Load the documents
    documents = loader.load()
    
    print(f"Loaded {len(documents)} document(s).")
    return documents

# A simple test to run this script directly
if __name__ == "__main__":
    documents = load_documents()
    # Print the first 200 characters of the first document's content
    if documents:
        print("\nSample content from the first document:")
        print(documents[0].page_content[:200])

