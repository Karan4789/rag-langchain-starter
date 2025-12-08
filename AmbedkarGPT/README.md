# AmbedkarGPT: A Simple RAG Project

This project is a basic implementation of a Retrieval-Augmented Generation (RAG) pipeline using LangChain. It is built to chat with documents about Dr. B.R. Ambedkar, allowing you to ask questions and receive answers based on the provided texts.

## What is Retrieval-Augmented Generation (RAG)?

Retrieval-Augmented Generation (RAG) is a technique for enhancing the accuracy and reliability of Large Language Models (LLMs) by providing them with information from an external knowledge base.

Instead of just relying on its pre-trained knowledge, the LLM can "look up" relevant information from your own documents to answer a question. This is particularly useful when you want the LLM to answer questions about specific, private, or very recent information.

The process typically involves two main stages:
1.  **Ingestion**: Your documents are loaded, split into smaller chunks, and converted into numerical representations (embeddings) which are then stored in a special database called a vector store. This happens automatically the first time you run the app.
2.  **Retrieval & Generation**: When you ask a question, the system searches the vector store for the most relevant document chunks. These chunks are then passed to the LLM along with your original question, providing it with the necessary context to generate a well-informed answer.

## Getting Started

Follow these steps to set up and run the project on your local machine.

### Prerequisites

*   Python 3.12+
*   [uv](https://github.com/astral-sh/uv) installed.
*   [Ollama](https://ollama.com/) installed and running locally.

### Setup

1.  **Clone the repository**
    ```bash
    git clone <your-repository-url>
    cd AmbedkarGPT-Intern-Task
    ```

2.  **Create and activate a virtual environment using `uv`**
    ```bash
    # Create the virtual environment
    uv venv

    # Activate the environment
    # For Windows (PowerShell)
    .\.venv\Scripts\Activate.ps1
    # For macOS/Linux
    source .venv/bin/activate
    ```

3.  **Sync dependencies using `uv`**
    This command reads the `pyproject.toml` file and installs the exact dependencies needed for the project, ensuring a consistent and clean environment.
    ```bash
    uv sync
    ```

4.  **Pull the Ollama model**
    This project uses the `mistral` model (Mistral 7B) for generating answers. Pull it via Ollama:
    ```bash
    ollama pull mistral
    ```

5.  **Add your documents**
    Place your `.txt` documents inside the `data/` directory. A sample file is already included.

### How to Run

To run the application, simply execute the `main.py` script from the root directory.

```bash
python main.py
```

This script will perform the following actions:
1.  **Check for a database**: If the `db/` directory doesn't exist, it will automatically run the ingestion pipeline. This involves loading documents from `data/`, splitting them into chunks, creating embeddings, and storing them in a ChromaDB vector store.
2.  **Start Q&A Session**: After ensuring the database is ready, it will launch an interactive command-line interface where you can ask questions.

Type your question and press Enter. To exit the session, type `exit`.

## Project Structure

```
rag-langchain-starter/
├── data/
│   └── speech.txt
├── db/
│   └── ... (ChromaDB files created after ingestion)
├── src/
│   ├── ingestion/
│   │   ├── embed.py       # Handles embedding creation (Sentence Transformers)
│   │   ├── load.py        # Loads .txt documents
│   │   ├── split.py       # Splits documents into chunks
│   │   └── store.py       # Stores chunks in ChromaDB
│   └── retrieval/
│       └── generate.py    # Generates answers using Ollama (Mistral)
├── test/
│   └── test.py            # Script to test the full ingestion pipeline
├── .env
├── .gitignore
├── .python-version
├── main.py                # Main entry point for the application
├── pyproject.toml
├── README.md
└── requirements.txt
```
