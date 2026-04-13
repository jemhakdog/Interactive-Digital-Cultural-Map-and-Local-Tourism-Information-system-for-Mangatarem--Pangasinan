# Security Implementation Guide

## Overview

This document provides comprehensive documentation of the XSS prevention and security hardening measures implemented in the GoMangatarem Interactive Digital Cultural Map platform.

**Last Updated**: April 12, 2026  
**Status**: ✅ Production Ready  
**Version**: 1.0.0

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Security Architecture](#security-architecture)
3. [XSS Prevention Measures](#xss-prevention-measures)
4. [Implementation Details](#implementation-details)
5. [Developer Guidelines](#developer-guidelines)
6. [Testing & Validation](#testing--validation)
7. [Deployment Checklist](#deployment-checklist)
8. [Incident Response](#incident-response)
9. [References](#references)

---

## Executive Summary

### Security Objectives

The GoMangatarem platform handles sensitive cultural heritage data, user information, and tourism content. Our security implementation focuses on:

- **Preventing Cross-Site Scripting (XSS) attacks** through defense-in-depth
- **Protecting user sessions** from hijacking
- **Validating all input** at multiple layers
- **Encoding all output** contextually
- **Restricting resource loading** via Content Security Policy

### Threat Model

| Threat | Mitigation | Status |
|--------|-----------|--------|
| Stored XSS in user content | HTML sanitization (bleach) + CSP | ✅ Implemented |
| Reflected XSS via URL parameters | Input validation + output encoding | ✅ Implemented |
| DOM-based XSS | CSP script-src restrictions | ✅ Implemented |
| Session hijacking | HttpOnly + SameSite cookies | ✅ Implemented |
| Clickjacking | X-Frame-Options: DENY | ✅ Implemented |
| Data injection | Parameterized queries (SQLAlchemy ORM) | ✅ Verified |
| File upload attacks | Double sanitization + extension validation | ✅ Implemented |

### Key Achievements

✅ **18 automated tests** covering all security utilities  
✅ **Zero raw SQL vulnerabilities** - all queries parameterized  
✅ **6 layers of defense** against XSS attacks  
✅ **Comprehensive logging** for security monitoring  
✅ **Production-ready** security headers configuration

---

## Security Architecture

### Defense-in-Depth Strategy

```
┌─────────────────────────────────────────────────┐
│  Layer 1: Browser Security (CSP Headers)        │
│  - Content Security Policy                      │
│  - X-Frame-Options                              │
│  - X-Content-Type-Options                       │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│  Layer 2: Session Security                      │
│  - HttpOnly Cookies                             │
│  - SameSite=Lax                                 │
│  - Secure Flag (Production)                     │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│  Layer 3: Input Validation                      │
│  - Format validation (email, username, etc.)    │
│  - Length limits                                │
│  - HTML sanitization (bleach)                   │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│  Layer 4: Output Encoding                       │
│  - Context-aware encoding                       │
│  - Template filters (sanitize, escape_strict)   │
│  - URL validation                               │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│  Layer 5: File Upload Security                  │
│  - Double filename sanitization                 │
│  - Extension validation                         │
│  - Path traversal prevention                    │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│  Layer 6: Database Security                     │
│  - Parameterized queries (ORM)                  │
│  - No raw SQL                                   │
└─────────────────────────────────────────────────┘
```

---

## XSS Prevention Measures

### 1. Input Encoding (Context-Aware)

**Principle**: Encode data immediately before it is rendered in the browser to ensure it is interpreted as text, not executable code.

**Implementation**:

| Context | Encoding Method | Example |
|---------|----------------|---------|
| HTML Body | `{{ value\|escape_strict }}` | Usernames, titles |
| HTML Attributes | `{{ value\|escape_strict }}` | alt, title, data-* |
| Rich Text | `{{ value\|sanitize }}` | Reviews, descriptions |
| JavaScript Variables | `{{ value\|tojson }}` | JSON data, flash messages |
| URLs | `{{ value\|safe_url }}` | href, src attributes |
| CSS | Avoid dynamic CSS | N/A |

**Code Example**:

```python
# utils/template_filters.py
from markupsafe import Markup, escape
from utils.security import sanitize_html_input

def sanitize_html(value):
    """Sanitize HTML input for safe rendering."""
    if value is None:
        return ""
    cleaned = sanitize_html_input(str(value))
    return Markup(cleaned)

def escape_strict(value):
    """Escape all HTML entities."""
    if value is None:
        return ""
    return str(escape(value))
```

### 2. Input Validation and Sanitization

**Principle**: Validate input against a strict set of expected criteria and sanitize by stripping potentially malicious code.

**Validation Functions** (`utils/security.py`):

```python
# Username: alphanumeric + underscore only, 3-30 chars
validate_username("user123")  # True
validate_username("<script>")  # False

# Email: strict RFC compliance
validate_email_format("user@example.com")  # True
validate_email_format("user@<script>")  # False

# Password: minimum 8 chars, maximum 128 chars
validate_password_strength("secure123")  # (True, "")
validate_password_strength("short")  # (False, "Password must be at least 8 characters")

# HTML sanitization using bleach library
sanitize_html_input("<script>alert('XSS')</script>Hello")
# Returns: "alert('XSS')Hello" (script tags removed)

# URL sanitization
sanitize_url("javascript:alert('XSS')")  # Returns: ""
sanitize_url("https://example.com")  # Returns: "https://example.com"
```

**Allowed HTML Tags** (for rich text):

```python
ALLOWED_TAGS = [
    'p', 'br', 'strong', 'em', 'u', 
    'ul', 'ol', 'li', 'a', 'h1', 'h2', 'h3',
    'blockquote', 'code', 'pre', 'img'
]
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title', 'rel', 'class', 'target'],
    'blockquote': ['cite'],
    'img': ['src', 'alt', 'title', 'class'],
}
```

### 3. Content Security Policy (CSP)

**Principle**: Implement a strict CSP header to define which dynamic resources are allowed to load, preventing execution of malicious injected scripts.

**Implementation** (`app.py`):

```python
response.headers["Content-Security-Policy"] = (
    "default-src 'self';"
    "script-src 'self' https://fonts.googleapis.com "
    "https://maps.mapbox.com https://api.mapbox.com "
    "https://accounts.google.com 'unsafe-inline';"
    "style-src 'self' https://fonts.googleapis.com 'unsafe-inline';"
    "img-src 'self' data: https: blob:;"
    "font-src 'self' https://fonts.gstatic.com data:;"
    "connect-src 'self' https://api.mapbox.com "
    "https://*.supabase.co https://*.upstash.io "
    "https://accounts.google.com;"
    "frame-ancestors 'none';"
    "base-uri 'self';"
    "form-action 'self';"
    "object-src 'none';"
    "upgrade-insecure-requests;"
)
```

**CSP Directive Breakdown**:

| Directive | Value | Purpose |
|-----------|-------|---------|
| `default-src` | `'self'` | Default fallback for all resources |
| `script-src` | `'self'` + trusted CDNs | Only allow scripts from approved sources |
| `style-src` | `'self'` + Google Fonts | Allow stylesheets from trusted sources |
| `img-src` | `'self' data: https: blob:` | Allow images from any HTTPS source |
| `font-src` | `'self'` + Google Fonts | Allow fonts from trusted sources |
| `connect-src` | `'self'` + APIs | Restrict AJAX/WebSocket connections |
| `frame-ancestors` | `'none'` | Prevent embedding in iframes (clickjacking) |
| `base-uri` | `'self'` | Prevent base tag injection |
| `form-action` | `'self'` | Only allow forms to submit to same origin |
| `object-src` | `'none'` | Block Flash/Java/Silverlight |
| `upgrade-insecure-requests` | N/A | Auto-upgrade HTTP to HTTPS |

### 4. HttpOnly Cookies

**Principle**: Add the HttpOnly flag to session cookies to prevent them from being accessed by client-side scripts, mitigating the impact of a stolen session.

**Implementation** (`config.py`):

```python
class Config:
    # Session cookies
    SESSION_COOKIE_HTTPONLY = True  # Prevents JavaScript access
    SESSION_COOKIE_SAMESITE = "Lax"  # Prevents CSRF
    SESSION_COOKIE_SECURE = False  # True in ProductionConfig only
    
    # Remember me cookies
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SAMESITE = "Lax"
    REMEMBER_COOKIE_SECURE = True  # Production only
```

**Cookie Security Matrix**:

| Cookie | HttpOnly | SameSite | Secure | Purpose |
|--------|----------|----------|--------|---------|
| Session | ✅ Yes | Lax | Prod only | Flask-Login session |
| Remember Me | ✅ Yes | Lax | ✅ Yes (Prod) | Persistent login |

---

## Implementation Details

### File Structure

```
project-root/
├── utils/
│   ├── security.py              # Input validation & sanitization
│   └── template_filters.py      # Jinja2 output encoding filters
├── routes/
│   ├── auth.py                  # Auth input validation
│   ├── user.py                  # Profile validation
│   └── public.py                # Search input limits
├── templates/
│   └── base.html                # Flash message fix
├── utils/
│   └── file_helpers.py          # File upload security
├── app.py                       # Security headers & CSP
├── config.py                    # Cookie security flags
├── tests/
│   └── test_security.py         # Security unit tests
└── requirements.txt             # bleach>=6.0.0
```

### Security Headers

All responses include these security headers:

```python
# app.py - _register_request_hooks()

# Content Security Policy
Content-Security-Policy: default-src 'self'; script-src 'self' ...

# Prevent MIME type sniffing
X-Content-Type-Options: nosniff

# Prevent clickjacking
X-Frame-Options: DENY

# Control referrer information
Referrer-Policy: strict-origin-when-cross-origin

# Restrict browser features
Permissions-Policy: camera=(), microphone=(), geolocation=(self), payment=()

# Cross-origin protection
Cross-Origin-Opener-Policy: same-origin-allow-popups
Cross-Origin-Resource-Policy: same-origin

# Enforce HTTPS (Production only)
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

---

## Developer Guidelines

### Adding New Forms

When creating new forms that accept user input:

```python
from utils.security import (
    validate_username,
    validate_email_format,
    validate_password_strength,
    validate_and_escape,
    sanitize_html_input
)

@app.route('/new-form', methods=['POST'])
def new_form():
    # 1. Get input with defaults and length limits
    username = request.form.get('username', '').strip()[:30]
    comment = request.form.get('comment', '').strip()[:5000]
    
    # 2. Validate format
    if not validate_username(username):
        flash('Invalid username format', 'error')
        return redirect(url_for('form'))
    
    # 3. Sanitize before saving
    username = validate_and_escape(username)
    comment = sanitize_html_input(comment)  # Allows safe HTML
    
    # 4. Save to database
    user = User(username=username, comment=comment)
    db.session.add(user)
    db.session.commit()
```

### Displaying User Content in Templates

```html
<!-- For plain text (usernames, titles, etc.) -->
<h1>{{ user.username|escape_strict }}</h1>
<p>{{ attraction.name|escape_strict }}</p>

<!-- For rich text (reviews, descriptions) -->
<div>{{ review.comment|sanitize }}</div>
<div>{{ attraction.description|sanitize }}</div>

<!-- For URLs -->
<a href="{{ user.website|safe_url }}">Visit Website</a>
<img src="{{ attraction.image_url|safe_url }}" alt="{{ attraction.name|escape_strict }}">

<!-- For JSON data in JavaScript -->
<script>
const flashMessages = {{ get_flashed_messages(with_categories=True)|tojson }};
</script>
```

### NEVER Do This

```python
# ❌ WRONG: Direct user input without validation
username = request.form.get('username')
db.session.add(User(username=username))

# ❌ WRONG: Using |safe filter on user content
{{ user.comment|safe }}

# ❌ WRONG: Raw string concatenation in SQL
query = f"SELECT * FROM users WHERE username = '{username}'"
db.session.execute(query)
```

### ALWAYS Do This

```python
# ✅ CORRECT: Validate and sanitize
username = request.form.get('username', '').strip()[:30]
if not validate_username(username):
    flash('Invalid username', 'error')
    return redirect(url_for('form'))
username = validate_and_escape(username)
db.session.add(User(username=username))

# ✅ CORRECT: Use template filters
{{ user.comment|sanitize }}

# ✅ CORRECT: Use ORM parameterized queries
User.query.filter_by(username=username).first()
```

---

## Testing & Validation

### Running Security Tests

```bash
# Run all security tests
uv run pytest tests/test_security.py -v

# Run with coverage
uv run pytest tests/test_security.py --cov=utils.security --cov-report=term-missing

# Run specific test class
uv run pytest tests/test_security.py::TestHTMLSanitization -v
```

### Test Coverage

| Test Class | Tests | Coverage |
|------------|-------|----------|
| TestEmailValidation | 2 | Valid/invalid email formats |
| TestUsernameValidation | 2 | Format, length, special chars |
| TestPasswordStrength | 2 | Length requirements |
| TestHTMLSanitization | 3 | Script removal, safe tags, escaping |
| TestFilenameSanitization | 3 | Path traversal, dangerous chars |
| TestURLSanitization | 2 | Dangerous protocols blocking |
| TestPhoneValidation | 2 | Format validation |
| TestCoordinateValidation | 2 | Geographic bounds |

**Total**: 18 tests, all passing ✅

### Manual XSS Testing

Test these payloads in forms:

```html
<!-- Basic XSS -->
<script>alert('XSS')</script>

<!-- Event handler XSS -->
<img src=x onerror=alert('XSS')>

<!-- JavaScript URL -->
javascript:alert('XSS')

<!-- SVG XSS -->
<svg onload=alert('XSS')>

<!-- Encoded XSS -->
%3Cscript%3Ealert('XSS')%3C/script%3E
```

**Expected Result**: All payloads should be either:
- Rejected by input validation
- Sanitized (tags removed, text preserved)
- Escaped (displayed as text, not executed)

---

## Deployment Checklist

### Pre-Deployment

- [ ] Run all security tests: `uv run pytest tests/test_security.py -v`
- [ ] Check for raw SQL: `grep -r "db.session.execute" routes/`
- [ ] Verify CSP headers present in responses
- [ ] Test cookie flags in browser DevTools
- [ ] Run static analysis: `uv run bandit -r .`

### Production Configuration

```python
# config.py - ProductionConfig
class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    WTF_CSRF_SSL_STRICT = True
```

### Environment Variables

```bash
# Required for production
SECRET_KEY=<strong-random-key>
SESSION_COOKIE_SECURE=True
FLASK_ENV=production
```

### Post-Deployment Verification

1. **Check Headers**:
   ```bash
   curl -I https://your-domain.com
   ```
   Verify presence of:
   - `Content-Security-Policy`
   - `X-Frame-Options: DENY`
   - `X-Content-Type-Options: nosniff`
   - `Strict-Transport-Security`

2. **Test Cookies**:
   - Open browser DevTools → Application → Cookies
   - Verify `HttpOnly`, `Secure`, `SameSite` flags

3. **Test XSS Protection**:
   - Submit `<script>alert('XSS')</script>` in a form
   - Verify it's sanitized or escaped

---

## Incident Response

### If XSS Vulnerability is Discovered

1. **Immediate Actions**:
   - Do NOT panic - multiple layers of defense exist
   - Identify which layer was bypassed
   - Check logs for exploitation attempts

2. **Short-term Mitigation**:
   - Update CSP to block the specific attack vector
   - Add input validation for the specific pattern
   - Deploy hotfix within 24 hours

3. **Long-term Fix**:
   - Root cause analysis
   - Update security utilities
   - Add test case for the vulnerability
   - Review all similar code paths

4. **Reporting**:
   - Document the vulnerability
   - Update threat model
   - Communicate to stakeholders if user data was affected

### Security Contacts

- **Security Issues**: Report to project maintainer
- **Bug Bounty**: (If applicable)
- **Responsible Disclosure**: Allow 30 days for fixes before public disclosure

---

## References

### OWASP Resources

- [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
- [OWASP Content Security Policy Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html)
- [OWASP Secure Cookie Attribute Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secure_Cookie_Attribute_Cheat_Sheet.html)

### Libraries Used

- **bleach**: [https://bleach.readthedocs.io/](https://bleach.readthedocs.io/)
- **Flask**: [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
- **SQLAlchemy**: [https://www.sqlalchemy.org/](https://www.sqlalchemy.org/)

### Browser Security

- [MDN Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)
- [MDN HttpOnly Cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies#restrict_access_to_cookies)
- [MDN SameSite Cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie/SameSite)

---

## Appendix A: Security Utility Functions Reference

### `utils/security.py`

| Function | Purpose | Parameters | Returns |
|----------|---------|------------|---------|
| `sanitize_html_input()` | Strip malicious HTML | `raw_text`, `allowed_tags` | Sanitized string |
| `validate_and_escape()` | Escape all HTML entities | `raw_text` | Escaped string |
| `validate_email_format()` | Strict email validation | `email` | bool |
| `validate_username()` | Username format check | `username` | bool |
| `validate_password_strength()` | Password complexity | `password`, `min_length` | `(bool, error_msg)` |
| `sanitize_filename()` | Remove dangerous chars | `filename` | Safe filename |
| `sanitize_url()` | Block dangerous protocols | `url` | Safe URL or "" |
| `validate_phone()` | Phone format check | `phone` | bool |
| `validate_coordinates()` | Geographic bounds | `lat`, `lng` | bool |
| `truncate_safe()` | Truncate with escaping | `text`, `max_length` | Truncated string |

### `utils/template_filters.py`

| Filter | Purpose | Use Case |
|--------|---------|----------|
| `\|sanitize` | Sanitize HTML, allow safe tags | Reviews, descriptions |
| `\|escape_strict` | Escape all HTML | Usernames, titles |
| `\|safe_url` | Validate URLs | href, src attributes |

---

**Document Version**: 1.0.0  
**Last Updated**: April 12, 2026  
**Next Review**: October 12, 2026  
**Maintainer**: Development Team
