"""Admin API router — admin-only management endpoints."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.database import get_db
from backend.app.core.dependencies import require_admin
from backend.app.models.user import User
from backend.app.schemas.auth import UserResponse

router = APIRouter()


def _user_to_response(user: User) -> UserResponse:
    """Map User model → UserResponse."""
    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.username,
        role=user.role or "user",
        is_approved=user.is_approved,
        created_at=user.created_at,
    )


@router.get("/users")
async def list_users(
    _admin: Annotated[User, Depends(require_admin)],
    db: Annotated[AsyncSession, Depends(get_db)],
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
) -> dict:
    """Return a paginated list of all users (admin only)."""
    # Total count
    count_result = await db.execute(select(func.count(User.id)))
    total = count_result.scalar_one()

    # Paginated users
    offset = (page - 1) * per_page
    result = await db.execute(
        select(User).order_by(User.id).offset(offset).limit(per_page)
    )
    users = result.scalars().all()

    return {
        "users": [_user_to_response(u) for u in users],
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": (total + per_page - 1) // per_page,
    }
