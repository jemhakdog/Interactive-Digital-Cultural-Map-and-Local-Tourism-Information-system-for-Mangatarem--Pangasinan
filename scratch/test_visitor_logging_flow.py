import pytest
from app import create_app
from extensions import db
from modules.auth.models import User
from modules.business.models import Establishment
from modules.attractions.models import Attraction
from modules.analytics.models import VisitorLog

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_visitor_logging_permissions(app, client):
    with app.app_context():
        # Setup users
        owner = User(username="owner", email="owner@test.com", role="business_owner", is_approved=True)
        owner.set_password("pass")
        
        steward = User(username="steward", email="steward@test.com", role="contributor", is_approved=True)
        steward.set_password("pass")
        
        other = User(username="other", email="other@test.com", role="business_owner", is_approved=True)
        other.set_password("pass")
        
        test_admin = User(username="test_admin", email="admin@test.com", role="admin", is_approved=True)
        test_admin.set_password("pass")

        db.session.add_all([owner, other, steward, test_admin])
        db.session.commit()
        
        # Create Establishment
        est = Establishment(
            owner_id=owner.id, 
            name="Test Hotel", 
            type="inn", 
            status="approved",
            latitude=15.1,
            longitude=120.1,
            description="A nice place"
        )
        # Create Attraction
        attr = Attraction(
            name="Test Park", 
            category="nature", 
            user_id=steward.id, 
            status="approved",
            latitude=15.2,
            longitude=120.2,
            description="Very green"
        )
        db.session.add_all([est, attr])
        db.session.commit()

        def login(username):
            return client.post("/auth/login", data={"username": username, "password": "pass"}, follow_redirects=True)

        # 1. Test Unauthenticated access
        resp = client.get(f"/analytics/log-visitor/establishment/{est.id}")
        assert resp.status_code == 302 # Redirect to login

        # 2. Test Owner access (Valid)
        login("owner")
        resp = client.get(f"/analytics/log-visitor/establishment/{est.id}")
        assert resp.status_code == 200
        assert b"Record Visitor" in resp.data
        assert b"Test Hotel" in resp.data

        # 3. Test Unauthorized Owner access
        login("other")
        resp = client.get(f"/analytics/log-visitor/establishment/{est.id}")
        assert resp.status_code == 302 # Redirect with error

        # 4. Test Steward access (Valid)
        login("steward")
        resp = client.get(f"/analytics/log-visitor/attraction/{attr.id}")
        assert resp.status_code == 200
        assert b"Test Park" in resp.data

        # 5. Test Admin access (Valid for everything)
        login("test_admin")
        resp = client.get(f"/analytics/log-visitor/establishment/{est.id}")
        assert resp.status_code == 200
        resp = client.get(f"/analytics/log-visitor/attraction/{attr.id}")
        assert resp.status_code == 200

        # 6. Test Submission
        login("steward")
        resp = client.post(f"/analytics/log-visitor/attraction/{attr.id}", data={
            "visitor_name": "Juan Dela Cruz",
            "visitor_age": "25",
            "visitor_address": "Mangatarem",
            "visitor_count": "1",
            "is_system_user": "false",
            "notes": "Test submission"
        }, follow_redirects=True)

        assert resp.status_code == 200
        assert b"recorded successfully" in resp.data

        # Verify DB
        log = VisitorLog.query.filter_by(visitor_name="Juan Dela Cruz").first()
        assert log is not None
        assert log.target_id == attr.id
        assert log.target_type == "attraction"
        assert log.logged_by == steward.id

def test_user_search_api(app, client):
    with app.app_context():
        user1 = User(username="tourist_one", email="t1@test.com", role="user", is_approved=True)
        user1.set_password("pass")
        user2 = User(username="tourist_two", email="t2@test.com", role="user", is_approved=True)
        user2.set_password("pass")
        staff = User(username="staff", email="staff@test.com", role="admin", is_approved=True)
        staff.set_password("pass")
        db.session.add_all([user1, user2, staff])
        db.session.commit()


        # Login as staff
        with client.session_transaction() as sess:
            sess['_user_id'] = str(staff.id)

        # Search for 'tourist_'
        resp = client.get("/auth/api/users/search?q=tourist_")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data is not None
        assert len(data) == 2
        assert any(u['username'] == "tourist_one" for u in data)

        # Search with short query
        resp = client.get("/auth/api/users/search?q=t")
        assert resp.status_code == 200
        assert resp.get_json() == []

