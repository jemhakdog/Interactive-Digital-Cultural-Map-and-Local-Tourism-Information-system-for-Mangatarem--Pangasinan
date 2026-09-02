"""
Integration tests for physical arrival verification and check-in API (FastAPI).

Port of the Flask-era tests/test_booking_arrival.py to the FastAPI TestClient
with JWT auth. Exercises POST /api/booking/verify-arrival.

NOTE: the FastAPI route currently does NOT write VisitorLog rows (port gap).
The assertions on VisitorLog below encode the intended behavior.
"""
import asyncio
from datetime import UTC, datetime

import pytest
from sqlalchemy import select

from backend.app.core.database import async_session_factory
from backend.app.models.analytics import VisitorLog
from backend.app.models.attractions import Attraction
from backend.app.models.booking import BookableAsset, BookingSlot, Reservation
from backend.app.models.business import Establishment
from backend.app.models.user import User


def _run(coro):
    return asyncio.run(coro)


@pytest.fixture
def setup_data(client, auth_headers):
    """Seed users/attractions/establishment/booking slot via direct DB session."""
    async def _seed():
        async with async_session_factory() as db:
            user = User(
                username="test_traveler",
                email="traveler@mangatarem.com",
                role="user",
                is_approved=True,
            )
            user.set_password("securepassword")
            db.add(user)
            await db.flush()

            church = Attraction(
                name="Mangatarem Holy Family Parish",
                description="Historic Roman Catholic parish church in Mangatarem.",
                category="culture",
                latitude=15.7905,
                longitude=120.2934,
                status="approved",
                is_verified=True,
            )
            db.add(church)
            far_spot = Attraction(
                name="Far Away Eco Park",
                description="Eco park located far away.",
                category="nature",
                latitude=15.8350,
                longitude=120.2934,
                status="approved",
                is_verified=True,
            )
            db.add(far_spot)
            cafe = Establishment(
                name="Mangatarem Heritage Cafe",
                description="Cozy heritage cafe.",
                type="restaurant",
                latitude=15.7906,
                longitude=120.2935,
                status="approved",
                owner=user,
            )
            db.add(cafe)
            await db.flush()

            asset = BookableAsset(attraction_id=church.id, daily_capacity=20, status="active")
            db.add(asset)
            await db.flush()

            today = datetime.now(UTC).date()
            slot = BookingSlot(bookable_asset_id=asset.id, date=today, total_capacity=20)
            db.add(slot)
            await db.flush()

            reservation = Reservation(
                user_id=user.id,
                booking_slot_id=slot.id,
                party_size=3,
                primary_contact="09171234567",
                status="confirmed",
            )
            db.add(reservation)
            await db.commit()

            return {
                "user_id": user.id,
                "church_id": church.id,
                "far_spot_id": far_spot.id,
                "cafe_id": cafe.id,
                "reservation_id": reservation.id,
            }

    return _run(_seed())


def _login_traveler(client):
    resp = client.post(
        "/api/auth/login",
        json={"email": "traveler@mangatarem.com", "password": "securepassword"},
    )
    assert resp.status_code == 200, resp.text
    return {"Authorization": f"Bearer {resp.json()['access_token']}"}


def test_unauthenticated_request_fails(client):
    """Verify unauthorized users cannot verify arrival."""
    response = client.post("/api/booking/verify-arrival", json={"latitude": 15.7905, "longitude": 120.2934})
    assert response.status_code == 401  # FastAPI OAuth2 requires a token


def test_invalid_payload_fails(client, setup_data):
    """Verify endpoint handles malformed or missing coordinate payloads."""
    headers = _login_traveler(client)

    # Empty body -> 422 (Pydantic)
    response = client.post("/api/booking/verify-arrival", json=None, headers=headers)
    assert response.status_code == 422

    # Missing coordinates -> 422
    response = client.post("/api/booking/verify-arrival", json={"latitude": 15.7905}, headers=headers)
    assert response.status_code == 422

    # Invalid numeric coordinate formats -> 422
    response = client.post(
        "/api/booking/verify-arrival",
        json={"latitude": "invalid_lat", "longitude": 120.2934},
        headers=headers,
    )
    assert response.status_code == 422


def test_arrival_check_in_within_proximity(client, setup_data):
    """Reservation checked in + VisitorLog written when within 100m."""
    headers = _login_traveler(client)
    response = client.post(
        "/api/booking/verify-arrival",
        json={"latitude": 15.79052, "longitude": 120.29342},
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["booking_attended"] is True
    assert data["place_name"] == "Mangatarem Holy Family Parish"

    # Reservation flipped to attended
    async def _check():
        async with async_session_factory() as db:
            res = await db.get(Reservation, setup_data["reservation_id"])
            assert res.status == "attended"
            log = (
                await db.execute(
                    select(VisitorLog).where(
                        VisitorLog.visitor_user_id == setup_data["user_id"],
                        VisitorLog.target_type == "attraction",
                        VisitorLog.target_id == setup_data["church_id"],
                    )
                )
            ).scalar_one_or_none()
            assert log is not None
            assert log.visitor_count == 3
            assert log.visitor_name == "test_traveler"
            assert "verified via GPS arrival" in log.notes

    _run(_check())


def test_arrival_check_in_outside_proximity(client, setup_data):
    """Check-in skipped when outside 100m."""
    headers = _login_traveler(client)
    response = client.post(
        "/api/booking/verify-arrival",
        json={"latitude": 15.7945, "longitude": 120.2934},
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["booking_attended"] is False

    async def _check():
        async with async_session_factory() as db:
            res = await db.get(Reservation, setup_data["reservation_id"])
            assert res.status == "confirmed"
            log = (
                await db.execute(
                    select(VisitorLog).where(
                        VisitorLog.visitor_user_id == setup_data["user_id"],
                        VisitorLog.target_type == "attraction",
                        VisitorLog.target_id == setup_data["church_id"],
                    )
                )
            ).scalar_one_or_none()
            assert log is None

    _run(_check())


def test_navigated_landmark_arrival(client, setup_data):
    """Navigated attraction arrival stops navigation, logs visit."""
    headers = _login_traveler(client)
    response = client.post(
        "/api/booking/verify-arrival",
        json={
            "latitude": 15.79061,
            "longitude": 120.29351,
            "navigated_target_id": setup_data["cafe_id"],
            "navigated_target_type": "establishment",
        },
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["navigated_arrived"] is True
    assert data["place_name"] == "Mangatarem Heritage Cafe"
    assert data["target_id"] == setup_data["cafe_id"]
    assert data["target_type"] == "establishment"

    async def _check():
        async with async_session_factory() as db:
            log = (
                await db.execute(
                    select(VisitorLog).where(
                        VisitorLog.visitor_user_id == setup_data["user_id"],
                        VisitorLog.target_type == "establishment",
                        VisitorLog.target_id == setup_data["cafe_id"],
                    )
                )
            ).scalar_one_or_none()
            assert log is not None
            assert log.visitor_count == 1
            assert "via GPS arrival at navigated destination" in log.notes

    _run(_check())


def test_duplicate_arrival_prevention(client, setup_data):
    """No duplicate VisitorLog entries on repeated hits."""
    headers = _login_traveler(client)
    payload = {
        "latitude": 15.79061,
        "longitude": 120.29351,
        "navigated_target_id": setup_data["cafe_id"],
        "navigated_target_type": "establishment",
    }
    res1 = client.post("/api/booking/verify-arrival", json=payload, headers=headers)
    assert res1.status_code == 200
    res2 = client.post(
        "/api/booking/verify-arrival",
        json={"latitude": 15.79062, "longitude": 120.29352, **payload},
        headers=headers,
    )
    assert res2.status_code == 200

    async def _check():
        async with async_session_factory() as db:
            rows = (
                await db.execute(
                    select(VisitorLog).where(
                        VisitorLog.visitor_user_id == setup_data["user_id"],
                        VisitorLog.target_type == "establishment",
                        VisitorLog.target_id == setup_data["cafe_id"],
                    )
                )
            ).scalars().all()
            assert len(rows) == 1

    _run(_check())
