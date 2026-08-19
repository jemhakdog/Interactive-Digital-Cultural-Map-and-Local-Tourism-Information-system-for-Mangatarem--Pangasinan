"""Analytics models — ported from modules/analytics/models.py."""
from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.models.base import Base


class AnalyticsPageView(Base):
    __tablename__ = "ANALYTICS_PAGE_VIEW"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    page_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    view_type: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    item_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    page_name: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    user_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    timestamp: Mapped[datetime | None] = mapped_column(
        DateTime, default=datetime.utcnow, index=True
    )
    session_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    device_info: Mapped[str | None] = mapped_column(Text, nullable=True)


class DatabaseAuditLog(Base):
    __tablename__ = "DATABASE_AUDIT_LOG"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("USER.id"), nullable=True, index=True
    )
    action: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    table_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    record_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(500), nullable=True)
    query_summary: Mapped[str | None] = mapped_column(String(500), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="success", index=True)
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime, default=datetime.utcnow, index=True
    )

    user = relationship("User", back_populates="audit_logs")

    @classmethod
    async def log_operation(
        cls,
        db,
        user_id: int | None,
        action: str,
        table_name: str,
        record_id: int | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
        query_summary: str | None = None,
        status: str = "success",
    ):
        log = cls(
            user_id=user_id,
            action=action,
            table_name=table_name,
            record_id=record_id,
            ip_address=ip_address,
            user_agent=user_agent,
            query_summary=query_summary,
            status=status,
        )
        db.add(log)
        await db.flush()
        return log


class VisitorLog(Base):
    __tablename__ = "VISITOR_LOG"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    target_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    target_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    visitor_count: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    visitor_name: Mapped[str | None] = mapped_column(String(150), nullable=True)
    visitor_age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    visitor_address: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_system_user: Mapped[bool] = mapped_column(Boolean, default=False)
    visit_date: Mapped[date | None] = mapped_column(Date, default=date.today, index=True)
    logged_by: Mapped[int] = mapped_column(
        Integer, ForeignKey("USER.id"), nullable=False, index=True
    )
    visitor_user_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("USER.id"), nullable=True, index=True
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime, default=datetime.utcnow)

    steward = relationship("User", foreign_keys=[logged_by])
    visitor_user = relationship("User", foreign_keys=[visitor_user_id])
