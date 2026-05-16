from app import create_app
from extensions import db
from modules.auth.models import User
from modules.business.models import Establishment

app = create_app()
with app.app_context():
    # Find the test owner
    username = "test_owner"
    user = User.query.filter_by(username=username).first()
    
    if not user:
        print(f"ERROR: User '{username}' not found. Run the previous script first.")
    else:
        # Check if they already have an establishment
        est = Establishment.query.filter_by(owner_id=user.id).first()
        
        if not est:
            new_est = Establishment(
                owner_id=user.id,
                name="Gisando Heritage Inn",
                type="inn",
                status="approved",
                latitude=15.7865,
                longitude=120.2987,
                description="A charming heritage-themed inn located in the heart of Mangatarem. Perfect for tourists seeking authentic local hospitality.",
                address="Poblacion, Mangatarem, Pangasinan",
                contact_number="0912-345-6789"
            )
            db.session.add(new_est)
            db.session.commit()
            print(f"SUCCESS: Created dummy establishment 'Gisando Heritage Inn' for user '{username}'")
        else:
            print(f"INFO: User '{username}' already has an establishment: '{est.name}'")
