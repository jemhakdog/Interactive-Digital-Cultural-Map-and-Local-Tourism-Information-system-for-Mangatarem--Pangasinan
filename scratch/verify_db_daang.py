import sys
import os
import json

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_dir)

from app import create_app
from modules.attractions.models import Attraction

app = create_app()
with app.app_context():
    daang = Attraction.query.filter(Attraction.name.like('%Daang Kalikasan%')).first()
    if daang:
        print(f"ATTRACTION: {daang.name}")
        print(f"PRIMARY COORDS: ({daang.latitude}, {daang.longitude})")
        print("OSM ALTERNATIVES IN DB:")
        print(json.dumps(daang.osm_alternatives, indent=2))
    else:
        print("Daang Kalikasan not found in DB!")
