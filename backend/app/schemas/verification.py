"""Pydantic schemas for BusinessVerification endpoints."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class VerificationCreate(BaseModel):
    """Submit business verification documents (business owner)."""
    permit_document_url: str = Field(..., min_length=1)
    other_document_url: str | None = None
