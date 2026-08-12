"""FastAPI application for the document-grounded chat experience."""

from __future__ import annotations

import shutil
import uuid
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from rag_service import RAGService

BASE_DIR = Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI(title="Aperture RAG")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
rag = RAGService(BASE_DIR / "chroma_db")


class Question(BaseModel):
    question: str


@app.get("/")
async def home() -> FileResponse:
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.get("/api/status")
async def status() -> dict:
    return {"ready": rag.ready, "document_name": rag.document_name}


@app.post("/api/documents")
async def upload_document(file: UploadFile = File(...)) -> dict:
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a PDF document.")
    if file.size and file.size > 25 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Please choose a PDF under 25 MB.")

    safe_name = f"{uuid.uuid4().hex}.pdf"
    destination = UPLOAD_DIR / safe_name
    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        pages, chunks = rag.ingest(destination, file.filename)
    except Exception as exc:
        destination.unlink(missing_ok=True)
        raise HTTPException(status_code=500, detail=f"Could not process this PDF: {exc}") from exc
    return {"message": "Document is ready", "name": file.filename, "pages": pages, "chunks": chunks}


@app.post("/api/chat")
async def chat(body: Question) -> dict:
    if not body.question.strip():
        raise HTTPException(status_code=400, detail="Please enter a question.")
    if not rag.ready:
        raise HTTPException(status_code=409, detail="Upload a document before asking a question.")
    try:
        answer, sources = rag.answer(body.question.strip())
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Could not answer that question: {exc}") from exc
    return {"answer": answer, "sources": sources}
