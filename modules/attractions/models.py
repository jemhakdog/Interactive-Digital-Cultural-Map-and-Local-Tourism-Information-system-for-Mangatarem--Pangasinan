from extensions import db
from datetime import datetime


class Attraction(db.Model):
    __tablename__ = 'ATTRACTION'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False, index=True) 
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    
    barangay_id = db.Column(db.Integer, db.ForeignKey('BARANGAY_INFO.id'), nullable=True, index=True)
    heritage_profile_id = db.Column(db.Integer, db.ForeignKey("HERITAGE_PROFILE.id"), nullable=True)
    
    barangay = db.relationship('BarangayInfo', backref='attractions')
    
    status = db.Column(db.String(20), default="pending", index=True)
    is_featured = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("USER.id"), nullable=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    user = db.relationship('User', foreign_keys=[user_id], backref='attractions')
    
    def to_dict(self):
        """Convert Attraction to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'image_url': self.image_url,
            'barangay_id': self.barangay_id,
            'barangay_name': self.barangay.name if self.barangay else None,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class AttractionReview(db.Model):
    __tablename__ = 'ATTRACTION_REVIEW'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("USER.id"), nullable=False)
    attraction_id = db.Column(db.Integer, db.ForeignKey("ATTRACTION.id"), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class UserFavoriteAttraction(db.Model):
    __tablename__ = 'USER_FAVORITE_ATTRACTION'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("USER.id"), nullable=False)
    attraction_id = db.Column(db.Integer, db.ForeignKey("ATTRACTION.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
