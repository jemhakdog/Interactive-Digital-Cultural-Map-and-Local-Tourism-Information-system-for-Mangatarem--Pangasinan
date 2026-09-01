"""
Unit tests for refactored clean code utilities.

Tests file helpers, logger helpers, and app constants.
"""

import logging
# import pytest  # Removed unused import
from unittest.mock import MagicMock, patch


# === Logger Helper Tests ===


class TestLoggerHelper:
    """Test centralized logging helper functions."""

    def test_log_entry_with_kwargs(self, caplog):
        """log_entry formats module/function/kwargs into an INFO message."""
        from utils.logger_helper import log_entry

        with caplog.at_level(logging.INFO):
            log_entry("auth", "login", method="POST", user="admin")

        assert "[auth] > login > ENTRY" in caplog.text
        assert "method=POST" in caplog.text
        assert "user=admin" in caplog.text

    def test_log_entry_without_kwargs(self, caplog):
        """log_entry works with no extra context."""
        from utils.logger_helper import log_entry

        with caplog.at_level(logging.INFO):
            log_entry("admin", "dashboard")

        assert "[admin] > dashboard > ENTRY" in caplog.text

    def test_log_success(self, caplog):
        """log_success emits an INFO record."""
        from utils.logger_helper import log_success

        with caplog.at_level(logging.INFO):
            log_success("auth", "login", "User 'admin' logged in")

        assert "SUCCESS" in caplog.text
        assert "User 'admin' logged in" in caplog.text

    def test_log_error(self, caplog):
        """log_error emits an ERROR record."""
        from utils.logger_helper import log_error

        with caplog.at_level(logging.ERROR):
            log_error("auth", "register", "Username already exists")

        assert "ERROR" in caplog.text
        assert "Username already exists" in caplog.text

    def test_no_print_calls(self, capsys):
        """Verify print() is no longer called (dual-logging removed)."""
        from utils.logger_helper import log_entry, log_query, log_success

        log_entry("mod", "fn")
        log_query("mod", "fn", "desc")
        log_success("mod", "fn", "ok")

        captured = capsys.readouterr()
        assert captured.out == "", "logger_helper should not emit print() output"


# === File Helper Tests ===


class TestFileHelpers:
    """Test shared file-upload utilities."""

    def test_allowed_file_accepts_valid(self):
        """allowed_file returns True for allowed extensions."""
        from utils.file_helpers import allowed_file

        app = MagicMock()
        app.config = {"ALLOWED_EXTENSIONS": {"png", "jpg", "gif"}}

        with patch("utils.file_helpers.current_app", app):
            assert allowed_file("photo.png") is True
            assert allowed_file("image.JPG") is True

    def test_allowed_file_rejects_invalid(self):
        """allowed_file returns False for disallowed extensions."""
        from utils.file_helpers import allowed_file

        app = MagicMock()
        app.config = {"ALLOWED_EXTENSIONS": {"png", "jpg"}}

        with patch("utils.file_helpers.current_app", app):
            assert allowed_file("script.exe") is False
            assert allowed_file("noext") is False

    def test_detect_media_type_video(self):
        """detect_media_type identifies video extensions."""
        from utils.file_helpers import detect_media_type

        assert detect_media_type("clip.mp4") == "video"
        assert detect_media_type("recording.mov") == "video"

    def test_detect_media_type_photo(self):
        """detect_media_type defaults to 'photo' for non-video files."""
        from utils.file_helpers import detect_media_type

        assert detect_media_type("image.png") == "photo"
        assert detect_media_type("pic.jpg") == "photo"

    def test_save_uploaded_file_returns_none_on_empty(self):
        """save_uploaded_file returns None when no file is provided."""
        from utils.file_helpers import save_uploaded_file

        app = MagicMock()
        app.config = {
            "ALLOWED_EXTENSIONS": {"png"},
            "UPLOAD_FOLDER": "/tmp",
        }

        with patch("utils.file_helpers.current_app", app):
            assert save_uploaded_file(None) is None

    def test_save_uploaded_file_returns_none_on_invalid_ext(self):
        """save_uploaded_file returns None for disallowed file types."""
        from utils.file_helpers import save_uploaded_file

        app = MagicMock()
        app.config = {
            "ALLOWED_EXTENSIONS": {"png"},
            "UPLOAD_FOLDER": "/tmp",
        }

        bad_file = MagicMock()
        bad_file.filename = "virus.exe"

        with patch("utils.file_helpers.current_app", app):
            assert save_uploaded_file(bad_file) is None
