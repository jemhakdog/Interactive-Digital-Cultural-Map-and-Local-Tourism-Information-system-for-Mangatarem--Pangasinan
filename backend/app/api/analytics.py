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


@router.get("/overview", summary="Get detailed analytics overview (admin only)")
async def analytics_overview(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_active_user)],
    start_date: str | None = Query(None, description="YYYY-MM-DD"),
    end_date: str | None = Query(None, description="YYYY-MM-DD"),
    days: int = Query(30, ge=7, le=365),
):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    from datetime import date, datetime, timedelta
    from sqlalchemy import func, desc, case
    from backend.app.models.analytics import AnalyticsPageView

    today = date.today()
    sd: date | None = None
    ed: date | None = None

    if start_date:
        try:
            sd = date.fromisoformat(start_date)
        except ValueError:
            pass
    if end_date:
        try:
            ed = date.fromisoformat(end_date)
        except ValueError:
            pass

    if not sd:
        sd = today - timedelta(days=days)
    if not ed:
        ed = today

    # 1. Total visitors & check-ins
    total_visitor_sum_stmt = select(func.coalesce(func.sum(VisitorLog.visitor_count), 0))
    total_checkins_stmt = select(func.count(VisitorLog.id))
    
    total_visitor_sum_stmt = total_visitor_sum_stmt.where(VisitorLog.visit_date >= sd, VisitorLog.visit_date <= ed)
    total_checkins_stmt = total_checkins_stmt.where(VisitorLog.visit_date >= sd, VisitorLog.visit_date <= ed)

    total_visitors = (await db.execute(total_visitor_sum_stmt)).scalar() or 0
    total_checkins = (await db.execute(total_checkins_stmt)).scalar() or 0

    # 2. Total all-time page views and period page views
    total_page_views = (await db.execute(select(func.count(AnalyticsPageView.id)))).scalar() or 0
    
    # 3. 7-day velocity
    week_ago = today - timedelta(days=7)
    recent_7d_stmt = select(func.coalesce(func.sum(VisitorLog.visitor_count), 0)).where(
        VisitorLog.visit_date >= week_ago, VisitorLog.visit_date <= today
    )
    recent_visitors_7d = (await db.execute(recent_7d_stmt)).scalar() or 0

    # 4. Target type breakdown (attractions vs establishments)
    type_stmt = (
        select(
            VisitorLog.target_type,
            func.coalesce(func.sum(VisitorLog.visitor_count), 0).label("visitors"),
            func.count(VisitorLog.id).label("checkins"),
        )
        .where(VisitorLog.visit_date >= sd, VisitorLog.visit_date <= ed)
        .group_by(VisitorLog.target_type)
    )
    type_rows = (await db.execute(type_stmt)).all()
    by_type = {
        "attraction": {"visitors": 0, "checkins": 0},
        "establishment": {"visitors": 0, "checkins": 0},
    }
    for row in type_rows:
        tt = "establishment" if row.target_type in ("establishment", "business") else row.target_type
        if tt in by_type:
            by_type[tt]["visitors"] += int(row.visitors)
            by_type[tt]["checkins"] += int(row.checkins)

    # 5. Daily trends
    trend_stmt = (
        select(
            VisitorLog.visit_date,
            func.coalesce(func.sum(VisitorLog.visitor_count), 0).label("visitors"),
            func.count(VisitorLog.id).label("checkins"),
        )
        .where(VisitorLog.visit_date >= sd, VisitorLog.visit_date <= ed)
        .group_by(VisitorLog.visit_date)
        .order_by(VisitorLog.visit_date.asc())
    )
    trend_rows = (await db.execute(trend_stmt)).all()
    trend_dict = {
        r.visit_date.isoformat() if hasattr(r.visit_date, "isoformat") else str(r.visit_date): {
            "visitors": int(r.visitors),
            "checkins": int(r.checkins),
        }
        for r in trend_rows if r.visit_date
    }

    # Fill full date range continuity
    daily_trends = []
    curr = sd
    while curr <= ed:
        curr_str = curr.isoformat()
        daily_trends.append({
            "date": curr_str,
            "visitors": trend_dict.get(curr_str, {}).get("visitors", 0),
            "checkins": trend_dict.get(curr_str, {}).get("checkins", 0),
        })
        curr += timedelta(days=1)

    # 6. Top destinations (Attractions & Establishments)
    top_stmt = (
        select(
            VisitorLog.target_type,
            VisitorLog.target_id,
            func.coalesce(func.sum(VisitorLog.visitor_count), 0).label("visitors"),
            func.count(VisitorLog.id).label("checkins"),
        )
        .where(VisitorLog.visit_date >= sd, VisitorLog.visit_date <= ed)
        .group_by(VisitorLog.target_type, VisitorLog.target_id)
        .order_by(desc("visitors"))
        .limit(10)
    )
    top_rows = (await db.execute(top_stmt)).all()

    # Pre-fetch attractions & establishments for name resolution
    attraction_ids = [r.target_id for r in top_rows if r.target_type == "attraction"]
    establishment_ids = [r.target_id for r in top_rows if r.target_type in ("establishment", "business")]

    attractions_map = {}
    if attraction_ids:
        att_res = await db.execute(select(Attraction.id, Attraction.name).where(Attraction.id.in_(attraction_ids)))
        attractions_map = {row.id: row.name for row in att_res.all()}

    establishments_map = {}
    if establishment_ids:
        est_res = await db.execute(select(Establishment.id, Establishment.name).where(Establishment.id.in_(establishment_ids)))
        establishments_map = {row.id: row.name for row in est_res.all()}

    top_destinations = []
    for r in top_rows:
        tt = "establishment" if r.target_type in ("establishment", "business") else r.target_type
        name = attractions_map.get(r.target_id) if tt == "attraction" else establishments_map.get(r.target_id)
        top_destinations.append({
            "target_type": tt,
            "target_id": r.target_id,
            "name": name or f"Destination #{r.target_id}",
            "visitors": int(r.visitors),
            "checkins": int(r.checkins),
        })

    # 7. Demographics
    age_stmt = select(
        case(
            (VisitorLog.visitor_age < 18, "0-17"),
            (VisitorLog.visitor_age.between(18, 35), "18-35"),
            (VisitorLog.visitor_age.between(36, 59), "36-59"),
            (VisitorLog.visitor_age >= 60, "60+"),
            else_="unspecified",
        ).label("age_group"),
        func.coalesce(func.sum(VisitorLog.visitor_count), 0).label("visitors"),
    ).where(VisitorLog.visit_date >= sd, VisitorLog.visit_date <= ed).group_by("age_group")
    
    age_rows = (await db.execute(age_stmt)).all()
    age_groups = {"0-17": 0, "18-35": 0, "36-59": 0, "60+": 0, "unspecified": 0}
    for row in age_rows:
        if row.age_group in age_groups:
            age_groups[row.age_group] = int(row.visitors)

    # System users vs guests
    user_type_stmt = select(
        VisitorLog.is_system_user,
        func.coalesce(func.sum(VisitorLog.visitor_count), 0).label("visitors"),
    ).where(VisitorLog.visit_date >= sd, VisitorLog.visit_date <= ed).group_by(VisitorLog.is_system_user)
    user_type_rows = (await db.execute(user_type_stmt)).all()
    system_users = 0
    guests = 0
    for row in user_type_rows:
        if row.is_system_user:
            system_users += int(row.visitors)
        else:
            guests += int(row.visitors)

    # 8. Recent Check-in Logs (up to 15)
    recent_logs_stmt = (
        select(VisitorLog)
        .order_by(VisitorLog.visit_date.desc(), VisitorLog.created_at.desc())
        .limit(15)
    )
    recent_logs_res = (await db.execute(recent_logs_stmt)).scalars().all()

    # Collect IDs for recent logs resolution
    recent_att_ids = [l.target_id for l in recent_logs_res if l.target_type == "attraction"]
    recent_est_ids = [l.target_id for l in recent_logs_res if l.target_type in ("establishment", "business")]
    steward_ids = [l.logged_by for l in recent_logs_res if l.logged_by]

    all_att_map = {**attractions_map}
    if recent_att_ids:
        needed = [i for i in recent_att_ids if i not in all_att_map]
        if needed:
            res = await db.execute(select(Attraction.id, Attraction.name).where(Attraction.id.in_(needed)))
            for row in res.all():
                all_att_map[row.id] = row.name

    all_est_map = {**establishments_map}
    if recent_est_ids:
        needed = [i for i in recent_est_ids if i not in all_est_map]
        if needed:
            res = await db.execute(select(Establishment.id, Establishment.name).where(Establishment.id.in_(needed)))
            for row in res.all():
                all_est_map[row.id] = row.name

    stewards_map = {}
    if steward_ids:
        res = await db.execute(select(User.id, User.name, User.username).where(User.id.in_(steward_ids)))
        for row in res.all():
            stewards_map[row.id] = row.name or row.username

    recent_logs_data = []
    for l in recent_logs_res:
        tt = "establishment" if l.target_type in ("establishment", "business") else l.target_type
        target_name = all_att_map.get(l.target_id) if tt == "attraction" else all_est_map.get(l.target_id)
        recent_logs_data.append({
            "id": l.id,
            "visitor_name": l.visitor_name or "Anonymous Visitor",
            "visitor_age": l.visitor_age,
            "visitor_address": l.visitor_address,
            "target_type": tt,
            "target_id": l.target_id,
            "target_name": target_name or f"Spot #{l.target_id}",
            "visitor_count": l.visitor_count,
            "is_system_user": l.is_system_user,
            "visit_date": l.visit_date.isoformat() if l.visit_date else None,
            "steward": stewards_map.get(l.logged_by, "Staff"),
            "notes": l.notes,
        })

    return {
        "period": {
            "start_date": sd.isoformat(),
            "end_date": ed.isoformat(),
            "days": (ed - sd).days + 1,
        },
        "summary": {
            "total_visitors": total_visitors,
            "total_checkins": total_checkins,
            "total_page_views": total_page_views,
            "recent_visitors_7d": recent_visitors_7d,
            "avg_group_size": round(total_visitors / total_checkins, 1) if total_checkins > 0 else 1.0,
        },
        "by_type": by_type,
        "daily_trends": daily_trends,
        "top_destinations": top_destinations,
        "demographics": {
            "age_groups": age_groups,
            "system_users": system_users,
            "guests": guests,
        },
        "recent_logs": recent_logs_data,
    }
