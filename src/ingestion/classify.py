# src/ingestion/classify.py

import os
import re


# Supported document types
DOCUMENT_TYPES = {
    "BOOK": "book",
    "RESEARCH_PAPER": "research_paper",
    "RESUME": "resume",
    "SPREADSHEET": "spreadsheet",
    "PRESENTATION": "presentation",
    "INVOICE": "invoice",
    "CONTRACT": "contract",
    "GENERAL": "general_document",
    "UNKNOWN": "unknown"
}


def classify_document(file_path: str, text: str = "") -> str:
    """
    Hybrid document classifier (Phase 1).

    Phase 1:
        - Rule-based classification.

    Phase 2 (later):
        - If no rule matches, call a small LLM.

    Parameters
    ----------
    file_path : str
        Original uploaded file path.

    text : str
        Extracted text (usually first page or first few paragraphs).

    Returns
    -------
    str
        One of the supported document types.
    """

    filename = os.path.basename(file_path).lower()
    extension = os.path.splitext(filename)[1].lower()

    text = text.lower()
    
    # Rule 1 : Spreadsheet

    if extension in [".csv", ".xlsx", ".xls"]:
        return DOCUMENT_TYPES["SPREADSHEET"]

    # Rule 2 : PowerPoint

    if extension in [".ppt", ".pptx"]:
        return DOCUMENT_TYPES["PRESENTATION"]

    # Rule 3 : Resume

    if (
        "resume" in filename
        or "cv" in filename
        or (
            "education" in text
            and "experience" in text
            and "skills" in text
        )
    ):
        return DOCUMENT_TYPES["RESUME"]

    # Rule 4 : Research Paper

    research_keywords = [
        "abstract",
        "introduction",
        "methodology",
        "results",
        "discussion",
        "references"
    ]

    if sum(keyword in text for keyword in research_keywords) >= 3:
        return DOCUMENT_TYPES["RESEARCH_PAPER"]
    
    # Rule 5 : Invoice

    invoice_keywords = [
        "invoice",
        "invoice number",
        "amount due",
        "bill to"
    ]

    if any(keyword in text for keyword in invoice_keywords):
        return DOCUMENT_TYPES["INVOICE"]

    # Rule 6 : Contract

    contract_keywords = [
        "agreement",
        "party",
        "terms",
        "conditions",
        "signature"
    ]

    if sum(keyword in text for keyword in contract_keywords) >= 2:
        return DOCUMENT_TYPES["CONTRACT"]

    # Rule 7 : Book

    book_keywords = [
        "chapter",
        "contents",
        "preface",
        "foreword",
        "prologue"
    ]

    if any(keyword in text for keyword in book_keywords):
        return DOCUMENT_TYPES["BOOK"]

    # No rule matched

    return DOCUMENT_TYPES["UNKNOWN"]