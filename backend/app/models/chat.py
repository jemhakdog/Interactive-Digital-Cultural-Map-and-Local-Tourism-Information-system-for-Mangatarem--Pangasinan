"""Chat models — ported from modules/chat/models.py."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.models.base import Base


class ChatRoom(Base):
    __tablename__ = "CHAT_ROOM"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(String(20), nullable=False)
    barangay_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("BARANGAY_INFO.id"), nullable=True, index=True
    )
    establishment_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("ESTABLISHMENT.id"), nullable=True, index=True
    )
    created_at: Mapped[datetime | None] = mapped_column(DateTime, default=datetime.utcnow)

    barangay = relationship("BarangayInfo")
    establishment = relationship("Establishment")
    messages = relationship("ChatMessage", back_populates="room", cascade="all, delete-orphan", lazy="dynamic")
    participants = relationship("ChatParticipant", back_populates="room", cascade="all, delete-orphan")


class ChatParticipant(Base):
    __tablename__ = "CHAT_PARTICIPANT"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chat_room_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("CHAT_ROOM.id"), nullable=False, index=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("USER.id"), nullable=False, index=True
    )
    joined_at: Mapped[datetime | None] = mapped_column(DateTime, default=datetime.utcnow)
    last_read_at: Mapped[datetime | None] = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    room = relationship("ChatRoom", back_populates="participants")


class ChatMessage(Base):
    __tablename__ = "CHAT_MESSAGE"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chat_room_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("CHAT_ROOM.id"), nullable=False, index=True
    )
    sender_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("USER.id"), nullable=False, index=True
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime, default=datetime.utcnow, index=True
    )
    is_system_msg: Mapped[bool] = mapped_column(Boolean, default=False)

    sender = relationship("User")
    room = relationship("ChatRoom", back_populates="messages")
