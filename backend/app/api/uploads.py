"""File upload endpoints — images and media for the tourism platform."""
from __future__ import annotations

import os
import uuid
from pathlib import Path
from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status

from backend.app.core.config import get_settings
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


def _validate_mime(content: bytes, ext: str) -> None:
    """Validate file magic bytes against extension for common media types."""
    if not content:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Uploaded file is empty.")

    signatures: dict[str, list[bytes]] = {
        "png": [b"\x89PNG\r\n\x1a\n"],
        "jpg": [b"\xff\xd8\xff"],
        "jpeg": [b"\xff\xd8\xff"],
        "gif": [b"GIF87a", b"GIF89a"],
        "pdf": [b"%PDF-"],
        "webp": [b"RIFF"],
    }
    expected = signatures.get(ext)
    if expected and not any(content.startswith(sig) for sig in expected):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File signature does not match claimed extension '.{ext}'.",
        )


def _upload_to_supabase(filename: str, content: bytes, content_type: str | None) -> str | None:
    """Attempt upload to Supabase Storage. Returns public URL on success or None to fallback."""
    settings = get_settings()
    if not settings.supabase_url or not settings.supabase_key:
        return None

    bucket = settings.supabase_storage_bucket
    base_url = settings.supabase_url.rstrip("/")
    endpoint = f"{base_url}/storage/v1/object/{bucket}/{filename}"
    headers = {
        "Authorization": f"Bearer {settings.supabase_key}",
        "apiKey": settings.supabase_key,
        "Content-Type": content_type or "application/octet-stream",
    }
    try:
        with httpx.Client(timeout=10.0) as client:
            resp = client.post(endpoint, content=content, headers=headers)
            if resp.status_code in (200, 201):
                return f"{base_url}/storage/v1/object/public/{bucket}/{filename}"
    except Exception:
        pass
    return None


def _validate_and_save(file: UploadFile, allowed: set[str]) -> dict:
    """Validate extension, MIME header, size; upload to Supabase or fallback to disk."""
    ext = (file.filename or "").rsplit(".", 1)[-1].lower() if file.filename else ""
    if ext not in allowed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File extension '.{ext}' not allowed. Accepted: {', '.join(sorted(allowed))}",
        )

    # Read content to check size and magic bytes
    content = file.file.read()
    if len(content) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large ({len(content) / 1024 / 1024:.1f}MB). Max is {MAX_FILE_SIZE_MB}MB.",
        )

    _validate_mime(content, ext)

    unique_name = f"{uuid.uuid4().hex}.{ext}"
    supabase_url = _upload_to_supabase(unique_name, content, file.content_type)

    if supabase_url:
        file_url = supabase_url
    else:
        dest = UPLOAD_DIR / unique_name
        dest.write_bytes(content)
        file_url = f"/uploads/{unique_name}"

    return {
        "url": file_url,
        "filename": unique_name,
        "original_name": file.filename,
        "size": len(content),
        "content_type": file.content_type,
    }


# ── Endpoints ──────────────────────────────────────────────────


@router.post("/image", summary="Upload a single image")
@router.post("/single", summary="Upload a single image (alias)", include_in_schema=False)
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
