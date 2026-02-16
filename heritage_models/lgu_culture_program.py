"""
LGU Culture Program model for Form 07 - LGU Programs and Projects for Culture.
Stores municipal-level cultural development policies and programs.
"""
from extensions import db
from datetime import datetime


class LGUCultureProgram(db.Model):
    """Model for LGU culture programs (Form 07)."""
    
    __tablename__ = 'lgu_culture_program'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Basic Information
    municipality = db.Column(db.String(100), nullable=False, unique=True, index=True)
    province = db.Column(db.String(100), nullable=False)
    
    # Core Development Principles (Section A)
    vision_statement = db.Column(db.Text, nullable=True)
    mission_statement = db.Column(db.Text, nullable=True)
    goal_statements = db.Column(db.Text, nullable=True)
    adoption_date = db.Column(db.Date, nullable=True)
    
    # Brief History (Section B)
    brief_history = db.Column(db.Text, nullable=True)
    
    # LGU Logo/Emblem (Section C)
    logo_url = db.Column(db.String(500), nullable=True)
    logo_legislation_date = db.Column(db.Date, nullable=True)
    logo_explanation = db.Column(db.Text, nullable=True)
    
    # Local Chief Executives (Section D)
    chief_executives = db.Column(db.JSON, nullable=True)  # Array of {name, term_start, term_end}
    
    # Policies and Action Agenda (Section E)
    resolutions = db.Column(db.JSON, nullable=True)  # Array of {year, nature, number}
    ordinances = db.Column(db.JSON, nullable=True)  # Array of {year, nature, number}
    ela_action_items = db.Column(db.JSON, nullable=True)  # Array of action items
    
    # Major Policies (Section F)
    major_policies = db.Column(db.JSON, nullable=True)  # Array of {date, title_summary}
    
    # Programs (Section G)
    program_strategies = db.Column(db.Text, nullable=True)
    
    # Annual Investment Plan (Section H)
    annual_investments = db.Column(db.JSON, nullable=True)  # {year: {program: amount}}
    
    # Culture Projects (Section H)
    culture_projects = db.Column(db.JSON, nullable=True)  # {year: {project: amount}}
    
    # Local Arts and Culture Council (Section I)
    arts_council = db.Column(db.JSON, nullable=True)  # {creation_date, legal_basis, functions, composition}
    
    # Alternative Livelihoods (Section J)
    alternative_livelihoods = db.Column(db.JSON, nullable=True)  # Array of {livelihood, lgu_support}
    
    # Community Culture Enterprises (Section K)
    community_enterprises = db.Column(db.JSON, nullable=True)  # Array of {name, nature, date_established}
    
    # People's Stories (Section L)
    peoples_stories = db.Column(db.Text, nullable=True)
    
    # References (Section M)
    key_informants = db.Column(db.JSON, nullable=True)
    references = db.Column(db.Text, nullable=True)
    
    # Metadata
    mapper_name = db.Column(db.String(200), nullable=True)
    date_profiled = db.Column(db.Date, nullable=True)
    
    # Approval Workflow
    status = db.Column(db.String(20), default='pending', index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True, index=True)
    reviewed_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<LGUCultureProgram {self.municipality}>'
