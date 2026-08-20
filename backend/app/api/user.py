"""Tourist user router — profile, stats, favorites, visits.

Mounted under /api/user (prefix applied centrally in main.py).
Auth: any logged-in user (Depends(get_current_user)) on every route.
"""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.database import get_db
from backend.app.core.dependencies import get_current_user
from backend.app.models.attractions import Attraction, Review, UserFavorite
from backend.app.models.business import Establishment
from backend.app.models.gamification import TouristCheckIn, UserPassport
from backend.app.models.user import User
from backend.app.schemas.user import (
    FavoriteResponse,
    UserProfileResponse,
    UserStatsResponse,
    VisitResponse,
)

router = APIRouter()


# ─────────────────────────────────────────────
# Local request model (shared schema lacks password)
# ─────────────────────────────────────────────
class ProfileUpdate(BaseModel):
    """Editable profile fields for the current user (+ optional password)."""
    name: str | None = Field(None, min_length=2, max_length=80)
    email: str | None = None
    password: str | None = Field(None, min_length=6)


# ─────────────────────────────────────────────
# GET /profile — current user profile
# ─────────────────────────────────────────────
@router.get("/profile", response_model=UserProfileResponse, summary="Get profile")
async def get_profile(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return UserProfileResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        name=current_user.username,  # frontend reads `name`
        role=current_user.role or "user",
        is_approved=current_user.is_approved,
        barangay_id=current_user.barangay_id,
        created_at=current_user.created_at,
    )


# ─────────────────────────────────────────────
# PUT /profile — update name/email (+ optional password)
# ─────────────────────────────────────────────
@router.put("/profile", response_model=UserProfileResponse, summary="Update profile")
async def update_profile(
    body: ProfileUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    # Guard against email collisions (excluding self).
    if body.email is not None and body.email != current_user.email:
        existing = await db.execute(select(User).where(User.email == body.email))
        if existing.scalar_one_or_none() is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already in use",
            )
        current_user.email = body.email

    if body.name is not None:
        current_user.username = body.name

    if body.password is not None:
        current_user.set_password(body.password)

    await db.flush()
    await db.refresh(current_user)
    return UserProfileResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        name=current_user.username,
        role=current_user.role or "user",
        is_approved=current_user.is_approved,
        barangay_id=current_user.barangay_id,
        created_at=current_user.created_at,
    )


# ─────────────────────────────────────────────
# GET /stats — dashboard stats
# ─────────────────────────────────────────────
@router.get("/stats", response_model=UserStatsResponse, summary="Dashboard stats")
async def get_stats(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    favorites_count = (
        await db.execute(
            select(func.count())
            .select_from(UserFavorite)
            .where(UserFavorite.user_id == current_user.id)
        )
    ).scalar() or 0

    reviews_count = (
        await db.execute(
            select(func.count())
            .select_from(Review)
            .where(Review.user_id == current_user.id)
        )
    ).scalar() or 0

    check_ins_count = 0
    visits_count = 0
    total_stamps = 0
    try:
        check_ins_count = (
            await db.execute(
                select(func.count())
                .select_from(TouristCheckIn)
                .where(TouristCheckIn.user_id == current_user.id)
            )
        ).scalar() or 0

        # Distinct attractions visited (places visited).
        visits_count = (
            await db.execute(
                select(func.count(func.distinct(TouristCheckIn.attraction_id)))
                .select_from(TouristCheckIn)
                .where(
                    TouristCheckIn.user_id == current_user.id,
                    TouristCheckIn.attraction_id.isnot(None),
                )
            )
        ).scalar() or 0

        # Passport progress = earned badges.
        total_stamps = (
            await db.execute(
                select(func.count())
                .select_from(UserPassport)
                .where(UserPassport.user_id == current_user.id)
            )
        ).scalar() or 0
    except Exception:
        # Relations may be absent in some environments — degrade gracefully.
        pass

    return UserStatsResponse(
        favorites_count=favorites_count,
        reviews_count=reviews_count,
        visits_count=visits_count,
        check_ins_count=check_ins_count,
        total_stamps=total_stamps,
    )


# ─────────────────────────────────────────────
# GET /favorites — list favorited attractions
# ─────────────────────────────────────────────
@router.get("/favorites", response_model=list[FavoriteResponse], summary="List favorites")
async def list_favorites(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    result = await db.execute(
        select(UserFavorite)
        .where(
            UserFavorite.user_id == current_user.id,
            UserFavorite.attraction_id.isnot(None),
        )
        .order_by(UserFavorite.created_at.desc())
    )
    favorites = result.scalars().all()

    out: list[FavoriteResponse] = []
    for fav in favorites:
        name = None
        if fav.attraction_id is not None:
            att = await db.get(Attraction, fav.attraction_id)
            name = att.name if att else None
        out.append(
            FavoriteResponse(
                id=fav.id,
                user_id=fav.user_id,
                attraction_id=fav.attraction_id,
                establishment_id=fav.establishment_id,
                event_id=fav.event_id,
                status=fav.status,
                created_at=fav.created_at,
                name=name,
                type="attraction",
            )
        )
    return out


# ─────────────────────────────────────────────
# POST /favorites/{attraction_id} — add favorite
# ─────────────────────────────────────────────
@router.post(
    "/favorites/{attraction_id}",
    response_model=FavoriteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add favorite",
)
async def add_favorite(
    attraction_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    att = await db.get(Attraction, attraction_id)
    if att is None:
        raise HTTPException(status_code=404, detail="Attraction not found")

    existing = await db.execute(
        select(UserFavorite).where(
            UserFavorite.user_id == current_user.id,
            UserFavorite.attraction_id == attraction_id,
        )
    )
    fav = existing.scalar_one_or_none()
    if fav is None:
        fav = UserFavorite(
            user_id=current_user.id,
            attraction_id=attraction_id,
            status="favorite",
        )
        db.add(fav)
        await db.flush()
        await db.refresh(fav)

    return FavoriteResponse(
        id=fav.id,
        user_id=fav.user_id,
        attraction_id=fav.attraction_id,
        establishment_id=fav.establishment_id,
        event_id=fav.event_id,
        status=fav.status,
        created_at=fav.created_at,
        name=att.name,
        type="attraction",
    )


# ─────────────────────────────────────────────
# DELETE /favorites/{attraction_id} — remove favorite
# ─────────────────────────────────────────────
@router.delete("/favorites/{attraction_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Remove favorite")
async def remove_favorite(
    attraction_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    result = await db.execute(
        select(UserFavorite).where(
            UserFavorite.user_id == current_user.id,
            UserFavorite.attraction_id == attraction_id,
        )
    )
    fav = result.scalar_one_or_none()
    if fav is not None:
        await db.delete(fav)


# ─────────────────────────────────────────────
# GET /visits — current user's check-ins
# ─────────────────────────────────────────────
@router.get("/visits", response_model=list[VisitResponse], summary="List visits")
async def list_visits(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    try:
        result = await db.execute(
            select(TouristCheckIn)
            .where(TouristCheckIn.user_id == current_user.id)
            .order_by(TouristCheckIn.verified_at.desc())
        )
        checkins = result.scalars().all()
    except Exception:
        return []

    out: list[VisitResponse] = []
    for c in checkins:
        if c.attraction_id is not None:
            target_type = "attraction"
            target_id = c.attraction_id
            att = await db.get(Attraction, c.attraction_id)
            target_name = att.name if att else None
        else:
            target_type = "establishment"
            target_id = c.establishment_id
            est = await db.get(Establishment, c.establishment_id) if c.establishment_id is not None else None
            target_name = est.name if est else None

        out.append(
            VisitResponse(
                id=c.id,
                target_type=target_type,
                target_id=target_id,
                target_name=target_name,
                visit_date=c.verified_at,
                visitor_count=1,
                created_at=c.verified_at,
            )
        )
    return out
