"""Empirical Adversarial Stress Tests for Milestone M2 (Booking Concurrency & Capacity Invariants).

Targets:
1. High-contention race condition with mixed party sizes (capacity over-subscription attack)
2. Same-user simultaneous duplicate reservation race (idempotency under concurrency)
3. Concurrent slot creation stampede on unseeded date (race to create slot)
4. Concurrent cancellation and re-booking race (capacity replenishment race)
5. Adversarial input fuzzing (negative/zero party size, invalid dates, non-existent assets)
6. Admin status transition tampering & RBAC enforcement
"""
from __future__ import annotations

import asyncio
from datetime import UTC, datetime, timedelta

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import func, select

from backend.app.api.auth import _create_access_token
from backend.app.core.database import async_session_factory
from backend.app.main import app
from backend.app.models.attractions import Attraction
from backend.app.models.booking import BookableAsset, BookingSlot, Reservation
from backend.app.models.user import User


async def _seed_user(email: str, username: str, role: str = "user") -> tuple[int, dict[str, str]]:
    """Helper to seed a user in the database and return (user_id, auth_headers)."""
    async with async_session_factory() as db:
        user = User(
            username=username,
            email=email,
            role=role,
            is_approved=True,
        )
        user.set_password("password123")
        db.add(user)
        await db.commit()
        user_id = user.id

    token = _create_access_token(user_id)
    headers = {"Authorization": f"Bearer {token}"}
    return user_id, headers


async def _seed_asset(capacity: int = 10, status: str = "active", requires_approval: bool = False) -> int:
    """Helper to seed an attraction and bookable asset, returning asset_id."""
    async with async_session_factory() as db:
        attraction = Attraction(
            name=f"Stress Spot {datetime.now(UTC).timestamp()}",
            description="Stress test attraction.",
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
            requires_approval=requires_approval,
        )
        db.add(asset)
        await db.commit()
        return asset.id


# ───────────────────────────────────────────────────────────────
# 1. High-Contention Race with Mixed Party Sizes
# ───────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_adversarial_high_contention_mixed_party_sizes():
    """25 concurrent users compete for 12 total seats with varied party sizes.

    Party size distribution:
    - 10 users requesting 1 seat
    - 10 users requesting 2 seats
    - 5 users requesting 3 seats
    Total seats demanded = 10 + 20 + 15 = 45 seats. Capacity = 12.

    Invariants:
    1. booked_count <= 12
    2. Sum of party_sizes for confirmed reservations == booked_count
    3. Exactly 0 overbooking
    4. Rejected requests get 400 with 'capacity' in detail
    5. Zero 500 errors
    """
    capacity = 12
    asset_id = await _seed_asset(capacity=capacity)
    target_date = (datetime.now(UTC) + timedelta(days=15)).strftime("%Y-%m-%d")
    date_obj = (datetime.now(UTC) + timedelta(days=15)).date()

    async with async_session_factory() as db:
        slot = BookingSlot(
            bookable_asset_id=asset_id,
            date=date_obj,
            total_capacity=capacity,
            booked_count=0,
        )
        db.add(slot)
        await db.commit()
        slot_id = slot.id

    # Create 25 distinct users
    users = [
        await _seed_user(f"stress_mix_{i}@mangatarem.com", f"stress_mix_{i}")
        for i in range(25)
    ]

    # Assign party sizes
    party_sizes = [1] * 10 + [2] * 10 + [3] * 5

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        tasks = [
            ac.post(
                "/api/booking/reserve",
                json={
                    "asset_id": asset_id,
                    "date": target_date,
                    "party_size": party_sizes[i],
                    "contact": f"099900000{i:02d}",
                },
                headers=users[i][1],
            )
            for i in range(25)
        ]
        responses = await asyncio.gather(*tasks)

    status_codes = [r.status_code for r in responses]
    assert all(code in (200, 400) for code in status_codes), f"Unexpected status codes: {status_codes}"

    successes = [r for r in responses if r.status_code == 200]
    rejections = [r for r in responses if r.status_code == 400]

    for rej in rejections:
        assert "capacity" in rej.json().get("detail", "").lower()

    # Verify database state invariants
    async with async_session_factory() as db:
        result = await db.execute(select(BookingSlot).where(BookingSlot.id == slot_id))
        updated_slot = result.scalar_one()

        # Invariant 1: booked_count never exceeds capacity
        assert updated_slot.booked_count <= capacity, (
            f"OVERBOOKING DETECTED: booked_count {updated_slot.booked_count} > capacity {capacity}"
        )

        # Invariant 2: sum of party sizes in reservations matches booked_count
        res_result = await db.execute(
            select(Reservation).where(
                Reservation.booking_slot_id == slot_id,
                Reservation.status != "cancelled",
            )
        )
        reservations = res_result.scalars().all()
        actual_reserved_seats = sum(r.party_size for r in reservations)
        assert actual_reserved_seats == updated_slot.booked_count, (
            f"MISMATCH: sum(party_size)={actual_reserved_seats} != slot.booked_count={updated_slot.booked_count}"
        )
        assert len(reservations) == len(successes)


# ───────────────────────────────────────────────────────────────
# 2. Same-User Simultaneous Duplicate Booking Race (Idempotency)
# ───────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_adversarial_same_user_concurrent_duplicate_booking():
    """10 simultaneous identical reservation requests from the SAME user.

    Invariants:
    1. Exactly ONE reservation is created for this user on this slot.
    2. booked_count increments by party_size ONCE, not 10 times.
    3. All 10 requests succeed (200), subsequent ones marked idempotent.
    4. No duplicate key integrity crashes (500).
    """
    asset_id = await _seed_asset(capacity=10)
    target_date = (datetime.now(UTC) + timedelta(days=16)).strftime("%Y-%m-%d")
    date_obj = (datetime.now(UTC) + timedelta(days=16)).date()

    user_id, headers = await _seed_user("idem_stress@mangatarem.com", "idem_stress")

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        tasks = [
            ac.post(
                "/api/booking/reserve",
                json={
                    "asset_id": asset_id,
                    "date": target_date,
                    "party_size": 2,
                    "contact": "09110000000",
                },
                headers=headers,
            )
            for _ in range(10)
        ]
        responses = await asyncio.gather(*tasks)

    status_codes = [r.status_code for r in responses]
    assert all(code == 200 for code in status_codes), f"Some requests failed: {status_codes}"

    reservation_ids = {r.json()["reservation_id"] for r in responses}
    assert len(reservation_ids) == 1, f"Multiple reservation IDs created for same user: {reservation_ids}"

    # Verify database state
    async with async_session_factory() as db:
        res_result = await db.execute(
            select(Reservation).where(
                Reservation.user_id == user_id,
            )
        )
        user_reservations = res_result.scalars().all()
        assert len(user_reservations) == 1, f"Expected 1 reservation in DB, got {len(user_reservations)}"

        slot_result = await db.execute(
            select(BookingSlot).where(
                BookingSlot.bookable_asset_id == asset_id,
                BookingSlot.date == date_obj,
            )
        )
        slot = slot_result.scalar_one()
        assert slot.booked_count == 2, f"Slot booked_count over-incremented: got {slot.booked_count}, expected 2"


# ───────────────────────────────────────────────────────────────
# 3. Concurrent Slot Creation Stampede on Unseeded Date
# ───────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_adversarial_concurrent_slot_creation_stampede():
    """12 concurrent requests simultaneously hit an unseeded date.

    Invariants:
    1. Exactly ONE BookingSlot row is created for (asset_id, date).
    2. No IntegrityError leaks out as HTTP 500.
    3. Capacity calculations are consistent.
    """
    capacity = 10
    asset_id = await _seed_asset(capacity=capacity)
    target_date = (datetime.now(UTC) + timedelta(days=20)).strftime("%Y-%m-%d")
    date_obj = (datetime.now(UTC) + timedelta(days=20)).date()

    users = [
        await _seed_user(f"stampede_{i}@mangatarem.com", f"stampede_{i}")
        for i in range(12)
    ]

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        tasks = [
            ac.post(
                "/api/booking/reserve",
                json={
                    "asset_id": asset_id,
                    "date": target_date,
                    "party_size": 1,
                    "contact": f"091200000{i:02d}",
                },
                headers=users[i][1],
            )
            for i in range(12)
        ]
        responses = await asyncio.gather(*tasks)

    for r in responses:
        assert r.status_code != 500, f"HTTP 500 during slot creation stampede: {r.text}"

    successes = [r for r in responses if r.status_code == 200]
    rejections = [r for r in responses if r.status_code == 400]

    assert len(successes) == 10, f"Expected 10 successes for capacity 10, got {len(successes)}"
    assert len(rejections) == 2, f"Expected 2 rejections for capacity 10, got {len(rejections)}"

    async with async_session_factory() as db:
        slots = (
            await db.execute(
                select(BookingSlot).where(
                    BookingSlot.bookable_asset_id == asset_id,
                    BookingSlot.date == date_obj,
                )
            )
        ).scalars().all()
        assert len(slots) == 1, f"Expected exactly 1 BookingSlot, got {len(slots)}"
        assert slots[0].booked_count == 10


# ───────────────────────────────────────────────────────────────
# 4. Concurrent Cancellation and Rebooking Race
# ───────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_adversarial_concurrent_cancellation_and_rebooking():
    """A slot at full capacity (5/5). Admin cancels 1 reservation while 5 new users race to book.

    Invariants:
    1. At most 1 new booking succeeds.
    2. booked_count never exceeds 5.
    3. Total active reservations match slot.booked_count.
    """
    asset_id = await _seed_asset(capacity=5)
    target_date = (datetime.now(UTC) + timedelta(days=25)).strftime("%Y-%m-%d")
    date_obj = (datetime.now(UTC) + timedelta(days=25)).date()

    admin_id, admin_headers = await _seed_user("admin_race@mangatarem.com", "admin_race", role="admin")

    # Seed 5 existing users and reservations filling the slot
    initial_users = [
        await _seed_user(f"init_user_{i}@mangatarem.com", f"init_user_{i}")
        for i in range(5)
    ]

    async with async_session_factory() as db:
        slot = BookingSlot(
            bookable_asset_id=asset_id,
            date=date_obj,
            total_capacity=5,
            booked_count=5,
        )
        db.add(slot)
        await db.flush()

        res_to_cancel = None
        for i in range(5):
            res = Reservation(
                user_id=initial_users[i][0],
                booking_slot_id=slot.id,
                party_size=1,
                primary_contact=f"0913000000{i}",
                status="confirmed",
            )
            db.add(res)
            if i == 0:
                res_to_cancel = res
        await db.commit()
        res_to_cancel_id = res_to_cancel.id
        slot_id = slot.id

    # 5 new competing users
    competitor_users = [
        await _seed_user(f"competitor_{i}@mangatarem.com", f"competitor_{i}")
        for i in range(5)
    ]

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Launch cancellation and 5 booking attempts concurrently
        cancel_task = ac.post(
            "/api/booking/admin/update-status",
            json={"reservation_id": res_to_cancel_id, "status": "cancelled"},
            headers=admin_headers,
        )
        booking_tasks = [
            ac.post(
                "/api/booking/reserve",
                json={
                    "asset_id": asset_id,
                    "date": target_date,
                    "party_size": 1,
                    "contact": f"091400000{i:02d}",
                },
                headers=competitor_users[i][1],
            )
            for i in range(5)
        ]

        all_responses = await asyncio.gather(cancel_task, *booking_tasks)
        cancel_resp = all_responses[0]
        booking_resps = all_responses[1:]

    assert cancel_resp.status_code == 200, f"Cancel failed: {cancel_resp.text}"

    new_successes = [r for r in booking_resps if r.status_code == 200]
    # At most 1 new booking could have claimed the cancelled seat
    assert len(new_successes) <= 1, f"Expected at most 1 new booking to succeed, got {len(new_successes)}"

    async with async_session_factory() as db:
        updated_slot = (
            await db.execute(select(BookingSlot).where(BookingSlot.id == slot_id))
        ).scalar_one()
        assert updated_slot.booked_count <= 5, f"Overbooking: booked_count={updated_slot.booked_count} > 5"

        active_res = (
            await db.execute(
                select(Reservation).where(
                    Reservation.booking_slot_id == slot_id,
                    Reservation.status != "cancelled",
                )
            )
        ).scalars().all()
        assert sum(r.party_size for r in active_res) == updated_slot.booked_count


# ───────────────────────────────────────────────────────────────
# 5. Adversarial Input Fuzzing
# ───────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_adversarial_input_validation():
    """Fuzzing input parameters to verify rejection without server crashes."""
    asset_id = await _seed_asset(capacity=10)
    target_date = (datetime.now(UTC) + timedelta(days=30)).strftime("%Y-%m-%d")
    _, headers = await _seed_user("fuzz_user@mangatarem.com", "fuzz_user")

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Zero party size
        resp = await ac.post(
            "/api/booking/reserve",
            json={"asset_id": asset_id, "date": target_date, "party_size": 0},
            headers=headers,
        )
        assert resp.status_code == 422

        # Negative party size
        resp = await ac.post(
            "/api/booking/reserve",
            json={"asset_id": asset_id, "date": target_date, "party_size": -3},
            headers=headers,
        )
        assert resp.status_code == 422

        # Invalid date format
        resp = await ac.post(
            "/api/booking/reserve",
            json={"asset_id": asset_id, "date": "not-a-date", "party_size": 1},
            headers=headers,
        )
        assert resp.status_code == 400

        # Impossible calendar date (Feb 30)
        resp = await ac.post(
            "/api/booking/reserve",
            json={"asset_id": asset_id, "date": "2026-02-30", "party_size": 1},
            headers=headers,
        )
        assert resp.status_code == 400

        # Non-existent asset
        resp = await ac.post(
            "/api/booking/reserve",
            json={"asset_id": 999999, "date": target_date, "party_size": 1},
            headers=headers,
        )
        assert resp.status_code == 400
        assert "not available" in resp.json().get("detail", "").lower()


# ───────────────────────────────────────────────────────────────
# 6. Admin Status Transition Tampering & RBAC
# ───────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_adversarial_status_transition_tampering():
    """Unauthorized status update attempts and illegal state transitions."""
    asset_id = await _seed_asset(capacity=5)
    target_date = (datetime.now(UTC) + timedelta(days=35)).strftime("%Y-%m-%d")

    regular_user_id, regular_headers = await _seed_user("reg_tamper@mangatarem.com", "reg_tamper", role="user")
    admin_id, admin_headers = await _seed_user("admin_tamper@mangatarem.com", "admin_tamper", role="admin")

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Reserve a slot
        res_resp = await ac.post(
            "/api/booking/reserve",
            json={"asset_id": asset_id, "date": target_date, "party_size": 1},
            headers=regular_headers,
        )
        assert res_resp.status_code == 200
        res_id = res_resp.json()["reservation_id"]

        # Regular user tries to update status -> 403 Forbidden
        hack_resp = await ac.post(
            "/api/booking/admin/update-status",
            json={"reservation_id": res_id, "status": "attended"},
            headers=regular_headers,
        )
        assert hack_resp.status_code == 403

        # Admin cancels reservation
        cancel_resp = await ac.post(
            "/api/booking/admin/update-status",
            json={"reservation_id": res_id, "status": "cancelled"},
            headers=admin_headers,
        )
        assert cancel_resp.status_code == 200

        # Admin attempts illegal transition: cancelled -> confirmed
        illegal_resp = await ac.post(
            "/api/booking/admin/update-status",
            json={"reservation_id": res_id, "status": "confirmed"},
            headers=admin_headers,
        )
        assert illegal_resp.status_code == 400
        assert "Cannot transition" in illegal_resp.json()["detail"]
