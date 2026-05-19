from extensions import db
from datetime import datetime

class ChatRoom(db.Model):
    __tablename__ = 'CHAT_ROOM'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)  # 'barangay', 'business', 'direct'
    barangay_id = db.Column(db.Integer, db.ForeignKey('BARANGAY_INFO.id'), nullable=True, index=True)
    establishment_id = db.Column(db.Integer, db.ForeignKey('ESTABLISHMENT.id'), nullable=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    barangay = db.relationship('BarangayInfo', backref=db.backref('chat_room', uselist=False))
    establishment = db.relationship('Establishment', backref=db.backref('chat_room', uselist=False))
    messages = db.relationship('ChatMessage', backref='room', cascade='all, delete-orphan', lazy='dynamic')
    participants = db.relationship('ChatParticipant', backref='room', cascade='all, delete-orphan')

class ChatParticipant(db.Model):
    __tablename__ = 'CHAT_PARTICIPANT'
    id = db.Column(db.Integer, primary_key=True)
    chat_room_id = db.Column(db.Integer, db.ForeignKey('CHAT_ROOM.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('USER.id'), nullable=False, index=True)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_read_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='chat_memberships')

class ChatMessage(db.Model):
    __tablename__ = 'CHAT_MESSAGE'
    id = db.Column(db.Integer, primary_key=True)
    chat_room_id = db.Column(db.Integer, db.ForeignKey('CHAT_ROOM.id'), nullable=False, index=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('USER.id'), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    is_system_msg = db.Column(db.Boolean, default=False)

    sender = db.relationship('User', backref='sent_messages')
