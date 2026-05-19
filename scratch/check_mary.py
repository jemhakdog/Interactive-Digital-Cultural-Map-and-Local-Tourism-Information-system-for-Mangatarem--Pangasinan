import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import Establishment

app = create_app()
with app.app_context():
    e = Establishment.query.filter_by(name='MARY').first()
    if e:
        print("Establishment details:")
        print(f"ID: {e.id}")
        print(f"Name: {e.name}")
        print(f"Status: {e.status}")
        print(f"Lat: {e.latitude}")
        print(f"Lng: {e.longitude}")
        print(f"Type: {e.type}")
        print(f"Owner ID: {e.owner_id}")
        print(f"Barangay ID: {e.barangay_id}")
        print(f"Menu Items Count: {len(e.menu_items)}")
        for item in e.menu_items:
            print(f"  - MenuItem: {item.name}, Price: {item.price}, Category: {item.category}, Available: {item.is_available}")
    else:
        print("Establishment MARY not found")
