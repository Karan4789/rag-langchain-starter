# src/ingestion/classify_llm.py

import os

from langchain_groq import ChatGroq

from core.config import (
    GROQ_API_KEY,
    CLASSIFIER_MODEL
)

ALLOWED_TYPES = {

    "book",
    "research_paper",
    "resume",
    "spreadsheet",
    "presentation",
    "invoice",
    "contract",
    "general_document"

}


def llm_classifier(file_path: str, text: str):

    filename = os.path.basename(file_path)

    prompt = f"""
        You are a document classifier.
        Classify the document into EXACTLY ONE category.

        Allowed labels:

        book
        research_paper
        resume
        spreadsheet
        presentation
        invoice
        contract
        general_document

        Filename:
        {filename}

        Document Text:
        {text}

        Rules:

        - Return ONLY one label
        - No explanation
        - No markdown
        - No JSON
"""

    model = ChatGroq(model=CLASSIFIER_MODEL,api_key=GROQ_API_KEY,temperature=0)

    response = model.invoke(
        prompt
    )

    prediction = (response.content.strip().lower())

    if prediction not in ALLOWED_TYPES:
        return "general_document"
    return prediction