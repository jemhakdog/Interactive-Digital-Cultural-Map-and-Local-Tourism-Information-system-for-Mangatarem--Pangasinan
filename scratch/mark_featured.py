import os
import sys

# Ensure the project directory is in the path
sys.path.append(os.getcwd())

from app import create_app
from extensions import db
from modules.attractions.models import Attraction
from modules.business.models import Establishment

def mark_featured():
    app = create_app()
    with app.app_context():
        print("Marking sample items as featured...")
        
        # Attractions
        attractions = Attraction.query.limit(3).all()
        for a in attractions:
            a.is_featured = True
            print(f"Featured Attraction: {a.name}")
            
        # Establishments
        establishments = Establishment.query.limit(2).all()
        for e in establishments:
            e.is_featured = True
            print(f"Featured Establishment: {e.name}")
            
        db.session.commit()
        print("Done!")

if __name__ == "__main__":
    mark_featured()
