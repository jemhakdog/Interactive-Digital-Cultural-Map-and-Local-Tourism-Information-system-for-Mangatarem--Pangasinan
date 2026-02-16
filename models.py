from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default="user")  # 'admin', 'contributor', or 'user'
    barangay = db.Column(db.String(100), nullable=True)
    is_approved = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Attraction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(
        db.String(50), nullable=False, index=True
    )  # Nature, Historical, Religious, etc.
    barangay = db.Column(db.String(100), nullable=True, index=True)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200), nullable=True)
    status = db.Column(
        db.String(20), default="pending", index=True
    )  # 'pending', 'approved'
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True, index=True)
    reviewed_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # === Heritage Fields (Form 02A & 03A Support) ===
    
    # Heritage Type Indicator
    heritage_type = db.Column(db.String(50), nullable=True)  # 'building', 'archaeological', 'natural', 'standard'
    
    # Form 02A - Tangible Immovable (Buildings) Fields
    building_type = db.Column(db.String(50), nullable=True)  # municipal_hall, church, bridge, etc.
    year_constructed = db.Column(db.Integer, nullable=True)
    ownership_type = db.Column(db.String(20), nullable=True)  # public/private
    declaration_legislation = db.Column(db.Text, nullable=True)
    physical_description = db.Column(db.Text, nullable=True)
    history_structure = db.Column(db.Text, nullable=True)
    occupation_status = db.Column(db.String(20), nullable=True)  # occupied/not_occupied
    stories_associated = db.Column(db.Text, nullable=True)
    condition = db.Column(db.String(20), nullable=True)  # excellent/good/fair/deteriorated/ruins
    condition_remarks = db.Column(db.Text, nullable=True)
    is_altered = db.Column(db.Boolean, nullable=True)
    is_original_site = db.Column(db.Boolean, nullable=True)
    integrity_remarks = db.Column(db.Text, nullable=True)
    conservation_measures = db.Column(db.Text, nullable=True)
    movable_heritage_list = db.Column(db.JSON, nullable=True)  # List of objects within premises
    
    # Form 03A - Tangible Movable (Archaeological) Fields
    object_type = db.Column(db.String(50), nullable=True)  # stone_tools, ceramics, metal, etc.
    place_found = db.Column(db.String(200), nullable=True)
    date_found = db.Column(db.Date, nullable=True)
    estimated_age = db.Column(db.String(100), nullable=True)
    acquisition_type = db.Column(db.String(50), nullable=True)
    materials = db.Column(db.String(200), nullable=True)
    dimensions = db.Column(db.String(100), nullable=True)
    comparative_criteria = db.Column(db.Text, nullable=True)  # Provenance, Rarity, etc.
    
    # Common Heritage Fields (applicable to Forms 02A & 03A)
    significance_types = db.Column(db.JSON, nullable=True)  # Array: ['historical', 'aesthetic', 'spiritual']
    constraints_threats = db.Column(db.Text, nullable=True)
    key_informants = db.Column(db.JSON, nullable=True)
    references = db.Column(db.Text, nullable=True)
    mapper_name = db.Column(db.String(200), nullable=True)
    date_profiled = db.Column(db.Date, nullable=True)



class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    barangay = db.Column(db.String(100), nullable=True)
    image_url = db.Column(db.String(200), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    status = db.Column(db.String(20), default="pending")  # 'pending', 'approved'
    category = db.Column(
        db.String(50), nullable=False, default="Civic"
    )  # 'Religious', 'Civic', 'Entertainment'
    reviewed_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class GalleryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)  # 'photo' or 'video'
    url = db.Column(db.String(200), nullable=False)
    caption = db.Column(db.String(200), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    status = db.Column(db.String(20), default="pending")  # 'pending', 'approved'
    reviewed_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)


class BarangayInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    barangay_name = db.Column(db.String(100), unique=True, nullable=False)
    history = db.Column(db.Text, nullable=True)
    cultural_assets = db.Column(db.Text, nullable=True)
    traditions = db.Column(db.Text, nullable=True)
    local_practices = db.Column(db.Text, nullable=True)
    unique_features = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class PageView(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    view_type = db.Column(
        db.String(50), nullable=False
    )  # 'attraction', 'event', 'page'
    item_id = db.Column(
        db.Integer, nullable=True
    )  # ID of the attraction or event, if applicable
    page_name = db.Column(
        db.String(100), nullable=True
    )  # Name of the page (e.g., 'home', 'map', 'events')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, nullable=True)  # Optional, if logged in


class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    attraction_id = db.Column(
        db.Integer, db.ForeignKey("attraction.id"), nullable=False
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class EventInterest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)
    status = db.Column(db.String(20), default="interested")  # 'interested', 'going'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    attraction_id = db.Column(
        db.Integer, db.ForeignKey("attraction.id"), nullable=False
    )
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    status = db.Column(
        db.String(20), default="pending"
    )  # 'pending', 'approved', 'rejected'
    reviewed_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# === Heritage Models (Tourism Forms) ===
# Import heritage models to register them with SQLAlchemy
from heritage_models.natural_heritage import NaturalHeritage  # noqa: E402, F401
from heritage_models.intangible_heritage import IntangibleHeritage  # noqa: E402, F401
from heritage_models.personality_profile import PersonalityProfile  # noqa: E402, F401
from heritage_models.cultural_institution import CulturalInstitution  # noqa: E402, F401
from heritage_models.lgu_culture_program import LGUCultureProgram  # noqa: E402, F401
