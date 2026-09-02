"""Pydantic request/response schemas for auth endpoints."""
from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, Field

# ---------- Enums ----------

class UserRole(str, Enum):
    admin = "admin"
    contributor = "contributor"
    business_owner = "business_owner"
    user = "user"


# ---------- Request schemas ----------

class LoginRequest(BaseModel):
    """Email + password login."""
    email: EmailStr
    password: str = Field(..., min_length=1)


class RegisterRequest(BaseModel):
    """New user registration."""
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)
    name: str = Field(..., min_length=2, max_length=80)
    role: UserRole = UserRole.user
    barangay: str | None = None


class GoogleAuthRequest(BaseModel):
    """Google OAuth login/signup request."""
    credential: str
    role: UserRole = UserRole.user


class ForgotPasswordRequest(BaseModel):
    """Forgot password request."""
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    """Reset password request."""
    token: str
    password: str = Field(..., min_length=6, max_length=128)


# ---------- Response schemas ----------

class TokenResponse(BaseModel):
    """JWT pair returned after login / register / refresh."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """Public user profile (no password)."""
    id: int
    email: str
    name: str
    role: str
    is_approved: bool
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class RefreshRequest(BaseModel):
    """Refresh token body."""
    refresh_token: str
