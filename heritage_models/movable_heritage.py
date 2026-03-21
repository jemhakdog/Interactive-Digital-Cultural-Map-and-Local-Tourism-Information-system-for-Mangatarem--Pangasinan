from extensions import db

class MovableHeritage(db.Model):
    """Detail model for tangible movable (archaeological) heritage (Form 03A)."""
    
    __tablename__ = 'MOVABLE_HERITAGE_DETAIL'
    
    # Linked to HeritageProfile
    heritage_profile_id = db.Column(db.Integer, db.ForeignKey('HERITAGE_PROFILE.id'), primary_key=True)
    profile = db.relationship('HeritageProfile', backref=db.backref('movable_details', uselist=False))
    
    # ERD Fields
    type_of_object = db.Column(db.String(100), nullable=True)
    material = db.Column(db.Text, nullable=True)
    dimensions = db.Column(db.String(100), nullable=True)
    current_location = db.Column(db.Text, nullable=True)
    state_of_conservation = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<MovableHeritage Detail for Profile {self.heritage_profile_id}>'


# Alias for registry imports
MOVABLE_HERITAGE_DETAIL = MovableHeritage
