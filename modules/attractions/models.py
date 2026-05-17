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
    directions = db.Column(db.Text, nullable=True)
    osm_alternatives = db.Column(db.JSON, nullable=True)
    
    barangay_id = db.Column(db.Integer, db.ForeignKey('BARANGAY_INFO.id'), nullable=True, index=True)
    heritage_profile_id = db.Column(db.Integer, db.ForeignKey("HERITAGE_PROFILE.id"), nullable=True)
    
    barangay = db.relationship('BarangayInfo', backref='attractions')
    
    status = db.Column(db.String(20), default="pending", index=True)
    is_featured = db.Column(db.Boolean, default=False)
    # Linked to User (steward) who manages this attraction
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
            'directions': self.directions,
            'barangay_id': self.barangay_id,
            'barangay_name': self.barangay.name if self.barangay else None,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'osm_alternatives': self.osm_alternatives
        }


class AttractionReview(db.Model):
    __tablename__ = 'ATTRACTION_REVIEW'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("USER.id"), nullable=False, index=True)
    attraction_id = db.Column(db.Integer, db.ForeignKey("ATTRACTION.id"), nullable=False, index=True)
    rating = db.Column(db.Integer, nullable=True)  # rating is now nullable for replies
    comment = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default="pending", index=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('ATTRACTION_REVIEW.id'), nullable=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('reviews', lazy='dynamic'))
    attraction = db.relationship('Attraction', backref=db.backref('reviews', lazy='dynamic'))
    photos = db.relationship('ReviewPhoto', backref='review', lazy='dynamic', cascade='all, delete-orphan')

    # Self-referential relationship for nested comment replies
    replies = db.relationship(
        'AttractionReview',
        backref=db.backref('parent', remote_side=[id]),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.user.username if self.user else 'Visitor',
            'attraction_id': self.attraction_id,
            'rating': self.rating,
            'comment': self.comment,
            'status': self.status,
            'parent_id': self.parent_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'photos': [p.to_dict() for p in self.photos.all()],
        }


class ReviewPhoto(db.Model):
    """Photos attached to a user review. No moderation — posted immediately."""
    __tablename__ = 'REVIEW_PHOTO'
    id = db.Column(db.Integer, primary_key=True)
    review_id = db.Column(db.Integer, db.ForeignKey('ATTRACTION_REVIEW.id'), nullable=False, index=True)
    url = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'url': self.url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class UserFavoriteAttraction(db.Model):
    __tablename__ = 'USER_FAVORITE_ATTRACTION'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("USER.id"), nullable=False)
    attraction_id = db.Column(db.Integer, db.ForeignKey("ATTRACTION.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
