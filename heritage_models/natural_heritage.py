"""
Natural Heritage model for Form 01A - Natural Resources and Land Formations.
Stores geological and physiographical heritage sites.
"""
from extensions import db


__all__ = ['NaturalHeritage', 'NATURAL_HERITAGE_DETAIL']


class NaturalHeritage(db.Model):
    """Detail model for natural heritage sites (Form 01A)."""
    
    __tablename__ = 'NATURAL_HERITAGE_DETAIL'
    
    # Linked to HeritageProfile
    heritage_profile_id = db.Column(db.Integer, db.ForeignKey('HERITAGE_PROFILE.id'), primary_key=True)
    profile = db.relationship('HeritageProfile', backref=db.backref('natural_details', uselist=False))
    
    # ERD Fields
    type_of_natural_heritage = db.Column(db.String(100), nullable=True)
    area_size = db.Column(db.String(100), nullable=True)
    primary_features = db.Column(db.Text, nullable=True)
    biodiversity_significance = db.Column(db.Text, nullable=True)
    meta_data = db.Column(db.JSON, nullable=True) # For template-specific fields
    
    def __repr__(self):
        return f'<NaturalHeritage Detail for Profile {self.heritage_profile_id}>'


# Alias for registry imports
NATURAL_HERITAGE_DETAIL = NaturalHeritage
