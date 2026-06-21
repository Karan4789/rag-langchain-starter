# src/ingestion/loaders/pdf.py

import os
from langchain_community.document_loaders import PyMuPDFLoader

def load_pdf(file_path):
    """
    Loads a PDF using PyMuPDFLoader.
    """
    print(f"   📄 Using PyMuPDFLoader for {os.path.basename(file_path)}...")
    loader = PyMuPDFLoader(file_path)
    return loader.load()
