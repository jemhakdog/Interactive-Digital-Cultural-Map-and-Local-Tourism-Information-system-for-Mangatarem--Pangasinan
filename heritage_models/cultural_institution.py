"""
Cultural Institution model for Form 06 - Cultural Institutions.
Stores information about libraries, museums, schools, and other cultural organizations.
"""
from extensions import db


class CulturalInstitution(db.Model):
    """Detail model for cultural institutions (Form 06)."""
    
    __tablename__ = 'institution_details'
    
    # Linked to HeritageProfile
    profile_id = db.Column(db.Integer, db.ForeignKey('heritage_profile.id'), primary_key=True)
    profile = db.relationship('HeritageProfile', backref=db.backref('institution_details', uselist=False))
    
    # Unique Fields
    municipality = db.Column(db.String(100), nullable=True)
    province = db.Column(db.String(100), nullable=True)
    institution_type = db.Column(db.String(100), nullable=True)
    mandate_description = db.Column(db.Text, nullable=True)
    milestones = db.Column(db.Text, nullable=True)
    condition_status = db.Column(db.Text, nullable=True)
    supporting_docs = db.Column(db.JSON, nullable=True)
    
    def __repr__(self):
        return f'<CulturalInstitution Detail for Profile {self.profile_id}>'
