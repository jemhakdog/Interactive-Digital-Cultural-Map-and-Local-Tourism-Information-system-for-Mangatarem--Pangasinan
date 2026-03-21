"""
Intangible Heritage model for Form 04A - Oral Traditions and Expressions.
Stores cultural practices, performances, and traditional knowledge.
"""
from extensions import db


__all__ = ['IntangibleHeritage', 'INTANGIBLE_HERITAGE_DETAIL']


class IntangibleHeritage(db.Model):
    """Detail model for intangible cultural heritage (Form 04A)."""
    
    __tablename__ = 'INTANGIBLE_HERITAGE_DETAIL'
    
    # Linked to HeritageProfile
    heritage_profile_id = db.Column(db.Integer, db.ForeignKey('HERITAGE_PROFILE.id'), primary_key=True)
    profile = db.relationship('HeritageProfile', backref=db.backref('intangible_details', uselist=False))
    
    # ERD Fields
    category = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    practitioners = db.Column(db.Text, nullable=True)
    transmission_mode = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<IntangibleHeritage Detail for Profile {self.heritage_profile_id}>'


# Alias for registry imports
INTANGIBLE_HERITAGE_DETAIL = IntangibleHeritage
