"""
Models for the Gamification Module.
Defines achievements, badges, tourist check-in records, and dynamic LGU rewards/coupons.
"""

from extensions import db
from datetime import datetime

class AchievementBadge(db.Model):
    """Represents a collectable digital badge awarded for visiting heritage trails."""
    __tablename__ = 'ACHIEVEMENT_BADGE'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    badge_image_url = db.Column(db.String(500), nullable=False)
    required_visits = db.Column(db.Integer, default=1)
    
    # JSON containing the list of required spot/attraction IDs (e.g. [1, 5, 12])
    target_locations = db.Column(db.JSON, nullable=False)
    
    # Optional promo discount awarded on unlock (e.g., {"discount": "10% off tupig", "merchant_id": 3})
    reward_promo = db.Column(db.JSON, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "badge_image_url": self.badge_image_url,
            "required_visits": self.required_visits,
            "target_locations": self.target_locations,
            "reward_promo": self.reward_promo
        }


class UserPassport(db.Model):
    """Tracks tourist passport stamps, visited locations, and unlocked badges."""
    __tablename__ = 'USER_PASSPORT'
    __table_args__ = (
        db.UniqueConstraint('user_id', 'badge_id', name='uq_user_badge'),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('USER.id', ondelete='CASCADE'), nullable=False, index=True)
    badge_id = db.Column(db.Integer, db.ForeignKey('ACHIEVEMENT_BADGE.id', ondelete='CASCADE'), nullable=False, index=True)
    unlocked_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    # Relationships
    user = db.relationship('User', backref=db.backref('passports', lazy=True, cascade='all, delete-orphan'))
    badge = db.relationship('AchievementBadge', backref=db.backref('unlocks', lazy=True, cascade='all, delete-orphan'))


class TouristCheckIn(db.Model):
    """Stores GPS-verified QR-scan logs at heritage sites and merchants."""
    __tablename__ = 'TOURIST_CHECK_IN'
    __table_args__ = (
        db.UniqueConstraint('user_id', 'attraction_id', name='uq_user_attraction'),
        db.UniqueConstraint('user_id', 'establishment_id', name='uq_user_establishment'),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('USER.id', ondelete='CASCADE'), nullable=False, index=True)
    attraction_id = db.Column(db.Integer, db.ForeignKey('ATTRACTION.id', ondelete='SET NULL'), nullable=True, index=True)
    establishment_id = db.Column(db.Integer, db.ForeignKey('ESTABLISHMENT.id', ondelete='SET NULL'), nullable=True, index=True)
    
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    distance_meters = db.Column(db.Float, nullable=True) # Distance from target spot at time of scan
    
    verified_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    user = db.relationship('User', backref=db.backref('check_ins', lazy=True, cascade='all, delete-orphan'))
