import os
import sys

sys.path.append(os.getcwd())

from app import create_app
from models import Attraction, Establishment

app = create_app()
with app.app_context():
    print("--- ATTRACTIONS ---")
    for a in Attraction.query.all():
        print(f"[{a.category}] {a.name}")
    
    print("\n--- ESTABLISHMENTS ---")
    for e in Establishment.query.all():
        print(f"[{e.type}] {e.name}")
