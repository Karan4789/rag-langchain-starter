# src/ingestion/loaders/load.py

import os
from .loaders.pdf import load_pdf
from .loaders.excel import load_excel

def load_documents(data_dir="data"):
    all_documents = []
    
    if not os.path.exists(data_dir):
        return []
    
    files = [f for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f))]
    print(f"📂 Found {len(files)} files in '{data_dir}'")

    for filename in files:
        file_path = os.path.join(data_dir, filename)
        ext = os.path.splitext(filename)[1].lower()

        # PDF Support
        if ext == ".pdf":
            try:
                docs = load_pdf(file_path)
                all_documents.extend(docs)
                print(f"   ✅ Loaded {len(docs)} chunks from {filename}")
            except Exception as e:
                print(f"   ❌ Failed to load {filename}: {e}")

        # Excel Support
        elif ext in [".xlsx", ".xls", ".csv"]:
            try:
                docs = load_excel(file_path)
                all_documents.extend(docs)
                print(f"   ✅ Loaded {len(docs)} rows from {filename}")
            except Exception as e:
                print(f"   ❌ Failed to load Excel {filename}: {e}")
        
        elif ext in [".docx", ".pptx"]:
            print(f"   ⏳ Office support coming soon for: {filename}")
            
        else:
            print(f"   ⚠️ Skipping: {filename}")
            
    return all_documents
