from extensions import db

class BuiltHeritage(db.Model):
    """Detail model for tangible immovable (built) heritage (Form 02A)."""
    
    __tablename__ = 'BUILT_HERITAGE_DETAIL'
    
    # Linked to HeritageProfile
    heritage_profile_id = db.Column(db.Integer, db.ForeignKey('HERITAGE_PROFILE.id'), primary_key=True)
    profile = db.relationship('HeritageProfile', backref=db.backref('built_details', uselist=False))
    
    # ERD Fields
    type_of_building = db.Column(db.String(100), nullable=True)
    year_constructed = db.Column(db.Integer, nullable=True)
    architect_builder = db.Column(db.String(200), nullable=True)
    architectural_style = db.Column(db.String(100), nullable=True)
    materials_used = db.Column(db.Text, nullable=True)
    state_of_conservation = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<BuiltHeritage Detail for Profile {self.heritage_profile_id}>'
