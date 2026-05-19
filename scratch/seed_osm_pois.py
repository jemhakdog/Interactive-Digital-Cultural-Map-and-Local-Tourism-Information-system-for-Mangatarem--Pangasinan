import os
import sys
import json
import math

# Ensure project directory is in the path
sys.path.append(os.getcwd())

from app import create_app
from extensions import db
from models import Attraction, Establishment, BarangayInfo, User

# Coordinates of our 8 seeded barangays to calculate the nearest one for POIs
BARANGAY_COORDS = {
    'Malabobo': (15.7033, 120.2758),
    'Poblacion': (15.7891, 120.2928),
    'Cabaluyan': (15.8012, 120.2854),
    'Bogtong': (15.7725, 120.3120),
    'Dorongan': (15.7610, 120.2650),
    'Quetegan': (15.8150, 120.3080),
    'Pacalat': (15.8320, 120.2950),
    'Parian': (15.7950, 120.2980),
}

def get_distance(lat1, lon1, lat2, lon2):
    """Simple Euclidean distance calculation for geofencing/nearest barangay."""
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

def seed_osm_pois():
    app = create_app()
    with app.app_context():
        print("Starting official OSM POI seeding...")

        # 1. Get admin user as owner
        admin = User.query.filter_by(role='admin').first()
        if not admin:
            admin = User.query.first()
        if not admin:
            print("Error: No administrative user found. Seed users first.")
            return
        print(f"Using owner/admin: {admin.username} (ID: {admin.id})")

        # 2. Get barangays from DB
        db_barangays = {b.name: b for b in BarangayInfo.query.all()}
        if not db_barangays:
            print("Error: No barangays found. Seed barangays first.")
            return
        print(f"Loaded {len(db_barangays)} barangays from database.")

        # 3. Load POIs from JSON
        json_path = "scratch/osm_pois.json"
        if not os.path.exists(json_path):
            print(f"Error: JSON file {json_path} not found. Run scratch/osm_search.py first.")
            return

        with open(json_path, "r", encoding="utf-8") as f:
            pois = json.load(f)
        print(f"Loaded {len(pois)} POIs from {json_path}")

        attractions_added = 0
        establishments_added = 0

        for poi in pois:
            name = poi['name']
            lat = poi['lat']
            lon = poi['lon']
            category = poi['category']
            tags = poi['tags']

            # Match to nearest barangay
            nearest_barangay_name = 'Poblacion'
            min_dist = float('inf')
            
            # First, check if any barangay name is explicitly mentioned in tags
            explicit_match = False
            for b_name in db_barangays:
                # Check street, place, name, description, etc.
                for tag_val in tags.values():
                    if isinstance(tag_val, str) and b_name.lower() in tag_val.lower():
                        nearest_barangay_name = b_name
                        explicit_match = True
                        break
                if explicit_match:
                    break

            if not explicit_match:
                # Calculate nearest based on distance
                for b_name, coords in BARANGAY_COORDS.items():
                    dist = get_distance(lat, lon, coords[0], coords[1])
                    if dist < min_dist:
                        min_dist = dist
                        nearest_barangay_name = b_name

            barangay = db_barangays.get(nearest_barangay_name)
            if not barangay:
                # Fallback to the first one available
                barangay = list(db_barangays.values())[0]

            # Construct address
            addr_parts = []
            if 'addr:housenumber' in tags:
                addr_parts.append(tags['addr:housenumber'])
            if 'addr:street' in tags:
                addr_parts.append(tags['addr:street'])
            addr_parts.append(barangay.name)
            addr_parts.append("Mangatarem, Pangasinan")
            address = ", ".join(addr_parts)

            contact_num = tags.get('contact:phone') or tags.get('phone') or tags.get('contact:mobile')
            email = tags.get('contact:email') or tags.get('email')
            website = tags.get('contact:website') or tags.get('website')

            # --- ESTABLISHMENTS ---
            if category in ['dining', 'accommodation']:
                # Deduce specific establishment type
                est_type = 'restaurant'
                if category == 'accommodation':
                    est_type = 'inn'
                elif 'amenity' in tags:
                    if tags['amenity'] == 'cafe':
                        est_type = 'cafe'
                    elif tags['amenity'] == 'fast_food':
                        est_type = 'fastfood'

                # Check for existing
                existing = Establishment.query.filter(Establishment.name.ilike(name)).first()
                if not existing:
                    # Determine description
                    desc = tags.get('description') or f"Official {est_type} establishment located in Barangay {barangay.name}, Mangatarem, Pangasinan."
                    if 'cuisine' in tags:
                        desc += f" Serves {tags['cuisine'].replace(';', ', ')} cuisine."
                    if 'opening_hours' in tags:
                        desc += f" Open hours: {tags['opening_hours']}."

                    est = Establishment(
                        name=name,
                        type=est_type,
                        description=desc,
                        address=address,
                        latitude=lat,
                        longitude=lon,
                        barangay_id=barangay.id,
                        contact_number=contact_num,
                        email=email,
                        website=website,
                        owner_id=admin.id,
                        status='approved',
                        is_featured=False,
                        price_range='moderate'
                    )
                    db.session.add(est)
                    establishments_added += 1
                    print(f"Added Establishment: {name} ({est_type}) in {barangay.name}")
                else:
                    print(f"Skipping existing establishment: {name}")

            # --- ATTRACTIONS ---
            else:
                # Classify attractions category
                attr_cat = 'Heritage'
                if category == 'religious':
                    attr_cat = 'Religious'
                elif category == 'leisure':
                    attr_cat = 'Nature'  # Pools, resorts, parks
                elif category == 'attraction':
                    attr_cat = 'Heritage'

                # Check for existing
                existing = Attraction.query.filter(Attraction.name.ilike(name)).first()
                if not existing:
                    desc = tags.get('description') or f"Official {attr_cat.lower()} point of interest in Barangay {barangay.name}, Mangatarem, Pangasinan."
                    if 'religion' in tags:
                        desc += f" Denomination: {tags.get('denomination', 'Christian')} ({tags['religion']})."

                    attr = Attraction(
                        name=name,
                        description=desc,
                        category=attr_cat,
                        latitude=lat,
                        longitude=lon,
                        barangay_id=barangay.id,
                        user_id=admin.id,
                        status='approved',
                        is_featured=False,
                        is_verified=True,
                        directions=f"Travel to Barangay {barangay.name}, Mangatarem, Pangasinan. Located at real-world coordinates ({lat}, {lon})."
                    )
                    db.session.add(attr)
                    attractions_added += 1
                    print(f"Added Attraction: {name} ({attr_cat}) in {barangay.name}")
                else:
                    print(f"Skipping existing attraction: {name}")

        db.session.commit()
        print(f"\nSeeding summary:")
        print(f"- Added {establishments_added} new establishments.")
        print(f"- Added {attractions_added} new attractions.")
        print("OSM POI database seeding finished successfully!")

if __name__ == "__main__":
    seed_osm_pois()
