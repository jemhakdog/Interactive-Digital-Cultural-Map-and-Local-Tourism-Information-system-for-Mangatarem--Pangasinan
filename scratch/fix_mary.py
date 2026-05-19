import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db, Establishment

app = create_app()
with app.app_context():
    e = Establishment.query.filter_by(name='MARY').first()
    if e:
        print(f"Current status: {e.status}")
        print(f"Current coordinates: Lat {e.latitude}, Lng {e.longitude}")
        
        # Approve the establishment
        e.status = 'approved'
        
        # Update coordinates to be in Mangatarem center (if it is 10.79)
        if abs(e.latitude - 10.79) < 0.1:
            e.latitude = 15.7889
            e.longitude = 120.2986
            print("Updating coordinates to Mangatarem Center: 15.7889, 120.2986")
        
        db.session.commit()
        print("Successfully approved and updated coordinates in database!")
    else:
        print("Establishment MARY not found")
