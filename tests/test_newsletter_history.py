"""
Tests for newsletter history API (FastAPI port of test_newsletter_history.py).

Flask-era asserted on the HTML archive page (/admin/newsletter/history).
FastAPI equivalent: GET /api/newsletter/history (JSON, admin-only).
"""
import asyncio

from sqlalchemy import select

from backend.app.models.user import User
from backend.app.models.notifications import NewsletterHistory
from backend.app.core.database import async_session_factory


def _run(coro):
    return asyncio.run(coro)


def _seed():
    async def _seed_async():
        async with async_session_factory() as db:
            admin = User(
                username="history_admin",
                email="history_admin@example.com",
                role="admin",
                is_approved=True,
            )
            admin.set_password("admin_pass")
            db.add(admin)
            regular = User(
                username="normal_steward",
                email="normal_steward@example.com",
                role="barangay_rep",
                is_approved=True,
            )
            regular.set_password("user_pass")
            db.add(regular)
            await db.flush()

            record = NewsletterHistory(
                subject="Admin Test Subject",
                content="Hello and welcome!",
                recipient_count=5,
            )
            db.add(record)
            await db.commit()
            return {"admin_id": admin.id, "record_id": record.id}

    return _run(_seed_async())


def _login(client, username, password):
    resp = client.post(
        "/api/auth/login",
        json={"email": f"{username}@example.com", "password": password},
    )
    assert resp.status_code == 200, resp.text
    return {"Authorization": f"Bearer {resp.json()['access_token']}"}


def test_unauthenticated_request_fails(client):
    """No token -> 401."""
    _seed()
    response = client.get("/api/newsletter/history")
    assert response.status_code == 401


def test_non_admin_forbidden(client):
    """Non-admin token -> 403."""
    _seed()
    headers = _login(client, "normal_steward", "user_pass")
    response = client.get("/api/newsletter/history", headers=headers)
    assert response.status_code == 403


def test_admin_history_succeeds(client):
    """Admin token -> 200 with records."""
    data = _seed()
    headers = _login(client, "history_admin", "admin_pass")
    response = client.get("/api/newsletter/history", headers=headers)
    assert response.status_code == 200
    records = response.json()
    assert any(r["subject"] == "Admin Test Subject" for r in records)
