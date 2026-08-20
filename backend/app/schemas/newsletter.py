"""Pydantic schemas for admin Newsletter endpoints."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class SubscriberResponse(BaseModel):
    """Newsletter subscriber row."""
    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime | None = None
    user_id: int | None = None

    model_config = {"from_attributes": True}


class NewsletterSend(BaseModel):
    """Compose + broadcast a newsletter dispatch."""
    subject: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)


class NewsletterHistoryResponse(BaseModel):
    """A previously sent newsletter dispatch."""
    id: int
    subject: str
    content: str | None = None
    recipient_count: int
    sender_id: int | None = None
    sent_at: datetime | None = None

    model_config = {"from_attributes": True}
