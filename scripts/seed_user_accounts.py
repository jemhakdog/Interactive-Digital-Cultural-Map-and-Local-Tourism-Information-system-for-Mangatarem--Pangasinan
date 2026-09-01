"""Seed the local database with accounts from user_accounts.md (idempotent)."""
import sys
from datetime import datetime

sys.path.insert(0, ".")
from app import create_app
from extensions import db
from models import User

# (id, username, email, role, approved, created_at)
ACCOUNTS = [
    (1, "admin", "admin@example.com", "admin", True, "2026-05-24 09:00:03.395546"),
    (2, "test_owner", "test_owner@example.com", "business_owner", True, "2026-05-24 09:00:03.766859"),
    (3, "tourist", "tourist@example.com", "user", True, "2026-05-24 09:00:04.171314"),
    (4, "dining_owner", "dining@example.com", "business_owner", True, "2026-05-24 09:00:04.556665"),
    (5, "hospitality_owner", "hospitality@example.com", "business_owner", True, "2026-05-24 09:00:04.859024"),
    (6, "jem", "jemcarlo46@gmail.com", "user", True, "2026-05-30 03:45:17.159900"),
    (7, "brgy_rep_test", "brgy_rep_test@example.com", "contributor", True, "2026-06-09 22:12:59.610086"),
    (8, "TestBusiness2026", "testbusiness2026@example.com", "user", False, "2026-07-29 07:57:12.259112"),
    (9, "BusinessOwner2026", "businessowner2026@example.com", "business_owner", True, "2026-07-29 07:59:57.973453"),
    (10, "BarangayGuard2026", "barangayguard2026@example.com", "contributor", True, "2026-07-29 08:37:40.889947"),
    (11, "steward", "steward@example.com", "contributor", True, "2026-07-29 10:06:31.085423"),
    (12, "TestUser", "test@example.com", "user", True, "2026-08-19 01:10:40.782237"),
    (13, "NewUser", "new@example.com", "user", True, "2026-08-19 01:12:31.513407"),
    (14, "FinalUser", "final@example.com", "user", True, "2026-08-19 01:12:47.669862"),
    (15, "adminuser", "admin@test.com", "admin", False, "2026-08-19 04:17:07.362135"),
    (16, "regularuser", "user@test.com", "user", True, "2026-08-19 04:17:08.489345"),
]
PASSWORD = "password123"


def main():
    app = create_app()
    with app.app_context():
        created = updated = unchanged = 0
        for uid, username, email, role, approved, created_at in ACCOUNTS:
            user = User.query.filter_by(username=username).first() or \
                   User.query.filter_by(email=email).first()
            if user is None:
                user = User(username=username, email=email)
                user.set_password(PASSWORD)
                created += 1
                db.session.add(user)
            else:
                user.username = username
                user.email = email
                updated += 1
            user.role = role
            user.is_approved = approved
            user.set_password(PASSWORD)  # md: all accounts share this password
            user.created_at = datetime.fromisoformat(created_at)
        db.session.commit()

        print(f"Created: {created}, Updated: {updated}")
        emails = {e for _, _, e, _, _, _ in ACCOUNTS}
        for u in User.query.filter(User.email.in_(emails)).order_by(User.id).all():
            ok = u.check_password(PASSWORD)
            print(f"  {u.id:>2} {u.username:<20} {u.email:<30} {u.role:<14} approved={u.is_approved} pw={'ok' if ok else 'MISMATCH'}")


if __name__ == "__main__":
    main()
