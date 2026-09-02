"""Pydantic schemas for the Notifications module."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, EmailStr


class SubscribeRequest(BaseModel):
    email: EmailStr


class SubscribeResponse(BaseModel):
    status: str
    message: str


class NotificationItem(BaseModel):
    id: int
    title: str
    message: str
    link: str | None = None
    is_read: bool
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class NotificationListResponse(BaseModel):
    notifications: list[NotificationItem]


class UnreadCountResponse(BaseModel):
    unread_count: int
