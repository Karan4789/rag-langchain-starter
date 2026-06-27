import os

from ingestion.classify_llm import llm_classifier


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


def classify_document(file_path: str, docs) -> str:

    sample = "\n".join(
        doc.page_content
        for doc in docs[:3]
    )[:3000]

    prediction = rule_classifier(
        file_path,
        sample
    )

    if prediction != DOCUMENT_TYPES["UNKNOWN"]:
        print(f"📄 Rule classifier: {prediction}")
        return prediction

    print("🤖 Using LLM fallback")

    prediction = llm_classifier(
        file_path,
        sample
    )

    print(f"📄 LLM classifier: {prediction}")

    return prediction


def rule_classifier(file_path: str, text: str) -> str:

    filename = os.path.basename(file_path).lower()
    extension = os.path.splitext(filename)[1].lower()

    text = text.lower()

    if extension in [".csv", ".xlsx", ".xls"]:
        return DOCUMENT_TYPES["SPREADSHEET"]

    if extension in [".ppt", ".pptx"]:
        return DOCUMENT_TYPES["PRESENTATION"]

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

    research_keywords = [
        "abstract",
        "introduction",
        "methodology",
        "results",
        "discussion",
        "references"
    ]

    if sum(
        keyword in text
        for keyword in research_keywords
    ) >= 3:
        return DOCUMENT_TYPES["RESEARCH_PAPER"]

    invoice_keywords = [
        "invoice",
        "invoice number",
        "amount due",
        "bill to"
    ]

    if any(
        keyword in text
        for keyword in invoice_keywords
    ):
        return DOCUMENT_TYPES["INVOICE"]

    contract_keywords = [
        "agreement",
        "party",
        "terms",
        "conditions",
        "signature"
    ]

    if sum(
        keyword in text
        for keyword in contract_keywords
    ) >= 2:
        return DOCUMENT_TYPES["CONTRACT"]

    book_keywords = [
        "chapter",
        "contents",
        "preface",
        "foreword",
        "prologue"
    ]

    if any(
        keyword in text
        for keyword in book_keywords
    ):
        return DOCUMENT_TYPES["BOOK"]

    return DOCUMENT_TYPES["UNKNOWN"]