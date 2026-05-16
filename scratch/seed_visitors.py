from app import create_app
from extensions import db
from modules.analytics.models import VisitorLog
from modules.attractions.models import Attraction
from modules.auth.models import User
from datetime import datetime

app = create_app()

def seed_visitors():
    with app.app_context():
        # Get target attraction
        attraction = Attraction.query.filter_by(name='Manleluag Spring Protected Landscape').first()
        if not attraction:
            print("Attraction not found!")
            return
            
        # Get admin user as steward
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("Admin user not found!")
            return

        visitors = [
            ("Juan Dela Cruz", 28, "Manila", True),
            ("Maria Clara", 24, "Pangasinan", False),
            ("Pedro Penduko", 35, "Dagupan", True),
            ("Gabriela Silang", 30, "Vigan", False),
            ("Jose Rizal", 35, "Calamba", True),
            ("Andres Bonifacio", 29, "Tondo", False),
            ("Melchora Aquino", 84, "Quezon City", True),
            ("Apolinario Mabini", 34, "Tanauan", False),
            ("Antonio Luna", 32, "Badoc", True),
            ("Marcelo H. Del Pilar", 38, "Bulacan", False),
            ("Juan Luna", 31, "Ilocos Norte", True),
            ("Gregorio Del Pilar", 24, "Bulacan", False),
        ]

        print(f"Seeding 12 visitors for {attraction.name}...")
        
        for name, age, address, is_system in visitors:
            log = VisitorLog(
                target_type='attraction',
                target_id=attraction.id,
                visitor_count=1,
                visitor_name=name,
                visitor_age=age,
                visitor_address=address,
                is_system_user=is_system,
                logged_by=admin.id,
                visit_date=datetime.now(),
                notes="Automated seed data for testing detailed registry"
            )
            db.session.add(log)
        
        db.session.commit()
        print("Successfully seeded 12 visitor records.")

if __name__ == "__main__":
    seed_visitors()
