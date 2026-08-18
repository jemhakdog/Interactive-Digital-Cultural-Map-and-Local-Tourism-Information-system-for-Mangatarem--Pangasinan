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
            {
                "barangay_name": "Malabobo",
                "name": "Malabobo Eco-Adventure & Bamboo Festival",
                "description": "Celebrate the lush bamboo groves of Malabobo with eco-tours, hand-crafted bamboo exhibitions, and traditional bamboo dance performances near the Manleluag Spring protected landscape.",
                "date": datetime(2026, 4, 12, 9, 0),
                "location": "Malabobo Eco-Park",
                "latitude": 15.7033,
                "longitude": 120.2758,
                "category": "Civic",
                "image_url": "https://images.unsplash.com/photo-1502082553048-f009c37129b9?q=80&w=2070&auto=format&fit=crop"
            },
            {
                "barangay_name": "Poblacion",
                "name": "Mangatarem Tupig Festival (Grand Fiesta)",
                "description": "The premier annual event of Mangatarem celebrating our signature native rice cake, Tupig. Features the Grand Tupig Cook-off, street dancing competition, and cultural night.",
                "date": datetime(2026, 12, 28, 8, 0),
                "location": "Municipal Town Plaza",
                "latitude": 15.7891,
                "longitude": 120.2928,
                "category": "Entertainment",
                "image_url": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?q=80&w=2074&auto=format&fit=crop"
            },
            {
                "barangay_name": "Cabaluyan",
                "name": "Cabaluyan Mango Harvest and Agri-Fiesta",
                "description": "Join the sweet harvest of the famous sweet carabao mangoes of Cabaluyan. Features fresh mango markets, family fruit-picking tours, and backyard farming seminars.",
                "date": datetime(2026, 5, 15, 7, 30),
                "location": "Cabaluyan Community Orchard",
                "latitude": 15.8012,
                "longitude": 120.2854,
                "category": "Entertainment",
                "image_url": "https://images.unsplash.com/photo-1553279768-865429fa0078?q=80&w=2074&auto=format&fit=crop"
            },
            {
                "barangay_name": "Bogtong",
                "name": "Bogtong Clay Pottery and Crafts Festival",
                "description": "Honoring the historic pottery-making tradition of Bogtong. Highlights include live clay-sculpting demonstrations, DIY pottery workshops for visitors, and an artisan stoneware fair.",
                "date": datetime(2026, 10, 20, 10, 0),
                "location": "Bogtong Pottery Workshop Center",
                "latitude": 15.7725,
                "longitude": 120.3120,
                "category": "Civic",
                "image_url": "https://images.unsplash.com/photo-1565192647048-f997ed87f5e2?q=80&w=2070&auto=format&fit=crop"
            },
            {
                "barangay_name": "Dorongan",
                "name": "Dorongan Golden Corn and Agricultural Fair",
                "description": "Dorongan's thanksgiving celebration for its bountiful corn harvests. Featuring corn-themed culinary contests, agricultural machinery displays, and traditional folk music.",
                "date": datetime(2026, 3, 18, 9, 30),
                "location": "Dorongan Barangay Hall Plaza",
                "latitude": 15.7610,
                "longitude": 120.2650,
                "category": "Civic",
                "image_url": "https://images.unsplash.com/photo-1551754655-cd27e38d20f6?q=80&w=2070&auto=format&fit=crop"
            },
            {
                "barangay_name": "Quetegan",
                "name": "Quetegan Basi Wine & Rice Harvest Festival",
                "description": "A celebration of traditional sugarcane wine (Basi) brewing and golden rice harvest. Enjoy local wine tastings, traditional rice-mashing rituals, and acoustic folk music under the stars.",
                "date": datetime(2026, 11, 24, 17, 0),
                "location": "Quetegan Heritage Fields",
                "latitude": 15.8150,
                "longitude": 120.3080,
                "category": "Entertainment",
                "image_url": "https://images.unsplash.com/photo-1543257580-7269da773bf5?q=80&w=2070&auto=format&fit=crop"
            },
            {
                "barangay_name": "Pacalat",
                "name": "Pacalat River Flotilla & Fishery Celebration",
                "description": "A vibrant river flotilla parade along the Pacalat River, celebrating inland fishery abundance and advocating for river conservation and sustainable angling.",
                "date": datetime(2026, 6, 8, 8, 30),
                "location": "Pacalat Riverbank Park",
                "latitude": 15.8320,
                "longitude": 120.2950,
                "category": "Civic",
                "image_url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=2073&auto=format&fit=crop"
            },
            {
                "barangay_name": "Parian",
                "name": "Parian Handloom Weaving & Abel Heritage Festival",
                "description": "A premium showcase of the centuries-old traditional handloom weaving of Parian. Features local 'Abel' textile fashion displays, loom-weaving workshops, and historical walking tours.",
                "date": datetime(2026, 9, 15, 13, 0),
                "location": "Parian Cultural Hall",
                "latitude": 15.7950,
                "longitude": 120.2980,
                "category": "Religious",
                "image_url": "https://images.unsplash.com/photo-1528747045269-390fe33c19f2?q=80&w=2070&auto=format&fit=crop"
            }
        ]

        for event_data in new_events:
            existing = Event.query.filter(Event.name.ilike(event_data["name"])).first()
            if not existing:
                brgy = BarangayInfo.query.filter(BarangayInfo.name.ilike(event_data["barangay_name"])).first()
                brgy_id = brgy.id if brgy else default_barangay.id
                event = Event(
                    name=event_data["name"],
                    category=event_data["category"],
                    description=event_data["description"],
                    date=event_data["date"],
                    location=event_data["location"],
                    latitude=event_data["latitude"],
                    longitude=event_data["longitude"],
                    barangay_id=brgy_id,
                    image_url=event_data["image_url"],
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
