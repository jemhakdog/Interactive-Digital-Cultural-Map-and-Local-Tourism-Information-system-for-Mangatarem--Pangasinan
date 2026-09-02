"""
Visitor Analytics and Logs tests.

Tests for visitor log model validation, date filters, page views, and export functionality.
"""

from backend.app.models.analytics import AnalyticsPageView, DatabaseAuditLog, VisitorLog


class TestVisitorLogModel:
    def test_visitor_log_creation(self):
        """Test that a visitor log can be instantiated with custom args."""
        log = VisitorLog(
            target_type="attraction",
            target_id=1,
            visitor_count=5,
            visitor_name="John Doe",
            visitor_age=30,
            visitor_address="Mangatarem, Pangasinan",
            is_system_user=True,
            logged_by=1,
            notes="Testing visitor log notes"
        )
        assert log.target_type == "attraction"
        assert log.target_id == 1
        assert log.visitor_count == 5
        assert log.visitor_name == "John Doe"
        assert log.visitor_age == 30
        assert log.visitor_address == "Mangatarem, Pangasinan"
        assert log.is_system_user is True
        assert log.logged_by == 1
        assert log.notes == "Testing visitor log notes"

    def test_database_audit_log_creation(self):
        """Test DatabaseAuditLog initialization to prevent dynamic kwargs issues."""
        log = DatabaseAuditLog(
            user_id=1,
            action="UPDATE",
            table_name="attraction",
            record_id=10,
            ip_address="127.0.0.1",
            user_agent="Mozilla/5.0",
            query_summary="Update attraction status",
            status="success"
        )
        assert log.user_id == 1
        assert log.action == "UPDATE"
        assert log.table_name == "attraction"
        assert log.record_id == 10
        assert log.ip_address == "127.0.0.1"
        assert log.user_agent == "Mozilla/5.0"
        assert log.query_summary == "Update attraction status"
        assert log.status == "success"

    def test_analytics_page_view_creation(self):
        """Test AnalyticsPageView initialization constructor behavior."""
        view = AnalyticsPageView(
            page_url="/map",
            view_type="page",
            item_id=None,
            page_name="map",
            user_id=1,
            session_id="session123",
            ip_address="192.168.1.1",
            device_info="Chrome Mobile"
        )
        assert view.page_url == "/map"
        assert view.view_type == "page"
        assert view.page_name == "map"
        assert view.user_id == 1
        assert view.session_id == "session123"
        assert view.ip_address == "192.168.1.1"
        assert view.device_info == "Chrome Mobile"
