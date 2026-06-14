from extensions import db
from datetime import datetime


class Announcement(db.Model):
    __tablename__ = 'ANNOUNCEMENT'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("USER.id"), nullable=False, index=True)
    barangay_id = db.Column(db.Integer, db.ForeignKey('BARANGAY_INFO.id'), nullable=True, index=True)
    status = db.Column(db.String(20), default="pending", index=True) # pending, approved, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('announcements', lazy=True))
    barangay = db.relationship('BarangayInfo', backref=db.backref('announcements', lazy=True))

    def to_dict(self):
        """Convert Announcement to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'user_id': self.user_id,
            'author_name': self.user.username if self.user else 'System',
            'barangay_id': self.barangay_id,
            'barangay_name': self.barangay.name if self.barangay else 'Central LGU',
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
