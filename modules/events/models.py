from extensions import db
from datetime import datetime


class Event(db.Model):
    __tablename__ = 'EVENT'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False) # Renamed from title to match ERD
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, index=True)
    location = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float, nullable=True) # Added for PGIS Harmonization
    longitude = db.Column(db.Float, nullable=True) # Added for PGIS Harmonization
    barangay_id = db.Column(db.Integer, db.ForeignKey('BARANGAY_INFO.id'), nullable=True, index=True)
    image_url = db.Column(db.String(500), nullable=True)
    
    barangay = db.relationship('BarangayInfo', backref='events')
    
    category = db.Column(db.String(50), nullable=False, default="Civic", index=True)
    status = db.Column(db.String(20), default="pending", index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("USER.id"), nullable=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    user = db.relationship('User', foreign_keys=[user_id], backref='events')
    
    def to_dict(self):
        """Convert Event to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'date': self.date.isoformat() if self.date else None,
            'location': self.location,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'barangay_id': self.barangay_id,
            'barangay_name': self.barangay.name if self.barangay else None,
            'image_url': self.image_url,
            'category': self.category,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# Backward Compatibility Shims
from modules.attractions.models import UserFavorite
UserEventInterest = UserFavorite



