from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import secrets


class User(UserMixin, db.Model):
    __tablename__ = 'USER'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False) # Renamed from password_hash to match ERD
    role = db.Column(db.String(20), default="user", index=True)  # 'admin', 'contributor', or 'user'
    barangay_id = db.Column(db.Integer, db.ForeignKey('BARANGAY_INFO.id'), nullable=True, index=True) # Renamed from barangay to match ERD
    is_approved = db.Column(db.Boolean, default=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    barangay = db.relationship('BarangayInfo', foreign_keys=[barangay_id], backref='residents')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class PasswordResetToken(db.Model):
    """Single-use, time-limited tokens for password reset."""
    __tablename__ = "PASSWORD_RESET_TOKEN"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("USER.id"), nullable=False, index=True)
    token = db.Column(db.String(128), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("reset_tokens", lazy=True))

    @classmethod
    def create_for_user(cls, user, expiry_minutes: int = 30) -> "PasswordResetToken":
        """Generate a new token for the given user."""
        token = cls(
            user_id=user.id,
            token=secrets.token_hex(32),
            expires_at=datetime.utcnow() + timedelta(minutes=expiry_minutes),
        )
        db.session.add(token)
        db.session.commit()
        return token

    @property
    def is_valid(self) -> bool:
        """True if token is unused and not expired."""
        from datetime import timezone
        
        expires = self.expires_at
        if expires.tzinfo is not None:
            # Normalize aware database datetime to naive UTC for comparison
            expires = expires.astimezone(timezone.utc).replace(tzinfo=None)
            
        return not self.used and datetime.utcnow() < expires
