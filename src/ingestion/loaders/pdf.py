# src/ingestion/loaders/pdf.py

import os
from langchain_community.document_loaders import PyMuPDFLoader

def load_pdf(file_path):
    """
    Loads a PDF using PyMuPDFLoader.
    """
    print(f"   📄 Using PyMuPDFLoader for {os.path.basename(file_path)}...")
    loader = PyMuPDFLoader(file_path)
    
    docs = loader.load()

    # Temporary checking for document type, can be improved with a more robust detection mechanism
    document_type = "book"

    for doc in docs:
        doc.metadata["file_type"] = "pdf"
        doc.metadata["document_type"] = document_type

    return docs

# return loader.load()
# document_type = detect_document_type(docs)