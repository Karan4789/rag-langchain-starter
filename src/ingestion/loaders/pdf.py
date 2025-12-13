import os
from langchain.schema import Document
from langchain_community.document_loaders import UnstructuredPDFLoader

# Try importing LlamaParse, but don't crash if it's not installed
try:
    from llama_parse import LlamaParse
    HAS_LLAMA_PARSE = True
except ImportError:
    HAS_LLAMA_PARSE = False

def load_pdf(file_path):
    """
    Loads a PDF using LlamaParse (High Quality) if API key is present,
    otherwise falls back to Unstructured (Local).
    """
    api_key = os.getenv("LLAMA_CLOUD_API_KEY")

    # OPTION 1: High Quality (LlamaParse)
    # Best for tables, charts, and complex layouts.
    if HAS_LLAMA_PARSE and api_key:
        print(f"   ✨ Using LlamaParse for {os.path.basename(file_path)}...")
        try:
            parser = LlamaParse(
                api_key=api_key,
                result_type="markdown",  # Markdown is best for LLMs
                verbose=True
            )
            # LlamaParse returns its own Document type, we need to convert to LangChain
            llama_docs = parser.load_data(file_path)
            
            # Convert to LangChain 'Document' format
            langchain_docs = []
            for doc in llama_docs:
                langchain_docs.append(
                    Document(
                        page_content=doc.text,
                        metadata={"source": file_path, "page_label": doc.metadata.get("page_label")}
                    )
                )
            return langchain_docs
        
        except Exception as e:
            print(f"   ⚠️ LlamaParse failed: {e}. Falling back to Unstructured.")
            # Fall through to Option 2

    # OPTION 2: Local Fallback (Unstructured)
    # Good for simple text-only PDFs.
    print(f"   📄 Using UnstructuredLoader for {os.path.basename(file_path)}...")
    loader = UnstructuredPDFLoader(file_path)
    return loader.load()
