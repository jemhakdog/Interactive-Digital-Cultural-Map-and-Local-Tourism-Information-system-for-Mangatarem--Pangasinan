"""
Scratch script to seed default LGU Achievement Badges in the database.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from extensions import db
from modules.gamification.models import AchievementBadge
from models import Attraction, Establishment

def seed_badges():
    app = create_app()
    with app.app_context():
        # Clean existing badges
        db.session.query(AchievementBadge).delete()
        
        # Get some sample attraction IDs to map
        attractions = Attraction.query.limit(3).all()
        attraction_ids = [a.id for a in attractions]
        
        if not attraction_ids:
            # Fallback mock IDs if attractions are not seeded yet
            attraction_ids = [1, 2, 3]

        badge1 = AchievementBadge(
            title="Heritage Pilgrim",
            description="Explore Mangatarem's sacred and historic foundations by visiting central historical plazas and churches.",
            badge_image_url="/static/img/badges/pilgrim.png",
            required_visits=len(attraction_ids[:2]),
            target_locations=attraction_ids[:2],
            reward_promo={"discount": "10% Off Lodging", "code": "PILGRIM10", "terms": "Valid at all LGU verified Homestays."}
        )

        badge2 = AchievementBadge(
            title="Eco-Adventurer",
            description="Journey through Mangatarem's lush natural parks, waterfalls, and rich green conservation trails.",
            badge_image_url="/static/img/badges/eco.png",
            required_visits=1,
            target_locations=[attraction_ids[-1]] if attraction_ids else [3],
            reward_promo={"discount": "Free Native Tupig Pack", "code": "ECOTUPIG", "terms": "Claim at any verified barangay market stand."}
        )

        badge3 = AchievementBadge(
            title="Mangatarem Foodie",
            description="Experience Mangatarem's authentic culinary heritage by dining at verified local establishments.",
            badge_image_url="/static/img/badges/foodie.png",
            required_visits=1,
            target_locations=[1], # Mock
            reward_promo={"discount": "15% Off Meals", "code": "FOODIE15", "terms": "For bills above 500 PHP at verified diners."}
        )

        db.session.add_all([badge1, badge2, badge3])
        db.session.commit()
        print("Default LGU Achievement Badges seeded successfully!")

if __name__ == "__main__":
    seed_badges()
