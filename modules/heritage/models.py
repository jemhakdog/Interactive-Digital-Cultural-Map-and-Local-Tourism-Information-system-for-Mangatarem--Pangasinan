from extensions import db
from datetime import datetime


class HeritageProfile(db.Model):
    """Base model for all cultural heritage and tourism forms."""
    __tablename__ = 'HERITAGE_PROFILE'
    
    id = db.Column(db.Integer, primary_key=True)
    asset_type = db.Column(db.String(50), nullable=False, index=True) # 'built', 'natural', etc.
    form_control_number = db.Column(db.String(100), unique=True, nullable=True) # Link to manual form
    form_data = db.Column(db.JSON, nullable=True) # Unified JSON storage for specific form fields
    
    # ERD Fields
    name_of_asset = db.Column(db.String(200), nullable=True)
    common_name = db.Column(db.String(200), nullable=True)
    barangay_id = db.Column(db.Integer, db.ForeignKey('BARANGAY_INFO.id'), nullable=True, index=True)
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
    template_slug = db.Column(db.String(100), nullable=True, index=True) # Tracks which form template was used
    mapper_name = db.Column(db.String(200), nullable=True)
    date_profiled = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(20), default='pending', index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("USER.id"), nullable=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    barangay = db.relationship('BarangayInfo', backref='profiles')
    user = db.relationship('User', foreign_keys=[user_id], backref='profiles')
