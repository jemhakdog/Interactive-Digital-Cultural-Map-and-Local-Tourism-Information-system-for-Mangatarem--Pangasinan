"""Tests for Authentication and Security Hardening (F1, F2, F3).

Covers:
- Strict Google OAuth verification and rejection of forged/invalid tokens with HTTP 401
- Acceptance of valid Google OAuth credentials (mocked verify_oauth2_token)
- Existence and completeness of .env.example (SECRET_KEY, DATABASE_URL, GOOGLE_CLIENT_ID)
- POST /api/auth/forgot-password token generation and UserNotification creation
- POST /api/auth/reset-password success and login verification
- Rejection of expired, invalid, and already-used reset tokens with HTTP 400
"""
from __future__ import annotations

import asyncio
import base64
import json
from datetime import UTC, datetime, timedelta
from pathlib import Path
from unittest.mock import patch

from google.auth.exceptions import GoogleAuthError
from sqlalchemy import select

from backend.app.core.database import async_session_factory
from backend.app.models.notifications import UserNotification
from backend.app.models.user import User


def _run(coro):
    return asyncio.run(coro)


# ───────────────────────────────────────────────────────────────
# F1: Google OAuth Security & Token Verification
# ───────────────────────────────────────────────────────────────

def test_google_auth_forged_jwt_token_rejected_with_401(client):
    """A forged JWT containing arbitrary email must be rejected with HTTP 401.

    It must NOT fall back to unverified base64 decoding to authenticate the user.
    """
    forged_payload = {
        "email": "victim_admin@mangatarem.gov.ph",
        "name": "Attacker Admin",
        "email_verified": True,
    }
    encoded_payload = base64.urlsafe_b64encode(json.dumps(forged_payload).encode()).decode().rstrip("=")
    forged_jwt = f"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.{encoded_payload}.fake_signature_bytes"

    response = client.post("/api/auth/google", json={"credential": forged_jwt})

    assert response.status_code == 401, (
        f"Expected 401 Unauthorized for forged token, but got {response.status_code}: {response.text}"
    )
    data = response.json()
    assert "Invalid Google OAuth credential" in data.get("detail", "")


def test_google_auth_malformed_token_rejected_with_401(client):
    """Malformed or garbage tokens must be rejected with HTTP 401."""
    response = client.post("/api/auth/google", json={"credential": "not.a.valid.jwt.token.structure"})
    assert response.status_code == 401
    assert "Invalid Google OAuth credential" in response.json().get("detail", "")


def test_google_auth_google_auth_error_rejected_with_401(client):
    """GoogleAuthError (e.g. invalid issuer) raised during verification must return HTTP 401, not 500."""
    with patch("google.oauth2.id_token.verify_oauth2_token", side_effect=GoogleAuthError("Invalid token issuer")):
        response = client.post("/api/auth/google", json={"credential": "some-unverified-credential"})
        assert response.status_code == 401, f"Expected 401 on GoogleAuthError, got {response.status_code}"
        assert "Invalid Google OAuth credential" in response.json().get("detail", "")


def test_google_auth_value_error_rejected_with_401(client):
    """ValueError (e.g. token expired, invalid signature) must return HTTP 401 without base64 bypass."""
    with patch("google.oauth2.id_token.verify_oauth2_token", side_effect=ValueError("Token expired")):
        response = client.post("/api/auth/google", json={"credential": "some-expired-credential"})
        assert response.status_code == 401, f"Expected 401 on ValueError, got {response.status_code}"
        assert "Invalid Google OAuth credential" in response.json().get("detail", "")


def test_google_auth_valid_credential_registers_and_authenticates(client):
    """A valid, verified Google credential creates a new user and issues JWTs."""
    mock_idinfo = {
        "email": "verified_tourist@example.com",
        "name": "Verified Tourist",
        "email_verified": True,
        "sub": "google-uid-12345",
    }

    with patch("google.oauth2.id_token.verify_oauth2_token", return_value=mock_idinfo):
        response = client.post("/api/auth/google", json={"credential": "valid.mocked.google.credential"})
        assert response.status_code == 200, response.text
        data = response.json()

        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

        # Verify authenticated identity via /api/auth/me
        me_resp = client.get("/api/auth/me", headers={"Authorization": f"Bearer {data['access_token']}"})
        assert me_resp.status_code == 200
        me_data = me_resp.json()
        assert me_data["email"] == "verified_tourist@example.com"
        assert me_data["role"] == "user"

    # Verify user exists in DB
    async def _check_db():
        async with async_session_factory() as db:
            result = await db.execute(select(User).where(User.email == "verified_tourist@example.com"))
            user = result.scalar_one_or_none()
            assert user is not None
            assert user.is_approved is True
            return user.id

    user_id = _run(_check_db())

    # Second login with same credential logs in existing user rather than duplicating
    with patch("google.oauth2.id_token.verify_oauth2_token", return_value=mock_idinfo):
        response2 = client.post("/api/auth/google", json={"credential": "valid.mocked.google.credential"})
        assert response2.status_code == 200
        data2 = response2.json()
        me_resp2 = client.get("/api/auth/me", headers={"Authorization": f"Bearer {data2['access_token']}"})
        assert me_resp2.status_code == 200
        assert me_resp2.json()["id"] == user_id


# ───────────────────────────────────────────────────────────────
# F2: Runtime Configuration Documentation (.env.example)
# ───────────────────────────────────────────────────────────────

def test_env_example_file_contains_mandatory_settings():
    """Verify .env.example exists and documents SECRET_KEY, DATABASE_URL, and GOOGLE_CLIENT_ID."""
    repo_root = Path(__file__).resolve().parent.parent
    env_example = repo_root / ".env.example"

    assert env_example.exists(), ".env.example must exist at the workspace root."

    content = env_example.read_text(encoding="utf-8")
    lines = [line.strip() for line in content.splitlines()]

    # Filter out pure comments to check actual variable declarations
    var_names = set()
    for line in lines:
        if line and not line.startswith("#"):
            key = line.split("=")[0].strip()
            var_names.add(key.upper())

    mandatory_vars = {"SECRET_KEY", "DATABASE_URL", "GOOGLE_CLIENT_ID"}
    missing = mandatory_vars - var_names

    assert not missing, (
        f".env.example is missing mandatory configuration variables: {missing}. "
        f"Present variables: {var_names}"
    )


# ───────────────────────────────────────────────────────────────
# F3: Password Reset Token Generation & User Notification
# ───────────────────────────────────────────────────────────────

def test_forgot_password_generates_token_and_notification(client):
    """POST /api/auth/forgot-password must set reset token and insert UserNotification."""
    # Seed user
    async def _seed():
        async with async_session_factory() as db:
            user = User(
                username="reset_user",
                email="reset_user@mangatarem.com",
                role="user",
                is_approved=True,
            )
            user.set_password("oldpassword123")
            db.add(user)
            await db.commit()

    _run(_seed())

    response = client.post("/api/auth/forgot-password", json={"email": "reset_user@mangatarem.com"})
    assert response.status_code == 200, response.text
    assert "detail" in response.json()

    # Verify reset token in DB and UserNotification created
    async def _verify_token_and_notification():
        async with async_session_factory() as db:
            result = await db.execute(select(User).where(User.email == "reset_user@mangatarem.com"))
            user = result.scalar_one_or_none()
            assert user is not None
            assert user.reset_token is not None
            assert len(user.reset_token) >= 32
            assert user.reset_token_expires_at is not None
            assert user.reset_token_used is False

            # Verify UserNotification record created
            notif_result = await db.execute(
                select(UserNotification).where(UserNotification.user_id == user.id)
            )
            notifications = notif_result.scalars().all()
            assert len(notifications) >= 1, "Expected at least 1 UserNotification created for password reset"

            reset_notif = notifications[0]
            assert "password" in reset_notif.title.lower() or "reset" in reset_notif.title.lower()
            assert user.reset_token in reset_notif.link or "/auth/reset-password" in reset_notif.link

    _run(_verify_token_and_notification())


def test_forgot_password_nonexistent_email_returns_200_without_notification(client):
    """Non-existent email should return 200 without exposing account existence or creating notifications."""
    response = client.post("/api/auth/forgot-password", json={"email": "nonexistent@mangatarem.com"})
    assert response.status_code == 200

    async def _verify_no_notifs():
        async with async_session_factory() as db:
            notif_result = await db.execute(select(UserNotification))
            assert len(notif_result.scalars().all()) == 0

    _run(_verify_no_notifs())


def test_reset_password_success_and_login_with_new_password(client):
    """POST /api/auth/reset-password updates password and allows login with new credentials."""
    # Seed user with reset token
    token = "test_valid_reset_token_64_characters_long_abcdef0123456789abcdef01234"
    async def _seed():
        async with async_session_factory() as db:
            user = User(
                username="reset_login_user",
                email="reset_login@mangatarem.com",
                role="user",
                is_approved=True,
                reset_token=token,
                reset_token_expires_at=datetime.now(UTC).replace(tzinfo=None) + timedelta(minutes=30),
                reset_token_used=False,
            )
            user.set_password("initialpassword123")
            db.add(user)
            await db.commit()

    _run(_seed())

    # Reset password
    reset_resp = client.post(
        "/api/auth/reset-password",
        json={"token": token, "password": "newpassword456"},
    )
    assert reset_resp.status_code == 200, reset_resp.text
    assert any(phrase in reset_resp.json().get("detail", "").lower() for phrase in ["successfully reset", "successfully updated"])

    # Old password fails
    old_login = client.post(
        "/api/auth/login",
        json={"email": "reset_login@mangatarem.com", "password": "initialpassword123"},
    )
    assert old_login.status_code == 401

    # New password succeeds
    new_login = client.post(
        "/api/auth/login",
        json={"email": "reset_login@mangatarem.com", "password": "newpassword456"},
    )
    assert new_login.status_code == 200
    assert "access_token" in new_login.json()


def test_reset_password_single_use_enforcement(client):
    """A reset token cannot be reused once consumed (E2E HTTP flow)."""
    # 1. Register user via /api/auth/register
    reg_resp = client.post(
        "/api/auth/register",
        json={
            "name": "single_use_user",
            "email": "single_use@mangatarem.com",
            "password": "pass123456Password!",
            "role": "user",
        },
    )
    assert reg_resp.status_code == 201, reg_resp.text

    # 2. Request forgot-password via /api/auth/forgot-password
    forgot_resp = client.post(
        "/api/auth/forgot-password",
        json={"email": "single_use@mangatarem.com"},
    )
    assert forgot_resp.status_code == 200, forgot_resp.text

    # 3. Query UserNotification for token
    async def _get_token():
        async with async_session_factory() as db:
            result = await db.execute(
                select(UserNotification).order_by(UserNotification.id.desc())
            )
            notif = result.scalars().first()
            assert notif is not None, "Expected UserNotification to be created"
            return notif.link.split("token=")[-1]

    token = _run(_get_token())
    assert token, "Token extracted from UserNotification must not be empty"

    # 4. First reset succeeds
    resp1 = client.post(
        "/api/auth/reset-password",
        json={"token": token, "password": "brandnewpassword1"},
    )
    assert resp1.status_code == 200

    # 5. Second reset with same token fails with 400
    resp2 = client.post(
        "/api/auth/reset-password",
        json={"token": token, "password": "brandnewpassword2"},
    )
    assert resp2.status_code == 400
    assert "Invalid or expired reset token" in resp2.json().get("detail", "")


def test_reset_password_expired_token_rejected_with_400(client):
    """An expired reset token must be rejected with HTTP 400."""
    token = "expired_token_abcdef0123456789abcdef0123456789abcdef0123456789abcdef0"
    async def _seed():
        async with async_session_factory() as db:
            user = User(
                username="expired_token_user",
                email="expired_token@mangatarem.com",
                role="user",
                is_approved=True,
                reset_token=token,
                reset_token_expires_at=datetime.now(UTC).replace(tzinfo=None) - timedelta(minutes=10),
                reset_token_used=False,
            )
            user.set_password("pass123456")
            db.add(user)
            await db.commit()

    _run(_seed())

    response = client.post(
        "/api/auth/reset-password",
        json={"token": token, "password": "newpassword123"},
    )
    assert response.status_code == 400
    assert "Invalid or expired reset token" in response.json().get("detail", "")


def test_reset_password_unknown_token_rejected_with_400(client):
    """An unknown/forged reset token must be rejected with HTTP 400."""
    response = client.post(
        "/api/auth/reset-password",
        json={"token": "non_existent_token_hex_value_1234567890", "password": "newpassword123"},
    )
    assert response.status_code == 400
    assert "Invalid or expired reset token" in response.json().get("detail", "")
