# src/ingestion/store.py

import time
import os
import pickle
from langchain_classic.storage import LocalFileStore
from langchain_classic.storage._lc_store import create_kv_docstore
from langchain_chroma import Chroma
from langchain_classic.retrievers import ParentDocumentRetriever
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter

from core.config import (
    DB_FOLDER,
    PARENT_DOCS_FOLDER,
    CHROMA_COLLECTION_NAME,
    CHILD_CHUNK_SIZE,
    CHILD_CHUNK_OVERLAP,
    PARENT_CHUNK_SIZE,
    PARENT_CHUNK_OVERLAP,
    INGESTION_BATCH_SIZE,
    BATCH_SLEEP_TIME
)

def ingest_documents(documents, embedding_function, batch_size=None):
    if batch_size is None:
        batch_size = INGESTION_BATCH_SIZE

    # 2. Initialize Vector Store (Child chunks)
    vectorstore = Chroma(
        collection_name=CHROMA_COLLECTION_NAME,
        persist_directory=DB_FOLDER,
        embedding_function=embedding_function,
        collection_metadata={"hnsw:space": "cosine"}
    )

    # 3. Initialize Doc Store (Parent chunks) 
    fs = LocalFileStore(PARENT_DOCS_FOLDER)
    store = create_kv_docstore(fs)

    # 4. Define Splitters
    child_splitter = RecursiveCharacterTextSplitter(chunk_size=CHILD_CHUNK_SIZE, chunk_overlap=CHILD_CHUNK_OVERLAP)
    parent_splitter = RecursiveCharacterTextSplitter(chunk_size=PARENT_CHUNK_SIZE, chunk_overlap=PARENT_CHUNK_OVERLAP)

    # 5. Create the Retriever
    retriever = ParentDocumentRetriever(
        vectorstore=vectorstore,
        docstore=store,
        child_splitter=child_splitter,
        parent_splitter=parent_splitter,
    )

    print(f"📦 Processing {len(documents)} documents using Parent Document Retrieval...")

    # 6. Add Documents in Batches
    for i in range(0, len(documents), batch_size):
        batch = documents[i : i + batch_size]
        print(f"   Processing batch {i//batch_size + 1} ({len(batch)} docs)... ", end="", flush=True)
        
        try:
            retriever.add_documents(batch, ids=None)
            print("✅")
            time.sleep(BATCH_SLEEP_TIME) 
        except Exception as e:
            print(f"\n   ❌ Error on batch: {e}")
            raise e

    print("✅ Ingestion Complete! Child chunks embedded, Parent docs stored.")
