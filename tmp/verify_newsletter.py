import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db, NewsletterSubscriber

app = create_app('testing')

with app.app_context():
    # 1. Clear testing subscribers if any
    NewsletterSubscriber.query.filter(NewsletterSubscriber.email.like('%@test.com')).delete()
    db.session.commit()
    print("Cleared existing test subscribers.")

    # 2. Test Subscription
    test_email = "tester@test.com"
    new_sub = NewsletterSubscriber(email=test_email)
    db.session.add(new_sub)
    db.session.commit()
    print(f"Subscribed: {test_email}")

    # 3. Verify in DB
    sub = NewsletterSubscriber.query.filter_by(email=test_email).first()
    if sub and sub.is_active:
        print("Verification SUCCESS: Subscriber found and active.")
    else:
        print("Verification FAILED: Subscriber not found or inactive.")

    # 4. Test Duplicate Subscription (should handle reactivation)
    sub.is_active = False
    db.session.commit()
    print(f"Deactivated {test_email}")

    # Simulate re-subscription logic from public.py
    existing = NewsletterSubscriber.query.filter_by(email=test_email).first()
    if existing:
        if not existing.is_active:
            existing.is_active = True
            db.session.commit()
            print("Successfully reactivated subscriber.")
    
    # 5. Final check
    final_sub = NewsletterSubscriber.query.filter_by(email=test_email).first()
    if final_sub and final_sub.is_active:
        print("Final Verification SUCCESS: Reactivation worked.")
    else:
        print("Final Verification FAILED.")

    # Cleanup
    db.session.delete(final_sub)
    db.session.commit()
    print("Cleanup complete.")
