"""
Personality Profile model for Form 05 - Significant Personalities.
Stores information about notable individuals in arts, science, politics, etc.
"""
from extensions import db
from datetime import datetime


class PersonalityProfile(db.Model):
    """Model for significant personalities (Form 05)."""
    
    __tablename__ = 'personality_profile'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Basic Information (Section I)
    name = db.Column(db.String(200), nullable=False, index=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    date_of_death = db.Column(db.Date, nullable=True)
    birth_place = db.Column(db.String(200), nullable=True)
    present_address = db.Column(db.String(300), nullable=True)  # If living
    age = db.Column(db.Integer, nullable=True)
    prominence_field = db.Column(db.String(100), nullable=False)  # Arts, Science, Politics, etc.
    photo_url = db.Column(db.String(500), nullable=True)
    
    # Biography (Section II)
    biography = db.Column(db.Text, nullable=True)  # Life story, awards, contributions
    
    # Significance (Section III)
    significance = db.Column(db.Text, nullable=True)  # Type and explanation
    
    # References (Section IV)
    works_achievements = db.Column(db.JSON, nullable=True)  # Array of works/achievements
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
        return f'<PersonalityProfile {self.name}>'
