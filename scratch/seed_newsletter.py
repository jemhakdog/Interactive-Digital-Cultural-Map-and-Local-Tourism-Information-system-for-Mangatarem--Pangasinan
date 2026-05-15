import os
from app import create_app
from extensions import db
from modules.notifications.models import NewsletterSubscriber
from datetime import datetime, timedelta
import random

def seed_newsletter():
    app = create_app()
    with app.app_context():
        print("Seeding dummy newsletter subscribers...")
        
        # List of dummy emails
        dummy_emails = [
            "juan.delacruz@example.com",
            "maria.clara@example.com",
            "rizal.fan@pangasinan.gov",
            "traveler123@gmail.com",
            "culture_lover@heritage.org",
            "mangatarem_local@yahoo.com",
            "visitor_test1@outlook.com",
            "tourist_guide@visitph.com",
            "heritage_watcher@unesco.org",
            "foodie_explorer@mangatarem.com",
            "nature_enthusiast@green.org",
            "history_buff@museum.ph",
            "student_researcher@up.edu.ph",
            "barangay_rep@mangatarem.gov.ph",
            "curious_mind@discovery.com"
        ]
        
        added_count = 0
        for email in dummy_emails:
            # Check if exists
            existing = NewsletterSubscriber.query.filter_by(email=email).first()
            if not existing:
                # Randomize created_at over the last 30 days
                days_ago = random.randint(0, 30)
                created_at = datetime.utcnow() - timedelta(days=days_ago)
                
                subscriber = NewsletterSubscriber(
                    email=email,
                    is_active=random.choice([True, True, True, False]), # 75% active
                    created_at=created_at
                )
                db.session.add(subscriber)
                added_count += 1
        
        db.session.commit()
        print(f"Successfully added {added_count} dummy subscribers.")

if __name__ == "__main__":
    seed_newsletter()
