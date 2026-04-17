from werkzeug.security import generate_password_hash
from app import create_app
from extensions import db
from models import User, BarangayInfo

def setup_contributor():
    app = create_app()
    with app.app_context():
        # Ensure at least one Barangay exists
        barangay = BarangayInfo.query.first()
        if not barangay:
            print("Creating default Barangay: General...")
            barangay = BarangayInfo(
                name="General",
                mission="Promoting cultural awareness and heritage preservation through digital participation.",
                vision="A connected community proud of its roots and heritage.",
                history="A vibrant community in Mangatarem with a rich history of agricultural success and cultural traditions.",
                cultural_assets="St. James the Apostle Church, Local Artisans",
                traditions="Pistay Dayat participation, Local fiestas",
                local_practices="Traditional farming, Weaver communities",
                unique_features="Scenic rice fields and historical landmarks"
            )
            db.session.add(barangay)
            db.session.commit()
            print(f"Created Barangay ID: {barangay.id}")
        else:
            print(f"Using existing Barangay: {barangay.name} (ID: {barangay.id})")

        username = "steward"
        email = "steward@example.com"
        password = "steward123"
        role = "contributor"

        user = User.query.filter_by(username=username).first()
        if user:
            print(f"User '{username}' already exists. Updating password, role, and approval status...")
            user.password = generate_password_hash(password)
            user.role = role
            user.email = email
            user.is_approved = True
            user.barangay_id = barangay.id
        else:
            print(f"Creating new user: {username}")
            user = User(
                username=username,
                email=email,
                password=generate_password_hash(password),
                role=role,
                is_approved=True,
                barangay_id=barangay.id
            )
            db.session.add(user)
        
        db.session.commit()
        print(f"SUCCESS: User '{username}' is ready to login with role '{role}' and password '{password}'.")
        print(f"Login URL: http://localhost:5002/auth/login")

if __name__ == "__main__":
    setup_contributor()
