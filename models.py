from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import secrets


class User(UserMixin, db.Model):
    __tablename__ = 'USER'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False) # Renamed from password_hash to match ERD
    role = db.Column(db.String(20), default="user")  # 'admin', 'contributor', or 'user'
    barangay_id = db.Column(db.Integer, db.ForeignKey('BARANGAY_INFO.id'), nullable=True) # Renamed from barangay to match ERD
    is_approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    barangay = db.relationship('BarangayInfo', backref='users')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class PasswordResetToken(db.Model):
    """Single-use, time-limited tokens for password reset."""
    __tablename__ = "PASSWORD_RESET_TOKEN"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("USER.id"), nullable=False, index=True)
    token = db.Column(db.String(128), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("reset_tokens", lazy=True))

    @classmethod
    def create_for_user(cls, user, expiry_minutes: int = 30) -> "PasswordResetToken":
        """Generate a new token for the given user."""
        token = cls(
            user_id=user.id,
            token=secrets.token_hex(32),
            expires_at=datetime.utcnow() + timedelta(minutes=expiry_minutes),
        )
        db.session.add(token)
        db.session.commit()
        return token

    @property
    def is_valid(self) -> bool:
        """True if token is unused and not expired."""
        from datetime import timezone
        
        expires = self.expires_at
        if expires.tzinfo is not None:
            # Normalize aware database datetime to naive UTC for comparison
            expires = expires.astimezone(timezone.utc).replace(tzinfo=None)
            
        return not self.used and datetime.utcnow() < expires


class HeritageProfile(db.Model):
    """Base model for all cultural heritage and tourism forms."""
    __tablename__ = 'HERITAGE_PROFILE'
    
    id = db.Column(db.Integer, primary_key=True)
    asset_type = db.Column(db.String(50), nullable=False) # 'built', 'natural', etc.
    form_control_number = db.Column(db.String(100), unique=True, nullable=True) # Link to manual form
    
    # ERD Fields
    name_of_asset = db.Column(db.String(200), nullable=True)
    common_name = db.Column(db.String(200), nullable=True)
    barangay_id = db.Column(db.Integer, db.ForeignKey('BARANGAY_INFO.id'), nullable=True)
    location_details = db.Column(db.Text, nullable=True)
    contact_person = db.Column(db.String(200), nullable=True)
    contact_number = db.Column(db.String(50), nullable=True)
    ownership_type = db.Column(db.String(50), nullable=True)
    owner_administrator = db.Column(db.String(200), nullable=True)
    usage_status = db.Column(db.String(50), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    
    # Shared Documentation
    significance = db.Column(db.Text, nullable=True)
    conservation_status = db.Column(db.Text, nullable=True)
    
    # Meta
    mapper_name = db.Column(db.String(200), nullable=True)
    date_profiled = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(20), default='pending', index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("USER.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    barangay = db.relationship('BarangayInfo', backref='profiles')
    user = db.relationship('User', foreign_keys=[user_id], backref='profiles')


class Attraction(db.Model):
    __tablename__ = 'ATTRACTION'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False, index=True) 
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    
    barangay_id = db.Column(db.Integer, db.ForeignKey('BARANGAY_INFO.id'), nullable=True)
    heritage_profile_id = db.Column(db.Integer, db.ForeignKey("HERITAGE_PROFILE.id"), nullable=True)
    
    barangay = db.relationship('BarangayInfo', backref='attractions')
    
    status = db.Column(db.String(20), default="pending", index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("USER.id"), nullable=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)


class Event(db.Model):
    __tablename__ = 'EVENT'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False) # Renamed from title to match ERD
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    barangay_id = db.Column(db.Integer, db.ForeignKey('BARANGAY_INFO.id'), nullable=True)
    image_url = db.Column(db.String(500), nullable=True)
    
    barangay = db.relationship('BarangayInfo', backref='events')
    
    category = db.Column(db.String(50), nullable=False, default="Civic")
    status = db.Column(db.String(20), default="pending")
    user_id = db.Column(db.Integer, db.ForeignKey("USER.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class GalleryItem(db.Model):
    __tablename__ = 'GALLERY_ITEM'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)  # 'photo' or 'video'
    url = db.Column(db.String(500), nullable=False)
    caption = db.Column(db.Text, nullable=True) # Changed from String(200) to Text
    user_id = db.Column(db.Integer, db.ForeignKey("USER.id"), nullable=True)
    status = db.Column(db.String(20), default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow) # Renamed from uploaded_at


class BarangayInfo(db.Model):
    __tablename__ = 'BARANGAY_INFO'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False) # Renamed from barangay_name
    map_geo_json = db.Column(db.JSON, nullable=True) # Renamed from cultural_assets/etc to match ERD
    location_data = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class AnalyticsPageView(db.Model):
    __tablename__ = 'ANALYTICS_PAGE_VIEW'
    id = db.Column(db.Integer, primary_key=True)
    page_url = db.Column(db.String(500), nullable=True) # Kept for compatibility
    view_type = db.Column(db.String(50), nullable=True)  # 'attraction', 'event', 'page'
    item_id = db.Column(db.Integer, nullable=True)       # ID of the attraction or event, if applicable
    page_name = db.Column(db.String(100), nullable=True) # Name of the page (e.g., 'home', 'map', 'events')
    user_id = db.Column(db.Integer, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    session_id = db.Column(db.String(100), nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    device_info = db.Column(db.Text, nullable=True)


class UserFavoriteAttraction(db.Model):
    __tablename__ = 'USER_FAVORITE_ATTRACTION'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("USER.id"), nullable=False)
    attraction_id = db.Column(db.Integer, db.ForeignKey("ATTRACTION.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class UserEventInterest(db.Model):
    __tablename__ = 'USER_EVENT_INTEREST'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("USER.id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("EVENT.id"), nullable=False)
    status = db.Column(db.String(20), default="interested")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class AttractionReview(db.Model):
    __tablename__ = 'ATTRACTION_REVIEW'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("USER.id"), nullable=False)
    attraction_id = db.Column(db.Integer, db.ForeignKey("ATTRACTION.id"), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class NewsletterSubscriber(db.Model):
    __tablename__ = 'NEWSLETTER_SUBSCRIBER'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<NewsletterSubscriber {self.email}>'


# === Business Portal Models (Establishments) ===

class Establishment(db.Model):
    """Business listing for accommodations and dining establishments."""
    __tablename__ = 'ESTABLISHMENT'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    type = db.Column(db.String(30), nullable=False, index=True)  # 'inn', 'restaurant', 'cafe', 'fastfood'
    description = db.Column(db.Text, nullable=True)
    address = db.Column(db.String(500), nullable=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    barangay_id = db.Column(db.Integer, db.ForeignKey('BARANGAY_INFO.id'), nullable=True)
    contact_number = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    website = db.Column(db.String(300), nullable=True)
    operating_hours = db.Column(db.JSON, nullable=True)
    price_range = db.Column(db.String(20), nullable=True)  # 'budget', 'moderate', 'premium'
    amenities = db.Column(db.JSON, nullable=True)
    cover_image_url = db.Column(db.String(500), nullable=True)
    logo_url = db.Column(db.String(500), nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('USER.id'), nullable=False, index=True)
    status = db.Column(db.String(20), default='pending', index=True)
    is_featured = db.Column(db.Boolean, default=False)
    rating_avg = db.Column(db.Float, default=0)
    review_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    barangay = db.relationship('BarangayInfo', backref='establishments')
    owner = db.relationship('User', backref=db.backref('establishments', lazy=True))
    rooms = db.relationship('EstablishmentRoom', backref='establishment', lazy=True, cascade='all, delete-orphan')
    menu_items = db.relationship('EstablishmentMenuItem', backref='establishment', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('EstablishmentReview', backref='establishment', lazy=True, cascade='all, delete-orphan')


class EstablishmentRoom(db.Model):
    """Room listing for inn/hotel establishments."""
    __tablename__ = 'ESTABLISHMENT_ROOM'

    id = db.Column(db.Integer, primary_key=True)
    establishment_id = db.Column(db.Integer, db.ForeignKey('ESTABLISHMENT.id', ondelete='CASCADE'), nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price_per_night = db.Column(db.Float, nullable=True)
    capacity = db.Column(db.Integer, default=2)
    amenities = db.Column(db.JSON, nullable=True)
    image_urls = db.Column(db.JSON, nullable=True)
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class EstablishmentMenuItem(db.Model):
    """Menu item for restaurant/cafe establishments."""
    __tablename__ = 'ESTABLISHMENT_MENU_ITEM'

    id = db.Column(db.Integer, primary_key=True)
    establishment_id = db.Column(db.Integer, db.ForeignKey('ESTABLISHMENT.id', ondelete='CASCADE'), nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=True)
    category = db.Column(db.String(50), nullable=True)  # 'appetizer', 'main', 'dessert', 'drinks', 'snacks'
    image_url = db.Column(db.String(500), nullable=True)
    is_available = db.Column(db.Boolean, default=True)
    is_bestseller = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class EstablishmentReview(db.Model):
    """User review for an establishment."""
    __tablename__ = 'ESTABLISHMENT_REVIEW'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('USER.id'), nullable=False, index=True)
    establishment_id = db.Column(db.Integer, db.ForeignKey('ESTABLISHMENT.id', ondelete='CASCADE'), nullable=False, index=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('establishment_reviews', lazy=True))


# === Heritage Models (Tourism Forms) ===

# Import heritage models to register them with SQLAlchemy
# === Heritage Models (Tourism Forms - Detail Tables) ===
from heritage_models.natural_heritage import NaturalHeritage  # Form 01A
from heritage_models.built_heritage import BuiltHeritage      # Form 02A
from heritage_models.movable_heritage import MovableHeritage  # Form 03A
from heritage_models.intangible_heritage import IntangibleHeritage  # Form 04A
from heritage_models.personality_profile import PersonalityProfile  # Form 05
from heritage_models.cultural_institution import CulturalInstitution  # Form 06
from heritage_models.lgu_culture_program import LGUCultureProgram  # Form 07
