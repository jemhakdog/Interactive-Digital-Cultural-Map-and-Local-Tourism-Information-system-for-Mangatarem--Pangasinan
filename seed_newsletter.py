import os
import sys
from datetime import datetime, timedelta

# Ensure the project directory is in the path
sys.path.append(os.getcwd())

from app import create_app
from extensions import db
from models import NewsletterSubscriber

def seed_newsletter():
    app = create_app()
    with app.app_context():
        print("Starting safe newsletter seeding...")
        
        subscribers_data = [
            {'email': 'jemcarlo46@gmail.com', 'is_active': True, 'days_ago': 0}, # today
            {'email': 'mangatarem.visitor@outlook.com', 'is_active': True, 'days_ago': 12},
            {'email': 'heritage.advocate@mangatarem.gov.ph', 'is_active': True, 'days_ago': 45},
            {'email': 'local.steward@poblacion.org', 'is_active': True, 'days_ago': 30},
            {'email': 'pangasinan.traveler@gmail.com', 'is_active': True, 'days_ago': 18},
            {'email': 'curious.explorer@yahoo.com', 'is_active': True, 'days_ago': 5},
            {'email': 'unsubscribed.user@example.com', 'is_active': False, 'days_ago': 60},
            
            # Realistic local Mangatarem/Pangasinan dummy subscribers
            {'email': 'juan.delacruz.mangatarem@gmail.com', 'is_active': True, 'days_ago': 25},
            {'email': 'maria.santos.pangasinan@yahoo.com', 'is_active': True, 'days_ago': 32},
            {'email': 'b.quetegan.steward@mangatarem.gov.ph', 'is_active': True, 'days_ago': 14},
            {'email': 'dorongan.rep@mangatarem.gov.ph', 'is_active': True, 'days_ago': 40},
            {'email': 'steward.malabobo@mangatarem.gov.ph', 'is_active': True, 'days_ago': 28},
            {'email': 'bogtong.heritage@gmail.com', 'is_active': True, 'days_ago': 50},
            {'email': 'poblacion.tourism@gmail.com', 'is_active': True, 'days_ago': 3},
            {'email': 'traveler.ph@outlook.com', 'is_active': True, 'days_ago': 8},
            {'email': 'up.diliman.historian@up.edu.ph', 'is_active': True, 'days_ago': 55},
            {'email': 'ust.heritage.center@ust.edu.ph', 'is_active': True, 'days_ago': 22},
            {'email': 'philippine.explorer@hotmail.com', 'is_active': True, 'days_ago': 19},
            {'email': 'adventurous.soul@gmail.com', 'is_active': True, 'days_ago': 15},
            {'email': 'ecotourism.champion@yahoo.com', 'is_active': True, 'days_ago': 9},
            {'email': 'local.business.owner@mangatarem.org', 'is_active': True, 'days_ago': 35},
            {'email': 'nature.photographer@outlook.ph', 'is_active': True, 'days_ago': 2},
            {'email': 'pangasinan.blogger@gmail.com', 'is_active': True, 'days_ago': 11},
            {'email': 'retired.teacher.mangatarem@gmail.com', 'is_active': True, 'days_ago': 48},
            {'email': 'inactive.user1@example.com', 'is_active': False, 'days_ago': 70},
            {'email': 'inactive.user2@example.com', 'is_active': False, 'days_ago': 80},
            {'email': 'inactive.user3@example.com', 'is_active': False, 'days_ago': 90},
            {'email': 'cultural.heritage.advocate@gmail.com', 'is_active': True, 'days_ago': 20},
            {'email': 'pila.liwanag@poblacion.org', 'is_active': True, 'days_ago': 4},
            {'email': 'antonio.luna@heritage.gov.ph', 'is_active': True, 'days_ago': 120},
            {'email': 'mangatarem.roots@yahoo.com', 'is_active': True, 'days_ago': 6},
            {'email': 'paskong.mangatarem@outlook.com', 'is_active': True, 'days_ago': 17}
        ]

        added_count = 0
        updated_count = 0
        
        for sub in subscribers_data:
            existing = NewsletterSubscriber.query.filter_by(email=sub['email']).first()
            created_date = datetime.utcnow() - timedelta(days=sub['days_ago'])
            
            if existing:
                existing.is_active = sub['is_active']
                existing.created_at = created_date
                updated_count += 1
            else:
                ns = NewsletterSubscriber(
                    email=sub['email'],
                    is_active=sub['is_active'],
                    created_at=created_date
                )
                db.session.add(ns)
                added_count += 1
                
        db.session.commit()
        print(f"Newsletter seeding completed: Added {added_count}, Updated {updated_count} subscribers.")

if __name__ == "__main__":
    seed_newsletter()
