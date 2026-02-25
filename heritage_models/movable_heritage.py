from extensions import db

class MovableHeritage(db.Model):
    """Detail model for tangible movable (archaeological) heritage (Form 03A)."""
    
    __tablename__ = 'movable_heritage_details'
    
    # Linked to HeritageProfile
    profile_id = db.Column(db.Integer, db.ForeignKey('heritage_profile.id'), primary_key=True)
    profile = db.relationship('HeritageProfile', backref=db.backref('movable_details', uselist=False))
    
    # Unique Fields
    object_type = db.Column(db.String(50), nullable=True)
    place_found = db.Column(db.String(200), nullable=True)
    date_found = db.Column(db.Date, nullable=True)
    estimated_age = db.Column(db.String(100), nullable=True)
    acquisition_type = db.Column(db.String(50), nullable=True)
    materials = db.Column(db.String(200), nullable=True)
    dimensions = db.Column(db.String(100), nullable=True)
    comparative_criteria = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<MovableHeritage Detail for Profile {self.profile_id}>'
