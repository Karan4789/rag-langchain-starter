# core/config.py

import os
from dotenv import load_dotenv

load_dotenv()


# PATHS
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_FOLDER = os.path.join(BASE_DIR, "data")
DB_FOLDER = os.path.join(BASE_DIR, "db")
PARENT_DOCS_FOLDER = os.path.join(DB_FOLDER, "parent_docs")

# Create directories if they don't exist
os.makedirs(DATA_FOLDER, exist_ok=True)
os.makedirs(DB_FOLDER, exist_ok=True)
os.makedirs(PARENT_DOCS_FOLDER, exist_ok=True)


# EMBEDDING & MODEL SETTINGS
# Using Ollama local embeddings (requires Ollama to be running)
EMBEDDING_MODEL = "nomic-embed-text:v1.5" #"embeddinggemma:latest" 
EMBEDDING_PROVIDER = "ollama"  # Options: "ollama", "openai", "huggingface"

# LLM Model for generation
LLM_MODEL = "llama-3.3-70b-versatile"  
LLM_PROVIDER = "groq"

# GROQ API Key (required for llama-3.3-70b-versatile)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# INGESTION SETTINGS
# Parent Document Retrieval - Chunk sizes
CHILD_CHUNK_SIZE = 400
CHILD_CHUNK_OVERLAP = 50

PARENT_CHUNK_SIZE = 1200
PARENT_CHUNK_OVERLAP = 150  

# Batch processing
INGESTION_BATCH_SIZE = 20
BATCH_SLEEP_TIME = 2.0  # seconds between batches

# RETRIEVAL SETTINGS

# Compression/Reranking
USE_RERANKING = True
RERANKING_MODEL = "ms-marco-MiniLM-L-12-v2"  # FlashRank model

# Context retrieval
TOP_K_RESULTS = 4  # Number of document chunks to retrieve

# VECTOR STORE SETTINGS
CHROMA_COLLECTION_NAME = "split_parents"
CHROMA_PERSIST_DIRECTORY = DB_FOLDER

# API SETTINGS
API_HOST = "localhost"
API_PORT = 8000
API_TITLE = "RAG Project"
API_VERSION = "1.0"
API_RELOAD = True  # Hot reload during development

# PROMPT TEMPLATES
RAG_PROMPT_TEMPLATE = """
{skill}

Answer using the provided context.

Context:
{context}

Question:
{question}
"""

# LOGGING
LOG_LEVEL = "INFO"  # Options: "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
