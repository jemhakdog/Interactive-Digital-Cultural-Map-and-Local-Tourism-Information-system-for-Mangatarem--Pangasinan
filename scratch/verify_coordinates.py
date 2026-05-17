import sys
from app import create_app
from extensions import db
from modules.attractions.models import Attraction

app = create_app()
with app.app_context():
    print("\n--- ATTRACTIONS COORDINATES VERIFICATION ---")
    attractions = Attraction.query.all()
    print(f"Total Attractions in DB: {len(attractions)}")
    for attr in attractions:
        print(f"ID: {attr.id:<2} | {attr.name:<40} | Coords: ({attr.latitude}, {attr.longitude})")
    print("-------------------------------------------\n")
