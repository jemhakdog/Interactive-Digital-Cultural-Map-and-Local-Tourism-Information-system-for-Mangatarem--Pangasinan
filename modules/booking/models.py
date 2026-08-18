from extensions import db
from datetime import datetime
import uuid

class BookableAsset(db.Model):
    """
    Defines the booking configuration for an Attraction or Heritage Profile.
    """
    __tablename__ = 'BOOKABLE_ASSET'
    
    id = db.Column(db.Integer, primary_key=True)
    # Polymorphic associations. One of these will be set.
    attraction_id = db.Column(db.Integer, db.ForeignKey('ATTRACTION.id', ondelete='CASCADE'), nullable=True, index=True)
    heritage_profile_id = db.Column(db.Integer, db.ForeignKey('HERITAGE_PROFILE.id', ondelete='CASCADE'), nullable=True, index=True)
    
    # Booking Settings
    daily_capacity = db.Column(db.Integer, default=50) # Total visitors allowed per day
    requires_approval = db.Column(db.Boolean, default=True) # Manual review vs auto-approve
    booking_instructions = db.Column(db.Text, nullable=True) # E.g. "Please bring valid ID"
    status = db.Column(db.String(20), default='active') # active, inactive
    
    # Audit
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    attraction = db.relationship('Attraction', backref=db.backref('bookable_asset', uselist=False, cascade='all, delete-orphan'))
    heritage_profile = db.relationship('HeritageProfile', backref=db.backref('bookable_asset', uselist=False, cascade='all, delete-orphan'))
    
    def to_dict(self):
        return {
            'id': self.id,
            'attraction_id': self.attraction_id,
            'heritage_profile_id': self.heritage_profile_id,
            'daily_capacity': self.daily_capacity,
            'requires_approval': self.requires_approval,
            'booking_instructions': self.booking_instructions,
            'status': self.status
        }


class BookingSlot(db.Model):
    """
    Tracks availability and bookings for a specific date.
    """
    __tablename__ = 'BOOKING_SLOT'
    
    id = db.Column(db.Integer, primary_key=True)
    bookable_asset_id = db.Column(db.Integer, db.ForeignKey('BOOKABLE_ASSET.id', ondelete='CASCADE'), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False, index=True)
    total_capacity = db.Column(db.Integer, nullable=False) # Copied from BookableAsset at time of creation, can be overridden
    booked_count = db.Column(db.Integer, default=0) # Sum of party_size for all non-cancelled reservations
    
    bookable_asset = db.relationship('BookableAsset', backref=db.backref('slots', lazy='dynamic', cascade='all, delete-orphan'))
    
    # Ensure one slot per asset per date
    __table_args__ = (
        db.UniqueConstraint('bookable_asset_id', 'date', name='uq_asset_date'),
    )
    
    @property
    def available_capacity(self):
        return max(0, self.total_capacity - self.booked_count)
        
    def to_dict(self):
        return {
            'id': self.id,
            'bookable_asset_id': self.bookable_asset_id,
            'date': self.date.isoformat(),
            'total_capacity': self.total_capacity,
            'booked_count': self.booked_count,
            'available_capacity': self.available_capacity
        }


def generate_qr_token():
    return uuid.uuid4().hex[:12].upper()

class Reservation(db.Model):
    """
    A booking made by a user.
    """
    __tablename__ = 'RESERVATION'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('USER.id'), nullable=False, index=True)
    booking_slot_id = db.Column(db.Integer, db.ForeignKey('BOOKING_SLOT.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Booking Details
    party_size = db.Column(db.Integer, default=1, nullable=False)
    primary_contact = db.Column(db.String(100), nullable=True) # Phone or email
    special_requests = db.Column(db.Text, nullable=True)
    
    # Status: 'pending', 'confirmed', 'cancelled', 'attended', 'no-show'
    status = db.Column(db.String(20), default='pending', index=True)
    
    # Security/Check-in
    qr_code_token = db.Column(db.String(20), unique=True, default=generate_qr_token, index=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('reservations', lazy='dynamic'))
    slot = db.relationship('BookingSlot', backref=db.backref('reservations', lazy='dynamic'))
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'booking_slot_id', name='uq_user_slot'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.user.username if self.user else 'Unknown',
            'booking_slot_id': self.booking_slot_id,
            'date': self.slot.date.isoformat() if self.slot else None,
            'party_size': self.party_size,
            'status': self.status,
            'qr_code_token': self.qr_code_token,
            'created_at': self.created_at.isoformat()
        }
