from app import create_app
from extensions import db
from models import Attraction, Establishment, Event, HeritageProfile

app = create_app()
with app.app_context():
    print('--- ATTRACTIONS ---')
    for a in Attraction.query.all():
        print(f"- {a.name}")
    
    print('\n--- ESTABLISHMENTS ---')
    for e in Establishment.query.all():
        print(f"- {e.name}")
        
    print('\n--- EVENTS ---')
    for ev in Event.query.all():
        print(f"- {ev.name}")
        
    print('\n--- HERITAGE ---')
    for h in HeritageProfile.query.all():
        print(f"- {h.name_of_asset or h.common_name}")
