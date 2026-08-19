"""Chat API router — rooms and messages.

Migrated from modules/chat/routes.py (Flask) to FastAPI.
"""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.app.core.database import get_db
from backend.app.core.dependencies import get_current_user
from backend.app.models.chat import ChatMessage, ChatParticipant, ChatRoom
from backend.app.models.user import User
from backend.app.schemas.chat import (
    ChatMessageListResponse,
    ChatMessageResponse,
    ChatRoomListResponse,
    ChatRoomResponse,
    SendMessageRequest,
    SendMessageResponse,
)

router = APIRouter()


@router.get("/", summary="List chat rooms for current user")
async def list_rooms(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):
    """Return rooms the current user is a participant of."""
    part_q = select(ChatParticipant.chat_room_id).where(ChatParticipant.user_id == user.id)
    room_ids = (await db.execute(part_q)).scalars().all()

    if not room_ids:
        return {"status": "success", "rooms": []}

    rooms_q = select(ChatRoom).where(ChatRoom.id.in_(room_ids))
    rooms = (await db.execute(rooms_q)).scalars().all()

    room_data = []
    for r in rooms:
        name = f"Room {r.id}"
        room_data.append({
            "id": r.id,
            "type": r.type,
            "name": name,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        })

    return {"status": "success", "rooms": room_data}


@router.get("/{room_id}", summary="Get chat room messages")
async def get_room_messages(
    room_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
):
    room_result = await db.execute(select(ChatRoom).where(ChatRoom.id == room_id))
    room = room_result.scalar_one_or_none()
    if not room:
        raise HTTPException(status_code=404, detail="Chat room not found")

    # Authorization
    part_result = await db.execute(
        select(ChatParticipant).where(
            ChatParticipant.chat_room_id == room_id,
            ChatParticipant.user_id == user.id,
        )
    )
    is_participant = part_result.scalar_one_or_none()
    if not is_participant and room.type != "barangay":
        raise HTTPException(status_code=403, detail="Not authorized to view this room")

    # Paginated messages
    msg_q = (
        select(ChatMessage)
        .where(ChatMessage.chat_room_id == room_id)
        .order_by(ChatMessage.created_at.desc())
    )
    count_q = select(func.count()).select_from(msg_q.subquery())
    total = (await db.execute(count_q)).scalar() or 0

    offset = (page - 1) * per_page
    msg_q = msg_q.offset(offset).limit(per_page)
    messages = (await db.execute(msg_q)).scalars().all()

    msg_data = []
    for msg in reversed(messages):
        msg_data.append({
            "id": msg.id,
            "sender_id": msg.sender_id,
            "sender_name": "System",
            "content": msg.content,
            "created_at": msg.created_at.isoformat() if msg.created_at else None,
            "is_system_msg": msg.is_system_msg,
        })

    pages = (total + per_page - 1) // per_page
    return {
        "status": "success",
        "room_id": room_id,
        "messages": msg_data,
        "has_next": page < pages,
        "has_prev": page > 1,
        "page": page,
    }


@router.post("/{room_id}/messages", status_code=201, summary="Send message")
async def send_message(
    room_id: int,
    body: SendMessageRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):
    room_result = await db.execute(select(ChatRoom).where(ChatRoom.id == room_id))
    room = room_result.scalar_one_or_none()
    if not room:
        raise HTTPException(status_code=404, detail="Chat room not found")

    # Check membership
    part_result = await db.execute(
        select(ChatParticipant).where(
            ChatParticipant.chat_room_id == room_id,
            ChatParticipant.user_id == user.id,
        )
    )
    if not part_result.scalar_one_or_none() and room.type != "barangay":
        raise HTTPException(status_code=403, detail="Not a participant of this room")

    msg = ChatMessage(
        chat_room_id=room_id,
        sender_id=user.id,
        content=body.content,
        is_system_msg=False,
    )
    db.add(msg)
    await db.flush()

    return {
        "status": "success",
        "message": {
            "id": msg.id,
            "sender_id": msg.sender_id,
            "sender_name": user.username,
            "content": msg.content,
            "created_at": msg.created_at.isoformat() if msg.created_at else None,
        },
    }
