from extensions import db
from datetime import datetime


class BarangayInfo(db.Model):
    __tablename__ = 'BARANGAY_INFO'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False) # Renamed from barangay_name
    
    # Narrative Fields
    mission = db.Column(db.Text, nullable=True)
    vision = db.Column(db.Text, nullable=True)
    history = db.Column(db.Text, nullable=True)
    cultural_assets = db.Column(db.Text, nullable=True)
    traditions = db.Column(db.Text, nullable=True)
    local_practices = db.Column(db.Text, nullable=True)
    unique_features = db.Column(db.Text, nullable=True)
    
    # Metadata
    user_id = db.Column(db.Integer, db.ForeignKey('USER.id'), nullable=True)
    
    # Relationships
    manager = db.relationship('User', foreign_keys=[user_id], backref='managed_barangay_info')
    
    map_geo_json = db.Column(db.JSON, nullable=True) # Renamed from cultural_assets/etc to match ERD
    location_data = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
