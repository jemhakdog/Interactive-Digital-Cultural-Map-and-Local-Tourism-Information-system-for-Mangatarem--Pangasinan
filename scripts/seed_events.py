from flask_app import app, db
from models import Event
from datetime import datetime, timedelta

def seed_events():
    with app.app_context():
        # Check if we already have events to avoid duplicates
        if Event.query.count() > 0:
            print("Events already exist. Skipping seed.")
            return

        events = [
            Event(
                title="St. Raymond's Feast",
                description="Join us for the annual feast of St. Raymond. A day of prayer, food, and community.",
                date=datetime.now() + timedelta(days=5),
                location="St. Raymond's Church",
                barangay="Poblacion",
                status="approved",
                image_url="https://mangatarem.gov.ph/wp-content/uploads/2022/06/DSC_0054.jpg"
            ),
            Event(
                title="Battle of the Bands",
                description="Rock out with the best local bands in Mangatarem! Free entry for everyone.",
                date=datetime.now() + timedelta(days=10),
                location="Public Plaza",
                barangay="Poblacion",
                status="approved",
                image_url="https://mangatarem.gov.ph/wp-content/uploads/2022/06/DSC_0098.jpg"
            ),
            Event(
                title="Civic Parade",
                description="A grand parade showcasing the different sectors of our community.",
                date=datetime.now() + timedelta(days=15),
                location="Mangatarem Streets",
                barangay="Poblacion",
                status="approved",
                image_url="https://mangatarem.gov.ph/wp-content/uploads/2022/06/DSC_0123.jpg"
            )
        ]

        for event in events:
            db.session.add(event)
        
        db.session.commit()
        print("Added 3 sample events.")

if __name__ == "__main__":
    seed_events()
