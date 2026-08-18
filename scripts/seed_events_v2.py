from app import app, db
from modules.events.models import Event
from datetime import datetime, timedelta

def seed_events_v2():
    with app.app_context():
        # Clear existing events if needed, or just add new ones
        # For testing purposes, we'll just add these 6 specific ones
        
        today = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
        
        events_data = [
            {
                "name": "Community Yoga Session",
                "description": "Start your day with a peaceful yoga session at the Mangatarem Public Plaza. Open to all ages.",
                "date": today,
                "location": "Public Plaza",
                "category": "Civic",
                "status": "approved",
                "image_url": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?q=80&w=2040&auto=format&fit=crop"
            },
            {
                "name": "Night Food Market",
                "description": "Taste the local delicacies of Mangatarem! Over 20 stalls offering street food and crafts.",
                "date": today + timedelta(hours=8), # Today evening
                "location": "Poblacion Market Area",
                "category": "Entertainment",
                "status": "approved",
                "image_url": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?q=80&w=2074&auto=format&fit=crop"
            },
            {
                "name": "St. Raymond's Feast Day",
                "description": "Celebrate our patron saint with a holy mass followed by a community banquet.",
                "date": today + timedelta(days=1),
                "location": "St. Raymond's Church",
                "category": "Religious",
                "status": "approved",
                "image_url": "https://images.unsplash.com/photo-1548625361-ec853f0cf786?q=80&w=2070&auto=format&fit=crop"
            },
            {
                "name": "Local Music Festival",
                "description": "Featuring bands from all over Pangasinan. A night of pure rock and roll.",
                "date": today + timedelta(days=5),
                "location": "Municipal Stadium",
                "category": "Entertainment",
                "status": "approved",
                "image_url": "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?q=80&w=2070&auto=format&fit=crop"
            },
            {
                "name": "Municipal Civic Parade",
                "description": "A grand parade celebrating our history and progress. Special guest appearances.",
                "date": today + timedelta(days=32), # Next month
                "location": "Main Streets",
                "category": "Civic",
                "status": "approved",
                "image_url": "https://images.unsplash.com/photo-1511632765486-a01980e01a18?q=80&w=2070&auto=format&fit=crop"
            },
            {
                "name": "Traditional Dance Workshop",
                "description": "Learn the traditional dances of Pangasinan. Taught by local masters.",
                "date": today + timedelta(days=35), # Next month
                "location": "Cultural Center",
                "category": "Religious", # Classified as religious/cultural for testing
                "status": "approved",
                "image_url": "https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?q=80&w=2069&auto=format&fit=crop"
            }
        ]

        added_count = 0
        for data in events_data:
            # Check if event already exists to avoid duplicates
            exists = Event.query.filter_by(name=data["name"]).first()
            if not exists:
                event = Event(**data)
                db.session.add(event)
                added_count += 1
        
        db.session.commit()
        print(f"Successfully added {added_count} new events.")

if __name__ == "__main__":
    seed_events_v2()
