"""Pydantic schemas for admin Document endpoints."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class DocumentCreate(BaseModel):
    """Create/update a document in the admin vault."""
    title: str = Field(..., min_length=1, max_length=200)
    category: str = Field("general", min_length=1, max_length=50)
    content: str | None = None
    file_url: str | None = None


class DocumentResponse(BaseModel):
    """Document as returned to clients."""
    id: int
    title: str
    category: str
    content: str | None = None
    file_url: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}
