from extensions import db
from datetime import datetime


class NewsletterSubscriber(db.Model):
    __tablename__ = 'NEWSLETTER_SUBSCRIBER'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<NewsletterSubscriber {self.email}>'


class NewsletterHistory(db.Model):
    __tablename__ = 'NEWSLETTER_HISTORY'
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    recipient_count = db.Column(db.Integer, default=0)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<NewsletterHistory {self.subject}>'

