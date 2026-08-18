from extensions import db
from datetime import datetime


class GalleryItem(db.Model):
    __tablename__ = 'GALLERY_ITEM'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)  # 'photo' or 'video'
    url = db.Column(db.String(500), nullable=False)
    caption = db.Column(db.Text, nullable=True) # Changed from String(200) to Text
    user_id = db.Column(db.Integer, db.ForeignKey("USER.id"), nullable=True, index=True)
    status = db.Column(db.String(20), default="pending", index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True) # Renamed from uploaded_at
