import os
import shutil
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import tempfile

from core_logic import docu_chat, ingest_pdf

app = FastAPI(title="Nexus RAG API")

# --- CORS --- allow your Vercel frontend + local dev
origins = [
    "http://localhost:5173",
    "https://your-actual-vercel-url.vercel.app",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Schemas ---
class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


# --- Routes ---
@app.get("/")
def root():
    return {"status": "Nexus RAG backend is running"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Send a message and get a RAG-grounded reply."""
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    try:
        reply = docu_chat(request.message)
        return ChatResponse(reply=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload a PDF to ingest into ChromaDB."""
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    temp_path = os.path.join(tempfile.gettempdir(), file.filename)
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        chunk_count = ingest_pdf(temp_path)
        return {"message": f"Ingested {chunk_count} chunks from {file.filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)