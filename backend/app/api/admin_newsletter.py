"""Admin Newsletter endpoints (mounted at /api/newsletter).

- GET  /subscribers -> list subscribers
- POST /send        -> record a newsletter dispatch (no real email in dev)
- GET  /history     -> list sent dispatches

Frontend: frontend/src/app/admin/newsletter/page.tsx
Schemas: backend/app/schemas/newsletter.py
Models:  backend/app/models/notifications.py
"""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.database import get_db
from backend.app.core.dependencies import require_admin
from backend.app.models.notifications import NewsletterHistory, NewsletterSubscriber
from backend.app.models.user import User
from backend.app.schemas.newsletter import (
    NewsletterHistoryResponse,
    NewsletterSend,
    SubscriberResponse,
)

router = APIRouter()


# ─────────────────────────────────────────────
# GET /subscribers — list subscribers
# ─────────────────────────────────────────────
@router.get(
    "/subscribers",
    response_model=list[SubscriberResponse],
    summary="List newsletter subscribers",
)
async def list_subscribers(
    db: Annotated[AsyncSession, Depends(get_db)],
    admin: Annotated[User, Depends(require_admin)],
):
    stmt = select(NewsletterSubscriber).order_by(
        NewsletterSubscriber.created_at.desc()
    )
    result = await db.execute(stmt)
    subscribers = result.scalars().all()
    return [SubscriberResponse.model_validate(s) for s in subscribers]


# ─────────────────────────────────────────────
# POST /send — record a newsletter dispatch
# ─────────────────────────────────────────────
@router.post(
    "/send",
    response_model=NewsletterHistoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Send (record) a newsletter dispatch",
)
async def send_newsletter(
    body: NewsletterSend,
    db: Annotated[AsyncSession, Depends(get_db)],
    admin: Annotated[User, Depends(require_admin)],
):
    # Count active subscribers (recipients). No real email is sent in dev.
    total_active = (
        await db.execute(
            select(func.count()).where(NewsletterSubscriber.is_active.is_(True))
        )
    ).scalar() or 0

    dispatch = NewsletterHistory(
        subject=body.subject,
        content=body.content,
        recipient_count=total_active,
        sender_id=admin.id,
    )
    db.add(dispatch)
    await db.flush()
    await db.refresh(dispatch)
    return NewsletterHistoryResponse.model_validate(dispatch)


# ─────────────────────────────────────────────
# GET /history — list sent dispatches
# ─────────────────────────────────────────────
@router.get(
    "/history",
    response_model=list[NewsletterHistoryResponse],
    summary="List newsletter dispatch history",
)
async def list_history(
    db: Annotated[AsyncSession, Depends(get_db)],
    admin: Annotated[User, Depends(require_admin)],
):
    stmt = select(NewsletterHistory).order_by(
        NewsletterHistory.sent_at.desc()
    )
    result = await db.execute(stmt)
    history = result.scalars().all()
    return [NewsletterHistoryResponse.model_validate(h) for h in history]


# ─────────────────────────────────────────────
# DELETE /subscribers/{id} — unsubscribe (deactivate) a subscriber
# ─────────────────────────────────────────────
@router.delete(
    "/subscribers/{subscriber_id}",
    summary="Unsubscribe a newsletter subscriber",
)
async def unsubscribe_subscriber(
    subscriber_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    admin: Annotated[User, Depends(require_admin)],
):
    """Deactivate a subscriber so they no longer count as a dispatch recipient."""
    subscriber = await db.get(NewsletterSubscriber, subscriber_id)
    if subscriber is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscriber not found")
    subscriber.is_active = False
    await db.flush()
    return {"success": True, "id": subscriber.id, "is_active": False}
