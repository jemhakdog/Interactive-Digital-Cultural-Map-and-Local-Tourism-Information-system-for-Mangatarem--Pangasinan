from extensions import db
from datetime import datetime


class NewsletterSubscriber(db.Model):
    __tablename__ = 'NEWSLETTER_SUBSCRIBER'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    is_active = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('USER.id', ondelete='SET NULL'), nullable=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('newsletter_subscriptions', lazy='dynamic'))

    def __repr__(self):
        return f'<NewsletterSubscriber {self.email}>'


class NewsletterHistory(db.Model):
    __tablename__ = 'NEWSLETTER_HISTORY'
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    recipient_count = db.Column(db.Integer, default=0)
    sender_id = db.Column(db.Integer, db.ForeignKey('USER.id', ondelete='SET NULL'), nullable=True, index=True)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)

    sender = db.relationship('User', backref=db.backref('sent_newsletters', lazy='dynamic'))

    def __repr__(self):
        return f'<NewsletterHistory {self.subject}>'


class UserNotification(db.Model):
    __tablename__ = 'USER_NOTIFICATION'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('USER.id', ondelete='CASCADE'), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(200), nullable=True)
    is_read = db.Column(db.Boolean, default=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    user = db.relationship('User', backref=db.backref('notifications', lazy='dynamic', cascade='all, delete-orphan'))

    def __repr__(self):
        return f'<UserNotification {self.title} to User {self.user_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'message': self.message,
            'link': self.link,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat()
        }


def create_notification(user_id, title, message, link=None):
    """Safely create a notification for a user."""
    try:
        notification = UserNotification(
            user_id=user_id,
            title=title,
            message=message,
            link=link
        )
        db.session.add(notification)
        db.session.commit()
        return notification
    except Exception as e:
        db.session.rollback()
        import logging
        logging.getLogger(__name__).error(f"Error creating notification: {e}")
        return None


