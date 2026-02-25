"""
LGU Culture Program model for Form 07 - LGU Programs and Projects for Culture.
Stores municipal-level cultural development policies and programs.
"""
from extensions import db


class LGUCultureProgram(db.Model):
    """Detail model for LGU culture programs (Form 07)."""
    
    __tablename__ = 'lgu_program_details'
    
    # Linked to HeritageProfile
    profile_id = db.Column(db.Integer, db.ForeignKey('heritage_profile.id'), primary_key=True)
    profile = db.relationship('HeritageProfile', backref=db.backref('lgu_details', uselist=False))
    
    # Unique Fields
    vision_statement = db.Column(db.Text, nullable=True)
    mission_statement = db.Column(db.Text, nullable=True)
    goal_statements = db.Column(db.Text, nullable=True)
    adoption_date = db.Column(db.Date, nullable=True)
    brief_history = db.Column(db.Text, nullable=True)
    logo_url = db.Column(db.String(500), nullable=True)
    logo_legislation_date = db.Column(db.Date, nullable=True)
    logo_explanation = db.Column(db.Text, nullable=True)
    chief_executives = db.Column(db.JSON, nullable=True)
    resolutions = db.Column(db.JSON, nullable=True)
    ordinances = db.Column(db.JSON, nullable=True)
    ela_action_items = db.Column(db.JSON, nullable=True)
    major_policies = db.Column(db.JSON, nullable=True)
    program_strategies = db.Column(db.Text, nullable=True)
    annual_investments = db.Column(db.JSON, nullable=True)
    culture_projects = db.Column(db.JSON, nullable=True)
    arts_council = db.Column(db.JSON, nullable=True)
    alternative_livelihoods = db.Column(db.JSON, nullable=True)
    community_enterprises = db.Column(db.JSON, nullable=True)
    peoples_stories = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<LGUCultureProgram Detail for Profile {self.profile_id}>'
