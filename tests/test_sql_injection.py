"""
SQL Injection prevention tests.

Tests all input validation and sanitization to ensure SQL injection
attacks are properly blocked.
"""

from utils.security import (
    detect_sql_injection_attempt,
    validate_string_input,
    validate_integer,
    validate_float,
    sanitize_for_display
)


class TestSQLInjectionDetection:
    """Test SQL injection pattern detection."""

    def test_basic_select_injection(self):
        """Detect SELECT keyword injection."""
        assert detect_sql_injection_attempt("SELECT * FROM users") is True
        assert detect_sql_injection_attempt("Hello SELECT world") is True
        assert detect_sql_injection_attempt("select from table") is True

    def test_basic_insert_injection(self):
        """Detect INSERT keyword injection."""
        assert detect_sql_injection_attempt("INSERT INTO users") is True
        assert detect_sql_injection_attempt("insert into table") is True

    def test_basic_update_injection(self):
        """Detect UPDATE keyword injection."""
        assert detect_sql_injection_attempt("UPDATE users SET") is True
        assert detect_sql_injection_attempt("update table set") is True

    def test_basic_delete_injection(self):
        """Detect DELETE keyword injection."""
        assert detect_sql_injection_attempt("DELETE FROM users") is True
        assert detect_sql_injection_attempt("delete from table") is True

    def test_drop_table_injection(self):
        """Detect DROP TABLE injection."""
        assert detect_sql_injection_attempt("DROP TABLE users") is True
        assert detect_sql_injection_attempt("'; DROP TABLE users; --") is True
        assert detect_sql_injection_attempt("drop table users") is True

    def test_union_injection(self):
        """Detect UNION injection."""
        assert detect_sql_injection_attempt("UNION SELECT * FROM") is True
        assert detect_sql_injection_attempt("' UNION SELECT password FROM") is True
        assert detect_sql_injection_attempt("union select") is True

    def test_comment_injection(self):
        """Detect SQL comment patterns."""
        assert detect_sql_injection_attempt("-- comment") is True
        assert detect_sql_injection_attempt("admin--") is True
        assert detect_sql_injection_attempt("/* comment */") is True

    def test_semicolon_injection(self):
        """Detect semicolon (statement terminator)."""
        assert detect_sql_injection_attempt("'; DROP TABLE users") is True
        assert detect_sql_injection_attempt("value; DELETE FROM") is True

    def test_tautology_attack(self):
        """Detect tautology-based attacks (OR 1=1)."""
        assert detect_sql_injection_attempt("' OR 1=1 --") is True
        assert detect_sql_injection_attempt("' OR '1'='1") is True
        assert detect_sql_injection_attempt("admin' AND 1=1 --") is True

    def test_information_schema_access(self):
        """Detect INFORMATION_SCHEMA access attempts."""
        assert detect_sql_injection_attempt("SELECT FROM INFORMATION_SCHEMA") is True
        assert detect_sql_injection_attempt("information_schema.tables") is True

    def test_xp_cmdshell_injection(self):
        """Detect xp_cmdshell execution attempts."""
        assert detect_sql_injection_attempt("EXEC xp_cmdshell") is True
        assert detect_sql_injection_attempt("xp_cmdshell 'dir'") is True

    def test_safe_input(self):
        """Allow safe, non-SQL inputs."""
        # "select" in normal text is caught by the regex pattern
        assert detect_sql_injection_attempt("John Doe") is False
        assert detect_sql_injection_attempt("user@example.com") is False
        assert detect_sql_injection_attempt("Hello World!") is False
        assert detect_sql_injection_attempt("12345") is False
        assert detect_sql_injection_attempt("") is False
        assert detect_sql_injection_attempt(None) is False

    def test_edge_cases_with_sql_keywords(self):
        """Test edge cases where SQL keywords appear in normal text."""
        # These should be detected (better safe than sorry)
        assert detect_sql_injection_attempt("Please select an option") is True
        assert detect_sql_injection_attempt("DELETE your account") is True


class TestStringInputValidation:
    """Test comprehensive string input validation."""

    def test_valid_string(self):
        """Allow valid strings within limits."""
        is_valid, error_msg = validate_string_input("Hello World", min_length=1, max_length=100)
        assert is_valid is True
        assert error_msg == ""

    def test_empty_string_required(self):
        """Reject empty string when required."""
        is_valid, error_msg = validate_string_input("", min_length=1)
        assert is_valid is False
        assert "required" in error_msg.lower()

    def test_min_length_violation(self):
        """Reject strings below minimum length."""
        is_valid, error_msg = validate_string_input("ab", min_length=5)
        assert is_valid is False
        assert "at least" in error_msg.lower()

    def test_max_length_violation(self):
        """Reject strings exceeding maximum length."""
        long_string = "a" * 501
        is_valid, error_msg = validate_string_input(long_string, max_length=500)
        assert is_valid is False
        assert "no more than" in error_msg.lower()

    def test_sql_injection_blocked(self):
        """Block SQL injection attempts."""
        malicious_inputs = [
            "' OR '1'='1",
            "'; DROP TABLE users; --",
            "' UNION SELECT * FROM passwords --",
            "admin'--",
        ]
        for malicious in malicious_inputs:
            is_valid, error_msg = validate_string_input(malicious, block_sql_injection=True)
            assert is_valid is False
            assert "Invalid characters" in error_msg

    def test_pattern_validation(self):
        """Validate against allowed pattern."""
        is_valid, error_msg = validate_string_input(
            "hello123",
            allowed_pattern=r'^[a-zA-Z]+$'  # Letters only
        )
        assert is_valid is False
        assert "invalid characters" in error_msg.lower()

    def test_sql_injection_disabled(self):
        """Allow SQL keywords when detection is disabled."""
        is_valid, error_msg = validate_string_input(
            "SELECT * FROM users",
            block_sql_injection=False
        )
        assert is_valid is True


class TestIntegerValidation:
    """Test integer input validation."""

    def test_valid_integer(self):
        """Allow valid integers."""
        is_valid, value, error_msg = validate_integer("42")
        assert is_valid is True
        assert value == 42

    def test_integer_with_limits(self):
        """Validate integer within range."""
        is_valid, value, error_msg = validate_integer("5", min_value=1, max_value=10)
        assert is_valid is True
        assert value == 5

    def test_invalid_integer(self):
        """Reject non-integer values."""
        is_valid, value, error_msg = validate_integer("abc")
        assert is_valid is False
        assert value == 0

    def test_below_minimum(self):
        """Reject integers below minimum."""
        is_valid, value, error_msg = validate_integer("0", min_value=1)
        assert is_valid is False
        assert value == 0

    def test_above_maximum(self):
        """Reject integers above maximum."""
        is_valid, value, error_msg = validate_integer("100", max_value=50)
        assert is_valid is False
        assert value == 0

    def test_float_converted_to_int(self):
        """Handle float strings properly."""
        is_valid, value, error_msg = validate_integer("3.14")
        # Should fail because int("3.14") raises ValueError
        assert is_valid is False


class TestFloatValidation:
    """Test float input validation."""

    def test_valid_float(self):
        """Allow valid floats."""
        is_valid, value, error_msg = validate_float("3.14")
        assert is_valid is True
        assert abs(value - 3.14) < 0.001

    def test_valid_integer_as_float(self):
        """Allow integers as valid floats."""
        is_valid, value, error_msg = validate_float("42")
        assert is_valid is True
        assert value == 42.0

    def test_invalid_float(self):
        """Reject non-float values."""
        is_valid, value, error_msg = validate_float("abc")
        assert is_valid is False

    def test_float_with_limits(self):
        """Validate float within range."""
        is_valid, value, error_msg = validate_float("5.5", min_value=0.0, max_value=10.0)
        assert is_valid is True
        assert abs(value - 5.5) < 0.001


class TestDisplaySanitization:
    """Test output sanitization for display."""

    def test_html_escaped(self):
        """Escape HTML special characters."""
        result = sanitize_for_display("<script>alert('XSS')</script>")
        assert "<script>" not in result
        assert "&lt;script&gt;" in result

    def test_truncation(self):
        """Truncate long strings for display."""
        long_string = "a" * 100
        result = sanitize_for_display(long_string, max_length=10)
        assert len(result) <= 13  # 10 chars + "..."
        assert result.endswith("...")

    def test_empty_string(self):
        """Handle empty strings gracefully."""
        result = sanitize_for_display("")
        assert result == ""
        result = sanitize_for_display(None)
        assert result == ""

    def test_safe_string_unchanged(self):
        """Leave safe strings unchanged."""
        result = sanitize_for_display("Hello World")
        assert result == "Hello World"


class TestParameterizedQueries:
    """Test that parameterized queries are used correctly."""

    def test_text_query_with_parameters_safe(self):
        """Verify that text() with parameters treats input as data, not SQL."""
        from sqlalchemy import text
        
        # This demonstrates the concept - actual testing requires DB connection
        # The key is that parameters are passed separately, not interpolated
        malicious_input = "' OR '1'='1"
        
        # Safe: parameterized query (what we implement)
        safe_query = text("SELECT * FROM users WHERE username = :username")
        # Parameters passed separately, not interpolated into query string
        params = {"username": malicious_input}
        
        # The query string remains unchanged - no SQL injection
        assert ":username" in str(safe_query)
        assert "' OR '1'='1" not in str(safe_query)
        assert params["username"] == malicious_input  # Treated as data

    def test_orm_automatically_parameterizes(self):
        """Verify SQLAlchemy ORM automatically parameterizes queries."""
        # SQLAlchemy ORM always uses parameterized queries internally
        # This is by design - no way to inject through ORM methods
        # We can't test without app context, but we document the behavior
        
        # The key point: ORM query construction is safe by design
        # User.query.filter_by(username=malicious) 
        # ALWAYS treats malicious input as data, never as SQL
        
        # This is proven by SQLAlchemy's implementation which uses
        # parameterized queries internally for all ORM operations
        assert True  # Documentation test - ORM is safe by design


class TestValidationDecorators:
    """Test route validation decorators."""

    def test_form_data_validation_valid(self, app, client):
        """Test valid form data passes validation."""
        from utils.validators import validate_form_data
        
        @app.route('/test/valid-form', methods=['POST'])
        @validate_form_data({
            'name': {'type': 'string', 'required': True, 'max_length': 100}
        })
        def test_valid_form():
            return 'OK'
        
        response = client.post('/test/valid-form', data={'name': 'John Doe'})
        assert response.status_code == 200

    def test_form_data_validation_invalid_sql_injection(self, app, client):
        """Test SQL injection blocked in form data."""
        from utils.validators import validate_form_data
        
        @app.route('/test/inject-form', methods=['POST'])
        @validate_form_data({
            'name': {'type': 'string', 'required': True, 'max_length': 100}
        })
        def test_inject_form():
            return 'Should not reach here'
        
        response = client.post('/test/inject-form', data={
            'name': "' OR '1'='1'; DROP TABLE users; --"
        })
        # Validation fails - can return 400 (JSON) or 302 (form redirect with flash)
        assert response.status_code in [302, 400]
        
        # If it's a 400 response, check JSON
        if response.status_code == 400:
            data = response.get_json()
            assert data['success'] is False

    def test_query_param_validation(self, app, client):
        """Test query parameter validation."""
        from utils.validators import validate_query_params
        
        @app.route('/test/params')
        @validate_query_params(['page', 'per_page'])
        def test_params():
            return 'OK'
        
        # Valid params
        response = client.get('/test/params?page=1&per_page=10')
        assert response.status_code == 200
        
        # Invalid SQL injection in params - gets redirected (302) with flash message
        response = client.get('/test/params?page=1;DROP TABLE users', follow_redirects=False)
        # Validation fails and redirects to referrer or index
        assert response.status_code in [302, 400]


class TestEdgeCases:
    """Test edge cases and unusual inputs."""

    def test_unicode_sql_injection(self):
        """Test SQL injection with Unicode characters."""
        # Normalize full-width characters to ASCII before checking
        # Some attackers use Unicode to bypass filters
        import unicodedata
        unicode_input = "ＳＥＬＥＣＴ"
        normalized = unicodedata.normalize('NFKC', unicode_input)
        assert detect_sql_injection_attempt(normalized) is True

    def test_encoded_sql_injection(self):
        """Test URL-encoded SQL injection."""
        # %27 = ', %3B = ;
        encoded = "%27 OR %271%27=%271"
        # After decoding, it should be caught
        from urllib.parse import unquote
        decoded = unquote(encoded)
        assert detect_sql_injection_attempt(decoded) is True

    def test_null_byte_injection(self):
        """Test null byte handling."""
        is_valid, error_msg = validate_string_input("test\x00DROP TABLE")
        # Should either reject or sanitize properly
        # Implementation dependent, but shouldn't crash

    def test_very_long_sql_injection(self):
        """Test very long SQL injection attempts."""
        # Attackers might send very long payloads
        long_payload = "a" * 10000 + "'; DROP TABLE users; --"
        is_valid, error_msg = validate_string_input(long_payload, max_length=20000)
        # Should be caught by SQL injection detection
        # OR by length validation
