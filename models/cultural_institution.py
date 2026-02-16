"""
Cultural Institution model for Form 06 - Cultural Institutions.
Stores information about libraries, museums, schools, and other cultural organizations.
"""
from extensions import db
from datetime import datetime


class CulturalInstitution(db.Model):
    """Model for cultural institutions (Form 06)."""
    
    __tablename__ = 'cultural_institution'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Basic Information (Section I)
    name = db.Column(db.String(200), nullable=False, index=True)
    municipality = db.Column(db.String(100), nullable=False)
    province = db.Column(db.String(100), nullable=False)
    location_address = db.Column(db.String(300), nullable=True)
    
    # Geographic coordinates (for mapping)
    lat = db.Column(db.Float, nullable=True)
    lng = db.Column(db.Float, nullable=True)
    
    # Photos
    facade_photo_url = db.Column(db.String(500), nullable=True)  # Building facade
    logo_url = db.Column(db.String(500), nullable=True)
    logo_description = db.Column(db.Text, nullable=True)  # Symbol meanings
    
    # Institution Type
    institution_type = db.Column(db.String(100), nullable=False)  # library, museum, school, etc.
    
    # Description (Section II)
    mandate_description = db.Column(db.Text, nullable=True)  # History, officials, contact
    milestones = db.Column(db.Text, nullable=True)
    
    # Stories (Section III)
    stories = db.Column(db.Text, nullable=True)
    
    # Significance (Section IV)
    significance = db.Column(db.Text, nullable=True)
    
    # Assessment (Section V)
    condition_status = db.Column(db.Text, nullable=True)
    constraints_threats = db.Column(db.Text, nullable=True)
    safeguarding_measures = db.Column(db.Text, nullable=True)
    
    # References (Section VI)
    supporting_docs = db.Column(db.JSON, nullable=True)  # photos, audio, writeups
    key_informants = db.Column(db.JSON, nullable=True)
    references = db.Column(db.Text, nullable=True)
    
    # Metadata
    mapper_name = db.Column(db.String(200), nullable=True)
    date_profiled = db.Column(db.Date, nullable=True)
    
    # Approval Workflow
    status = db.Column(db.String(20), default='pending', index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True, index=True)
    reviewed_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<CulturalInstitution {self.name}>'
