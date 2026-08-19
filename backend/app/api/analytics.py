"""Analytics API router — visitor log, page views.

Migrated from modules/analytics/routes.py (Flask) to FastAPI.
"""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.database import get_db
from backend.app.core.dependencies import get_current_active_user, get_current_user
from backend.app.models.analytics import VisitorLog
from backend.app.models.attractions import Attraction
from backend.app.models.business import Establishment
from backend.app.models.user import User
from backend.app.schemas.analytics import VisitorLogRequest

router = APIRouter()


@router.post(
    "/log-visitor/{target_type}/{target_id}",
    status_code=status.HTTP_201_CREATED,
    summary="Log a visitor for an attraction or establishment",
)
async def log_visitor(
    target_type: str,
    target_id: int,
    body: VisitorLogRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_active_user)],
):
    if target_type not in ("establishment", "attraction"):
        raise HTTPException(status_code=400, detail="Invalid target type")

    # Permission check
    if target_type == "establishment":
        result = await db.execute(select(Establishment).where(Establishment.id == target_id))
        target = result.scalar_one_or_none()
        if not target:
            raise HTTPException(status_code=404, detail="Establishment not found")
        if target.owner_id != user.id and user.role != "admin":
            raise HTTPException(status_code=403, detail="Unauthorized")
    else:
        result = await db.execute(select(Attraction).where(Attraction.id == target_id))
        target = result.scalar_one_or_none()
        if not target:
            raise HTTPException(status_code=404, detail="Attraction not found")
        is_steward = target.user_id == user.id
        is_rep = user.role == "contributor" and target.barangay_id == user.barangay_id
        if not is_steward and not is_rep and user.role != "admin":
            raise HTTPException(status_code=403, detail="Access denied")

    log = VisitorLog(
        target_type=target_type,
        target_id=target_id,
        visitor_name=body.visitor_name,
        visitor_age=body.visitor_age,
        visitor_address=body.visitor_address,
        is_system_user=body.is_system_user,
        visitor_count=max(1, body.visitor_count),
        logged_by=user.id,
        notes=body.notes,
    )
    db.add(log)

    return {"success": True, "message": f"Visitor log recorded for '{getattr(target, 'name', 'Unknown')}'"}


@router.get("/summary", summary="Get analytics summary (admin only)")
async def analytics_summary(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_active_user)],
):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    from sqlalchemy import func
    from backend.app.models.analytics import DatabaseAuditLog, AnalyticsPageView

    # Total visitors
    visitor_count = await db.execute(select(func.count(VisitorLog.id)))
    total_visitors = visitor_count.scalar() or 0

    # Total page views
    page_view_count = await db.execute(select(func.count(AnalyticsPageView.id)))
    total_page_views = page_view_count.scalar() or 0

    # Recent visitors (last 7 days)
    from datetime import datetime, timedelta
    week_ago = datetime.utcnow() - timedelta(days=7)
    recent_count = await db.execute(
        select(func.count(VisitorLog.id)).where(VisitorLog.created_at >= week_ago)
    )
    recent_visitors = recent_count.scalar() or 0

    return {
        "total_visitors": total_visitors,
        "total_page_views": total_page_views,
        "recent_visitors_7d": recent_visitors,
    }
