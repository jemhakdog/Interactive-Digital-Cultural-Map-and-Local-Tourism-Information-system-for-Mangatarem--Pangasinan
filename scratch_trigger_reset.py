from app import app
from models import db, User, PasswordResetToken

def create_user_and_trigger_reset(email, username):
    with app.app_context():
        user = User.query.filter_by(email=email).first()
        if not user:
            print(f"User '{email}' not found. Creating...")
            user = User(username=username, email=email, role="user", is_approved=True)
            user.set_password("OldPassword123!")
            db.session.add(user)
            db.session.commit()
            print(f"Created user with ID {user.id}")
            
        token = PasswordResetToken.create_for_user(user, 30)
        reset_url = f"http://localhost:5000/auth/reset-password/{token.token}"
        print(f"Reset URL for {email}: {reset_url}")

create_user_and_trigger_reset("jemcarlo46@gmail.com", "jemcarlo46")
create_user_and_trigger_reset("jem carlo46@gmail.com", "jemcarlo_space")
