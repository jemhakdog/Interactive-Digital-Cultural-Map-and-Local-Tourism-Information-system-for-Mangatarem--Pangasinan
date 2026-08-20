"""Admin document vault CRUD.

Mounted in main.py with prefix ``/api/documents`` (tags=["documents"]).
Auth: admin only (Depends(require_admin)).
"""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.database import get_db
from backend.app.core.dependencies import require_admin
from backend.app.models.document import Document
from backend.app.models.user import User
from backend.app.schemas.document import DocumentCreate, DocumentResponse

router = APIRouter()


async def _get_document_or_404(document_id: int, db: AsyncSession) -> Document:
    doc = await db.get(Document, document_id)
    if doc is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc


# ─────────────────────────────────────────────
# GET /api/documents — list all
# ─────────────────────────────────────────────
@router.get(
    "/",
    response_model=list[DocumentResponse],
    summary="List documents",
)
async def list_documents(
    db: Annotated[AsyncSession, Depends(get_db)],
    admin: Annotated[User, Depends(require_admin)],
):
    stmt = select(Document).order_by(Document.created_at.desc())
    result = await db.execute(stmt)
    return result.scalars().all()


# ─────────────────────────────────────────────
# POST /api/documents — create
# ─────────────────────────────────────────────
@router.post(
    "/",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create document",
)
async def create_document(
    body: DocumentCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    admin: Annotated[User, Depends(require_admin)],
):
    doc = Document(**body.model_dump())
    db.add(doc)
    await db.flush()
    await db.refresh(doc)
    return doc


# ─────────────────────────────────────────────
# GET /api/documents/{id} — get one
# ─────────────────────────────────────────────
@router.get(
    "/{document_id}",
    response_model=DocumentResponse,
    summary="Get document",
)
async def get_document(
    document_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    admin: Annotated[User, Depends(require_admin)],
):
    return await _get_document_or_404(document_id, db)


# ─────────────────────────────────────────────
# PUT /api/documents/{id} — update
# ─────────────────────────────────────────────
@router.put(
    "/{document_id}",
    response_model=DocumentResponse,
    summary="Update document",
)
async def update_document(
    document_id: int,
    body: DocumentCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    admin: Annotated[User, Depends(require_admin)],
):
    doc = await _get_document_or_404(document_id, db)
    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(doc, field, value)
    await db.flush()
    await db.refresh(doc)
    return doc


# ─────────────────────────────────────────────
# DELETE /api/documents/{id} — delete
# ─────────────────────────────────────────────
@router.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete document",
)
async def delete_document(
    document_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    admin: Annotated[User, Depends(require_admin)],
):
    doc = await _get_document_or_404(document_id, db)
    await db.delete(doc)
