from flask import Flask
from flask_login import LoginManager
from models import db, User, Attraction
import json
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mangatarem.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'mp4'}

# Initialize database
db.init_app(app)
with app.app_context():
    db.create_all()

# Initialize login manager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def seed_database():
    """Seed the database with initial data"""
    # Check if attractions exist
    if Attraction.query.first() is None:
        data_path = os.path.join(app.root_path, 'data', 'attractions.json')
        if os.path.exists(data_path):
            with open(data_path, 'r') as f:
                data = json.load(f)
                for item in data:
                    attraction = Attraction(
                        name=item['name'],
                        category=item['category'],
                        barangay=item.get('barangay'),
                        description=item['description'],
                        lat=item['lat'],
                        lng=item['lng'],
                        image_url=item['image'],
                        status='approved'
                    )
                    db.session.add(attraction)
            db.session.commit()
            print("Database seeded with attractions.")

    # Create default admin if not exists
    if User.query.filter_by(username='admin').first() is None:
        admin = User(username='admin', email='admin@example.com', role='admin', is_approved=True)
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Default admin created.")

    # Create default contributor (Barangay Rep) if not exists
    if User.query.filter_by(username='barangay').first() is None:
        contributor = User(username='barangay', email='barangay@example.com', role='contributor', barangay='Poblacion', is_approved=True)
        contributor.set_password('barangay123')
        db.session.add(contributor)
        db.session.commit()
        print("Default contributor created.")

# Register all blueprints
from routes import register_blueprints
register_blueprints(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_database()
    app.run(debug=True)
