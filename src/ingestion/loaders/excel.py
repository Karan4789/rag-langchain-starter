# src/ingestion/loaders/excel.py

import os
import json
import pandas as pd
from langchain_classic.schema import Document


def load_excel(file_path):
    """
    Loads CSV/Excel files and converts each row into a JSON document.

    Example stored content:

    {
        "Employee": "Alice",
        "Department": "HR",
        "Salary": 50000
    }
    """

    print(f"   📊 Processing table data from {os.path.basename(file_path)}...")

    # Load dataframe
    if file_path.lower().endswith(".csv"):
        df = pd.read_csv(file_path)
        file_type = "csv"
    else:
        df = pd.read_excel(file_path)
        file_type = "excel"

    # Replace NaN values
    df = df.fillna("")

    documents = []

    # Convert each row to JSON
    for index, row in df.iterrows():

        record = {
            key: value
            for key, value in row.to_dict().items()
            if str(value).strip()
        }

        documents.append(
            Document(
                page_content=json.dumps(
                    record,
                    ensure_ascii=False,
                    indent=2
                ),
                metadata={
                    "source": file_path,
                    "file_name": os.path.basename(file_path),
                    "file_type": file_type,
                    "document_type": "spreadsheet",
                    "row": index + 1
                }
            )
        )

    print(
        f"   ✅ Converted {len(documents)} rows into JSON documents"
    )

    return documents