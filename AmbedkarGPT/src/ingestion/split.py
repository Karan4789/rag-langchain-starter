
# I'm using RecursiveCharacterTextSplitter because it's smarter about how it chunks the text.
# It tries to keep related paragraphs and sentences together, which is better for context.
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.ingestion.load import load_documents

def split_documents(documents):
    """
    Splits the loaded documents into smaller chunks using a recursive character splitter.

    Args:
        documents: A list of Document objects loaded from files.

    Returns:
        A list of smaller Document objects (chunks).
    """
    

    text_splitter = RecursiveCharacterTextSplitter(
        # Set a smaller chunk size to ensure splitting
        chunk_size=100,
        chunk_overlap=25
    )
    
    chunks = text_splitter.split_documents(documents)
    
    print(f"Split {len(documents)} document(s) into {len(chunks)} chunks.")
    return chunks

# A simple test to run this script directly
if __name__ == "__main__":
    documents = load_documents()
    chunks = split_documents(documents)
    if chunks:
        print(f"\nTotal chunks: {len(chunks)}")
        print("\nSample chunk content:")
        print(chunks[0].page_content)
