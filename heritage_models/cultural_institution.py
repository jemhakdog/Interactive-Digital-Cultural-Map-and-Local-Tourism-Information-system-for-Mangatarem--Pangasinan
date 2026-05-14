"""
Cultural Institution model for Form 06 - Cultural Institutions.
Stores information about libraries, museums, schools, and other cultural organizations.
"""
from extensions import db


__all__ = ['CulturalInstitution', 'INSTITUTION_DETAIL']


class CulturalInstitution(db.Model):
    """Detail model for cultural institutions (Form 06)."""
    
    __tablename__ = 'INSTITUTION_DETAIL'
    
    # Linked to HeritageProfile
    heritage_profile_id = db.Column(db.Integer, db.ForeignKey('HERITAGE_PROFILE.id'), primary_key=True)
    profile = db.relationship('HeritageProfile', backref=db.backref('institution_details', uselist=False))
    
    # ERD Fields
    type_of_institution = db.Column(db.String(100), nullable=True)
    year_established = db.Column(db.Integer, nullable=True)
    head_of_institution = db.Column(db.String(200), nullable=True)
    activities_services = db.Column(db.Text, nullable=True)
    meta_data = db.Column(db.JSON, nullable=True) # For template-specific fields
    
    def __repr__(self):
        return f'<CulturalInstitution Detail for Profile {self.heritage_profile_id}>'


# Alias for registry imports
INSTITUTION_DETAIL = CulturalInstitution
