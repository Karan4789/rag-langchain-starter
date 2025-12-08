# src/ingestion/embed.py

from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv


load_dotenv()


def get_embedding_function():
    """
    Initializes and returns the embedding model using Sentence Transformers.
    """
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    model_kwargs = {"device": "cpu"}
    
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs
    )
    return embeddings
