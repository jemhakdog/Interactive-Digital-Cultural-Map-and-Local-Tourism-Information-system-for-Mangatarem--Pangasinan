"""
Intangible Heritage model for Form 04A - Oral Traditions and Expressions.
Stores cultural practices, performances, and traditional knowledge.
"""
from extensions import db
from datetime import datetime


class IntangibleHeritage(db.Model):
    """Model for intangible cultural heritage (Form 04A)."""
    
    __tablename__ = 'intangible_heritage'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Basic Information (Section I)
    name = db.Column(db.String(200), nullable=False, index=True)
    type = db.Column(db.String(50), nullable=False)  # proverbs, songs, myths, chants, etc.
    photo_url = db.Column(db.String(500), nullable=True)
    geographical_range = db.Column(db.Text, nullable=True)  # Textual description of where practiced
    related_domains = db.Column(db.JSON, nullable=True)  # Array: performing arts, rituals, etc.
    
    # Description (Section II)
    description = db.Column(db.Text, nullable=True)  # History, processes, beliefs, settings
    
    # Culture Bearers (Section II.B)
    culture_bearers = db.Column(db.Text, nullable=True)  # Description of practitioners
    culture_bearer_photos = db.Column(db.JSON, nullable=True)  # Array of photo URLs
    
    # Transmission (Section II.C)
    transmission_mode = db.Column(db.Text, nullable=True)  # How knowledge is passed on
    
    # Associated Objects and Resources (Section II.D & E)
    objects_used = db.Column(db.JSON, nullable=True)  # Array of objects with details
    flora_fauna_used = db.Column(db.JSON, nullable=True)  # Array of flora/fauna with uses
    
    # Stories (Section III)
    stories_associated = db.Column(db.Text, nullable=True)
    
    # Significance (Section IV)
    significance = db.Column(db.Text, nullable=True)  # Type and explanation
    
    # Assessment (Section V)
    practice_status = db.Column(db.String(100), nullable=True)  # Current condition
    constraints_threats = db.Column(db.Text, nullable=True)
    safeguarding_measures = db.Column(db.JSON, nullable=True)  # Array of measure types
    safeguarding_description = db.Column(db.Text, nullable=True)
    
    # References (Section VI)
    supporting_docs = db.Column(db.JSON, nullable=True)  # audio, video, photos
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
        return f'<IntangibleHeritage {self.name}>'
