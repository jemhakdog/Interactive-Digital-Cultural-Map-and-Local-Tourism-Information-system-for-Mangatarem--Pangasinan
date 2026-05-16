from app import create_app
from extensions import db
from modules.auth.models import User

app = create_app()
with app.app_context():
    users = User.query.all()
    print("Existing Users:")
    for u in users:
        print(f"- {u.username} ({u.role})")

    # Create new business owner if not exists
    username = "test_owner"
    if not User.query.filter_by(username=username).first():
        new_owner = User(
            username=username,
            email="test_owner@example.com",
            role="business_owner",
            is_approved=True
        )
        new_owner.set_password("owner123")
        db.session.add(new_owner)
        db.session.commit()
        print(f"\nSUCCESS: Created user '{username}' with password 'owner123'")
    else:
        print(f"\nINFO: User '{username}' already exists.")
