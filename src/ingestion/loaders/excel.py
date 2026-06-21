# src/ingestion/loaders/excel.py
import pandas as pd
from langchain_classic.schema import Document

def load_excel(file_path):
    """
    Loads Excel or CSV files and converts each row into a text chunk.
    Best for "Lookup" questions (e.g., "What is Alice's role?").
    """
    print(f"   📊 Processing table data from {file_path}...")
    
    # 1. Detect format and load into Pandas DataFrame
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    else:
        # Requires 'openpyxl' installed
        df = pd.read_excel(file_path)

    # 2. Clean data (fill NaNs)
    df = df.fillna("")

    documents = []
    
    # 3. Iterate over rows
    for index, row in df.iterrows():
        # Create a text representation of the row
        # Format: "Column: Value \n Column: Value"
        content_parts = []
        for col_name, val in row.items():
            # Skip empty cells to save tokens
            if str(val).strip():
                content_parts.append(f"{col_name}: {val}")
        
        row_text = "\n".join(content_parts)
        
        # Create LangChain Document
        # We store the Row Number in metadata so we can find it later
        doc = Document(
            page_content=row_text,
            metadata={
                "source": file_path,
                "row": index + 1
            }
        )
        documents.append(doc)

    return documents
