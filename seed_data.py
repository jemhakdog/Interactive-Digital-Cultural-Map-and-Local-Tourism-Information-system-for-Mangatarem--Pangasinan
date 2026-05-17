import os
import sys

# Ensure the project directory is in the path
sys.path.append(os.getcwd())

from app import create_app
from extensions import db
from models import User, BarangayInfo, Attraction, Establishment, NewsletterSubscriber

def seed_data():
    app = create_app()
    with app.app_context():
        print("Starting data seeding...")

        # 1. Create Admin User
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@mangatarem.gov.ph',
                role='admin',
                is_approved=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.flush()
            print("Admin user created.")
        else:
            print("Admin user already exists.")

        # 2. Create Barangays
        barangay_names = ['Poblacion', 'Malabobo', 'Bogtong', 'Dorongan', 'Quetegan']
        barangays = {}
        for name in barangay_names:
            b = BarangayInfo.query.filter_by(name=name).first()
            if not b:
                b = BarangayInfo(
                    name=name,
                    mission=f"Mission of {name}",
                    vision=f"Vision of {name}",
                    history=f"History of {name}"
                )
                db.session.add(b)
                db.session.flush()
                print(f"Barangay {name} created.")
            barangays[name] = b

        # 3. Create Attractions (Nature, Heritage, Religious)
        attractions_data = [
            {
                'name': 'Manleluag Spring Protected Landscape',
                'description': 'A protected area known for its hot springs and diverse flora and fauna.',
                'category': 'Nature',
                'latitude': 15.7033,
                'longitude': 120.2758,
                'barangay': 'Malabobo'
            },
            {
                'name': 'St. Raymund of Peñafort Parish',
                'description': 'A historic Catholic church in the heart of Mangatarem.',
                'category': 'Religious',
                'latitude': 15.7901,
                'longitude': 120.2917,
                'barangay': 'Poblacion'
            },
            {
                'name': 'Mangatarem Heritage Museum',
                'description': 'A museum showcasing the cultural and historical heritage of the town.',
                'category': 'Heritage',
                'latitude': 15.7895,
                'longitude': 120.2925,
                'barangay': 'Poblacion'
            }
        ]

        for attr in attractions_data:
            if not Attraction.query.filter_by(name=attr['name']).first():
                a = Attraction(
                    name=attr['name'],
                    description=attr['description'],
                    category=attr['category'],
                    latitude=attr['latitude'],
                    longitude=attr['longitude'],
                    barangay_id=barangays[attr['barangay']].id,
                    user_id=admin.id,
                    status='approved',
                    is_featured=True
                )
                db.session.add(a)
                print(f"Attraction {attr['name']} created.")

        # 4. Create Establishments (inn, restaurant, cafe, fastfood)
        establishments_data = [
            {
                'name': 'Mangatarem View Hotel',
                'type': 'inn',
                'description': 'Comfortable stay with a view of the mountains.',
                'latitude': 15.7920,
                'longitude': 120.2930,
                'barangay': 'Poblacion'
            },
            {
                'name': 'Pangasinan Flavors',
                'type': 'restaurant',
                'description': 'Traditional Filipino dishes and local specialties.',
                'latitude': 15.7880,
                'longitude': 120.2910,
                'barangay': 'Poblacion'
            },
            {
                'name': 'The Brew Hub',
                'type': 'cafe',
                'description': 'Freshly brewed local coffee and pastries.',
                'latitude': 15.7910,
                'longitude': 120.2900,
                'barangay': 'Poblacion'
            },
            {
                'name': 'Quick Bites Mangatarem',
                'type': 'fastfood',
                'description': 'Fast and delicious meals for people on the go.',
                'latitude': 15.7890,
                'longitude': 120.2940,
                'barangay': 'Poblacion'
            }
        ]

        for est in establishments_data:
            if not Establishment.query.filter_by(name=est['name']).first():
                e = Establishment(
                    name=est['name'],
                    type=est['type'],
                    description=est['description'],
                    latitude=est['latitude'],
                    longitude=est['longitude'],
                    barangay_id=barangays[est['barangay']].id,
                    owner_id=admin.id,
                    status='approved',
                    is_featured=True,
                    price_range='moderate'
                )
                db.session.add(e)
                print(f"Establishment {est['name']} created.")

        # 5. Create Newsletter Subscribers
        subscribers_data = [
            {'email': 'mangatarem.visitor@outlook.com', 'is_active': True},
            {'email': 'heritage.advocate@mangatarem.gov.ph', 'is_active': True},
            {'email': 'local.steward@poblacion.org', 'is_active': True},
            {'email': 'pangasinan.traveler@gmail.com', 'is_active': True},
            {'email': 'curious.explorer@yahoo.com', 'is_active': True},
            {'email': 'unsubscribed.user@example.com', 'is_active': False}
        ]

        for sub in subscribers_data:
            if not NewsletterSubscriber.query.filter_by(email=sub['email']).first():
                ns = NewsletterSubscriber(
                    email=sub['email'],
                    is_active=sub['is_active']
                )
                db.session.add(ns)
                print(f"Newsletter subscriber {sub['email']} created.")

        db.session.commit()
        print("Data seeding completed successfully!")

if __name__ == "__main__":
    seed_data()
