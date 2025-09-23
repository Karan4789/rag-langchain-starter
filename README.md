# Simple RAG Project

This project is a basic implementation of a Retrieval-Augmented Generation (RAG) pipeline. It's designed for beginners to understand the core concepts of RAG and see them in action.

## What is Retrieval-Augmented Generation (RAG)?

Retrieval-Augmented Generation (RAG) is a technique for enhancing the accuracy and reliability of Large Language Models (LLMs) by providing them with information from an external knowledge base.

In simple terms, instead of just relying on its pre-trained knowledge, the LLM can "look up" relevant information from your own documents to answer a question. This is particularly useful when you want the LLM to answer questions about specific, private, or very recent information.

The process typically involves two main stages:
1.  **Ingestion**: Your documents are loaded, split into smaller chunks, and converted into numerical representations (embeddings) which are then stored in a special database called a vector store.
2.  **Retrieval & Generation**: When you ask a question, the system searches the vector store for the most relevant document chunks. These chunks are then passed to the LLM along with your original question, providing it with the necessary context to generate a well-informed answer.

For a more detailed explanation, check out this article on [Retrieval-Augmented Generation](https://medium.com/%40bellasenior/retrieval-augmented-generation-23005432cbc1).

## Getting Started

Follow these steps to set up and run the project on your local machine.

### Prerequisites

*   Python 3.8+
*   [Ollama](https://ollama.com/) installed and running locally.
*   A Google API key for the Gemini model.

### Setup

1.  **Clone the repository**
    ```bash
    git clone <your-repository-url>
    cd rag-langchain-starter
    ```

2.  **Create and activate a virtual environment**
    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install dependencies**
    Your `requirements.txt` file should contain the following:
    ```txt
    langchain
    langchain-chroma
    langchain-community
    langchain-google-genai
    langchain-ollama
    pypdf
    python-dotenv
    ```
    Then, install the packages:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Pull the Ollama embedding model**
    This project uses `nomic-embed-text` for creating embeddings. Pull it via Ollama:
    ```bash
    ollama pull nomic-embed-text
    ```

5.  **Add your documents**
    Place your PDF documents inside the `data/` directory.

6.  **Set up environment variables**
    Create a file named `.env` in the root of the project and add your Google API key:
    ```
    GOOGLE_API_KEY="your-google-api-key-here"
    ```

### How to Run

The RAG pipeline is executed in two main phases: Ingestion and Querying.

1.  **Ingestion**
    This process loads your documents, splits them, creates embeddings using Ollama, and stores them in a Chroma vector database.
    ```bash
    python main.py
    ```
    This script will process the documents in the `data/` directory and create a vector store in the `db/` directory.

2.  **Querying**
    Once ingestion is complete, you can ask questions. This script retrieves relevant context from the database and uses Google's Gemini model to generate an answer.
    ```bash
    python src/retrieval/generate.py "Your question here"
    ```

## Project Structure

```
rag-langchain-starter/
├── data/
│   └── source_documents/
│       └── Sample_data.pdf
├── db/
│   ├── ... (ChromaDB files)
│   └── chroma.sqlite3
├── src/
│   ├── core/
│   │   └── __init__.py
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── embed.py       # Handles embedding creation (Ollama)
│   │   ├── load.py        # Loads PDF documents
│   │   ├── split.py       # Splits documents into chunks
│   │   └── store.py       # Stores chunks in ChromaDB
│   ├── retrieval/
│   │   ├── __init__.py
│   │   ├── generate.py    # Generates answers using Gemini
│   │   └── search.py      # Searches for relevant chunks
├── tests/
│   └── test_ingestion.py
├── .env
├── .gitignore
├── .python-version
├── main.py                # Main script for the ingestion pipeline
├── pyproject.toml
├── README.md
└── requirements.txt
```
