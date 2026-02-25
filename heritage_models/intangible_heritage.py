"""
Intangible Heritage model for Form 04A - Oral Traditions and Expressions.
Stores cultural practices, performances, and traditional knowledge.
"""
from extensions import db


class IntangibleHeritage(db.Model):
    """Detail model for intangible cultural heritage (Form 04A)."""
    
    __tablename__ = 'intangible_heritage_details'
    
    # Linked to HeritageProfile
    profile_id = db.Column(db.Integer, db.ForeignKey('heritage_profile.id'), primary_key=True)
    profile = db.relationship('HeritageProfile', backref=db.backref('intangible_details', uselist=False))
    
    # Unique Fields
    heritage_type = db.Column(db.String(50), nullable=True)  # oral_tradition, performing_arts, etc.
    geographical_range = db.Column(db.Text, nullable=True)
    related_domains = db.Column(db.JSON, nullable=True)
    culture_bearers = db.Column(db.Text, nullable=True)
    culture_bearer_photos = db.Column(db.JSON, nullable=True)
    transmission_mode = db.Column(db.Text, nullable=True)
    objects_used = db.Column(db.JSON, nullable=True)
    flora_fauna_used = db.Column(db.JSON, nullable=True)
    safeguarding_measures = db.Column(db.JSON, nullable=True)
    supporting_docs = db.Column(db.JSON, nullable=True)
    
    def __repr__(self):
        return f'<IntangibleHeritage Detail for Profile {self.profile_id}>'
