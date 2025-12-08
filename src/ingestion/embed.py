# src/ingestion/embed.py

#from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_ollama import OllamaEmbeddings
from dotenv import load_dotenv

load_dotenv()

def get_embedding_function():
    """
    Initializes and returns the embedding model.
    """
   
    embeddings = OllamaEmbeddings(model="embeddinggemma:300m")
    return embeddings
