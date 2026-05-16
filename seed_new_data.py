from app import create_app
from extensions import db
from models import Attraction, Establishment, Event, HeritageProfile, BarangayInfo, User
from datetime import datetime

def seed_data():
    app = create_app()
    with app.app_context():
        # Get default barangay (prefer Poblacion)
        default_barangay = BarangayInfo.query.filter(BarangayInfo.name.ilike('%Poblacion%')).first()
        if not default_barangay:
            default_barangay = BarangayInfo.query.first()
        
        if not default_barangay:
            print("Error: No barangay found in database. Please seed barangays first.")
            return

        # Get default owner (admin)
        admin_user = User.query.filter_by(role='admin').first()
        if not admin_user:
            admin_user = User.query.first()
        
        if not admin_user:
            print("Error: No user found in database. Please seed users first.")
            return

        print(f"Using default barangay: {default_barangay.name} (ID: {default_barangay.id})")
        print(f"Using default owner: {admin_user.username} (ID: {admin_user.id})")

        # Mangatarem roughly center coordinates
        DEFAULT_LAT = 15.7891
        DEFAULT_LNG = 120.2928

        # --- ATTRACTIONS ---
        new_attractions = [
            {"name": "Pacalat River", "category": "Nature", "description": "A scenic river in Mangatarem."},
            {"name": "Canding (Kanding) Falls", "category": "Nature", "description": "Beautiful natural waterfalls."},
            {"name": "Municipal Town Plaza", "category": "Public Space", "description": "The central gathering place of the municipality."}
        ]

        for attr_data in new_attractions:
            existing = Attraction.query.filter(Attraction.name.ilike(attr_data["name"])).first()
            if not existing:
                attr = Attraction(
                    name=attr_data["name"],
                    category=attr_data["category"],
                    description=attr_data["description"],
                    latitude=DEFAULT_LAT,
                    longitude=DEFAULT_LNG,
                    barangay_id=default_barangay.id,
                    status="approved"
                )
                db.session.add(attr)
                print(f"Added Attraction: {attr_data['name']}")
            else:
                print(f"Skipping duplicate Attraction: {attr_data['name']}")

        # --- ESTABLISHMENTS ---
        new_establishments = [
            {"name": "Teraoka Farm (Organic Farm)", "type": "inn", "description": "Organic farming and tourism destination."},
            {"name": "Our Farm Republic (Organic Farm)", "type": "inn", "description": "A hub for organic farming and education."},
            {"name": "ag.KAPI.ta Cafe", "type": "cafe", "description": "Local cafe featuring Mangatarem flavors."}
        ]

        for est_data in new_establishments:
            existing = Establishment.query.filter(Establishment.name.ilike(est_data["name"])).first()
            if not existing:
                est = Establishment(
                    name=est_data["name"],
                    type=est_data["type"],
                    description=est_data["description"],
                    address=f"{default_barangay.name}, Mangatarem",
                    latitude=DEFAULT_LAT,
                    longitude=DEFAULT_LNG,
                    barangay_id=default_barangay.id,
                    owner_id=admin_user.id,
                    status="approved"
                )
                db.session.add(est)
                print(f"Added Establishment: {est_data['name']}")
            else:
                print(f"Skipping duplicate Establishment: {est_data['name']}")

        # --- EVENTS ---
        new_events = [
            {"name": "Tupig Festival", "category": "Festival", "description": "Annual celebration of the local tupig delicacy.", "date": datetime(2026, 12, 1)}
        ]

        for event_data in new_events:
            existing = Event.query.filter(Event.name.ilike(event_data["name"])).first()
            if not existing:
                event = Event(
                    name=event_data["name"],
                    category=event_data["category"],
                    description=event_data["description"],
                    date=event_data["date"],
                    location="Municipal Plaza",
                    latitude=DEFAULT_LAT,
                    longitude=DEFAULT_LNG,
                    barangay_id=default_barangay.id,
                    status="approved"
                )
                db.session.add(event)
                print(f"Added Event: {event_data['name']}")
            else:
                print(f"Skipping duplicate Event: {event_data['name']}")

        # --- HERITAGE ---
        new_heritage = [
            {"name": "Mangatarem Municipal Hall", "type": "built", "description": "The historic seat of local government."},
            {"name": "Dr. Jose Rizal Monument", "type": "built", "description": "A monument dedicated to the national hero."},
            {"name": "Old Convent", "type": "built", "description": "A historic religious structure."},
            {"name": "Heritage Houses (Corleto, Don Ramon Ventenilla, and Aviles Residences)", "type": "built", "description": "Well-preserved traditional Filipino houses."}
        ]

        for heritage_data in new_heritage:
            existing = HeritageProfile.query.filter(
                (HeritageProfile.name_of_asset.ilike(heritage_data["name"])) | 
                (HeritageProfile.common_name.ilike(heritage_data["name"]))
            ).first()
            if not existing:
                heritage = HeritageProfile(
                    name_of_asset=heritage_data["name"],
                    asset_type=heritage_data["type"],
                    significance=heritage_data["description"],
                    location_details=f"{default_barangay.name}, Mangatarem",
                    latitude=DEFAULT_LAT,
                    longitude=DEFAULT_LNG,
                    barangay_id=default_barangay.id,
                    status="approved"
                )
                db.session.add(heritage)
                print(f"Added Heritage: {heritage_data['name']}")
            else:
                print(f"Skipping duplicate Heritage: {heritage_data['name']}")

        db.session.commit()
        print("\nSeeding completed successfully!")

if __name__ == "__main__":
    seed_data()
