from pydantic import BaseModel

from fastapi import APIRouter
from storage import generate_presigned_url
from db import save_file_metadata

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "ok"}

class UploadRequest(BaseModel):
    filename: str

@router.post("/upload")
def get_upload_url(request: UploadRequest):
    url = generate_presigned_url(request.filename)
    save_file_metadata(request.filename, status="pending")
    return {"upload_url": url, "filename": request.filename}
