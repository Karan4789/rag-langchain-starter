import time
import os
import pickle
from langchain.storage import LocalFileStore
from langchain.storage._lc_store import create_kv_docstore
from langchain_chroma import Chroma
from langchain.retrievers import ParentDocumentRetriever
from langchain.text_splitter import RecursiveCharacterTextSplitter

def ingest_documents(documents, embedding_function, batch_size=45):
    # 1. Define Paths
    vector_db_path = "db/"
    parent_docs_path = "db/parent_docs" 

    # 2. Initialize Vector Store (Child chunks)
    vectorstore = Chroma(
        collection_name="split_parents",
        persist_directory=vector_db_path,
        embedding_function=embedding_function
    )

    # 3. Initialize Doc Store (Parent chunks) 
    fs = LocalFileStore(parent_docs_path)
    store = create_kv_docstore(fs)

    # 4. Define Splitters
    child_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)
    parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)

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
            time.sleep(1.0) 
        except Exception as e:
            print(f"\n   ❌ Error on batch: {e}")
            raise e

    print("✅ Ingestion Complete! Child chunks embedded, Parent docs stored.")
