"""
Personality Profile model for Form 05 - Significant Personalities.
Stores information about notable individuals in arts, science, politics, etc.
"""
from extensions import db


__all__ = ['PersonalityProfile', 'PERSONALITY_DETAIL']


class PersonalityProfile(db.Model):
    """Detail model for significant personalities (Form 05)."""
    
    __tablename__ = 'PERSONALITY_DETAIL'
    
    # Linked to HeritageProfile
    heritage_profile_id = db.Column(db.Integer, db.ForeignKey('HERITAGE_PROFILE.id'), primary_key=True)
    profile = db.relationship('HeritageProfile', backref=db.backref('personality_details', uselist=False))
    
    # ERD Fields
    full_name = db.Column(db.String(200), nullable=True)
    dates_of_birth_death = db.Column(db.String(100), nullable=True)
    place_of_birth = db.Column(db.String(200), nullable=True)
    major_achievements = db.Column(db.Text, nullable=True)
    meta_data = db.Column(db.JSON, nullable=True) # For template-specific fields
    
    def __repr__(self):
        return f'<PersonalityProfile Detail for Profile {self.heritage_profile_id}>'


# Alias for registry imports
PERSONALITY_DETAIL = PersonalityProfile
