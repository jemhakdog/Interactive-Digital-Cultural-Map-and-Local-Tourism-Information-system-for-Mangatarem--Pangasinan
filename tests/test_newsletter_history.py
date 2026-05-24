from models import NewsletterHistory, User
from extensions import db

def test_newsletter_history_model(app):
    """Test creating and saving a NewsletterHistory record."""
    with app.app_context():
        history = NewsletterHistory(
            subject="Cultural Map Updates",
            content="<p>Discover new spots on the interactive map!</p>",
            recipient_count=12
        )
        db.session.add(history)
        db.session.commit()
        
        # Verify persistence
        saved = NewsletterHistory.query.filter_by(subject="Cultural MapUpdates").first()
        # Whoops, typo above, let's look by exact subject
        saved = NewsletterHistory.query.filter_by(subject="Cultural Map Updates").first()
        assert saved is not None
        assert saved.recipient_count == 12
        assert "<p>Discover" in saved.content
        assert saved.sent_at is not None

def test_admin_history_routes(app, client):
    """Test accessing the history routes as admin and non-admin."""
    with app.app_context():
        # Add test record
        record = NewsletterHistory(
            subject="Admin Test Subject",
            content="Hello and welcome!",
            recipient_count=5
        )
        db.session.add(record)
        
        # Create an admin user and helper roles
        admin = User(username="history_admin", email="admin@history.com", role="admin", is_approved=True)
        admin.set_password("admin_pass")
        db.session.add(admin)
        
        regular_user = User(username="normal_steward", email="steward@history.com", role="barangay_rep", is_approved=True)
        regular_user.set_password("user_pass")
        db.session.add(regular_user)
        
        db.session.commit()
        
        record_id = record.id
        admin_id = admin.id
        user_id = regular_user.id

    # 1. Unauthenticated request should fail
    response = client.get("/admin/newsletter/history")
    assert response.status_code == 302 # Redirect to login

    # 2. Regular user (non-admin) should fail with permissions error
    client.post("/auth/login", data={"username": "normal_steward", "password": "user_pass"}, follow_redirects=True)
    response = client.get("/admin/newsletter/history")
    assert response.status_code == 302 # Redirect to index due to admin_required decorator
    client.get("/auth/logout")
    
    # 3. Admin user should succeed
    client.post("/auth/login", data={"username": "history_admin", "password": "admin_pass"}, follow_redirects=True)
        
    response = client.get("/admin/newsletter/history")
    assert response.status_code == 200
    assert b"Dispatch Records Archive" in response.data
    assert b"Admin Test Subject" in response.data

    # 4. JSON Content AJAX endpoint should succeed and return exact payload
    response = client.get(f"/admin/newsletter/history/{record_id}/content")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["subject"] == "Admin Test Subject"
    assert json_data["content"] == "Hello and welcome!"
    assert json_data["recipient_count"] == 5
    assert "sent_at" in json_data
