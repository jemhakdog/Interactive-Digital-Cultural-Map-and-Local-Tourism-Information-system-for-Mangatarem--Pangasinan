"""
Natural Heritage model for Form 01A - Natural Resources and Land Formations.
Stores geological and physiographical heritage sites.
"""
from extensions import db


class NaturalHeritage(db.Model):
    """Detail model for natural heritage sites (Form 01A)."""
    
    __tablename__ = 'natural_heritage_details'
    
    # Linked to HeritageProfile
    profile_id = db.Column(db.Integer, db.ForeignKey('heritage_profile.id'), primary_key=True)
    profile = db.relationship('HeritageProfile', backref=db.backref('natural_details', uselist=False))
    
    # Unique Fields (Section I & V)
    subcategory = db.Column(db.String(50), nullable=True)  # mountain, cave, etc.
    area_hectares = db.Column(db.Float, nullable=True)
    ownership = db.Column(db.String(200), nullable=True)
    protection_status = db.Column(db.String(100), nullable=True)
    
    def __repr__(self):
        return f'<NaturalHeritage Detail for Profile {self.profile_id}>'
