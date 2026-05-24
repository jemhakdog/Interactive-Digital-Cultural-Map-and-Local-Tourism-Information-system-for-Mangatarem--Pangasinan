"""
Unit and integration tests for physical arrival verification and check-in API.
"""

import pytest
from datetime import datetime
from models import User, Attraction, Establishment, VisitorLog
from modules.booking.models import BookableAsset, BookingSlot, Reservation
from extensions import db


class TestBookingArrivalVerification:
    
    @pytest.fixture
    def setup_data(self, app):
        """Set up test environment models in DB."""
        with app.app_context():
            # 1. Create a dummy user
            user = User(username="test_traveler", email="traveler@mangatarem.com", role="user", is_approved=True)
            user.set_password("securepassword")
            db.session.add(user)
            
            # 2. Create attractions (e.g. Mangatarem Church and a far away place)
            # Mangatarem Church roughly: 15.7905, 120.2934
            church = Attraction(
                name="Mangatarem Holy Family Parish",
                description="Historic Roman Catholic parish church in Mangatarem.",
                category="culture",
                latitude=15.7905,
                longitude=120.2934,
                status="approved",
                is_verified=True
            )
            db.session.add(church)
            
            # Far attraction (e.g. 5 kilometers away: 15.8350, 120.2934)
            far_spot = Attraction(
                name="Far Away Eco Park",
                description="Eco park located far away.",
                category="nature",
                latitude=15.8350,
                longitude=120.2934,
                status="approved",
                is_verified=True
            )
            db.session.add(far_spot)

            # 3. Create an establishment (e.g. Local Cafe at 15.7906, 120.2935)
            cafe = Establishment(
                name="Mangatarem Heritage Cafe",
                description="Cozy heritage cafe.",
                type="restaurant",
                latitude=15.7906,
                longitude=120.2935,
                status="approved",
                owner=user
            )
            db.session.add(cafe)
            
            db.session.commit()
            
            # Save IDs for thread-safe/session-safe lookup in tests
            user_id = user.id
            church_id = church.id
            far_spot_id = far_spot.id
            cafe_id = cafe.id
            
            # 4. Bind booking slot & reservation for today
            today = datetime.utcnow().date()
            
            asset = BookableAsset(attraction_id=church_id, daily_capacity=20, status="active")
            db.session.add(asset)
            db.session.commit()
            
            slot = BookingSlot(bookable_asset_id=asset.id, date=today, total_capacity=20)
            db.session.add(slot)
            db.session.commit()
            
            reservation = Reservation(
                user_id=user_id,
                booking_slot_id=slot.id,
                party_size=3,
                primary_contact="09171234567",
                status="confirmed"
            )
            db.session.add(reservation)
            db.session.commit()
            
            yield {
                'user_id': user_id,
                'church_id': church_id,
                'far_spot_id': far_spot_id,
                'cafe_id': cafe_id,
                'reservation_id': reservation.id
            }

    def test_unauthenticated_request_fails(self, client):
        """Verify unauthorized users cannot verify arrival."""
        response = client.post('/booking/api/verify-arrival', json={
            'latitude': 15.7905,
            'longitude': 120.2934
        })
        assert response.status_code in (302, 401)  # Flask-Login redirects or returns 401 for unauthenticated users

    def test_invalid_payload_fails(self, client, setup_data):
        """Verify endpoint handles malformed or missing coordinate payloads."""
        # Authenticate traveler
        with client.session_transaction() as sess:
            sess['_user_id'] = str(setup_data['user_id'])
            sess['_fresh'] = True
            
        # Empty body
        response = client.post('/booking/api/verify-arrival', json=None)
        assert response.status_code == 400
        
        # Missing coordinates
        response = client.post('/booking/api/verify-arrival', json={'latitude': 15.7905})
        assert response.status_code == 400
        
        # Invalid numeric coordinate formats
        response = client.post('/booking/api/verify-arrival', json={
            'latitude': "invalid_lat",
            'longitude': 120.2934
        })
        assert response.status_code == 400

    def test_arrival_check_in_within_proximity(self, app, client, setup_data):
        """Verify reservation is checked in and VisitorLog written when user is within 100 meters."""
        # Authenticate traveler
        with client.session_transaction() as sess:
            sess['_user_id'] = str(setup_data['user_id'])
            sess['_fresh'] = True
            
        # Call API at coordinates extremely close to Mangatarem Church (church latitude=15.7905, longitude=120.2934)
        response = client.post('/booking/api/verify-arrival', json={
            'latitude': 15.79052,  # roughly 2 meters away
            'longitude': 120.29342
        })
        
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['success'] is True
        assert json_data['booking_attended'] is True
        assert json_data['place_name'] == "Mangatarem Holy Family Parish"
        
        # Verify DB updates in app context
        with app.app_context():
            res = Reservation.query.get(setup_data['reservation_id'])
            assert res.status == 'attended'
            
            # Visitor log must be logged automatically
            log = VisitorLog.query.filter_by(
                visitor_user_id=setup_data['user_id'],
                target_type='attraction',
                target_id=setup_data['church_id']
            ).first()
            assert log is not None
            assert log.visitor_count == 3
            assert log.visitor_name == "test_traveler"
            assert "verified via GPS arrival" in log.notes

    def test_arrival_check_in_outside_proximity(self, app, client, setup_data):
        """Verify reservation check-in is skipped if user is outside the 100-meter proximity bounds."""
        # Authenticate traveler
        with client.session_transaction() as sess:
            sess['_user_id'] = str(setup_data['user_id'])
            sess['_fresh'] = True
            
        # Coordinates located far away (approx 500 meters from church)
        response = client.post('/booking/api/verify-arrival', json={
            'latitude': 15.7945,  
            'longitude': 120.2934
        })
        
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['success'] is True
        assert json_data['booking_attended'] is False
        
        # Verify DB is unchanged
        with app.app_context():
            res = Reservation.query.get(setup_data['reservation_id'])
            assert res.status == 'confirmed'
            
            log = VisitorLog.query.filter_by(
                visitor_user_id=setup_data['user_id'],
                target_type='attraction',
                target_id=setup_data['church_id']
            ).first()
            assert log is None

    def test_navigated_landmark_arrival(self, app, client, setup_data):
        """Verify navigated attraction arrival stops navigation, logs visit, and updates status correctly."""
        # Authenticate traveler
        with client.session_transaction() as sess:
            sess['_user_id'] = str(setup_data['user_id'])
            sess['_fresh'] = True
            
        # User is navigating to local Cafe (15.7906, 120.2935) and physically gets within 5 meters
        response = client.post('/booking/api/verify-arrival', json={
            'latitude': 15.79061,
            'longitude': 120.29351,
            'navigated_target_id': setup_data['cafe_id'],
            'navigated_target_type': 'establishment'
        })
        
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['success'] is True
        assert json_data['navigated_arrived'] is True
        assert json_data['place_name'] == "Mangatarem Heritage Cafe"
        assert json_data['target_id'] == setup_data['cafe_id']
        assert json_data['target_type'] == 'establishment'
        
        # Verify visit was safely recorded in VisitorLog
        with app.app_context():
            log = VisitorLog.query.filter_by(
                visitor_user_id=setup_data['user_id'],
                target_type='establishment',
                target_id=setup_data['cafe_id']
            ).first()
            assert log is not None
            assert log.visitor_count == 1
            assert "via GPS arrival at navigated destination" in log.notes

    def test_duplicate_arrival_prevention(self, app, client, setup_data):
        """Verify system does not write multiple duplicate VisitorLog entries on repeated API hits."""
        with client.session_transaction() as sess:
            sess['_user_id'] = str(setup_data['user_id'])
            sess['_fresh'] = True
            
        # Hit 1: Arrive at Cafe
        res1 = client.post('/booking/api/verify-arrival', json={
            'latitude': 15.79061,
            'longitude': 120.29351,
            'navigated_target_id': setup_data['cafe_id'],
            'navigated_target_type': 'establishment'
        })
        assert res1.status_code == 200
        
        # Hit 2: Repeat checking location
        res2 = client.post('/booking/api/verify-arrival', json={
            'latitude': 15.79062,
            'longitude': 120.29352,
            'navigated_target_id': setup_data['cafe_id'],
            'navigated_target_type': 'establishment'
        })
        assert res2.status_code == 200
        
        # Verify there is exactly one log entry for today
        with app.app_context():
            logs = VisitorLog.query.filter_by(
                visitor_user_id=setup_data['user_id'],
                target_type='establishment',
                target_id=setup_data['cafe_id']
            ).all()
            assert len(logs) == 1
