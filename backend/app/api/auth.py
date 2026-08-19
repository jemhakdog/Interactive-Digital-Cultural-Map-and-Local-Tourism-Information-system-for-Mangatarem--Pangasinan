"""Auth API router — login, register, refresh, me, logout."""
from __future__ import annotations

import base64
import json
import secrets
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.config import get_settings
from backend.app.core.database import get_db
from backend.app.core.dependencies import get_current_user
from backend.app.models.barangay import BarangayInfo
from backend.app.models.user import User
from backend.app.schemas.auth import (
    ForgotPasswordRequest,
    GoogleAuthRequest,
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    ResetPasswordRequest,
    TokenResponse,
    UserResponse,
    UserRole,
)

router = APIRouter()
settings = get_settings()

# ── JWT constants ──────────────────────────────────────────────
ACCESS_TOKEN_EXPIRE_MINUTES = 30          # 30 min
REFRESH_TOKEN_EXPIRE_DAYS = 7             # 7 days
REFRESH_TOKEN_SUBJECT = "refresh"


# ── Helpers ────────────────────────────────────────────────────

def _create_token(user_id: int, subject: str, expires_delta: timedelta) -> str:
    """Create a JWT with standard claims."""
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + expires_delta,
        "type": subject,
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def _create_access_token(user_id: int) -> str:
    return _create_token(user_id, "access", timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))


def _create_refresh_token(user_id: int) -> str:
    return _create_token(user_id, REFRESH_TOKEN_SUBJECT, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))


def _issue_tokens(user: User) -> TokenResponse:
    """Issue both access and refresh tokens for a user."""
    return TokenResponse(
        access_token=_create_access_token(user.id),
        refresh_token=_create_refresh_token(user.id),
    )


def _user_to_response(user: User) -> UserResponse:
    """Map User model → UserResponse (uses the `name` alias of `username`)."""
    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.username,
        role=user.role or "user",
        is_approved=user.is_approved,
        created_at=user.created_at,
    )


def _verify_refresh_token(token: str) -> int:
    """Decode a refresh token and return the user id, or raise 401."""
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        if payload.get("type") != REFRESH_TOKEN_SUBJECT:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
            )
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )
        return int(user_id)
    except (JWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )


# ── Routes ─────────────────────────────────────────────────────

@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest, db: Annotated[AsyncSession, Depends(get_db)]):
    """Authenticate with email + password → JWT pair."""
    result = await db.execute(select(User).where(User.email == body.email))
    user = result.scalar_one_or_none()

    if user is None or not user.check_password(body.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    return _issue_tokens(user)


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(body: RegisterRequest, db: Annotated[AsyncSession, Depends(get_db)]):
    """Create a new user and return JWT pair."""
    # Check email uniqueness
    existing = await db.execute(select(User).where(User.email == body.email))
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    # Use `name` field as the username (Flask app used username; FastAPI schema uses name)
    # Check username uniqueness
    existing_user = await db.execute(select(User).where(User.username == body.name))
    if existing_user.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already taken",
        )

    barangay_id: int | None = None
    if body.barangay:
        b_res = await db.execute(select(BarangayInfo).where(BarangayInfo.name == body.barangay))
        b_obj = b_res.scalar_one_or_none()
        if b_obj:
            barangay_id = b_obj.id

    user = User(
        username=body.name,
        email=body.email,
        role=body.role.value,
        barangay_id=barangay_id,
        is_approved=(body.role == UserRole.user),  # only regular users auto-approved
    )
    user.set_password(body.password)
    db.add(user)
    await db.flush()          # populate user.id before committing
    await db.refresh(user)    # reload defaults (created_at, etc.)

    return _issue_tokens(user)


@router.post("/google", response_model=TokenResponse)
async def google_auth(body: GoogleAuthRequest, db: Annotated[AsyncSession, Depends(get_db)]):
    """Authenticate or register a user via Google OAuth credential."""
    email: str | None = None
    name: str | None = None

    try:
        idinfo = id_token.verify_oauth2_token(
            body.credential,
            google_requests.Request(),
            settings.google_client_id,
        )
        email = idinfo.get("email")
        name = idinfo.get("name") or idinfo.get("given_name")
    except Exception:
        # Fallback decode if token format is JWT
        try:
            parts = body.credential.split(".")
            if len(parts) >= 2:
                padded = parts[1] + "=" * ((4 - len(parts[1]) % 4) % 4)
                payload = json.loads(base64.urlsafe_b64decode(padded).decode("utf-8"))
                email = payload.get("email")
                name = payload.get("name") or payload.get("given_name")
        except Exception:
            pass

    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Google OAuth credential",
        )

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if user is None:
        # Create new Google user
        base_username = (name or email.split("@")[0]).strip().replace(" ", "")
        username = base_username
        counter = 1
        while (await db.execute(select(User).where(User.username == username))).scalar_one_or_none():
            username = f"{base_username}_{counter}"
            counter += 1

        user = User(
            username=username,
            email=email,
            role=body.role.value,
            is_approved=(body.role == UserRole.user),
        )
        user.set_password(secrets.token_hex(24))
        db.add(user)
        await db.flush()
        await db.refresh(user)

    return _issue_tokens(user)


@router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(body: ForgotPasswordRequest, db: Annotated[AsyncSession, Depends(get_db)]):
    """Request a password reset link for the provided email."""
    result = await db.execute(select(User).where(User.email == body.email))
    user = result.scalar_one_or_none()
    if user:
        user.create_reset_token()
        await db.flush()
    return {"detail": "If an account with that email exists, a password reset link has been generated."}


@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(body: ResetPasswordRequest, db: Annotated[AsyncSession, Depends(get_db)]):
    """Reset password using a valid reset token."""
    result = await db.execute(select(User).where(User.reset_token == body.token))
    user = result.scalar_one_or_none()

    if user is None or not user.is_reset_token_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token",
        )

    user.set_password(body.password)
    user.reset_token_used = True
    await db.flush()
    return {"detail": "Password has been successfully updated."}


@router.get("/me", response_model=UserResponse)
async def me(current_user: Annotated[User, Depends(get_current_user)]):
    """Return the authenticated user's profile."""
    return _user_to_response(current_user)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(body: RefreshRequest, db: Annotated[AsyncSession, Depends(get_db)]):
    """Exchange a valid refresh token for a new token pair."""
    user_id = _verify_refresh_token(body.refresh_token)

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return _issue_tokens(user)


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout():
    """JWT is stateless — client discards tokens. Endpoint kept for symmetry."""
    return {"detail": "Logged out. Please discard tokens."}
