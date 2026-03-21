"""
LGU Culture Program model for Form 07 - LGU Programs and Projects for Culture.
Stores municipal-level cultural development policies and programs.
"""
from extensions import db


__all__ = ['LGUCultureProgram', 'LGU_PROGRAM_DETAIL']


class LGUCultureProgram(db.Model):
    """Detail model for LGU culture programs (Form 07)."""
    
    __tablename__ = 'LGU_PROGRAM_DETAIL'
    
    # Linked to HeritageProfile
    heritage_profile_id = db.Column(db.Integer, db.ForeignKey('HERITAGE_PROFILE.id'), primary_key=True)
    profile = db.relationship('HeritageProfile', backref=db.backref('lgu_details', uselist=False))
    
    # ERD Fields
    program_name = db.Column(db.String(200), nullable=True)
    starting_year = db.Column(db.Integer, nullable=True)
    description = db.Column(db.Text, nullable=True)
    culture_projects = db.Column(db.JSON, nullable=True)
    
    def __repr__(self):
        return f'<LGUCultureProgram Detail for Profile {self.heritage_profile_id}>'


# Alias for registry imports
LGU_PROGRAM_DETAIL = LGUCultureProgram
