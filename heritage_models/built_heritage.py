from extensions import db

class BuiltHeritage(db.Model):
    """Detail model for tangible immovable (built) heritage (Form 02A)."""
    
    __tablename__ = 'built_heritage_details'
    
    # Linked to HeritageProfile
    profile_id = db.Column(db.Integer, db.ForeignKey('heritage_profile.id'), primary_key=True)
    profile = db.relationship('HeritageProfile', backref=db.backref('built_details', uselist=False))
    
    # Unique Fields
    building_type = db.Column(db.String(50), nullable=True)
    year_constructed = db.Column(db.Integer, nullable=True)
    ownership_type = db.Column(db.String(20), nullable=True)
    declaration_legislation = db.Column(db.Text, nullable=True)
    physical_description = db.Column(db.Text, nullable=True)
    history_structure = db.Column(db.Text, nullable=True)
    occupation_status = db.Column(db.String(20), nullable=True)
    is_altered = db.Column(db.Boolean, nullable=True)
    is_original_site = db.Column(db.Boolean, nullable=True)
    integrity_remarks = db.Column(db.Text, nullable=True)
    movable_heritage_list = db.Column(db.JSON, nullable=True)
    
    def __repr__(self):
        return f'<BuiltHeritage Detail for Profile {self.profile_id}>'
