"""
Natural Heritage model for Form 01A - Natural Resources and Land Formations.
Stores geological and physiographical heritage sites.
"""
from extensions import db
from datetime import datetime


class NaturalHeritage(db.Model):
    """Model for natural heritage sites (Form 01A)."""
    
    __tablename__ = 'natural_heritage'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Basic Information (Section I)
    name = db.Column(db.String(200), nullable=False, index=True)
    subcategory = db.Column(db.String(50), nullable=False)  # mountain, cave, valley, etc.
    location = db.Column(db.String(200), nullable=False)
    area_hectares = db.Column(db.Float, nullable=True)
    ownership = db.Column(db.String(200), nullable=True)  # Ownership/jurisdiction
    
    # Geographic coordinates (for mapping integration)
    lat = db.Column(db.Float, nullable=True)
    lng = db.Column(db.Float, nullable=True)
    
    # Description (Section II)
    description = db.Column(db.Text, nullable=True)  # Physical features
    
    # Stories (Section III)
    stories = db.Column(db.Text, nullable=True)  # Associated stories/legends
    
    # Significance (Section IV)
    significance = db.Column(db.Text, nullable=True)  # Type and explanation
    
    # Conservation (Section V)
    protection_status = db.Column(db.String(100), nullable=True)
    constraints_threats = db.Column(db.Text, nullable=True)
    conservation_measures = db.Column(db.Text, nullable=True)
    
    # References (Section VI)
    key_informants = db.Column(db.JSON, nullable=True)  # Array of informant details
    references = db.Column(db.Text, nullable=True)
    
    # Metadata
    mapper_name = db.Column(db.String(200), nullable=True)
    date_profiled = db.Column(db.Date, nullable=True)
    photo_url = db.Column(db.String(500), nullable=True)
    
    # Approval Workflow
    status = db.Column(db.String(20), default='pending', index=True)  # pending/approved/rejected
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True, index=True)
    reviewed_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<NaturalHeritage {self.name}>'
