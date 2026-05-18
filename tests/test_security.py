"""
Security utility tests.

Tests for input validation and sanitization functions.
"""

import sys
import os

# Add parent directory to path so we can import utils
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.security import (
    validate_email_format,
    validate_username,
    validate_password_strength,
    sanitize_html_input,
    validate_and_escape,
    sanitize_filename,
    sanitize_url,
    validate_phone,
    validate_coordinates,
)


class TestEmailValidation:
    def test_valid_emails(self):
        assert validate_email_format("user@example.com") is True
        assert validate_email_format("test.user@domain.org") is True
        assert validate_email_format("user+tag@example.co.uk") is True

    def test_invalid_emails(self):
        assert validate_email_format("invalid") is False
        assert validate_email_format("user@") is False
        assert validate_email_format("@example.com") is False
        assert validate_email_format("") is False
        assert validate_email_format("user@example") is False


class TestUsernameValidation:
    def test_valid_usernames(self):
        assert validate_username("user123") is True
        assert validate_username("test_user") is True
        assert validate_username("abc") is True
        assert validate_username("User_Name_123") is True

    def test_invalid_usernames(self):
        assert validate_username("ab") is False  # Too short
        assert validate_username("user name") is False  # Space
        assert validate_username("user<script>") is False  # XSS attempt
        assert validate_username("") is False
        assert validate_username("a" * 31) is False  # Too long


class TestPasswordStrength:
    def test_valid_passwords(self):
        is_valid, _ = validate_password_strength("password123")
        assert is_valid is True
        is_valid, _ = validate_password_strength("a" * 128)
        assert is_valid is True

    def test_invalid_passwords(self):
        is_valid, msg = validate_password_strength("short")
        assert is_valid is False
        assert "at least 8 characters" in msg

        is_valid, msg = validate_password_strength("a" * 129)
        assert is_valid is False
        assert "too long" in msg

        is_valid, msg = validate_password_strength("")
        assert is_valid is False


class TestHTMLSanitization:
    def test_sanitize_removes_script_tags(self):
        malicious = "<script>alert('XSS')</script>Hello"
        sanitized = sanitize_html_input(malicious)
        assert "<script>" not in sanitized
        assert "</script>" not in sanitized
        assert "Hello" in sanitized

    def test_sanitize_allows_safe_tags(self):
        content = "<p>This is <strong>bold</strong> text</p>"
        sanitized = sanitize_html_input(content)
        assert "<p>" in sanitized
        assert "<strong>" in sanitized

    def test_escape_all_html(self):
        user_input = "<script>alert('XSS')</script>"
        escaped = validate_and_escape(user_input)
        assert "&lt;script&gt;" in escaped
        assert "<script>" not in escaped


class TestFilenameSanitization:
    def test_normal_filenames(self):
        assert sanitize_filename("photo.jpg") == "photo.jpg"
        assert sanitize_filename("my_file.png") == "my_file.png"

    def test_path_traversal(self):
        assert "../etc/passwd" not in sanitize_filename("../../etc/passwd")
        assert "..\\" not in sanitize_filename("..\\windows\\system32")

    def test_dangerous_characters(self):
        sanitized = sanitize_filename("file<script>.exe")
        assert "<" not in sanitized
        assert ">" not in sanitized


class TestURLSanitization:
    def test_safe_urls(self):
        assert sanitize_url("https://example.com") == "https://example.com"
        assert sanitize_url("/relative/path") == "/relative/path"
        assert sanitize_url("#anchor") == "#anchor"

    def test_dangerous_urls(self):
        assert sanitize_url("javascript:alert('XSS')") == ""
        assert sanitize_url("data:text/html,<script>") == ""
        assert sanitize_url("vbscript:msgbox(1)") == ""


class TestPhoneValidation:
    def test_valid_phones(self):
        assert validate_phone("+1234567890") is True
        assert validate_phone("123-456-7890") is True
        assert validate_phone("(123) 456-7890") is True

    def test_invalid_phones(self):
        assert validate_phone("abc1234567") is False
        assert validate_phone("123") is False  # Too short


class TestCoordinateValidation:
    def test_valid_coords(self):
        assert validate_coordinates(15.9949, 120.4869) is True
        assert validate_coordinates(-90, -180) is True
        assert validate_coordinates(90, 180) is True

    def test_invalid_coords(self):
        assert validate_coordinates(91, 0) is False
        assert validate_coordinates(0, 181) is False
        assert validate_coordinates("invalid", 0) is False
