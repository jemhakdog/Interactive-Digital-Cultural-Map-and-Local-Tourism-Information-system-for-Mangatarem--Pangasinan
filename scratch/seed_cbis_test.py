import os
import sys
from datetime import datetime

# Ensure the project directory is in the path
sys.path.append(os.getcwd())

from app import create_app
from extensions import db
from models import User, BarangayInfo, Event, Attraction

def seed_test_data():
    app = create_app()
    with app.app_context():
        print("Searching for steward user...")
        steward = User.query.filter_by(username='steward').first()
        if not steward:
            print("ERROR: User 'steward' not found. Please run setup_contributor.py first.")
            return

        barangay = steward.barangay
        if not barangay:
            print(f"ERROR: User 'steward' is not linked to any barangay.")
            return

        print(f"Targeting Barangay: {barangay.name} (ID: {barangay.id})")

        # 1. Update Mission and Vision
        barangay.mission = "To prioritize cultural heritage preservation through participatory digital mapping and community inclusivity."
        barangay.vision = "A digitally-engaged and culturally-aware Malabobo community that celebrates its unique traditions for future generations."
        print("Updated Mission and Vision statement.")

        # 2. Add a new Community Event
        existing_event = Event.query.filter_by(name="Malabobo Heritage Weaving Workshop", barangay_id=barangay.id).first()
        if not existing_event:
            new_event = Event(
                name="Malabobo Heritage Weaving Workshop",
                description="A hands-on workshop demonstrating traditional weaving techniques unique to Malabobo, led by local elders.",
                date=datetime(2026, 4, 25),
                location="Malabobo Community Center",
                latitude=15.7895, # Specific location in Malabobo
                longitude=120.2860,
                category="Cultural Workshop",
                barangay_id=barangay.id,
                user_id=steward.id,
                status="approved"
            )
            db.session.add(new_event)
            print("Added new community event with coordinates.")

        # 3. Add a community attraction
        existing_attraction = Attraction.query.filter_by(name="Malabobo Century Tree", barangay_id=barangay.id).first()
        if not existing_attraction:
            community_attr = Attraction(
                name="Malabobo Century Tree",
                description="A massive historical tree that has served as a meeting point for generations of Malabobo residents.",
                category="Natural Heritage",
                latitude=15.7885, # Slightly different location to test clustered view
                longitude=120.2850,
                barangay_id=barangay.id,
                user_id=1,
                status="approved"
            )
            db.session.add(community_attr)
            print("Added community attraction with coordinates.")

        db.session.commit()
        print("SUCCESS: Database manually synchronized with test data.")

if __name__ == "__main__":
    seed_test_data()
