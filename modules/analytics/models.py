from extensions import db
from datetime import datetime


class AnalyticsPageView(db.Model):
    __tablename__ = 'ANALYTICS_PAGE_VIEW'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    page_url = db.Column(db.String(500), nullable=True) # Kept for compatibility
    view_type = db.Column(db.String(50), nullable=True, index=True)  # 'attraction', 'event', 'page'
    item_id = db.Column(db.Integer, nullable=True, index=True)       # ID of the attraction or event, if applicable
    page_name = db.Column(db.String(100), nullable=True, index=True) # Name of the page (e.g., 'home', 'map', 'events')
    user_id = db.Column(db.Integer, nullable=True, index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    session_id = db.Column(db.String(100), nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    device_info = db.Column(db.Text, nullable=True)

    def __init__(self, **kwargs):
        super(AnalyticsPageView, self).__init__(**kwargs)


class DatabaseAuditLog(db.Model):
    """Audit log for database operations (security monitoring)."""
    __tablename__ = 'DATABASE_AUDIT_LOG'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('USER.id'), nullable=True, index=True)
    action = db.Column(db.String(50), nullable=False, index=True)  # INSERT, UPDATE, DELETE, SELECT
    table_name = db.Column(db.String(100), nullable=False, index=True)
    record_id = db.Column(db.Integer, nullable=True, index=True)  # ID of affected record
    ip_address = db.Column(db.String(45), nullable=True)  # IPv4 or IPv6
    user_agent = db.Column(db.String(500), nullable=True)
    query_summary = db.Column(db.String(500), nullable=True)  # Brief description, not full query
    status = db.Column(db.String(20), default='success', index=True)  # success, failed, blocked
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    user = db.relationship('User', backref=db.backref('audit_logs', lazy=True))

    def __init__(self, **kwargs):
        super(DatabaseAuditLog, self).__init__(**kwargs)

    @classmethod
    def log_operation(cls, user_id, action, table_name, record_id=None, 
                     ip_address=None, user_agent=None, query_summary=None, status='success'):
        """Create an audit log entry."""
        log = cls(
            user_id=user_id,
            action=action,
            table_name=table_name,
            record_id=record_id,
            ip_address=ip_address,
            user_agent=user_agent,
            query_summary=query_summary,
            status=status
        )
        db.session.add(log)
        db.session.commit()
        return log


class VisitorLog(db.Model):
    """Consolidated visitor log for establishments and attractions."""
    __tablename__ = 'VISITOR_LOG'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    target_type = db.Column(db.String(50), nullable=False, index=True)  # 'establishment', 'attraction'
    target_id = db.Column(db.Integer, nullable=False, index=True)
    visitor_count = db.Column(db.Integer, default=1, nullable=False)
    
    # Detailed Visitor Data (Optional)
    visitor_name = db.Column(db.String(150), nullable=True)
    visitor_age = db.Column(db.Integer, nullable=True)
    visitor_address = db.Column(db.String(255), nullable=True)
    is_system_user = db.Column(db.Boolean, default=False)

    visit_date = db.Column(db.Date, default=datetime.utcnow().date, index=True)
    logged_by = db.Column(db.Integer, db.ForeignKey('USER.id'), nullable=False, index=True)
    visitor_user_id = db.Column(db.Integer, db.ForeignKey('USER.id'), nullable=True, index=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    steward = db.relationship('User', foreign_keys=[logged_by], backref=db.backref('visitor_logs', lazy=True))
    visitor_user = db.relationship('User', foreign_keys=[visitor_user_id], backref=db.backref('personal_visits', lazy=True))

    def __init__(self, **kwargs):
        super(VisitorLog, self).__init__(**kwargs)

    @property
    def target_name(self):
        """Helper to get the name of the attraction or establishment."""
        from models import Attraction, Establishment
        if self.target_type == 'attraction':
            obj = Attraction.query.get(self.target_id)
            return obj.name if obj else f"Unknown Attraction #{self.target_id}"
        elif self.target_type == 'establishment':
            obj = Establishment.query.get(self.target_id)
            return obj.name if obj else f"Unknown Establishment #{self.target_id}"
        return f"Unknown Target #{self.target_id}"
