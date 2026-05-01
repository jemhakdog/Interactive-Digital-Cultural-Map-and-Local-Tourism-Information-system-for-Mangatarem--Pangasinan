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
