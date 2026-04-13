# Deployment Security Checklist

## Overview

This checklist ensures all security measures are properly configured before and after deploying the GoMangatarem platform to production.

**Last Updated**: April 12, 2026  
**Version**: 1.0.0

---

## Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Environment Configuration](#environment-configuration)
3. [Security Headers Verification](#security-headers-verification)
4. [Cookie Security Verification](#cookie-security-verification)
5. [Database Security](#database-security)
6. [File Upload Security](#file-upload-security)
7. [Rate Limiting](#rate-limiting)
8. [Post-Deployment Testing](#post-deployment-testing)
9. [Ongoing Monitoring](#ongoing-monitoring)
10. [Incident Response](#incident-response)

---

## Pre-Deployment Checklist

### Code Quality

- [ ] All security tests passing:
  ```bash
  uv run pytest tests/test_security.py -v
  ```

- [ ] No raw SQL queries in codebase:
  ```bash
  grep -r "db.session.execute" routes/ --include="*.py"
  grep -r "\.text(" routes/ --include="*.py"
  ```
  **Expected**: Only legitimate uses in `utils/tile_generator.py` with parameterized queries

- [ ] No `|safe` filters on user-generated content in templates:
  ```bash
  grep -r "|safe" templates/ --include="*.html" | grep -v "tojson"
  ```
  **Expected**: Only `|safe` should be in `url_for()` contexts or static content

- [ ] Static analysis completed:
  ```bash
  uv run bandit -r . -ll
  ```
  **Expected**: No high/critical severity issues

### Dependencies

- [ ] All dependencies up to date:
  ```bash
  uv pip compile requirements.in -o requirements.txt
  ```

- [ ] `bleach` package included in `requirements.txt`:
  ```bash
  grep bleach requirements.txt
  ```
  **Expected**: `bleach>=6.0.0`

- [ ] No known vulnerabilities in dependencies:
  ```bash
  uv pip check
  ```

### Configuration Files

- [ ] `config.py` has production security flags:
  ```python
  class ProductionConfig(Config):
      DEBUG = False
      SESSION_COOKIE_SECURE = True
      REMEMBER_COOKIE_SECURE = True
      WTF_CSRF_SSL_STRICT = True
  ```

- [ ] `app.py` includes security headers in `_register_request_hooks()`:
  - Content-Security-Policy
  - X-Frame-Options: DENY
  - X-Content-Type-Options: nosniff
  - Referrer-Policy
  - Permissions-Policy
  - Strict-Transport-Security (conditional on SESSION_COOKIE_SECURE)

- [ ] Template filters registered in `create_app()`:
  ```python
  from utils.template_filters import register_filters
  register_filters(app)
  ```

---

## Environment Configuration

### Required Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `SECRET_KEY` | ✅ Yes | Cryptographically secure random key for session signing | `openssl rand -hex 32` |
| `FLASK_ENV` | ✅ Yes | Must be `production` in production environment | `production` |
| `DATABASE_URL` | ✅ Yes | Supabase connection pooler URI | `postgresql://user:pass@db.host:6543/postgres` |
| `SUPABASE_URL` | ✅ Yes | Supabase project URL | `https://xxxxx.supabase.co` |
| `SUPABASE_KEY` | ✅ Yes | Supabase service role key | `eyJhbG...` |
| `MAIL_SERVER` | ✅ Yes | SMTP server for email notifications | `smtp.gmail.com` |
| `MAIL_USERNAME` | ✅ Yes | SMTP account | `noreply@domain.com` |
| `MAIL_PASSWORD` | ✅ Yes | SMTP password/app password | `xxxx xxxx xxxx xxxx` |

### Secret Key Generation

Generate a cryptographically secure secret key:

```bash
# Option 1: Using openssl
openssl rand -hex 32

# Option 2: Using Python
python -c "import secrets; print(secrets.token_hex(32))"

# Option 3: Using uv
uv run python -c "import secrets; print(secrets.token_hex(32))"
```

**NEVER** use:
- Hardcoded keys from documentation
- Simple strings like "password" or "secret"
- Keys shorter than 32 characters

### Vercel Environment Variables Setup

1. Go to **Vercel Dashboard** → Your Project → **Settings** → **Environment Variables**
2. Add each variable from the table above
3. Set scope to **Production** (and Preview/Development if needed)
4. Click **Save**

---

## Security Headers Verification

### Testing Headers

After deployment, verify all security headers are present:

```bash
curl -I https://your-domain.com
```

**Expected Response Headers**:

```
HTTP/2 200
content-type: text/html; charset=utf-8

# Security Headers
content-security-policy: default-src 'self'; script-src 'self' https://fonts.googleapis.com https://maps.mapbox.com https://api.mapbox.com https://accounts.google.com 'unsafe-inline'; ...
x-content-type-options: nosniff
x-frame-options: DENY
referrer-policy: strict-origin-when-cross-origin
permissions-policy: camera=(), microphone=(), geolocation=(self), payment=()
cross-origin-opener-policy: same-origin-allow-popups
cross-origin-resource-policy: same-origin
strict-transport-security: max-age=31536000; includeSubDomains
```

### Header Validation Checklist

- [ ] `Content-Security-Policy` present and correctly formatted
- [ ] `X-Frame-Options: DENY` present (prevents clickjacking)
- [ ] `X-Content-Type-Options: nosniff` present (prevents MIME sniffing)
- [ ] `Referrer-Policy: strict-origin-when-cross-origin` present
- [ ] `Permissions-Policy` present with restricted features
- [ ] `Strict-Transport-Security` present (HTTPS enforcement)
- [ ] `Cross-Origin-Opener-Policy` present
- [ ] `Cross-Origin-Resource-Policy` present

### CSP Validation

Use online tools to validate CSP:

```bash
# Using report-uri.com CSP validator
# Visit: https://cspvalidator.org/

# Or use Mozilla's CSP Evaluator
# Visit: https://csp-evaluator.withgoogle.com/
```

**Common CSP Issues**:

| Issue | Solution |
|-------|----------|
| Inline scripts blocked | Add nonce or move to external file |
| External fonts not loading | Add font CDN to `font-src` |
| Map not rendering | Ensure Mapbox domains in `script-src` and `connect-src` |
| Google Sign-In not working | Ensure `accounts.google.com` in allowed sources |

---

## Cookie Security Verification

### Testing Cookies

1. Open browser DevTools → **Application** → **Cookies** → Your Domain
2. Check the following cookies:

| Cookie | HttpOnly | Secure | SameSite | Expected Value |
|--------|----------|--------|----------|----------------|
| `session` | ✅ Yes | ✅ Yes (HTTPS) | Lax | Flask session cookie |
| `remember_token` | ✅ Yes | ✅ Yes | Lax | Remember me token |

### Validation Checklist

- [ ] `session` cookie has `HttpOnly` flag set
- [ ] `session` cookie has `Secure` flag set (HTTPS only)
- [ ] `session` cookie has `SameSite=Lax` attribute
- [ ] `remember_token` cookie has `HttpOnly` flag set
- [ ] `remember_token` cookie has `Secure` flag set
- [ ] `remember_token` cookie has `SameSite=Lax` attribute

### Testing in Browser Console

```javascript
// Try to access cookies from JavaScript (should fail due to HttpOnly)
console.log(document.cookie);
// Expected: Should NOT show session cookie value
```

---

## Database Security

### Connection Security

- [ ] Using **Transaction Pooler** (Port 6543) for production
- [ ] Connection string uses strong database password
- [ ] Database user has minimal required permissions
- [ ] SSL/TLS enabled for database connections

### Query Security

- [ ] All queries use SQLAlchemy ORM (parameterized by default)
- [ ] No raw SQL string concatenation
- [ ] MVT tile generator uses `text()` with bound parameters
- [ ] Database migrations reviewed for SQL injection

### Data Protection

- [ ] Passwords hashed with `werkzeug.security.generate_password_hash`
- [ ] Password reset tokens are single-use and time-limited
- [ ] Sensitive data not logged (check `utils/logger_helper.py`)
- [ ] API endpoints return only necessary data

---

## File Upload Security

### Configuration

- [ ] `UPLOAD_FOLDER` is outside web root (if possible)
- [ ] `ALLOWED_EXTENSIONS` restricts to safe file types
- [ ] File size limits configured (default: Flask's 16MB)

### Testing File Uploads

Test these malicious filenames:

```
../../etc/passwd
<script>alert('XSS')</script>.jpg
file.php.png
%2e%2e%2f%2e%2e%2fetc%2fpasswd
```

**Expected Results**:
- All files rejected or sanitized
- Saved filenames contain only alphanumeric, underscore, hyphen, and single dot
- No directory traversal possible
- No executable files uploaded

### Validation Checklist

- [ ] Double sanitization applied: `secure_filename(sanitize_filename(file.filename))`
- [ ] Extension validation after sanitization
- [ ] Uploaded files served as static content (not executed)
- [ ] File upload errors logged securely

---

## Rate Limiting

### Current Configuration

```python
# extensions.py
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="memory://",
    default_limits=["100 per minute"],
)

# routes/auth.py
@auth_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute")

@auth_bp.route("/register", methods=["GET", "POST"])
@limiter.limit("5 per minute")

# routes/api.py
@api_bp.route("/attractions")
@limiter.limit("20 per minute")
```

### Validation Checklist

- [ ] Authentication endpoints limited to 5 requests/minute
- [ ] API endpoints limited to 20 requests/minute
- [ ] Search endpoint limited to 20 requests/minute
- [ ] Rate limit headers present in responses:
  ```
  X-RateLimit-Limit: 5
  X-RateLimit-Remaining: 4
  X-RateLimit-Reset: 1617234567
  ```

### Testing Rate Limits

```bash
# Send 6 rapid requests to login endpoint
for i in {1..6}; do
  curl -X POST https://your-domain.com/login
  echo "Request $i: $?"
done
```

**Expected**: 6th request should return `429 Too Many Requests`

---

## Post-Deployment Testing

### Automated Security Tests

```bash
# Run full test suite
uv run pytest tests/ -v --cov=. --cov-report=html

# Run security-specific tests
uv run pytest tests/test_security.py -v

# Check coverage
uv run pytest tests/test_security.py --cov=utils.security --cov-report=term-missing
```

### Manual Penetration Testing

#### XSS Testing

Test these payloads in all form fields:

```html
<script>alert('XSS')</script>
<img src=x onerror=alert('XSS')>
<svg onload=alert('XSS')>
javascript:alert('XSS')
"><script>alert('XSS')</script>
```

**Expected**: All payloads sanitized or escaped.

#### SQL Injection Testing

Test these payloads in search and filter fields:

```
' OR '1'='1
" OR "1"="1
' UNION SELECT NULL--
"; DROP TABLE users--
```

**Expected**: Treated as literal strings, no SQL errors exposed.

#### Authentication Testing

- [ ] Try login with SQL injection in username field
- [ ] Try login with SQL injection in password field
- [ ] Try registration with duplicate usernames
- [ ] Try registration with duplicate emails
- [ ] Try registration with XSS in username
- [ ] Test password reset token reuse (should fail)
- [ ] Test expired password reset tokens (should fail)

#### Authorization Testing

- [ ] Try accessing `/admin` as regular user
- [ ] Try accessing `/user` without login
- [ ] Try accessing another user's profile edit
- [ ] Try submitting forms without CSRF token

### Browser DevTools Testing

1. **Console**: Check for JavaScript errors
2. **Network**: Verify HTTPS for all requests
3. **Application**: Check cookie flags
4. **Sources**: Verify no inline scripts with user data

---

## Ongoing Monitoring

### Log Monitoring

Monitor these logs for security incidents:

| Log Source | What to Monitor | Alert Threshold |
|------------|----------------|-----------------|
| **Vercel Logs** | 4xx/5xx errors, CSP violations | >10% error rate |
| **Application Logs** | Failed logins, validation failures | >50/hour |
| **Database Logs** | Slow queries, connection errors | >5 second queries |
| **Rate Limiter** | 429 responses | >100/hour |

### Security Log Examples

```python
# Failed login attempts (routes/auth.py)
log_error("auth", "login", f"Invalid credentials for '{username}'")

# Validation failures (routes/auth.py)
log_error("auth", "register", f"Username '{username}' already exists")

# File upload rejections (utils/file_helpers.py)
logger.warning("Rejected uploaded file with invalid name: %s", file.filename)
```

### Regular Security Audits

**Monthly**:
- [ ] Review application logs for anomalies
- [ ] Check dependency vulnerabilities
- [ ] Test rate limiting effectiveness

**Quarterly**:
- [ ] Full penetration test
- [ ] CSP policy review
- [ ] Cookie security review
- [ ] Database permission audit

**Annually**:
- [ ] Complete security audit
- [ ] Update threat model
- [ ] Review and update this checklist
- [ ] Security training for developers

---

## Incident Response

### Security Incident Detected

1. **Immediate Actions** (within 1 hour):
   - [ ] Identify the vulnerability being exploited
   - [ ] Determine affected endpoints/users
   - [ ] Enable enhanced logging if not already active
   - [ ] Notify project maintainer

2. **Short-term Mitigation** (within 24 hours):
   - [ ] Deploy CSP update if XSS exploited
   - [ ] Block offending IP addresses if brute force
   - [ ] Rotate secret keys if compromised
   - [ ] Patch vulnerability in code

3. **Long-term Resolution** (within 7 days):
   - [ ] Root cause analysis completed
   - [ ] Fix deployed to production
   - [ ] Test cases added for vulnerability
   - [ ] Documentation updated
   - [ ] Stakeholders notified (if user data affected)

### Common Incident Scenarios

| Incident | Immediate Action | Long-term Fix |
|----------|------------------|---------------|
| XSS discovered | Update CSP, sanitize input | Add validation, update tests |
| SQL injection found | Parameterize query immediately | Code review, add tests |
| Session hijacking | Force logout all users, rotate SECRET_KEY | Review cookie flags, add monitoring |
| File upload exploit | Remove malicious files, patch upload handler | Add extension validation, update tests |
| Brute force attack | Block IP, increase rate limiting | Add CAPTCHA, implement account lockout |

### Contact Information

- **Security Issues**: Report to project maintainer via private channel
- **Vulnerability Disclosure**: Allow 30 days for fixes before public disclosure
- **Emergency Contact**: (Add emergency contact details)

---

## Deployment Commands Reference

### Build and Test Locally

```bash
# Install dependencies
uv pip install -r requirements.txt

# Run all tests
uv run pytest tests/ -v

# Run security tests
uv run pytest tests/test_security.py -v

# Run static analysis
uv run bandit -r . -ll

# Build frontend assets
python build/build.py

# Test production configuration
uv run python -c "from app import create_app; app = create_app('production')"
```

### Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy to preview
vercel

# Deploy to production
vercel --prod
```

### Verify Deployment

```bash
# Check health endpoint
curl -I https://your-domain.com

# Test API
curl https://your-domain.com/api/attractions

# Check security headers
curl -I https://your-domain.com | grep -E "(content-security-policy|x-frame-options|x-content-type)"

# Test authentication
curl -X POST https://your-domain.com/login -d "username=test&password=test" -v
```

---

**Document Version**: 1.0.0  
**Last Updated**: April 12, 2026  
**Next Review**: October 12, 2026  
**Maintainer**: Development Team
