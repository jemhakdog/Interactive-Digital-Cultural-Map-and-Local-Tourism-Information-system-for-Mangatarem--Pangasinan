"""File upload endpoints — images and media for the tourism platform."""
from __future__ import annotations

import os
import uuid
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status

from backend.app.core.dependencies import get_current_user
from backend.app.models.user import User

router = APIRouter()

# ── Configuration ──────────────────────────────────────────────
UPLOAD_DIR = Path(__file__).resolve().parent.parent.parent / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
ALLOWED_MEDIA_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp", "mp4"}
ALLOWED_DOC_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp", "pdf", "doc", "docx"}
MAX_FILE_SIZE_MB = 15
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024


def _validate_and_save(file: UploadFile, allowed: set[str]) -> dict:
    """Validate extension & size, save with UUID filename, return metadata."""
    ext = (file.filename or "").rsplit(".", 1)[-1].lower() if file.filename else ""
    if ext not in allowed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File extension '.{ext}' not allowed. Accepted: {', '.join(sorted(allowed))}",
        )

    # Read content to check size
    content = file.file.read()
    if len(content) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large ({len(content) / 1024 / 1024:.1f}MB). Max is {MAX_FILE_SIZE_MB}MB.",
        )

    unique_name = f"{uuid.uuid4().hex}.{ext}"
    dest = UPLOAD_DIR / unique_name
    dest.write_bytes(content)

    return {
        "url": f"/uploads/{unique_name}",
        "filename": unique_name,
        "original_name": file.filename,
        "size": len(content),
        "content_type": file.content_type,
    }


# ── Endpoints ──────────────────────────────────────────────────


@router.post("/image", summary="Upload a single image")
async def upload_image(
    file: UploadFile,
    user: Annotated[User, Depends(get_current_user)],
):
    """Upload a single image (jpg/png/gif/webp). Returns URL + metadata."""
    return _validate_and_save(file, ALLOWED_IMAGE_EXTENSIONS)


@router.post("/document", summary="Upload a verification document")
async def upload_document(
    file: UploadFile,
    user: Annotated[User, Depends(get_current_user)],
):
    """Upload a document (pdf/png/jpg/webp/doc/docx). Returns URL + metadata."""
    return _validate_and_save(file, ALLOWED_DOC_EXTENSIONS)


@router.post("/multiple", summary="Upload multiple images")
async def upload_images(
    files: list[UploadFile],
    user: Annotated[User, Depends(get_current_user)],
):
    """Upload multiple images (jpg/png/gif/webp/mp4). Returns list of metadata."""
    if not files:
        raise HTTPException(status_code=400, detail="No files provided.")
    if len(files) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 files per request.")

    results = []
    for f in files:
        results.append(_validate_and_save(f, ALLOWED_MEDIA_EXTENSIONS))
    return {"files": results, "count": len(results)}
