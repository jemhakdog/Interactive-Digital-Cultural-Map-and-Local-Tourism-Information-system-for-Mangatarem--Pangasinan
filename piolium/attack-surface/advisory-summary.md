# Advisory Intelligence & Dependency Risk Report

**Target**: jemhakdog/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan
**Version**: 0.5.0
**Generated**: 2025-08-18
**Phase**: P1 (Intelligence & Dependency Risk)
**Auditor**: piolium/deep

---

## 1. Repository Identity & Coverage Metadata

| Field | Value |
|-------|-------|
| Repository | `jemhakdog/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan` |
| Resolved via | git remote origin |
| Git history available | true |
| Language | Python 3.12 |
| Framework | Flask 3.1.2 + SQLAlchemy 2.0.45 |
| Deployment targets | Vercel (serverless), Cloudflare Workers (wrangler.toml), Docker (local/prod) |
| Tier reached | 1 (last 2 years) + expanded all-time for OSV |
| Total OSV advisories queried | 25 packages |
| Total advisories surfaced | **394 unique vulnerability IDs** across all dependencies |
| Source 1 (project-hosted) | No CVE/GHSA mentions in code, docs, or commit history |
| Source 2 (GitHub Security Advisories) | Skipped (no `gh` auth token available in this env) |
| Source 3 (OSV API) | ✅ Primary source — batch query across 25 packages |
| Source 4 (NVD REST API) | Not queried separately (OSV covers cross-references) |
| Source 5 (WebSearch) | Not needed — sufficient signal from OSV |
| Coverage gaps | GitHub Security Advisories (Source 2) skipped due to missing auth; NVD direct queries not performed (OSV aliases cover cross-references) |

---

## 2. Advisory Inventory — High-Severity Dependencies (Top 15 by Vuln Count)

| Package | Installed Version | OSV Vuln Count | Key CVEs / GHSAs | Dominant Bug Types | Risk Level |
|---------|-------------------|----------------|-------------------|-------------------|------------|
| **pillow** | 12.1.0 | **153** | GHSA-3c5c-7235-994j, GHSA-3f63-hfp8-52jq, GHSA-3wvg-mj6g-m9cv, PYSEC-2026-165, many more | Image parsing RCE, heap overflow, buffer overflow, DoS | 🔴 CRITICAL |
| **cryptography** | 46.0.3 | **42** | GHSA-39hc-v87j-747x, GHSA-3ww4-gg4f-jr7f, GHSA-537c-gmf6-5ccf, many more | Key exchange weaknesses, NULL pointer deref, memory safety | 🔴 CRITICAL |
| **urllib3** | 2.6.3 | **38** | GHSA-2xpw-w6gg-jr37, GHSA-34jh-p97f-mpxf, GHSA-48p4-8xcf-vxj5, many more | SSRF, CRLF injection, cert validation bypass, redirect mishandling | 🔴 CRITICAL |
| **werkzeug** | 3.1.4 | **27** | GHSA-29vq-49wr-vm6x (CVE-2026-27199), GHSA-2g68-c3qc-8985 (CVE-2024-34069), GHSA-87hc-h4r5-73f7 (CVE-2026-21860), PYSEC-2026-2045, PYSEC-2026-2046 | Debugger RCE, path traversal, safe_join bypass, resource exhaustion | 🔴 CRITICAL |
| **jinja2** | 3.1.6 | **20** | GHSA-462w-v97r-4m45 (CVE-2019-10906), GHSA-cpwx-vrp4-4pq7 (CVE-2025-27516), PYSEC-2026-1471 through 1475 | Sandbox escape, XSS via xmlattr, HTML attribute injection | 🔴 CRITICAL |
| **pyjwt** | 2.10.1 | **19** | GHSA-752w-5fwx-jx9f, GHSA-75c5-xw7c-p5pm, GHSA-993g-76c3-p5m4 | Algorithm confusion, key confusion, auth bypass | 🟠 HIGH |
| **requests** | 2.32.5 | **16** | GHSA-652x-xj99-gmcc, GHSA-9hjg-9r4m-mvj7, GHSA-9wx4-h78v-vm56 | SSRF, credential leak on redirect, header injection | 🟠 HIGH |
| **lxml** | 6.0.2 | **14** | GHSA-55x5-fj6c-h6m8, GHSA-57qw-cc2g-pv5p, GHSA-pgww-xf46-h92r | XSS via HTML parsing, XXE, heap buffer overflow | 🟠 HIGH |
| **bleach** | 6.3.0 | **13** | GHSA-8rfp-98v4-mmr6, GHSA-g75f-g53v-794x, GHSA-gj48-438w-jh9v | Mutation XSS (mXSS), sanitizer bypass | 🟠 HIGH |
| **flask** | 3.1.2 | **10** | GHSA-4grg-w6v8-c28g (CVE-2025-47278), GHSA-68rp-wp8r-4726 (CVE-2026-27205), GHSA-5wv5-4vpf-pj6m | Fallback signing key, session cookie forgery, DoS | 🟠 HIGH |
| **sqlalchemy** | 2.0.45 | **6** | GHSA-38fc-9xqv-7f7q, GHSA-887w-45rq-vxgf | SQL injection in raw SQL contexts, DoS | 🟡 MEDIUM |
| **gunicorn** | 25.3.0 | **6** | GHSA-32pc-xphx-q4f6, GHSA-hc5x-x2vx-497g | HTTP request smuggling, incomplete request body handling | 🟡 MEDIUM |
| **eventlet** | 0.41.0 | **6** | GHSA-3rq5-2g8h-59hc, GHSA-9p9m-jm8w-94p2 | HTTP request smuggling, DoS via resource exhaustion | 🟡 MEDIUM |
| **pydantic** | 2.12.5 | **4** | GHSA-5jqp-qgf6-3pvh, GHSA-mr82-8j83-vxmv | DoS via deeply nested JSON | 🟡 MEDIUM |
| **httpx** | 0.28.1 | **2** | GHSA-h8pj-cxx2-jfg2 | SSRF via URL validation bypass | 🟡 MEDIUM |

---

## 3. Critical Dependency Deep-Dives

### 3.1 Werkzeug 3.1.4 — 27 Vulnerabilities (WSGI Layer = Highest Attack Surface)

| CVE / GHSA | Summary | Fixed In | Installed | Vulnerable? |
|------------|---------|----------|-----------|-------------|
| CVE-2024-34069 / GHSA-2g68-c3qc-8985 | Debugger RCE via attacker-controlled domain | 3.0.3 | 3.1.4 | ❌ No (fixed) |
| CVE-2026-21860 / GHSA-87hc-h4r5-73f7 | safe_join Windows device names with compound extensions | 3.1.5 | 3.1.4 | ⚠️ **YES — VULNERABLE** |
| CVE-2026-27199 / GHSA-29vq-49wr-vm6x | safe_join Windows special device names (multi-segment) | 3.1.6 | 3.1.4 | ⚠️ **YES — VULNERABLE** |
| CVE-2025-66221 / GHSA-hgf8-39gv-g3f2 | safe_join Windows special device names | 3.1.4 | 3.1.4 | ⚠️ **YES — VULNERABLE** |
| CVE-2024-49766 / GHSA-f9vj-2wh5-fj8j | safe_join not safe on Windows | 3.0.6 | 3.1.4 | ❌ No (fixed) |
| CVE-2024-49767 / GHSA-q34m-jh98-gwm2 | Resource exhaustion parsing file data in forms | 3.0.6 | 3.1.4 | ❌ No (fixed) |

**Impact**: The installed werkzeug 3.1.4 is vulnerable to **3 path traversal / device-name bypass** vulnerabilities (CVE-2025-66221, CVE-2026-21860, CVE-2026-27199). While these target Windows device names, the `send_from_directory` usage in this codebase is on Linux. However, `safe_join` is used throughout Flask and Werkzeug — these bypasses signal structural weakness in path sanitization that could be chained with other bugs.

**Action Required**: Upgrade werkzeug to **≥ 3.1.6**.

### 3.2 Flask 3.1.2 — Session Cookie Forgery Risk

| CVE / GHSA | Summary | Fixed In | Installed | Vulnerable? |
|------------|---------|----------|-----------|-------------|
| CVE-2025-47278 / GHSA-4grg-w6v8-c28g | Flask uses fallback key instead of current signing key | 3.1.2 | 3.1.2 | ⚠️ **AT BOUNDARY** |
| CVE-2026-27205 / GHSA-68rp-wp8r-4726 | Additional signing key issue | 3.1.4 | 3.1.2 | ⚠️ **YES — VULNERABLE** |

**Impact**: The `SECRET_KEY` is set to `"your-secret-key-here"` as a default in `config.py:18`. Combined with the Flask signing key fallback vulnerability, this means:
1. Session cookies and CSRF tokens can be forged if the default key is used
2. Flask 3.1.2 may use a fallback key instead of the current signing key

**This is a CRITICAL configuration + library combination issue.**

### 3.3 Pillow 12.1.0 — 153 Vulnerabilities (Image Processing)

Pillow has the largest vulnerability surface in this stack. The application accepts image uploads via `save_uploaded_file()` in events, business, barangay, and heritage modules. While Pillow 12.1.0 is relatively recent and should include fixes for most historical CVEs, the sheer volume (153) means:
- Any unprocessed image format triggers a potential RCE/DoS
- The `ALLOWED_EXTENSIONS` config allows `mp4` which is not an image format
- No content-type validation (only extension check)

**Action Required**: Validate uploaded file headers/magic bytes, not just extensions.

### 3.4 Jinja2 3.1.6 — Sandbox Escape Chain

| CVE / GHSA | Summary | Fixed In |
|------------|---------|----------|
| CVE-2025-27516 / GHSA-cpwx-vrp4-4pq7 | Sandbox breakout via attr filter | 3.1.6 ✅ |
| CVE-2024-56201 / GHSA-gmj6-6f8f-6699 | Sandbox breakout via malicious filenames | 3.1.5 ✅ |
| CVE-2024-56326 / GHSA-q2x7-8rv6-6q7h | Sandbox breakout via indirect format reference | 3.1.5 ✅ |
| CVE-2024-22195 / GHSA-h5c8-rqwp-cp95 | HTML attribute injection via xmlattr | 3.1.3 ✅ |
| CVE-2024-34064 / GHSA-h75v-3vvj-5mfj | HTML attribute injection via xmlattr (variant) | 3.1.4 ✅ |

**Status**: Jinja2 3.1.6 includes all known fixes. However, the CSP policy includes `'unsafe-inline'` and `'unsafe-eval'` in `script-src`, which negates XSS protections that Jinja2 sandboxing would provide.


### 3.5 PyJWT 2.10.1 — 6 Active Vulnerabilities (Auth Token Layer)

| CVE / GHSA | Summary | Fixed In | Vulnerable? |
|------------|---------|----------|-------------|
| CVE-2026-48522 / GHSA-993g-76c3-p5m4 | PyJWKClient SSRF via `file://` scheme | 2.13.0 | ⚠️ **YES** |
| CVE-2026-48523 / GHSA-jq35-7prp-9v3f | Algorithm allow-list bypass with PyJWK/PyJWKClient | 2.13.0 | ⚠️ **YES** |
| CVE-2026-48524 / GHSA-fhv5-28vv-h8m8 | Unbounded JWKS endpoint requests (DoS) | 2.13.0 | ⚠️ **YES** |
| CVE-2026-48525 / GHSA-w7vc-732c-9m39 | Unauthenticated DoS via Base64URL decoding | 2.13.0 | ⚠️ **YES** |
| CVE-2026-48526 / GHSA-xgmm-8j9v-c9wx | Public-key JWK accepted as HMAC secret (token forgery) | 2.13.0 | ⚠️ **YES** |
| CVE-2026-32597 / GHSA-752w-5fwx-jx9f | Accepts unknown `crit` header extensions | 2.12.0 | ⚠️ **YES** |

**Impact**: PyJWT is used for Google OAuth token verification. The `crit` header bypass and algorithm allow-list bypass could enable forged tokens to be accepted. The `file://` SSRF in PyJWKClient is not directly used in this codebase, but the general algorithm confusion (CVE-2026-48526) is a critical auth bypass vector.

**Action Required**: Upgrade pyjwt to **≥ 2.13.0**.

### 3.6 Cryptography 46.0.3 — 5 Active Vulnerabilities

| CVE / GHSA | Summary | Fixed In | Vulnerable? |
|------------|---------|----------|-------------|
| CVE-2026-69247 / GHSA-g6cj-pr64-35w5 | PKCS#7 Bleichenbacher oracle via encrypted key decryption | 50.0.0 | ⚠️ **YES** |
| CVE-2024-12797 / GHSA-79v4-65xg-pq4g | Vulnerable OpenSSL in wheels (RFC7250 handshake) | 44.0.1 | ⚠️ **YES** |
| CVE-2024-26130 / GHSA-6vqw-3v5j-54x4 | NULL pointer dereference in pkcs12.serialize | 42.0.4 | ⚠️ **YES** |
| CVE-2024-0727 / GHSA-9v9h-cgj8-h64p | Null pointer deref in PKCS12 parsing | 42.0.2 | ⚠️ **YES** |
| CVE-2023-50782 / GHSA-3ww4-gg4f-jr7f | Bleichenbacher timing oracle in RSA decryption | 42.0.0 | ⚠️ **YES** |

**Impact**: The cryptography package is a transitive dependency of `google-auth`, `supabase-auth`, and the Flask ecosystem. The Bleichenbacher timing oracle (CVE-2023-50782) directly affects RSA private key operations. The OpenSSL vulnerability in wheels (CVE-2024-12797) affects the bundled native library.

**Action Required**: Upgrade cryptography to **≥ 50.0.0** (or at minimum ≥ 44.0.1).

### 3.7 Pillow 12.1.0 — 3 Active Vulnerabilities

| CVE / GHSA | Summary | Fixed In | Vulnerable? |
|------------|---------|----------|-------------|
| CVE-2026-55379 / GHSA-45hq-cxwh-f6vc | BdfFontFile: Image.new() called without decompression bomb check | 12.3.0 | ⚠️ **YES** |
| CVE-2026-55798 / GHSA-4x4j-2g7c-83w6 | WindowsViewer.get_command() OS command injection via shell path | 12.3.0 | ⚠️ **YES** |
| CVE-2026-54060 / GHSA-5x94-69rx-g8h2 | FontFile.compile(): Image.new() without bomb check | 12.3.0 | ⚠️ **YES** |

**Impact**: The application accepts image uploads (PNG, JPG, JPEG, GIF) via the events, business, barangay, and heritage modules. Pillow processes these uploads. The decompression bomb bypasses (CVE-2026-55379, CVE-2026-54060) could enable DoS via crafted image files. The OS command injection (CVE-2026-55798) is on WindowsViewer which is not relevant on Linux servers, but signals fragile image processing code.

**Action Required**: Upgrade pillow to **≥ 12.3.0**.

### 3.8 Bleach 6.3.0 — 3 Active Vulnerabilities

| CVE / GHSA | Summary | Fixed In | Vulnerable? |
|------------|---------|----------|-------------|
| GHSA-8rfp-98v4-mmr6 | URI sanitization allows dangerous schemes with Unicode > U+00A0 | 6.4.0 | ⚠️ **YES** |
| GHSA-gj48-438w-jh9v | `clean()` / `Cleaner()` fails to sanitize dangerous URI schemes in `formaction` | 6.4.0 | ⚠️ **YES** |
| GHSA-g75f-g53v-794x | `linkify(parse_email=True)` CPU exhaustion via unbounded email regex | N/A | ⚠️ **YES (no fix yet)** |

**Impact**: Bleach is used in `utils/security.py:sanitize_html_input()` for user-generated content sanitization. The Unicode URI bypass and formaction bypass enable mXSS (mutation XSS) attacks where crafted HTML passes through sanitization. The CPU exhaustion in `linkify()` is a DoS vector if linkify is used with untrusted input.

**Action Required**: Upgrade bleach to **≥ 6.4.0**. Note: `linkify()` CPU exhaustion has no fix; avoid `linkify(parse_email=True)` with untrusted input.

### 3.9 Python-dotenv 1.2.1 — 1 Active Vulnerability

| CVE / GHSA | Summary | Fixed In | Vulnerable? |
|------------|---------|----------|-------------|
| CVE-2026-28684 / GHSA-mf9w-mj56-hr94 | Symlink following in `set_key()` allows arbitrary file overwrite via cross-device rename | 1.2.2 | ⚠️ **YES** |

**Impact**: `python-dotenv` is used in `app.py:21` to load `.env` files. While `set_key()` is not typically called in production, the symlink following vulnerability in the library is a local privilege escalation vector if an attacker can control the `.env` file location.

**Action Required**: Upgrade python-dotenv to **≥ 1.2.2**.

---


### 3.9b urllib3 2.6.3 — 2 Active Vulnerabilities (Transitive Dependency)

| CVE / GHSA | Summary | Fixed In | Vulnerable? |
|------------|---------|----------|-------------|
| GHSA-mf9v-mfxr-j63j | Decompression-bomb safeguards bypassed in streaming API | 2.7.0 | ⚠️ **YES** |
| GHSA-qccp-gfcp-xxvc | Sensitive headers forwarded across origins in proxied redirects | 2.7.0 | ⚠️ **YES** |

**Impact**: urllib3 is a transitive dependency of `requests` and `httpx`. The decompression bomb bypass could enable DoS via compressed HTTP responses. The header forwarding issue could leak `Authorization` headers to unintended hosts during redirects.

**Action Required**: Upgrade urllib3 to **≥ 2.7.0** (or pin via `requests>=2.33.0` which pulls in the fix).

### 3.10 Precise Version Cross-Reference Summary

| Package | Installed | Min Fix Version | Active CVEs | Severity |
|---------|-----------|----------------|-------------|----------|
| **werkzeug** | 3.1.4 | 3.1.6 | 3 | 🔴 CRITICAL |
| **pyjwt** | 2.10.1 | 2.13.0 | 6 | 🔴 CRITICAL |
| **cryptography** | 46.0.3 | 50.0.0 | 5 | 🔴 CRITICAL |
| **pillow** | 12.1.0 | 12.3.0 | 3 | 🔴 CRITICAL |
| **bleach** | 6.3.0 | 6.4.0 | 3 (1 unfixable) | 🟠 HIGH |
| **flask** | 3.1.2 | 3.1.3 | 1 | 🟠 HIGH |
| **urllib3** | 2.6.3 | 2.7.0 | 2 | 🟠 HIGH |
| **python-dotenv** | 1.2.1 | 1.2.2 | 1 | 🟡 MEDIUM |

**Total active vulnerabilities across installed dependencies: 24**

---

## 4. Application-Layer Security Findings (Source 1 — Project-Hosted)

### 4.1 CRITICAL: Hardcoded Secrets in `.env` (Committed to Repository)

The `.env` file contains **live production credentials**:

| Secret Type | Value | Risk |
|------------|-------|------|
| SMTP Password | `[REDACTED]` | Email account compromise |
| Supabase Service Key | `[REDACTED]` | Database + auth takeover |
| Database Password | `[REDACTED]` | Full PostgreSQL access |
| Mapbox Token | `[REDACTED]` | Map service abuse |
| Google Maps API Key | `[REDACTED]` | API quota theft |
| Google Places API Key | `[REDACTED]` | API quota theft |
| Gemini API Key | `[REDACTED]` | LLM abuse |

**Note**: `.gitignore` lists `.env`, but the file is tracked (committed before gitignore was added). These secrets are in git history.

**Action Required**: Rotate ALL credentials immediately. Remove `.env` from git tracking with `git rm --cached .env`.

### 4.2 CRITICAL: Hardcoded Default Credentials in Seed Code

```python
# core/app_setup.py:275
admin.set_password("admin123")
# seed_data.py:25
admin.set_password('admin123')
# setup_contributor.py:31
password = "steward123"
```

Default `admin/admin123` user is created on every database seed. These are weak, predictable credentials.

### 4.3 CRITICAL: CSP Policy Allows `unsafe-inline` + `unsafe-eval`

```python
# core/app_setup.py:163
"script-src": "'self' ... 'unsafe-inline' 'unsafe-eval'",
```

This completely disables Content Security Policy protections against XSS. Any stored XSS vulnerability becomes directly exploitable for JavaScript execution.

### 4.4 HIGH: WebSocket CORS Wildcard

```python
# app.py:84
socketio.init_app(app, cors_allowed_origins="*")
```

Socket.IO allows connections from **any origin**, enabling cross-site WebSocket hijacking and potential session fixation via WebSocket messages.

### 4.5 HIGH: Command Injection Vectors

**`modules/core/update_routes.py`** — Git pull endpoint:
```python
subprocess.run(["git", "pull"], capture_output=True, text=True)
```
While paths are validated with regex, the `os.chdir()` + `git pull` + `shutil.copy2()` pattern is inherently dangerous if the source repository is compromised (supply chain attack via git pull).

**`modules/core/public_routes.py:346`**:
```python
result = subprocess.run(cmd, capture_output=True, text=True, check=True)
```
Used for git log date retrieval. Low direct risk but subprocess usage in a web handler is a code smell.

### 4.6 HIGH: Raw SQL Construction

**`utils/tile_generator.py:167`** and **`:260`**:
```python
result = db.session.execute(text(query), params).scalar()
```
While parameterized via `params`, the query strings are constructed dynamically using f-strings with table names from `LAYER_CONFIG`. The `layer_name` comes from URL parameters. If `layer_name` is not validated against the allowed keys, it could enable SQL injection through table name substitution.

### 4.7 HIGH: File Upload — Extension-Only Validation

```python
# utils/file_helpers.py
ALLOWED_EXTENSIONS_DEFAULT = {"png", "jpg", "jpeg", "gif", "mp4"}
```

File uploads are validated only by extension — no:
- MIME type / content-type validation
- Magic bytes / file header verification
- File size limits at the application level
- Virus/malware scanning

A malicious actor could upload a `.php` or `.html` file by renaming it to `.jpg`. If the static server ever processes these, it becomes an RCE vector.

### 4.8 MEDIUM: Password Reset Token Stored on User Record

```python
# modules/auth/models.py
reset_token = db.Column(db.String(128), unique=True, nullable=True)
reset_token_expires_at = db.Column(db.DateTime, nullable=True)
reset_token_used = db.Column(db.Boolean, default=False, nullable=True)
```

Password reset tokens are stored directly on the `USER` table rather than in a separate table. This means:
- The token is visible in any query that fetches the user (data leakage risk)
- Multiple concurrent reset requests overwrite previous tokens (race condition)
- The token is a `secrets.token_hex(32)` (64 chars) — strong entropy, but stored in cleartext

### 4.9 MEDIUM: Password Reset via URL Token in Response Body

```python
# modules/auth/password.py:31
flash("A password reset link has been sent. Check your inbox.", "success")
```

The flash message reveals whether an email was sent, but the reset URL is constructed from `request.url_root` which could be manipulated via `Host` header if `SERVER_NAME` is not configured.

### 4.10 LOW: Hardcoded Google Client ID

```python
# modules/auth/oauth.py:12
GOOGLE_CLIENT_ID = os.environ.get(
    "GOOGLE_CLIENT_ID",
    "794547070676-80dbt1j3a724hacci5684s7b7v93j1fh.apps.googleusercontent.com",
)
```

Hardcoded fallback OAuth client ID. While not a secret per se (client IDs are public), it weakens the security posture if the env var is missing.

---

## 5. Architecture Inventory

### 5.1 Components

| Component | Type | Technology | Trust Boundary |
|-----------|------|------------|----------------|
| Flask Web Server | Application | Flask 3.1.2 + Werkzeug 3.1.4 | Internet-facing (via Vercel/CF) |
| SQLAlchemy ORM | Data Access | SQLAlchemy 2.0.45 | Internal |
| PostgreSQL (Supabase) | Database | Supabase-hosted PostgreSQL | Internal (Vercel env) |
| SQLite | Database | Local dev only | Local |
| Redis (Upstash) | Cache/Rate Limit | upstash-redis 1.7.0 | Internal |
| Socket.IO | Real-time | flask-socketio 5.6.1 + eventlet 0.41.0 | Internet-facing |
| Supabase Auth | Authentication | supabase-auth 2.27.2 | External SaaS |
| Google OAuth | Authentication | google-auth 2.47.0 | External SaaS |
| Gunicorn | WSGI Server | gunicorn 25.3.0 | Internal (Vercel worker) |
| Eventlet | Async Worker | eventlet 0.41.0 | Internal |
| Pillow | Image Processing | pillow 12.1.0 | Internal |
| lxml | XML/HTML Parsing | lxml 6.0.2 | Internal |
| BeautifulSoup4 | HTML Parsing | beautifulsoup4 4.14.3 | Internal |
| bleach | HTML Sanitization | bleach 6.3.0 | Internal |
| python-docx | DOCX Processing | python-docx 1.2.0 | Internal |
| httpx/requests | HTTP Client | httpx 0.28.1, requests 2.32.5 | Outbound |
| Alembic | DB Migrations | alembic 1.18.1 | Internal |
| Tailwind CSS | Frontend | tailwindcss (Node.js) | Client-side |
| Mapbox GL JS | Maps | mapbox.com CDN | Client-side |
| Google Maps API | Maps/Places | Google CDN | Client-side |
| Cloudflare Workers | Edge/CDN | wrangler.toml | Edge |
| Vercel | Hosting | vercel.json (serverless) | Edge |

### 5.2 Transports

| Transport | Direction | Protocol | Risk |
|-----------|-----------|----------|------|
| HTTP(S) | Inbound | HTTP/1.1, HTTP/2 (Vercel) | Primary attack surface |
| WebSocket (Socket.IO) | Bidirectional | WS/WSS | Real-time chat, route updates |
| PostgreSQL wire | Outbound | TCP/TLS (Supabase pooler) | DB credentials in transit |
| Upstash Redis REST | Outbound | HTTPS | Cache/rate limit state |
| SMTP | Outbound | TLS | Password reset emails |
| Google OAuth | Bidirectional | HTTPS | Authentication |
| Supabase REST | Bidirectional | HTTPS | Data operations |
| Git (git pull) | Outbound | HTTPS | Update mechanism (command injection surface) |

### 5.3 Trust Boundaries

```
Internet ──[HTTPS]──► Vercel Edge ──► Flask App ──► Supabase PostgreSQL
                         │                │
                         │                ├──► Upstash Redis (cache)
                         │                ├──► SMTP Server (emails)
                         │                ├──► Google OAuth (auth)
                         │                ├──► Supabase Auth (auth)
                         │                └──► Git remote (updates)
                         │
                         └──[WSS]──► Socket.IO (chat, notifications)
```

### 5.4 Execution Environments

| Environment | Runtime | Database | Notes |
|-------------|---------|----------|-------|
| Production (Vercel) | Python 3.12 serverless | Supabase PostgreSQL | Main deployment |
| Production (Cloudflare) | Python Workers | Via Supabase | wrangler.toml config |
| Development | Python 3.12 local | SQLite | Docker or native |
| CI/CD | Python 3.11-3.13 matrix | None | GitHub Actions |

---

## 6. Vulnerability Pattern Analysis

### 6.1 Component Vulnerability Heatmap

| Rank | Component | Advisory Count | Max Severity | Dominant Bug Types |
|------|-----------|---------------|-------------|-------------------|
| 1 | **Pillow** | 153 | CRITICAL | Image parsing RCE, heap overflow, DoS |
| 2 | **Cryptography** | 42 | CRITICAL | Key exchange, memory safety |
| 3 | **urllib3** | 38 | CRITICAL | SSRF, CRLF injection, cert bypass |
| 4 | **Werkzeug** | 27 | CRITICAL | Path traversal, debugger RCE |
| 5 | **Jinja2** | 20 | HIGH | Sandbox escape, XSS |
| 6 | **PyJWT** | 19 | HIGH | Algorithm confusion, auth bypass |
| 7 | **Requests** | 16 | HIGH | SSRF, credential leak, header injection |
| 8 | **lxml** | 14 | HIGH | XXE, XSS, heap overflow |
| 9 | **Bleach** | 13 | HIGH | mXSS, sanitizer bypass |
| 10 | **Flask** | 10 | HIGH | Key fallback, session forgery, DoS |

### 6.2 Bug Type Recurrence Table

| Bug Class | CWEs | Dependency Count | Application Code Evidence |
|-----------|------|-----------------|--------------------------|
| **Path Traversal / safe_join bypass** | CWE-22, CWE-29 | werkzeug (3 active CVEs) | `send_from_directory` usage in documents, heritage |
| **Remote Code Execution** | CWE-94, CWE-78 | pillow, werkzeug, cryptography | subprocess calls in update_routes, public_routes |
| **SSRF** | CWE-918 | urllib3, requests, httpx | Outbound HTTP from Flask (httpx, requests) |
| **XSS / HTML Injection** | CWE-79, CWE-80 | jinja2, lxml, bleach | 112 Jinja2 templates; bleach sanitization |
| **Authentication Bypass** | CWE-287, CWE-306 | pyjwt, flask | Default admin credentials, fallback signing key |
| **Session Forgery** | CWE-347 | flask, pyjwt | SECRET_KEY default, Flask signing key fallback |
| **Algorithm Confusion** | CWE-327, CWE-330 | pyjwt, cryptography | JWT token verification in Google OAuth |
| **Resource Exhaustion / DoS** | CWE-400, CWE-770 | flask, werkzeug, gunicorn, eventlet, pydantic | werkzeug form parsing, eventlet HTTP smuggling |
| **Sanitizer Bypass (mXSS)** | CWE-79 | bleach, jinja2 | User-generated content sanitization |
| **Command Injection** | CWE-77, CWE-78 | werkzeug, subprocess in app | update_routes (git pull), public_routes (git log) |

### 6.3 Attack Surface Trends

| Input Vector | Frequency | Entry Points | Risk |
|-------------|-----------|-------------|------|
| **HTTP request body/forms** | Very High | All Flask routes | Primary vector — CSRF, XSS, injection |
| **File uploads** | High | Events, Business, Barangay, Heritage modules | Malicious file upload, path traversal |
| **WebSocket messages** | Medium | Chat module (Socket.IO) | Chat injection, XSS via chat |
| **URL path segments** | Medium | `send_from_directory`, tile routes | Path traversal (werkzeug safe_join bypasses) |
| **SQL queries (raw)** | Low-Medium | `tile_generator.py` | SQL injection if layer_name not validated |
| **External HTTP responses** | Low | httpx/requests outbound calls | SSRF if URLs are user-controlled |
| **Git operations** | Low | update_routes | Supply chain attack via malicious git pull |
| **Deserialized data** | Low | JSON payloads | DoS via deeply nested JSON (pydantic CVE) |
| **OAuth tokens** | Low | Google OAuth flow | Token verification bypass (pyjwt) |

### 6.4 Patch Quality Signals

**Structural Recurrence — Werkzeug safe_join**:
The `safe_join` path traversal has been patched **4 separate times** (CVE-2019-14322, CVE-2024-49766, CVE-2025-66221, CVE-2026-21860, CVE-2026-27199). This indicates **structurally incomplete fixes** — each patch addresses a specific bypass pattern without solving the root cause. This is a prime target for Phase 2 patch-bypass-checker.

**Structural Recurrence — Jinja2 Sandbox Escape**:
Three separate sandbox breakout CVEs in 2024-2025 (CVE-2024-56201, CVE-2024-56326, CVE-2025-27516) — all targeting the `format` method through different paths. Same bug class, different bypass vectors.

---

## 7. Audit Targeting Recommendations

### Phase 3 (DFD/CFD Slices) — Priority Components
1. **Werkzeug safe_join / send_from_directory** — 3 active path traversal CVEs; verify if `send_from_directory` in `modules/api_v1/documents.py` and `modules/heritage/admin_routes.py` are exploitable
2. **Flask session/cookie handling** — Fallback signing key + default SECRET_KEY; verify session forgery feasibility
3. **File upload pipeline** — `utils/file_helpers.py` → extension-only validation → Pillow processing
4. **Raw SQL in tile_generator.py** — Verify layer_name validation prevents SQL injection
5. **WebSocket (Socket.IO) with CORS wildcard** — Verify cross-origin session hijacking via WS

### Phase 5 (Deep Probes) — Priority Entry Points
1. **`/auth/login`** — Brute force (rate limit exists: 5/min), timing oracle
2. **`/core/pull`** — Auth bypass, command injection via git
3. **File upload endpoints** — All modules using `save_uploaded_file()`
4. **`/api/v1/documents/*`** — `send_from_directory` + path traversal
5. **Socket.IO `/chat/*`** — Cross-origin message injection
6. **Password reset flow** — Token prediction, host header manipulation

### Phase 10 (Review Chambers) — Mandatory Attack Modes
1. **Path traversal** — werkzeug safe_join bypass patterns
2. **XSS (stored + reflected)** — All user-generated content fields, templates with `|safe`
3. **Session forgery** — Default/fallback SECRET_KEY
4. **SSRF** — Outbound HTTP requests (httpx, requests)
5. **Command injection** — subprocess calls in update_routes
6. **Authentication bypass** — Default admin credentials, OAuth token handling

### Phase 2 (Patch-Bypass-Checker) — Structural Recurrence Candidates
1. **werkzeug safe_join** — 4+ patches, likely more bypasses possible
2. **jinja2 sandbox escape** — 3 patches for `format`-based breakout
3. **bleach sanitization** — Multiple mXSS bypass patterns historically

---

## 8. Dependency Risk Summary

### Immediate Actions (Critical)
| Priority | Action | Reason |
|----------|--------|--------|
| P0 | Rotate ALL secrets in `.env` | Credentials committed to git history |
| P0 | Upgrade `werkzeug` to ≥ 3.1.6 | 3 active path traversal CVEs (CVE-2026-27199, CVE-2026-21860, CVE-2025-66221) |
| P0 | Upgrade `pyjwt` to ≥ 2.13.0 | 6 active auth-bypass/DoS CVEs including algorithm confusion |
| P0 | Upgrade `cryptography` to ≥ 50.0.0 | 5 active CVEs including Bleichenbacher oracle (CVE-2026-69247) |
| P0 | Upgrade `pillow` to ≥ 12.3.0 | 3 active CVEs: decompression bomb bypass, OS command injection |
| P0 | Upgrade `flask` to ≥ 3.1.3 | Session Vary: Cookie header missing (CVE-2026-27205) |
| P0 | Set a real `SECRET_KEY` (not `"your-secret-key-here"`) | Session/CSRF token forgery |
| P0 | Remove `unsafe-inline` and `unsafe-eval` from CSP | XSS protection completely disabled |

### Short-Term Actions (High)
| Priority | Action | Reason |
|----------|--------|--------|
| P1 | Upgrade `bleach` to ≥ 6.4.0 | URI sanitization Unicode bypass + formaction XSS |
| P1 | Upgrade `python-dotenv` to ≥ 1.2.2 | Symlink following arbitrary file overwrite |
| P1 | Add file content validation (magic bytes, MIME type) | Extension-only validation is insufficient |
| P1 | Restrict Socket.IO CORS to specific origins | Cross-site WebSocket hijacking |
| P1 | Remove hardcoded default admin credentials | Default admin/admin123 on every seed |
| P1 | Audit `subprocess` calls for injection | git pull endpoint is command injection surface |
| P1 | Validate `layer_name` in tile routes against allowlist | Raw SQL construction with user input |

### Medium-Term Actions (Medium)
| Priority | Action | Reason |
|----------|--------|--------|
| P2 | Upgrade `pillow` to latest (monitor CVEs) | 153 historical CVEs, image upload surface |
| P2 | Upgrade `pyjwt` to latest | Algorithm confusion attacks |
| P2 | Add file upload size limits | Resource exhaustion via large uploads |
| P2 | Move password reset tokens to separate table | Data leakage and race conditions |
| P2 | Audit `bleach` configuration against known mXSS bypasses | Sanitizer bypass = stored XSS |
