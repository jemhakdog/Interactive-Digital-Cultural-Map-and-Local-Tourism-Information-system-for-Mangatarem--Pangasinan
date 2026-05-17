import os
import sys

sys.path.append(os.getcwd())

from app import create_app
from models import Attraction, Establishment, NewsletterSubscriber

app = create_app()
with app.app_context():
    print("--- ATTRACTIONS ---")
    for a in Attraction.query.all():
        print(f"[{a.category}] {a.name}")
    
    print("\n--- ESTABLISHMENTS ---")
    for e in Establishment.query.all():
        print(f"[{e.type}] {e.name}")

    print("\n--- NEWSLETTER SUBSCRIBERS ---")
    for s in NewsletterSubscriber.query.all():
        status = "Active" if s.is_active else "Inactive"
        print(f"[{status}] {s.email} (joined: {s.created_at})")
