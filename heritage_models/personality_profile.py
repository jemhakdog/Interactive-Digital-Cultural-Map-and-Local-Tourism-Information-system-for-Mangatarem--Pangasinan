"""
Personality Profile model for Form 05 - Significant Personalities.
Stores information about notable individuals in arts, science, politics, etc.
"""
from extensions import db


class PersonalityProfile(db.Model):
    """Detail model for significant personalities (Form 05)."""
    
    __tablename__ = 'personality_details'
    
    # Linked to HeritageProfile
    profile_id = db.Column(db.Integer, db.ForeignKey('heritage_profile.id'), primary_key=True)
    profile = db.relationship('HeritageProfile', backref=db.backref('personality_details', uselist=False))
    
    # Unique Fields (Section I & II)
    date_of_birth = db.Column(db.Date, nullable=True)
    date_of_death = db.Column(db.Date, nullable=True)
    birth_place = db.Column(db.String(200), nullable=True)
    present_address = db.Column(db.String(300), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    prominence_field = db.Column(db.String(100), nullable=True)
    biography = db.Column(db.Text, nullable=True)
    works_achievements = db.Column(db.JSON, nullable=True)
    
    def __repr__(self):
        return f'<PersonalityProfile Detail for Profile {self.profile_id}>'
