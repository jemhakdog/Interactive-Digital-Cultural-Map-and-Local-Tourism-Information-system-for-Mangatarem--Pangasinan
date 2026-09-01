"""User model — ported from modules/auth/models.py."""
from __future__ import annotations

import secrets
from datetime import datetime, timedelta, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash
from passlib.context import CryptContext

from backend.app.models.base import Base

# Legacy passlib bcrypt hashes (user created before the Werkzeug migration)
_bcrypt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "USER"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str | None] = mapped_column(String(20), default="user", index=True)
    barangay_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("BARANGAY_INFO.id"), nullable=True, index=True
    )
    is_approved: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime, default=datetime.utcnow, index=True
    )
    reset_token: Mapped[str | None] = mapped_column(
        String(128), unique=True, nullable=True
    )
    reset_token_expires_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True
    )
    reset_token_used: Mapped[bool | None] = mapped_column(Boolean, default=False, nullable=True)

    # Relationships
    barangay = relationship("BarangayInfo", foreign_keys=[barangay_id], back_populates="residents")
    managed_barangay_info = relationship("BarangayInfo", foreign_keys="[BarangayInfo.user_id]")
    attractions = relationship("Attraction", foreign_keys="[Attraction.user_id]")
    events = relationship("Event", foreign_keys="[Event.user_id]")
    establishments = relationship("Establishment", foreign_keys="[Establishment.owner_id]")
    profiles = relationship("HeritageProfile", foreign_keys="[HeritageProfile.user_id]")
    favorites = relationship("UserFavorite", back_populates="user", lazy="dynamic")
    reviews = relationship("Review", back_populates="user", lazy="dynamic")
    announcements = relationship("Announcement", foreign_keys="[Announcement.user_id]")
    audit_logs = relationship("DatabaseAuditLog", back_populates="user")
    newsletter_subscriptions = relationship("NewsletterSubscriber", back_populates="user", lazy="dynamic")
    sent_newsletters = relationship("NewsletterHistory", back_populates="sender", lazy="dynamic")
    notifications = relationship("UserNotification", back_populates="user", lazy="dynamic", cascade="all, delete-orphan")
    passports = relationship("UserPassport", back_populates="user", lazy=True, cascade="all, delete-orphan")
    check_ins = relationship("TouristCheckIn", back_populates="user", lazy=True, cascade="all, delete-orphan")
    reservations = relationship("Reservation", back_populates="user", lazy="dynamic")
    business_verification = relationship("BusinessVerification", back_populates="user", uselist=False)
    chat_memberships = relationship("ChatParticipant")
    sent_messages = relationship("ChatMessage")

    def set_password(self, password: str) -> None:
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        try:
            return check_password_hash(self.password, password)
        except ValueError:
            # Legacy bcrypt hashes use passlib format Werkzeug can't parse
            return _bcrypt.verify(password, self.password)

    # --- Password-reset helpers (ported from Flask shim) ---
    def create_reset_token(self, expiry_minutes: int = 30) -> str:
        self.reset_token = secrets.token_hex(32)
        self.reset_token_expires_at = datetime.utcnow() + timedelta(minutes=expiry_minutes)
        self.reset_token_used = False
        return self.reset_token

    @property
    def is_reset_token_valid(self) -> bool:
        if self.reset_token_expires_at is None:
            return False
        expires = self.reset_token_expires_at
        if expires.tzinfo is not None:
            expires = expires.astimezone(timezone.utc).replace(tzinfo=None)
        return not self.reset_token_used and datetime.utcnow() < expires
