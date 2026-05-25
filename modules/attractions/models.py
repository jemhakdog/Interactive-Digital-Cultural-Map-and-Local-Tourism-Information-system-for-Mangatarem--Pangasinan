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
    physical_status = db.Column(db.String(50), default="Open Public", nullable=True)
    is_verified = db.Column(db.Boolean, default=True, nullable=True)
    
    # Practical Details
    opening_hours = db.Column(db.String(100), nullable=True)
    entrance_fee = db.Column(db.String(100), nullable=True)
    contact_info = db.Column(db.String(100), nullable=True)
    facilities = db.Column(db.Text, nullable=True)
    
    # Safety and Environmental Advisories
    advisory_message = db.Column(db.Text, nullable=True)
    advisory_status = db.Column(db.String(20), nullable=True, default="Normal")
    
    # Linked to User (steward) who manages this attraction
    user_id = db.Column(db.Integer, db.ForeignKey("USER.id"), nullable=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    user = db.relationship('User', foreign_keys=[user_id], backref='attractions')
    
    @property
    def rating(self):
        """Calculate the average rating of approved reviews."""
        approved_reviews = self.reviews.filter_by(
            status="approved", 
            parent_id=None
        ).all()
        if not approved_reviews:
            return None
        ratings = [r.rating for r in approved_reviews if r.rating is not None]
        if not ratings:
            return None
        return round(sum(ratings) / len(ratings), 1)

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
            'physical_status': self.physical_status,
            'is_verified': self.is_verified,
            'opening_hours': self.opening_hours,
            'entrance_fee': self.entrance_fee,
            'contact_info': self.contact_info,
            'facilities': self.facilities,
            'advisory_message': self.advisory_message,
            'advisory_status': self.advisory_status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'osm_alternatives': self.osm_alternatives
        }


class Review(db.Model):
    __tablename__ = 'REVIEW'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("USER.id"), nullable=False, index=True)
    
    # Nullable explicit foreign keys
    attraction_id = db.Column(db.Integer, db.ForeignKey("ATTRACTION.id", ondelete='CASCADE'), nullable=True, index=True)
    establishment_id = db.Column(db.Integer, db.ForeignKey("ESTABLISHMENT.id", ondelete='CASCADE'), nullable=True, index=True)
    
    rating = db.Column(db.Integer, nullable=True)  # rating is now nullable for replies
    comment = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default="pending", index=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('REVIEW.id', ondelete='CASCADE'), nullable=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('reviews', lazy='dynamic'))
    attraction = db.relationship('Attraction', backref=db.backref('reviews', lazy='dynamic'))
    
    photos = db.relationship('ReviewPhoto', backref='review', lazy='dynamic', cascade='all, delete-orphan')

    # Self-referential relationship for nested comment replies
    replies = db.relationship(
        'Review',
        backref=db.backref('parent', remote_side=[id]),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    __table_args__ = (
        db.CheckConstraint(
            '(attraction_id IS NOT NULL AND establishment_id IS NULL) OR '
            '(attraction_id IS NULL AND establishment_id IS NOT NULL)',
            name='ck_review_target'
        ),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.user.username if self.user else 'Visitor',
            'attraction_id': self.attraction_id,
            'establishment_id': self.establishment_id,
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
    review_id = db.Column(db.Integer, db.ForeignKey('REVIEW.id', ondelete='CASCADE'), nullable=False, index=True)
    url = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'url': self.url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class UserFavorite(db.Model):
    __tablename__ = 'USER_FAVORITE'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("USER.id"), nullable=False, index=True)
    
    # Nullable explicit foreign keys
    attraction_id = db.Column(db.Integer, db.ForeignKey("ATTRACTION.id", ondelete='CASCADE'), nullable=True, index=True)
    establishment_id = db.Column(db.Integer, db.ForeignKey("ESTABLISHMENT.id", ondelete='CASCADE'), nullable=True, index=True)
    event_id = db.Column(db.Integer, db.ForeignKey("EVENT.id", ondelete='CASCADE'), nullable=True, index=True)
    
    status = db.Column(db.String(20), default="favorite", index=True) # e.g. 'favorite' or 'interested'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship('User', backref=db.backref('favorites', lazy='dynamic'))

    __table_args__ = (
        db.CheckConstraint(
            '(attraction_id IS NOT NULL AND establishment_id IS NULL AND event_id IS NULL) OR '
            '(attraction_id IS NULL AND establishment_id IS NOT NULL AND event_id IS NULL) OR '
            '(attraction_id IS NULL AND establishment_id IS NULL AND event_id IS NOT NULL)',
            name='ck_favorite_target'
        ),
    )

class MapFeedback(db.Model):
    """Anonymous or logged-in feedback submitted directly from the map."""
    __tablename__ = 'MAP_FEEDBACK'
    id = db.Column(db.Integer, primary_key=True)
    attraction_id = db.Column(db.Integer, db.ForeignKey("ATTRACTION.id"), nullable=True)
    feedback_type = db.Column(db.String(50), nullable=False) # 'review', 'correction', 'safety'
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="pending") # pending, resolved, dismissed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    attraction = db.relationship('Attraction', backref='map_feedbacks')

# Backward Compatibility Shims
AttractionReview = Review
UserFavoriteAttraction = UserFavorite
