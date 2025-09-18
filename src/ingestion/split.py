# src/ingestion/split.py

from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_documents(documents):
    """
    Splits the loaded documents into smaller chunks.

    Args:
        documents: A list of Document objects loaded from files.

    Returns:
        A list of smaller Document objects (chunks).
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1024,  
        chunk_overlap=100   
    )
    
    chunks = text_splitter.split_documents(documents)
    
    print(f"Split {len(documents)} document(s) into {len(chunks)} chunks.")
    return chunks

