from extensions import db
from datetime import datetime


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
    reviews = db.relationship('Review', backref='establishment', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert Establishment to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'description': self.description,
            'address': self.address,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'barangay_id': self.barangay_id,
            'barangay_name': self.barangay.name if self.barangay else None,
            'contact_number': self.contact_number,
            'email': self.email,
            'website': self.website,
            'operating_hours': self.operating_hours,
            'price_range': self.price_range,
            'amenities': self.amenities,
            'cover_image_url': self.cover_image_url,
            'logo_url': self.logo_url,
            'status': self.status,
            'is_featured': self.is_featured,
            'rating_avg': self.rating_avg,
            'review_count': self.review_count,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


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






class BusinessVerification(db.Model):
    __tablename__ = 'BUSINESS_VERIFICATION'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("USER.id"), nullable=False, index=True)
    permit_document_url = db.Column(db.String(500), nullable=False)
    other_document_url = db.Column(db.String(500), nullable=True)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship("User", backref=db.backref("business_verification", uselist=False))

# Backward Compatibility Shims
from modules.attractions.models import Review, UserFavorite
EstablishmentReview = Review
UserFavoriteEstablishment = UserFavorite

