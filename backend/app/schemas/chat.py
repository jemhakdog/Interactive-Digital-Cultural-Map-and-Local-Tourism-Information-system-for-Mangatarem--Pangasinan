"""Pydantic schemas for the Chat module."""
from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel


class ChatRoomResponse(BaseModel):
    id: int
    type: str | None = None
    name: str
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class ChatRoomListResponse(BaseModel):
    status: str
    rooms: list[ChatRoomResponse]


class ChatMessageResponse(BaseModel):
    id: int
    sender_id: int | None = None
    sender_name: str = "System"
    content: str
    created_at: datetime | None = None
    is_system_msg: bool = False


class ChatMessageListResponse(BaseModel):
    status: str
    room_id: int
    messages: list[ChatMessageResponse]
    has_next: bool
    has_prev: bool
    page: int


class SendMessageRequest(BaseModel):
    content: str


class SendMessageResponse(BaseModel):
    status: str
    message: ChatMessageResponse
