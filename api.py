import os
import shutil
import sys
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel

sys.path.append(os.path.abspath("src"))

from core.config import DATA_FOLDER, API_TITLE, API_VERSION, API_HOST, API_PORT, API_RELOAD
from retrieval.generate import query_rag
from ingestion.store import ingest_documents
from ingestion.load import load_documents
from ingestion.embed import get_embedding_function
import uvicorn

app = FastAPI(title=API_TITLE, version=API_VERSION)

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    sources: list[str]

@app.get("/")
def health_check():
    return {"status": "active"}

@app.post("/query", response_model=QueryResponse)
def ask_question(request: QueryRequest):
    try:
        result = query_rag(request.question)
        return {
            "answer": result["answer"],
            "sources": [s[:200] + "..." for s in result["sources"]]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest")
async def upload_and_ingest(file: UploadFile = File(...)):
    """
    Upload a file (PDF) to the server, save it to /data, and ingest it.
    """
    try:
        # 1. Save the uploaded file to 'data/' folder
        file_location = os.path.join(DATA_FOLDER, file.filename)
        
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        print(f" Saved file to {file_location}")

        # 2. Trigger Ingestion (Processes ALL files in data/)
        # Note: Ideally, you'd only ingest the NEW file, but for now we re-run all.
        print(" Starting ingestion...")
        documents = load_documents()
        embedding_function = get_embedding_function()
        ingest_documents(documents, embedding_function)
        
        return {
            "message": f"Successfully uploaded {file.filename} and re-ingested knowledge base.",
            "file_path": file_location
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host=API_HOST, port=API_PORT, reload=API_RELOAD)
