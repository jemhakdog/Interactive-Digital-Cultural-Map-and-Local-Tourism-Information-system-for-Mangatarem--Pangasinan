"""Attraction CRUD + review routes.

Migrated from modules/attractions/routes.py (Flask) to FastAPI.
"""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.database import get_db
from backend.app.core.dependencies import get_current_active_user, require_admin
from backend.app.models.attractions import Attraction, Review
from backend.app.models.barangay import BarangayInfo
from backend.app.models.user import User
from backend.app.schemas.attraction import (
    AttractionCreate,
    AttractionListResponse,
    AttractionResponse,
    AttractionUpdate,
    PaginationMeta,
    ReviewCreate,
    ReviewCreateResponse,
    ReviewListResponse,
    ReviewResponse,
    ReviewSummary,
)

router = APIRouter()


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────
async def _get_attraction_or_404(attraction_id: int, db: AsyncSession) -> Attraction:
    att = await db.get(Attraction, attraction_id)
    if att is None:
        raise HTTPException(status_code=404, detail="Attraction not found")
    return att


async def _get_rating(attraction_id: int, db: AsyncSession) -> float | None:
    """Compute average rating for an attraction asynchronously."""
    stmt = (
        select(func.avg(Review.rating))
        .where(
            Review.attraction_id == attraction_id,
            Review.status == "approved",
            Review.parent_id.is_(None),
            Review.rating.isnot(None),
        )
    )
    result = await db.execute(stmt)
    avg_rating = result.scalar()
    return round(avg_rating, 1) if avg_rating else None


async def _attraction_to_dict(a: Attraction, db: AsyncSession) -> dict:
    barangay_name = None
    if a.barangay_id:
        b = await db.get(BarangayInfo, a.barangay_id)
        barangay_name = b.name if b else None

    return {
        "id": a.id,
        "name": a.name,
        "description": a.description,
        "category": a.category,
        "latitude": a.latitude,
        "longitude": a.longitude,
        "image_url": a.image_url,
        "barangay_id": a.barangay_id,
        "barangay_name": barangay_name,
        "status": a.status,
        "is_featured": a.is_featured,
        "physical_status": a.physical_status,
        "is_verified": a.is_verified,
        "opening_hours": a.opening_hours,
        "entrance_fee": a.entrance_fee,
        "contact_info": a.contact_info,
        "facilities": a.facilities,
        "advisory_message": a.advisory_message,
        "advisory_status": a.advisory_status,
        "directions": a.directions,
        "osm_alternatives": a.osm_alternatives,
        "heritage_profile_id": a.heritage_profile_id,
        "rating": await _get_rating(a.id, db),
        "created_at": a.created_at.isoformat() if a.created_at else None,
    }


async def _review_to_dict(r: Review, db: AsyncSession, include_replies: bool = True) -> dict:
    user = await db.get(User, r.user_id)
    d = {
        "id": r.id,
        "user_id": r.user_id,
        "username": user.username if user else "Visitor",
        "attraction_id": r.attraction_id,
        "establishment_id": r.establishment_id,
        "rating": r.rating,
        "comment": r.comment,
        "status": r.status,
        "parent_id": r.parent_id,
        "created_at": r.created_at.isoformat() if r.created_at else None,
        "photos": [{"id": i, "url": url} for i, url in enumerate(r.photo_urls or [])],
    }
    if include_replies:
        replies_stmt = (
            select(Review)
            .where(Review.parent_id == r.id, Review.status == "approved")
            .order_by(Review.created_at.asc())
        )
        replies_result = await db.execute(replies_stmt)
        d["replies"] = [
            await _review_to_dict(reply, db, include_replies=False)
            for reply in replies_result.scalars().all()
        ]
    else:
        d["replies"] = []
    return d


def _haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Simple haversine distance in km."""
    import math

    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


# ─────────────────────────────────────────────
# GET /api/attractions — list all
# ─────────────────────────────────────────────
@router.get("/", response_model=AttractionListResponse, summary="List attractions")
async def list_attractions(
    db: Annotated[AsyncSession, Depends(get_db)],
    page: Annotated[int, Query(ge=1)] = 1,
    per_page: Annotated[int, Query(ge=1, le=100)] = 20,
    category: str | None = None,
    barangay: str | None = None,
    is_featured: bool | None = None,
    lat: float | None = Query(None, ge=-90, le=90),
    lng: float | None = Query(None, ge=-180, le=180),
    radius: float = Query(10.0, gt=0),
):
    stmt = (
        select(Attraction)
        .where(Attraction.status == "approved")
        .order_by(Attraction.is_featured.desc(), Attraction.name)
    )

    if category and category != "all":
        stmt = stmt.where(Attraction.category == category)
    if barangay and barangay != "all":
        stmt = stmt.join(
            BarangayInfo, Attraction.barangay_id == BarangayInfo.id
        ).where(BarangayInfo.name == barangay)
    if is_featured is not None:
        stmt = stmt.where(Attraction.is_featured == is_featured)

    # Count total for pagination
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await db.execute(count_stmt)).scalar() or 0

    offset = (page - 1) * per_page
    stmt = stmt.offset(offset).limit(per_page)
    result = await db.execute(stmt)
    attractions = result.scalars().all()

    items = []
    for a in attractions:
        d = await _attraction_to_dict(a, db)
        if lat is not None and lng is not None and a.latitude and a.longitude:
            dist = _haversine(lat, lng, a.latitude, a.longitude)
            d["distance"] = round(dist, 2)
            if dist > radius:
                continue
        items.append(d)

    if lat is not None and lng is not None:
        items.sort(key=lambda x: x.get("distance", float("inf")))

    pages = max(1, -(-total // per_page))  # ceil division
    return AttractionListResponse(
        attractions=[AttractionResponse(**a) for a in items],
        pagination=PaginationMeta(
            page=page,
            per_page=per_page,
            total=total,
            pages=pages,
            has_next=page < pages,
            has_prev=page > 1,
        ),
    )


# ─────────────────────────────────────────────
# GET /api/attractions/{id} — detail
# ─────────────────────────────────────────────
@router.get("/{attraction_id}", response_model=AttractionResponse, summary="Attraction detail")
async def get_attraction(
    attraction_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    att = await _get_attraction_or_404(attraction_id, db)
    return AttractionResponse(**await _attraction_to_dict(att, db))


# ─────────────────────────────────────────────
# POST /api/attractions — create (admin)
# ─────────────────────────────────────────────
@router.post(
    "/",
    response_model=AttractionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create attraction",
)
async def create_attraction(
    body: AttractionCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    admin: Annotated[User, Depends(require_admin)],
):
    att = Attraction(
        **body.model_dump(),
        status="approved",
        user_id=admin.id,
    )
    db.add(att)
    await db.flush()
    await db.refresh(att)
    return AttractionResponse(**await _attraction_to_dict(att, db))


# ─────────────────────────────────────────────
# PUT /api/attractions/{id} — update (admin)
# ─────────────────────────────────────────────
@router.put(
    "/{attraction_id}",
    response_model=AttractionResponse,
    summary="Update attraction",
)
async def update_attraction(
    attraction_id: int,
    body: AttractionUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    admin: Annotated[User, Depends(require_admin)],
):
    att = await _get_attraction_or_404(attraction_id, db)
    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(att, field, value)
    await db.flush()
    await db.refresh(att)
    return AttractionResponse(**await _attraction_to_dict(att, db))


# ─────────────────────────────────────────────
# DELETE /api/attractions/{id} — delete (admin)
# ─────────────────────────────────────────────
@router.delete(
    "/{attraction_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete attraction",
)
async def delete_attraction(
    attraction_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    admin: Annotated[User, Depends(require_admin)],
):
    att = await _get_attraction_or_404(attraction_id, db)
    await db.delete(att)


# ─────────────────────────────────────────────
# GET /api/attractions/{id}/reviews — list reviews
# ─────────────────────────────────────────────
@router.get(
    "/{attraction_id}/reviews",
    response_model=ReviewListResponse,
    summary="List attraction reviews",
)
async def list_reviews(
    attraction_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    page: Annotated[int, Query(ge=1)] = 1,
    per_page: Annotated[int, Query(ge=1, le=20)] = 6,
):
    await _get_attraction_or_404(attraction_id, db)

    # Approved root reviews
    base_stmt = (
        select(Review)
        .where(
            Review.attraction_id == attraction_id,
            Review.parent_id.is_(None),
            Review.status == "approved",
        )
        .order_by(Review.created_at.desc())
    )

    count_stmt = select(func.count()).select_from(base_stmt.subquery())
    total = (await db.execute(count_stmt)).scalar() or 0

    offset = (page - 1) * per_page
    stmt = base_stmt.offset(offset).limit(per_page)
    result = await db.execute(stmt)
    reviews = result.scalars().all()

    reviews_data = [await _review_to_dict(r, db) for r in reviews]

    # Rating summary
    sum_stmt = (
        select(Review.rating)
        .where(
            Review.attraction_id == attraction_id,
            Review.status == "approved",
            Review.parent_id.is_(None),
            Review.rating.is_not(None),
        )
    )
    ratings = [(await db.execute(sum_stmt)).scalars().all()]
    flat_ratings = [r for batch in ratings for r in batch]
    avg = round(sum(flat_ratings) / len(flat_ratings), 1) if flat_ratings else 0
    distribution = {str(i): flat_ratings.count(i) for i in range(1, 6)}

    pages = max(1, -(-total // per_page))
    return ReviewListResponse(
        reviews=[ReviewResponse(**rd) for rd in reviews_data],
        pending_reviews=[],
        summary=ReviewSummary(average=avg, total=len(flat_ratings), distribution=distribution),
        pagination=PaginationMeta(
            page=page,
            per_page=per_page,
            total=total,
            pages=pages,
            has_next=page < pages,
            has_prev=page > 1,
        ),
    )


# ─────────────────────────────────────────────
# POST /api/attractions/{id}/reviews — add review
# ─────────────────────────────────────────────
@router.post(
    "/{attraction_id}/reviews",
    response_model=ReviewCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Post a review",
)
async def post_review(
    attraction_id: int,
    body: ReviewCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_active_user)],
):
    await _get_attraction_or_404(attraction_id, db)

    if body.parent_id:
        parent = await db.get(Review, body.parent_id)
        if parent is None:
            raise HTTPException(status_code=404, detail="Parent review not found")
        if parent.parent_id is not None:
            raise HTTPException(status_code=400, detail="Cannot reply to a sub-reply")
        if parent.attraction_id != attraction_id:
            raise HTTPException(status_code=400, detail="Parent review does not match this attraction")
    else:
        if body.rating is None or not (1 <= body.rating <= 5):
            raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")

    review = Review(
        user_id=user.id,
        attraction_id=attraction_id,
        rating=body.rating,
        comment=body.comment,
        parent_id=body.parent_id,
        status="approved",
    )
    db.add(review)
    await db.flush()
    await db.refresh(review)

    return ReviewCreateResponse(
        success=True,
        review_id=review.id,
        photos_saved=0,
        message="Your review has been posted successfully. Thank you!",
    )
