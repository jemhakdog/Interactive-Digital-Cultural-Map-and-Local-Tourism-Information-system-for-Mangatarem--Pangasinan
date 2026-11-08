"""Tests for Chat Subsystem and Sender Identity Modernization (F5).

Covers:
- Chat room creation, participant membership, and room listing
- Sending chat messages via POST /api/chat/{room_id}/messages
- Verification that GET /api/chat/{room_id} message history returns actual sender username in sender_name (not hardcoded "System")
- Verification that system messages (is_system_msg=True) continue to return "System" in sender_name
- Authorization: Non-participants cannot view or send messages in private rooms (HTTP 403)
- Pagination and chronological message ordering
"""
from __future__ import annotations

import asyncio
from datetime import UTC, datetime

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select

from backend.app.core.database import async_session_factory
from backend.app.main import app
from backend.app.models.chat import ChatMessage, ChatParticipant, ChatRoom
from backend.app.models.user import User


def _run(coro):
    return asyncio.run(coro)


async def _create_chat_user(email: str, username: str) -> tuple[int, dict[str, str]]:
    """Seed a user and return (user_id, auth_headers)."""
    async with async_session_factory() as db:
        user = User(
            username=username,
            email=email,
            role="user",
            is_approved=True,
        )
        user.set_password("password123")
        db.add(user)
        await db.commit()
        user_id = user.id

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        resp = await ac.post("/api/auth/login", json={"email": email, "password": "password123"})
        assert resp.status_code == 200, resp.text
        token = resp.json()["access_token"]
        return user_id, {"Authorization": f"Bearer {token}"}


async def _create_chat_room(room_type: str = "direct", participants: list[int] | None = None) -> int:
    """Seed a chat room with participants and return room_id."""
    async with async_session_factory() as db:
        room = ChatRoom(type=room_type)
        db.add(room)
        await db.flush()

        if participants:
            for uid in participants:
                part = ChatParticipant(chat_room_id=room.id, user_id=uid)
                db.add(part)

        await db.commit()
        return room.id


# ───────────────────────────────────────────────────────────────
# F5: Chat History Sender Identity & Message Flow
# ───────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_chat_room_listing_and_membership():
    """Users only see chat rooms they are participants of; non-members get 403."""
    user1_id, user1_headers = await _create_chat_user("chat_u1@mangatarem.com", "chat_user1")
    user2_id, _ = await _create_chat_user("chat_u2@mangatarem.com", "chat_user2")
    _, user3_headers = await _create_chat_user("chat_u3@mangatarem.com", "chat_user3")

    room_id = await _create_chat_room(room_type="direct", participants=[user1_id, user2_id])

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # User 1 sees the room in listing
        resp1 = await ac.get("/api/chat/", headers=user1_headers)
        assert resp1.status_code == 200
        rooms1 = resp1.json().get("rooms", [])
        assert any(r["id"] == room_id for r in rooms1)

        # User 3 (not a participant) cannot view the room
        resp3 = await ac.get(f"/api/chat/{room_id}", headers=user3_headers)
        assert resp3.status_code == 403
        assert "Not authorized" in resp3.json().get("detail", "")


@pytest.mark.asyncio
async def test_send_chat_message_success():
    """Participant can send a message and receives correct sender_name in response."""
    user1_id, user1_headers = await _create_chat_user("chat_sender@mangatarem.com", "tourist_alice")
    user2_id, _ = await _create_chat_user("chat_partner@mangatarem.com", "guide_bob")

    room_id = await _create_chat_room(room_type="direct", participants=[user1_id, user2_id])

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        resp = await ac.post(
            f"/api/chat/{room_id}/messages",
            json={"content": "Hello, is the Heritage Parish open today?"},
            headers=user1_headers,
        )
        assert resp.status_code == 201, resp.text
        data = resp.json()
        assert data["status"] == "success"
        msg = data["message"]
        assert msg["sender_id"] == user1_id
        assert msg["sender_name"] == "tourist_alice"
        assert msg["content"] == "Hello, is the Heritage Parish open today?"


@pytest.mark.asyncio
async def test_chat_history_returns_actual_sender_username():
    """GET /api/chat/{room_id} must return actual sender username in sender_name, NOT 'System'."""
    user1_id, user1_headers = await _create_chat_user("alice@mangatarem.com", "alice_traveler")
    user2_id, user2_headers = await _create_chat_user("bob@mangatarem.com", "bob_staff")

    room_id = await _create_chat_room(room_type="direct", participants=[user1_id, user2_id])

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Alice sends message
        m1 = await ac.post(
            f"/api/chat/{room_id}/messages",
            json={"content": "Inquiry about eco-park trail guidelines"},
            headers=user1_headers,
        )
        assert m1.status_code == 201

        # Bob replies
        m2 = await ac.post(
            f"/api/chat/{room_id}/messages",
            json={"content": "Eco-park trails are open from 6am to 5pm"},
            headers=user2_headers,
        )
        assert m2.status_code == 201

        # Fetch message history
        history_resp = await ac.get(f"/api/chat/{room_id}", headers=user1_headers)
        assert history_resp.status_code == 200
        messages = history_resp.json().get("messages", [])
        assert len(messages) == 2

        # Verify real sender usernames are populated, not hardcoded "System"
        msg_alice = messages[0]
        assert msg_alice["sender_id"] == user1_id
        assert msg_alice["sender_name"] == "alice_traveler", (
            f"Expected sender_name='alice_traveler' for user message, got {msg_alice['sender_name']!r}"
        )
        assert msg_alice["is_system_msg"] is False

        msg_bob = messages[1]
        assert msg_bob["sender_id"] == user2_id
        assert msg_bob["sender_name"] == "bob_staff", (
            f"Expected sender_name='bob_staff' for user message, got {msg_bob['sender_name']!r}"
        )
        assert msg_bob["is_system_msg"] is False


@pytest.mark.asyncio
async def test_chat_system_message_returns_system():
    """System messages (is_system_msg=True) must still return 'System' in sender_name."""
    user1_id, user1_headers = await _create_chat_user("sys_test_u1@mangatarem.com", "charlie")
    room_id = await _create_chat_room(room_type="general", participants=[user1_id])

    # Seed one system message and one user message
    async with async_session_factory() as db:
        sys_msg = ChatMessage(
            chat_room_id=room_id,
            sender_id=user1_id,
            content="Charlie joined the room.",
            is_system_msg=True,
        )
        user_msg = ChatMessage(
            chat_room_id=room_id,
            sender_id=user1_id,
            content="Good morning everyone!",
            is_system_msg=False,
        )
        db.add_all([sys_msg, user_msg])
        await db.commit()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        resp = await ac.get(f"/api/chat/{room_id}", headers=user1_headers)
        assert resp.status_code == 200
        messages = resp.json().get("messages", [])
        assert len(messages) == 2

        system_msg_item = next(m for m in messages if m["is_system_msg"] is True)
        assert system_msg_item["sender_name"] == "System"

        user_msg_item = next(m for m in messages if m["is_system_msg"] is False)
        assert user_msg_item["sender_name"] == "charlie"


@pytest.mark.asyncio
async def test_chat_history_pagination():
    """Pagination parameters page and per_page are respected."""
    user1_id, user1_headers = await _create_chat_user("page_u@mangatarem.com", "pager")
    room_id = await _create_chat_room(room_type="direct", participants=[user1_id])

    async with async_session_factory() as db:
        for i in range(5):
            msg = ChatMessage(
                chat_room_id=room_id,
                sender_id=user1_id,
                content=f"Message {i}",
                is_system_msg=False,
            )
            db.add(msg)
        await db.commit()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Page 1 with per_page 3
        resp = await ac.get(f"/api/chat/{room_id}?page=1&per_page=3", headers=user1_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["messages"]) == 3
        assert data["page"] == 1
        assert data["has_next"] is True
        assert data["has_prev"] is False

        # Page 2 with per_page 3
        resp2 = await ac.get(f"/api/chat/{room_id}?page=2&per_page=3", headers=user1_headers)
        assert resp2.status_code == 200
        data2 = resp2.json()
        assert len(data2["messages"]) == 2
        assert data2["page"] == 2
        assert data2["has_next"] is False
        assert data2["has_prev"] is True


@pytest.mark.asyncio
async def test_send_message_unauthorized_cases():
    """Unauthenticated users receive 401; non-participants receive 403; non-existent room receives 404."""
    user1_id, user1_headers = await _create_chat_user("auth_u1@mangatarem.com", "member_user")
    _, outsider_headers = await _create_chat_user("auth_u2@mangatarem.com", "outsider_user")

    room_id = await _create_chat_room(room_type="direct", participants=[user1_id])

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Unauthenticated -> 401
        r_unauth = await ac.post(f"/api/chat/{room_id}/messages", json={"content": "test"})
        assert r_unauth.status_code == 401

        # Outsider user -> 403
        r_outsider = await ac.post(
            f"/api/chat/{room_id}/messages",
            json={"content": "intruder"},
            headers=outsider_headers,
        )
        assert r_outsider.status_code == 403

        # Non-existent room -> 404
        r_404 = await ac.post(
            "/api/chat/999999/messages",
            json={"content": "ghost room"},
            headers=user1_headers,
        )
        assert r_404.status_code == 404
