"""Tests for Booking Concurrency, Race Condition Prevention, and Capacity Constraints (F4).

Covers:
- Concurrent reservation requests on limited capacity slots (preventing over-subscription)
- Verification that total reservations do not exceed total_capacity, excess requests receive HTTP 400
- Concurrent slot creation on an unseeded date without HTTP 500 crashes
- Sequential capacity boundary enforcement
- Idempotent re-submission handling
"""
from __future__ import annotations

import asyncio
from datetime import UTC, datetime, timedelta

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select

from backend.app.core.database import async_session_factory
from backend.app.main import app
from backend.app.models.attractions import Attraction
from backend.app.models.booking import BookableAsset, BookingSlot, Reservation
from backend.app.models.user import User


def _run(coro):
    return asyncio.run(coro)


async def _create_test_user(email: str, username: str) -> dict[str, str]:
    """Helper to seed a user and return Authorization headers."""
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

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        resp = await ac.post("/api/auth/login", json={"email": email, "password": "password123"})
        assert resp.status_code == 200, resp.text
        token = resp.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}


async def _seed_asset(capacity: int = 10, status: str = "active") -> int:
    """Helper to seed an attraction and bookable asset, returning asset_id."""
    async with async_session_factory() as db:
        attraction = Attraction(
            name=f"Spot {datetime.now(UTC).timestamp()}",
            description="Test attraction for booking concurrency.",
            category="nature",
            latitude=15.79,
            longitude=120.29,
            status="approved",
            is_verified=True,
        )
        db.add(attraction)
        await db.flush()

        asset = BookableAsset(
            attraction_id=attraction.id,
            daily_capacity=capacity,
            status=status,
            requires_approval=False,
        )
        db.add(asset)
        await db.commit()
        return asset.id


# ───────────────────────────────────────────────────────────────
# F4: Concurrency & Race Condition Prevention
# ───────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_concurrent_reservations_cannot_exceed_capacity():
    """When concurrent users attempt to book more seats than available, excess requests receive HTTP 400.

    Ensures booked_count never exceeds total_capacity under concurrent loads.
    """
    asset_id = await _seed_asset(capacity=5)
    target_date = (datetime.now(UTC) + timedelta(days=2)).strftime("%Y-%m-%d")
    date_obj = (datetime.now(UTC) + timedelta(days=2)).date()

    # Pre-seed slot with total_capacity=5, booked_count=4 (only 1 seat remains)
    async with async_session_factory() as db:
        slot = BookingSlot(
            bookable_asset_id=asset_id,
            date=date_obj,
            total_capacity=5,
            booked_count=4,
        )
        db.add(slot)
        await db.commit()
        slot_id = slot.id

    # Create 3 distinct users to compete for the final 1 seat
    user_headers = [
        await _create_test_user(f"rush_user_{i}@mangatarem.com", f"rush_user_{i}")
        for i in range(3)
    ]

    # Concurrently fire reservation requests
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        tasks = [
            ac.post(
                "/api/booking/reserve",
                json={
                    "asset_id": asset_id,
                    "date": target_date,
                    "party_size": 1,
                    "contact": f"0917000000{i}",
                },
                headers=user_headers[i],
            )
            for i in range(3)
        ]
        responses = await asyncio.gather(*tasks)

    status_codes = [r.status_code for r in responses]
    successes = [r for r in responses if r.status_code == 200]
    rejections = [r for r in responses if r.status_code == 400]

    # Exactly 1 request should succeed; 2 should be rejected
    assert len(successes) == 1, (
        f"Expected exactly 1 successful reservation for 1 remaining seat, got {len(successes)}. "
        f"Status codes: {status_codes}"
    )
    assert len(rejections) == 2, (
        f"Expected 2 rejections with 400, got {len(rejections)}. Status codes: {status_codes}"
    )

    for rej in rejections:
        assert "capacity" in rej.json().get("detail", "").lower()

    # Verify database state integrity
    async with async_session_factory() as db:
        result = await db.execute(select(BookingSlot).where(BookingSlot.id == slot_id))
        updated_slot = result.scalar_one()
        assert updated_slot.booked_count <= 5, (
            f"Over-subscription detected! booked_count={updated_slot.booked_count} > total_capacity=5"
        )
        assert updated_slot.booked_count == 5


@pytest.mark.asyncio
async def test_concurrent_bulk_reservations_exact_capacity_exhaustion():
    """6 concurrent users each booking party_size=2 on total_capacity=10.

    Exactly 5 should succeed (10 seats allocated), 1 should fail with 400.
    """
    asset_id = await _seed_asset(capacity=10)
    target_date = (datetime.now(UTC) + timedelta(days=3)).strftime("%Y-%m-%d")
    date_obj = (datetime.now(UTC) + timedelta(days=3)).date()

    async with async_session_factory() as db:
        slot = BookingSlot(
            bookable_asset_id=asset_id,
            date=date_obj,
            total_capacity=10,
            booked_count=0,
        )
        db.add(slot)
        await db.commit()
        slot_id = slot.id

    users = [
        await _create_test_user(f"bulk_user_{i}@mangatarem.com", f"bulk_user_{i}")
        for i in range(6)
    ]

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        tasks = [
            ac.post(
                "/api/booking/reserve",
                json={
                    "asset_id": asset_id,
                    "date": target_date,
                    "party_size": 2,
                    "contact": f"0918000000{i}",
                },
                headers=users[i],
            )
            for i in range(6)
        ]
        responses = await asyncio.gather(*tasks)

    status_codes = [r.status_code for r in responses]
    successes = [r for r in responses if r.status_code == 200]
    rejections = [r for r in responses if r.status_code == 400]

    assert len(successes) == 5, f"Expected 5 successes for 10 seats, got {len(successes)}: {status_codes}"
    assert len(rejections) == 1, f"Expected 1 rejection, got {len(rejections)}: {status_codes}"

    async with async_session_factory() as db:
        result = await db.execute(select(BookingSlot).where(BookingSlot.id == slot_id))
        updated_slot = result.scalar_one()
        assert updated_slot.booked_count == 10

        res_result = await db.execute(
            select(Reservation).where(
                Reservation.booking_slot_id == slot_id,
                Reservation.status != "cancelled",
            )
        )
        reservations = res_result.scalars().all()
        assert len(reservations) == 5
        total_reserved_seats = sum(r.party_size for r in reservations)
        assert total_reserved_seats == 10


@pytest.mark.asyncio
async def test_concurrent_slot_creation_on_unseeded_date():
    """Multiple concurrent users reserving on an unseeded date must NOT crash with HTTP 500.

    One request creates the slot; concurrent requests safely retrieve the created slot.
    """
    asset_id = await _seed_asset(capacity=20)
    unseeded_date = (datetime.now(UTC) + timedelta(days=10)).strftime("%Y-%m-%d")
    date_obj = (datetime.now(UTC) + timedelta(days=10)).date()

    users = [
        await _create_test_user(f"unseeded_user_{i}@mangatarem.com", f"unseeded_user_{i}")
        for i in range(4)
    ]

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        tasks = [
            ac.post(
                "/api/booking/reserve",
                json={
                    "asset_id": asset_id,
                    "date": unseeded_date,
                    "party_size": 2,
                    "contact": f"0919000000{i}",
                },
                headers=users[i],
            )
            for i in range(4)
        ]
        responses = await asyncio.gather(*tasks)

    # NONE of the requests should crash with 500
    for idx, resp in enumerate(responses):
        assert resp.status_code != 500, (
            f"User {idx} experienced a 500 crash during concurrent slot creation: {resp.text}"
        )
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.text}"

    # Verify exactly 1 BookingSlot exists for this asset and date
    async with async_session_factory() as db:
        result = await db.execute(
            select(BookingSlot).where(
                BookingSlot.bookable_asset_id == asset_id,
                BookingSlot.date == date_obj,
            )
        )
        slots = result.scalars().all()
        assert len(slots) == 1, f"Expected exactly 1 BookingSlot created, found {len(slots)}"
        assert slots[0].booked_count == 8  # 4 users * 2 seats each


@pytest.mark.asyncio
async def test_sequential_capacity_boundary():
    """Sequential check: booking succeeds when capacity exists and fails when exceeded."""
    asset_id = await _seed_asset(capacity=2)
    target_date = (datetime.now(UTC) + timedelta(days=4)).strftime("%Y-%m-%d")

    user1_headers = await _create_test_user("seq1@mangatarem.com", "seq_user1")
    user2_headers = await _create_test_user("seq2@mangatarem.com", "seq_user2")

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # User 1 books 2 seats (all capacity)
        resp1 = await ac.post(
            "/api/booking/reserve",
            json={"asset_id": asset_id, "date": target_date, "party_size": 2, "contact": "09111111111"},
            headers=user1_headers,
        )
        assert resp1.status_code == 200
        assert resp1.json()["success"] is True

        # User 2 attempts to book 1 seat -> 400
        resp2 = await ac.post(
            "/api/booking/reserve",
            json={"asset_id": asset_id, "date": target_date, "party_size": 1, "contact": "09222222222"},
            headers=user2_headers,
        )
        assert resp2.status_code == 400
        assert "capacity" in resp2.json()["detail"].lower()


@pytest.mark.asyncio
async def test_idempotent_reservation_resubmission():
    """Re-submitting the exact same reservation returns existing reservation without double-counting."""
    asset_id = await _seed_asset(capacity=5)
    target_date = (datetime.now(UTC) + timedelta(days=5)).strftime("%Y-%m-%d")

    user_headers = await _create_test_user("idem@mangatarem.com", "idem_user")

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        payload = {"asset_id": asset_id, "date": target_date, "party_size": 2, "contact": "09333333333"}
        resp1 = await ac.post("/api/booking/reserve", json=payload, headers=user_headers)
        assert resp1.status_code == 200
        res1_id = resp1.json()["reservation_id"]

        resp2 = await ac.post("/api/booking/reserve", json=payload, headers=user_headers)
        assert resp2.status_code == 200
        data2 = resp2.json()
        assert data2["reservation_id"] == res1_id
        assert data2.get("idempotent") is True


@pytest.mark.asyncio
async def test_inactive_asset_cannot_be_booked():
    """Reservations on inactive assets receive HTTP 400."""
    asset_id = await _seed_asset(capacity=10, status="inactive")
    target_date = (datetime.now(UTC) + timedelta(days=6)).strftime("%Y-%m-%d")

    user_headers = await _create_test_user("inactive@mangatarem.com", "inactive_user")

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        resp = await ac.post(
            "/api/booking/reserve",
            json={"asset_id": asset_id, "date": target_date, "party_size": 1, "contact": "09444444444"},
            headers=user_headers,
        )
        assert resp.status_code == 400
        assert "Asset not available" in resp.json()["detail"]
