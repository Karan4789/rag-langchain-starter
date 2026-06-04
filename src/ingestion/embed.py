# src/ingestion/embed.py

from langchain_ollama import OllamaEmbeddings
from dotenv import load_dotenv
from core.config import EMBEDDING_MODEL

load_dotenv()

def get_embedding_function():
    """
    Initializes and returns the embedding model.
    """
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    return embeddings
