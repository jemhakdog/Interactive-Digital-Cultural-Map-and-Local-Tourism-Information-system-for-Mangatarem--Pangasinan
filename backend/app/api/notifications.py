"""Notifications API router — newsletter subscribe, mark-read.

Migrated from modules/notifications/routes.py (Flask) to FastAPI.
"""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.database import get_db
from backend.app.core.dependencies import get_current_user
from backend.app.models.notifications import NewsletterSubscriber, UserNotification
from backend.app.models.user import User
from backend.app.schemas.notification import (
    NotificationItem,
    NotificationListResponse,
    SubscribeRequest,
    SubscribeResponse,
    UnreadCountResponse,
)

router = APIRouter()


@router.post("/subscribe", response_model=SubscribeResponse, summary="Subscribe to newsletter")
async def subscribe(
    body: SubscribeRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    # Check if user exists
    user_q = select(User).where(User.email == body.email)
    user_result = await db.execute(user_q)
    existing_user = user_result.scalar_one_or_none()
    user_id = existing_user.id if existing_user else None

    # Check existing subscription
    sub_q = select(NewsletterSubscriber).where(NewsletterSubscriber.email == body.email)
    sub_result = await db.execute(sub_q)
    existing_sub = sub_result.scalar_one_or_none()

    if existing_sub:
        if not existing_sub.is_active or existing_sub.user_id != user_id:
            existing_sub.is_active = True
            existing_sub.user_id = user_id
            return SubscribeResponse(status="success", message="Welcome back! You've been resubscribed.")
        return SubscribeResponse(status="info", message="You are already subscribed!")

    new_sub = NewsletterSubscriber(email=body.email, user_id=user_id)
    db.add(new_sub)
    return SubscribeResponse(status="success", message="Thank you for subscribing!")


@router.post("/mark-read", summary="Mark all notifications as read")
async def mark_all_read(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):
    result = await db.execute(
        select(UserNotification).where(
            UserNotification.user_id == user.id,
            UserNotification.is_read == False,  # noqa: E712
        )
    )
    notifications = result.scalars().all()
    for n in notifications:
        n.is_read = True
    return {"status": "success", "message": "All notifications marked as read"}


@router.post("/mark-read/{notification_id}", summary="Mark single notification as read")
async def mark_single_read(
    notification_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):
    result = await db.execute(
        select(UserNotification).where(
            UserNotification.id == notification_id,
            UserNotification.user_id == user.id,
        )
    )
    notification = result.scalar_one_or_none()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    notification.is_read = True
    return {"status": "success", "message": "Notification marked as read"}


@router.get(
    "/",
    response_model=NotificationListResponse,
    summary="List recent notifications for current user",
)
async def list_notifications(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    result = await db.execute(
        select(UserNotification)
        .where(UserNotification.user_id == user.id)
        .order_by(UserNotification.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    notifications = result.scalars().all()
    return NotificationListResponse(
        notifications=[NotificationItem.model_validate(n) for n in notifications]
    )


@router.get(
    "/unread",
    response_model=UnreadCountResponse,
    summary="Count unread notifications for current user",
)
async def unread_count(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):
    result = await db.execute(
        select(func.count(UserNotification.id)).where(
            UserNotification.user_id == user.id,
            UserNotification.is_read == False,  # noqa: E712
        )
    )
    count = result.scalar() or 0
    return UnreadCountResponse(unread_count=count)
