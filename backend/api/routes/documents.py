import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from backend.core.auth import get_current_user
import chromadb
from chromadb.config import Settings as ChromaSettings
from backend.core.config import settings

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/upload")
async def upload_document(
    file:         UploadFile = File(...),
    current_user: dict       = Depends(get_current_user),
):
    if not file.filename.endswith((".txt", ".pdf", ".json")):
        raise HTTPException(status_code=400, detail="Only .txt, .pdf, .json supported")

    content  = await file.read()
    text     = content.decode("utf-8", errors="ignore")
    doc_id   = str(uuid.uuid4())

    try:
        client     = chromadb.HttpClient(
            host=settings.CHROMA_HOST,
            port=settings.CHROMA_PORT,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        collection = client.get_or_create_collection("uploaded_docs")
        collection.upsert(
            documents=[text],
            ids=[doc_id],
            metadatas=[{"filename": file.filename, "uploaded_by": current_user["username"]}],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ChromaDB error: {e}")

    return {
        "id":       doc_id,
        "filename": file.filename,
        "status":   "ingested",
        "message":  "Document successfully ingested into ChromaDB",
    }

@router.get("/")
async def list_documents(current_user: dict = Depends(get_current_user)):
    return {"message": "Document listing coming in Day 5", "documents": []}