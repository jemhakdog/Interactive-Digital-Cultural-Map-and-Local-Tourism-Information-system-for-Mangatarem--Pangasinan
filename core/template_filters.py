"""
Custom Jinja2 template filters for secure output encoding.

Registers filters that can be used in templates:
- {{ value|sanitize }} - Sanitizes HTML, allowing safe tags
- {{ value|escape_strict }} - Escapes all HTML entities
- {{ value|safe_url }} - Validates and sanitizes URLs
"""

from markupsafe import Markup, escape
from utils.security import sanitize_html_input, sanitize_url


# Allowed HTML tags for rich text rendering in templates
ALLOWED_TEMPLATE_TAGS = [
    'p', 'br', 'strong', 'em', 'u', 'ul', 'ol', 'li', 
    'a', 'h1', 'h2', 'h3', 'blockquote', 'code', 'pre', 'img'
]
ALLOWED_TEMPLATE_ATTRIBUTES = {
    'a': ['href', 'title', 'rel', 'class', 'target'],
    'blockquote': ['cite'],
    'img': ['src', 'alt', 'title', 'class'],
}


def sanitize_html(value):
    """
    Sanitize HTML input for safe rendering.
    
    Use this for user-generated content that needs to preserve
    some HTML formatting (reviews, descriptions, etc.)
    
    Usage in template: {{ review.comment|sanitize }}
    
    Args:
        value: Raw string from database/user input
        
    Returns:
        Markup-safe sanitized HTML
    """
    if value is None:
        return ""
    
    cleaned = sanitize_html_input(
        str(value), 
        allowed_tags=ALLOWED_TEMPLATE_TAGS
    )
    return Markup(cleaned)


def escape_strict(value):
    """
    Escape all HTML entities - no HTML will be rendered.
    
    Use this for fields that should never contain HTML
    (usernames, titles, names, etc.)
    
    Usage in template: {{ user.username|escape_strict }}
    
    Args:
        value: Raw string to escape
        
    Returns:
        HTML-escaped string
    """
    if value is None:
        return ""
    return str(escape(value))


def safe_url(value):
    """
    Validate and sanitize URL for use in href/src attributes.
    
    Blocks javascript:, data:, and other dangerous protocols.
    
    Usage in template: <a href="{{ url|safe_url }}">
    
    Args:
        value: URL string to sanitize
        
    Returns:
        Safe URL or empty string if invalid
    """
    if value is None:
        return ""
    return sanitize_url(str(value))


def register_filters(app):
    """
    Register custom security filters with Flask app.
    
    Call this after creating the Flask app instance.
    
    Args:
        app: Flask application instance
    """
    app.jinja_env.filters['sanitize'] = sanitize_html
    app.jinja_env.filters['escape_strict'] = escape_strict
    app.jinja_env.filters['safe_url'] = safe_url
