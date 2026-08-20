"""Admin visitor registry + visits analytics endpoints.

Mounted under /api by the wire agent (relative routes below).
Data source: VisitorLog model (no dedicated Visit model needed).
"""
from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.database import get_db
from backend.app.core.dependencies import require_admin
from backend.app.models.analytics import VisitorLog
from backend.app.models.attractions import Attraction
from backend.app.models.business import Establishment
from backend.app.models.user import User
from backend.app.schemas.visitor import (
    VisitResponse,
    VisitorRegistryResponse,
)

router = APIRouter()


# ─────────────────────────────────────────────
# Local response model (stats view for /visits)
# ─────────────────────────────────────────────
class VisitStatsResponse(BaseModel):
    """Analytics summary for the admin visits dashboard."""
    total: int = 0
    month_total: int = 0
    top_location: str | None = None


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────
def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid date: {value}")


async def _target_name(db: AsyncSession, target_type: str, target_id: int) -> str | None:
    """Resolve a visitor-log target's display name."""
    if target_type == "attraction":
        obj = await db.get(Attraction, target_id)
    elif target_type in ("establishment", "business"):
        obj = await db.get(Establishment, target_id)
    else:
        return None
    return getattr(obj, "name", None) if obj else None


async def _to_visit_response(v: VisitorLog, db: AsyncSession) -> VisitResponse:
    steward_user = await db.get(User, v.logged_by)
    return VisitResponse(
        id=v.id,
        visitor_name=v.visitor_name,
        visitor_age=v.visitor_age,
        visitor_address=v.visitor_address,
        target_type=v.target_type,
        target_id=v.target_id,
        target_name=await _target_name(db, v.target_type, v.target_id),
        visit_date=v.visit_date,
        steward=steward_user.username if steward_user else None,
        visitor_count=v.visitor_count,
        is_system_user=v.is_system_user,
        created_at=v.created_at,
    )


# ─────────────────────────────────────────────
# GET /visitor-registry — list visitor registry
# ─────────────────────────────────────────────
@router.get(
    "/visitor-registry",
    response_model=VisitorRegistryResponse,
    summary="List the visitor registry (admin)",
)
async def list_visitor_registry(
    db: Annotated[AsyncSession, Depends(get_db)],
    admin: Annotated[User, Depends(require_admin)],
    target_type: str | None = Query(None, description="attraction | establishment"),
    target_id: int | None = None,
    start_date: str | None = Query(None, description="YYYY-MM-DD"),
    end_date: str | None = Query(None, description="YYYY-MM-DD"),
    search: str | None = Query(None, description="visitor name substring"),
    page: Annotated[int, Query(ge=1)] = 1,
    per_page: Annotated[int, Query(ge=1, le=100)] = 20,
):
    stmt = select(VisitorLog)
    count_stmt = select(func.count()).select_from(VisitorLog)

    if target_type:
        # frontend filter uses "business"; model stores "establishment"
        tt = "establishment" if target_type == "business" else target_type
        stmt = stmt.where(VisitorLog.target_type == tt)
        count_stmt = count_stmt.where(VisitorLog.target_type == tt)
    if target_id is not None:
        stmt = stmt.where(VisitorLog.target_id == target_id)
        count_stmt = count_stmt.where(VisitorLog.target_id == target_id)

    sd = _parse_date(start_date)
    ed = _parse_date(end_date)
    if sd is not None:
        stmt = stmt.where(VisitorLog.visit_date >= sd)
        count_stmt = count_stmt.where(VisitorLog.visit_date >= sd)
    if ed is not None:
        stmt = stmt.where(VisitorLog.visit_date <= ed)
        count_stmt = count_stmt.where(VisitorLog.visit_date <= ed)

    if search:
        pattern = f"%{search.lower()}%"
        stmt = stmt.where(func.lower(VisitorLog.visitor_name).like(pattern))
        count_stmt = count_stmt.where(func.lower(VisitorLog.visitor_name).like(pattern))

    total = (await db.execute(count_stmt)).scalar() or 0

    stmt = stmt.order_by(
        VisitorLog.created_at.desc(), VisitorLog.visit_date.desc()
    ).offset((page - 1) * per_page).limit(per_page)

    rows = (await db.execute(stmt)).scalars().all()
    visitors = [await _to_visit_response(v, db) for v in rows]

    return VisitorRegistryResponse(visitors=visitors, total=total)


# ─────────────────────────────────────────────
# GET /visits — visitor analytics summary
# ─────────────────────────────────────────────
@router.get(
    "/visits",
    response_model=VisitStatsResponse,
    summary="Visitor analytics summary (admin)",
)
async def visits_stats(
    db: Annotated[AsyncSession, Depends(get_db)],
    admin: Annotated[User, Depends(require_admin)],
    start_date: str | None = Query(None, description="YYYY-MM-DD; bounds the period total"),
    end_date: str | None = Query(None, description="YYYY-MM-DD; bounds the period total"),
):
    sd = _parse_date(start_date)
    ed = _parse_date(end_date)

    # Period-bounded total (all logs when no bounds given)
    total_stmt = select(func.coalesce(func.sum(VisitorLog.visitor_count), 0))
    if sd is not None:
        total_stmt = total_stmt.where(VisitorLog.visit_date >= sd)
    if ed is not None:
        total_stmt = total_stmt.where(VisitorLog.visit_date <= ed)
    total = int((await db.execute(total_stmt)).scalar() or 0)

    # Current-month total (independent of the requested period; DB-agnostic)
    today = date.today()
    if today.month == 12:
        month_end = date(today.year, 12, 31)
    else:
        month_end = date(today.year, today.month + 1, 1) - timedelta(days=1)
    month_start = date(today.year, today.month, 1)
    month_stmt = (
        select(func.coalesce(func.sum(VisitorLog.visitor_count), 0))
        .where(VisitorLog.visit_date >= month_start)
        .where(VisitorLog.visit_date <= month_end)
    )
    month_total = int((await db.execute(month_stmt)).scalar() or 0)

    # Top location (period-bounded) by summed visitor_count
    top_stmt = (
        select(
            VisitorLog.target_type,
            VisitorLog.target_id,
            func.coalesce(func.sum(VisitorLog.visitor_count), 0).label("vc"),
        )
        .group_by(VisitorLog.target_type, VisitorLog.target_id)
        .order_by(func.sum(VisitorLog.visitor_count).desc())
        .limit(1)
    )
    if sd is not None:
        top_stmt = top_stmt.where(VisitorLog.visit_date >= sd)
    if ed is not None:
        top_stmt = top_stmt.where(VisitorLog.visit_date <= ed)
    top_row = (await db.execute(top_stmt)).first()
    top_location = None
    if top_row and top_row.target_id:
        top_location = await _target_name(db, top_row.target_type, top_row.target_id)

    return VisitStatsResponse(
        total=total,
        month_total=month_total,
        top_location=top_location,
    )
