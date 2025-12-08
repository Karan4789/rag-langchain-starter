# RAG System with Parent Document Retrieval

A Retrieval-Augmented Generation (RAG) system that uses **Parent Document Retrieval** and **FlashrankRerank** to provide accurate answers from your PDF documents.

## What is RAG?

Retrieval-Augmented Generation (RAG) enhances Large Language Models (LLMs) by grounding their responses in your own documents. Instead of relying solely on pre-trained knowledge, the system retrieves relevant information from your documents to generate accurate, context-aware answers.

**How it works:**
1. **Ingestion**: Documents are loaded, split into parent and child chunks, embedded, and stored in a vector database
2. **Retrieval**: When you ask a question, the system searches for relevant child chunks, retrieves their parent chunks for better context, and reranks them
3. **Generation**: The LLM uses the retrieved context to generate an informed answer

For more details, read this article: [Retrieval-Augmented Generation](https://medium.com/%40bellasenior/retrieval-augmented-generation-23005432cbc1)

## Key Features

- **Parent Document Retrieval**: Searches using small chunks but retrieves larger parent chunks for better context
- **FlashrankRerank**: Improves result quality by reranking retrieved documents
- **Local Embeddings**: Uses Ollama's `embeddinggemma:300m` model locally
- **Google Gemini**: Powered by `gemini-2.5-flash` for answer generation

## Prerequisites

- Python 3.12+
- [Ollama](https://ollama.com/) installed and running
- Google API key for Gemini

## Setup

1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
   cd rag
   ```

2. **Create and activate a virtual environment**
   ```bash
   # Windows
   uv venv
   .\venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   uv sync
   ```

4. **Pull the Ollama embedding model**
   ```bash
   ollama pull embeddinggemma:300m
   ```

5. **Set up environment variables**
   Create a `.env` file in the project root:
   ```
   GOOGLE_API_KEY=your-google-api-key-here
   ```

6. **Add your documents**
   Place PDF files in the `data/` directory

## Usage

### 1. Ingest Documents

Run the ingestion pipeline to process your PDFs:

```bash
python src/ingest.py
```

This will:
- Load all PDFs from `data/`
- Split them into parent chunks (2000 chars) and child chunks (400 chars)
- Create embeddings for child chunks using Ollama
- Store everything in ChromaDB at `db/`

### 2. Query Your Documents

Ask questions about your documents:

```bash
python src/retrieval/generate.py "What is the main topic?"
```

The system will:
- Search for relevant child chunks
- Retrieve parent chunks for context
- Rerank results using Flashrank
- Generate an answer using Google Gemini

### 3. Run Full Pipeline (Optional)

Run ingestion and query in one command:

```bash
python app.py "Your question here"
```

This clears the database, re-ingests documents, and generates an answer.

## Project Structure

```
rag/
├── data/                           # Your PDF documents
├── db/                             # ChromaDB vector store
│   ├── chroma.sqlite3
│   ├── a381fad3-.../              # Vector embeddings
│   └── parent_docs/               # Parent document store
├── src/
│   ├── ingest.py                  # Main ingestion script
│   ├── ingestion/
│   │   ├── load.py                # Load PDFs
│   │   ├── embed.py               # Ollama embeddings
│   │   └── store.py               # Parent Document Retrieval storage
│   └── retrieval/
│       ├── generate.py            # Generate answers with reranking
│       └── search.py              # Basic similarity search
├── app.py                         # Full pipeline runner
├── .env                           # API keys
├── requirements.txt
└── README.md
```

## How Parent Document Retrieval Works

1. **Child Chunks (400 chars)**: Small, focused chunks for precise embedding and search
2. **Parent Chunks (2000 chars)**: Larger chunks that provide full context to the LLM
3. **Search Process**: 
   - Query is embedded and matched against child chunks
   - Parent chunks are retrieved for matched children
   - Results are reranked using Flashrank
   - Top parent chunks are sent to the LLM

This approach balances search precision with contextual richness.

## Technologies

- **LangChain**: RAG orchestration
- **Ollama** (`embeddinggemma:300m`): Local embeddings
- **ChromaDB**: Vector database
- **Google Gemini** (`gemini-2.5-flash`): LLM for generation
- **Flashrank**: Result reranking
- **FastAPI**: (Future) API endpoints

## Troubleshooting

- **Ollama connection error**: Make sure Ollama is running (`ollama serve`)
- **Google API error**: Verify your `GOOGLE_API_KEY` in `.env`
- **Empty results**: Ensure documents are properly ingested before querying