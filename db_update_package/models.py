from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default="user")  # 'admin', 'contributor', or 'user'
    barangay = db.Column(db.String(100), nullable=True)
    is_approved = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Attraction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(
        db.String(50), nullable=False, index=True
    )  # Nature, Historical, Religious, etc.
    barangay = db.Column(db.String(100), nullable=True, index=True)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200), nullable=True)
    status = db.Column(
        db.String(20), default="pending", index=True
    )  # 'pending', 'approved'
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True, index=True)
    reviewed_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    barangay = db.Column(db.String(100), nullable=True)
    image_url = db.Column(db.String(200), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    status = db.Column(db.String(20), default="pending")  # 'pending', 'approved'
    category = db.Column(
        db.String(50), nullable=False, default="Civic"
    )  # 'Religious', 'Civic', 'Entertainment'
    reviewed_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class GalleryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)  # 'photo' or 'video'
    url = db.Column(db.String(200), nullable=False)
    caption = db.Column(db.String(200), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    status = db.Column(db.String(20), default="pending")  # 'pending', 'approved'
    reviewed_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)


class BarangayInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    barangay_name = db.Column(db.String(100), unique=True, nullable=False)
    history = db.Column(db.Text, nullable=True)
    cultural_assets = db.Column(db.Text, nullable=True)
    traditions = db.Column(db.Text, nullable=True)
    local_practices = db.Column(db.Text, nullable=True)
    unique_features = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class AnalyticsPageView(db.Model):
    __tablename__ = 'analytics_page_view'
    id = db.Column(db.Integer, primary_key=True)
    view_type = db.Column(
        db.String(50), nullable=False
    )  # 'attraction', 'event', 'page'
    item_id = db.Column(
        db.Integer, nullable=True
    )  # ID of the attraction or event, if applicable
    page_name = db.Column(
        db.String(100), nullable=True
    )  # Name of the page (e.g., 'home', 'map', 'events')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, nullable=True)  # Optional, if logged in


class UserFavoriteAttraction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    attraction_id = db.Column(
        db.Integer, db.ForeignKey("attraction.id"), nullable=False
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class UserEventInterest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)
    status = db.Column(db.String(20), default="interested")  # 'interested', 'going'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class AttractionReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    attraction_id = db.Column(
        db.Integer, db.ForeignKey("attraction.id"), nullable=False
    )
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    status = db.Column(
        db.String(20), default="pending"
    )  # 'pending', 'approved', 'rejected'
    reviewed_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
