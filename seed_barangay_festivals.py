import os
import sys
from datetime import datetime

# Add the project directory to python path
sys.path.append(os.getcwd())

from app import create_app
from extensions import db
from models import Event, BarangayInfo, User

def seed_festivals():
    app = create_app()
    with app.app_context():
        print("Starting Barangay Festivals seeding...")
        
        # 1. Get default admin user
        admin_user = User.query.filter_by(role='admin').first() or User.query.first()
        if not admin_user:
            print("Error: No user found in the database. Please seed users first.")
            return
            
        admin_id = admin_user.id
        print(f"Using creator user: {admin_user.username} (ID: {admin_id})")
        
        # 2. Define the 8 high-quality local festivals
        festivals_data = [
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
        
        # 3. Add to Database
        added_count = 0
        skipped_count = 0
        
        for data in festivals_data:
            barangay_name = data["barangay_name"]
            barangay = BarangayInfo.query.filter(BarangayInfo.name.ilike(barangay_name)).first()
            
            if not barangay:
                print(f"Warning: Barangay '{barangay_name}' not found. Skipping event '{data['name']}'.")
                skipped_count += 1
                continue
                
            # Check if this festival already exists
            existing = Event.query.filter(Event.name.ilike(data["name"])).first()
            if existing:
                print(f"Event '{data['name']}' already exists. Skipping.")
                skipped_count += 1
                continue
                
            # Create new event
            event = Event(
                name=data["name"],
                description=data["description"],
                date=data["date"],
                location=data["location"],
                latitude=data["latitude"],
                longitude=data["longitude"],
                barangay_id=barangay.id,
                category=data["category"],
                image_url=data["image_url"],
                status="approved",
                user_id=admin_id
            )
            db.session.add(event)
            added_count += 1
            print(f"Adding festival: '{data['name']}' for Barangay '{barangay.name}'")
            
        if added_count > 0:
            db.session.commit()
            print(f"Successfully seeded {added_count} new festivals to the database!")
        else:
            print("No new festivals were added (all exist or skipped).")
            
if __name__ == "__main__":
    seed_festivals()
