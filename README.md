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
*   An API key from an LLM provider (e.g., OpenAI).

### Setup

1.  **Clone the repository**
    ```bash
    git clone <your-repository-url>
    cd rag
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
    Create a `requirements.txt` file with the following content:
    ```txt
    langchain
    langchain-community
    langchain-openai
    pypdf
    python-dotenv
    faiss-cpu
    ```
    Then, install the packages:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Add your documents**
    Place your PDF documents inside the `data/` directory. If the directory doesn't exist, create it at the root of the project.

5.  **Set up environment variables**
    Create a file named `.env` in the root of the project and add your LLM API key:
    ```
    OPENAI_API_KEY="your-api-key-here"
    ```

### How to Run

The RAG pipeline is executed in two main phases: Ingestion and Querying.

1.  **Ingestion**
    This one-time process loads your documents, splits them into chunks, creates embeddings, and stores them in a vector database.
    ```bash
    python src/ingest.py
    ```
    This script will process the documents in the `data/` directory and create a vector store in the `vector_store/` directory.

2.  **Querying**
    Once ingestion is complete, you can ask questions.
    ```bash
    python src/query.py "Your question here"
    ```
    This will use the vector store to find relevant context and generate an answer.

## Project Structure

```
rag-langchain-starter/
├── data/
│   └── source_documents/
│       └── Sample_data.pdf
├── db/
│   ├── 29891a8f-0165-4f40-8ff8-ceb52e94674e/
│   └── chroma.sqlite3
├── src/
│   ├── core/
│   │   └── __init__.py
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── embed.py
│   │   ├── load.py
│   │   ├── split.py
│   │   └── store.py
│   ├── retrieval/
│   │   ├── __init__.py
│   │   ├── generate.py
│   │   └── search.py
├── tests/
│   └── test_ingestion.py
├── .env
├── .gitignore
├── .python-version
├── main.py
├── pyproject.toml
├── README.md
└── requirements.txt

```
