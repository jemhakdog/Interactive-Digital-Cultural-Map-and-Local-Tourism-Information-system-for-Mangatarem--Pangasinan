"""
Security utilities for input validation and sanitization.

Provides functions for:
- HTML sanitization using bleach
- Input validation (email, phone, coordinates)
- Filename sanitization
- Output encoding using markupsafe
- SQL injection prevention
- Comprehensive field validation
"""

import re
from typing import Optional, Any
from markupsafe import escape


# Try to import bleach, fallback if not available
try:
    import bleach
    BLEACH_AVAILABLE = True
except ImportError:
    BLEACH_AVAILABLE = False

# Allowed HTML tags for rich text fields (reviews, descriptions)
ALLOWED_TAGS = ['p', 'br', 'strong', 'em', 'u', 'ul', 'ol', 'li', 'a', 'h1', 'h2', 'h3', 'blockquote', 'code', 'pre']
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title', 'rel'],
    'blockquote': ['cite'],
}


def sanitize_html_input(raw_text: str, allowed_tags: Optional[list] = None) -> str:
    """
    Strip potentially malicious HTML from user input.
    
    Uses bleach to clean HTML, allowing only safe tags and attributes.
    Falls back to escape() if bleach is not available.
    
    Args:
        raw_text: Raw user input that may contain HTML
        allowed_tags: Optional list of allowed HTML tags
        
    Returns:
        Sanitized HTML string
    """
    if not raw_text:
        return ""
    
    tags = allowed_tags or ALLOWED_TAGS
    
    if BLEACH_AVAILABLE:
        return bleach.clean(
            raw_text, 
            tags=tags, 
            attributes=ALLOWED_ATTRIBUTES, 
            strip=True
        )
    
    # Fallback: escape all HTML
    return str(escape(raw_text))


def validate_and_escape(raw_text: str) -> str:
    """
    Escape all HTML entities for safe rendering.
    
    Use this for fields that should never contain HTML
    (usernames, titles, etc.)
    
    Args:
        raw_text: Raw user input
        
    Returns:
        HTML-escaped string
    """
    if not raw_text:
        return ""
    return str(escape(raw_text))


def validate_phone(phone: str) -> bool:
    """
    Validate phone number contains only digits, spaces, dashes, and plus.
    
    Args:
        phone: Phone number string to validate
        
    Returns:
        True if valid phone format, False otherwise
    """
    if not phone:
        return False
    return bool(re.match(r'^[\d\s\-\+\(\)]{7,20}$', phone))


def validate_coordinates(lat: float, lng: float) -> bool:
    """
    Validate geographic coordinates are within reasonable bounds.
    
    Args:
        lat: Latitude value
        lng: Longitude value
        
    Returns:
        True if coordinates are valid, False otherwise
    """
    try:
        lat_f = float(lat)
        lng_f = float(lng)
        return -90 <= lat_f <= 90 and -180 <= lng_f <= 180
    except (TypeError, ValueError):
        return False


def sanitize_filename(filename: str) -> str:
    """
    Remove path traversal and dangerous characters from filenames.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename safe for storage
    """
    if not filename:
        return ""
    
    # Remove path components
    filename = filename.split('/')[-1].split('\\')[-1]
    
    # Remove dangerous characters
    filename = re.sub(r'[^\w\-_\.]', '_', filename)
    
    # Remove multiple dots (prevent extension bypass)
    filename = re.sub(r'\.{2,}', '.', filename)
    
    # Remove leading dots
    filename = filename.lstrip('.')
    
    # Truncate to reasonable length
    return filename[:255]


def validate_email_format(email: str) -> bool:
    """
    Strict email validation.
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid email format, False otherwise
    """
    if not email:
        return False
    return bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email))


def validate_username(username: str) -> bool:
    """
    Validate username format (alphanumeric + underscore only).
    
    Args:
        username: Username to validate
        
    Returns:
        True if valid username format, False otherwise
    """
    if not username:
        return False
    return bool(re.match(r'^[a-zA-Z0-9_]{3,30}$', username))


def validate_password_strength(password: str, min_length: int = 8) -> tuple[bool, str]:
    """
    Validate password meets minimum strength requirements.
    
    Args:
        password: Password to validate
        min_length: Minimum password length
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not password:
        return False, "Password is required"
    
    if len(password) < min_length:
        return False, f"Password must be at least {min_length} characters"
    
    if len(password) > 128:
        return False, "Password is too long (max 128 characters)"
    
    return True, ""


def truncate_safe(text: str, max_length: int = 500) -> str:
    """
    Truncate text safely, escaping HTML first.
    
    Args:
        text: Text to truncate
        max_length: Maximum length of output
        
    Returns:
        Truncated and escaped text
    """
    if not text:
        return ""
    
    escaped = str(escape(text))
    if len(escaped) <= max_length:
        return escaped
    return escaped[:max_length] + '...'


def sanitize_url(url: str) -> str:
    """
    Validate and sanitize URL, preventing javascript: protocols.

    Args:
        url: URL to sanitize

    Returns:
        Safe URL or empty string if invalid
    """
    if not url:
        return ""

    # Remove whitespace and control characters
    url = re.sub(r'[\s\x00-\x1f]', '', url)

    # Block dangerous protocols
    dangerous_protocols = ['javascript:', 'data:', 'vbscript:', 'file:']
    url_lower = url.lower()

    for protocol in dangerous_protocols:
        if url_lower.startswith(protocol):
            return ""

    # Allow safe protocols
    if url_lower.startswith(('http://', 'https://', '/', '#', 'mailto:', 'tel:')):
        return url[:500]  # Truncate to reasonable length

    # Relative URLs
    if not url_lower.startswith(('http', 'ftp')):
        return url[:500]

    return ""


def detect_sql_injection_attempt(input_str: str) -> bool:
    """
    Detect potential SQL injection patterns in input.

    Args:
        input_str: Input string to check

    Returns:
        True if SQL injection pattern detected, False otherwise
    """
    if not input_str:
        return False

    # Common SQL injection patterns
    sql_patterns = [
        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|ALTER|CREATE|EXEC)\b)",
        r"(--|/\*|\*/)",  # SQL comments (removed ;, @@, @ to reduce false positives)
        r"(\bOR\b\s+\d+=\d+)",
        r"(\bAND\b\s+\d+=\d+)",
        r"('(\s)*(OR|AND)(\s)*')",
        r"(EXEC(\s)*\()",
        r"(xp_cmdshell|INFORMATION_SCHEMA|sys\.tables)",
    ]

    input_upper = input_str.upper()
    for pattern in sql_patterns:
        if re.search(pattern, input_upper, re.IGNORECASE):
            return True

    return False


def validate_string_input(value: str, min_length: int = 0, max_length: int = 500,
                          allowed_pattern: Optional[str] = None,
                          block_sql_injection: bool = True) -> tuple[bool, str]:
    """
    Validate string input with comprehensive checks.

    Args:
        value: String value to validate
        min_length: Minimum allowed length
        max_length: Maximum allowed length
        allowed_pattern: Regex pattern for allowed characters
        block_sql_injection: Whether to check for SQL injection

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not value and min_length > 0:
        return False, "Input is required"

    if not value:
        return True, ""

    if len(value) < min_length:
        return False, f"Input must be at least {min_length} characters"

    if len(value) > max_length:
        return False, f"Input must be no more than {max_length} characters"

    if block_sql_injection and detect_sql_injection_attempt(value):
        return False, "Invalid characters detected"

    if allowed_pattern and not re.match(allowed_pattern, value):
        return False, "Input contains invalid characters"

    return True, ""


def validate_integer(value: Any, min_value: Optional[int] = None,
                    max_value: Optional[int] = None) -> tuple[bool, int, str]:
    """
    Validate and safely convert integer input.

    Args:
        value: Value to validate and convert
        min_value: Minimum allowed value
        max_value: Maximum allowed value

    Returns:
        Tuple of (is_valid, sanitized_value, error_message)
    """
    try:
        int_value = int(value)
    except (ValueError, TypeError):
        return False, 0, "Invalid integer value"

    if min_value is not None and int_value < min_value:
        return False, 0, f"Value must be at least {min_value}"

    if max_value is not None and int_value > max_value:
        return False, 0, f"Value must be no more than {max_value}"

    return True, int_value, ""


def validate_float(value: Any, min_value: Optional[float] = None,
                  max_value: Optional[float] = None) -> tuple[bool, float, str]:
    """
    Validate and safely convert float input.

    Args:
        value: Value to validate and convert
        min_value: Minimum allowed value
        max_value: Maximum allowed value

    Returns:
        Tuple of (is_valid, sanitized_value, error_message)
    """
    try:
        float_value = float(value)
    except (ValueError, TypeError):
        return False, 0.0, "Invalid numeric value"

    if min_value is not None and float_value < min_value:
        return False, 0.0, f"Value must be at least {min_value}"

    if max_value is not None and float_value > max_value:
        return False, 0.0, f"Value must be no more than {max_value}"

    return True, float_value, ""


def validate_boolean(value: Any) -> tuple[bool, bool]:
    """
    Validate and convert boolean input.

    Args:
        value: Value to convert

    Returns:
        Tuple of (is_valid, sanitized_value)
    """
    if isinstance(value, bool):
        return True, value

    if isinstance(value, str):
        if value.lower() in ['true', '1', 'yes', 'on']:
            return True, True
        elif value.lower() in ['false', '0', 'no', 'off']:
            return True, False

    if isinstance(value, (int, float)):
        if value in [0, 1]:
            return True, bool(value)

    return False, False


def sanitize_for_display(value: str, max_length: Optional[int] = None) -> str:
    """
    Sanitize string for safe display in UI (escape all HTML).

    Args:
        value: String to sanitize
        max_length: Optional maximum length

    Returns:
        HTML-escaped string safe for display
    """
    if not value:
        return ""

    escaped = str(escape(value))

    if max_length and len(escaped) > max_length:
        return escaped[:max_length] + '...'

    return escaped
