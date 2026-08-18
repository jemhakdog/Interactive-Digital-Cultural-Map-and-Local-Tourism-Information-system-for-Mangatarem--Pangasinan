# Phase 7 — Specification, Framework Contract & Parser Gap Analysis

> **Generated**: 2026-08-18  
> **Repository**: jemhakdog/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan  
> **Commit**: 30bc3e7f  
> **Audit mode**: deep

---

## Specs & Frameworks Analyzed

| Spec/Framework | Version | Relevance |
|---------------|---------|-----------|
| RFC 6749 — OAuth 2.0 | October 2012 | Google OAuth login flow (state parameter) |
| RFC 7239 — Forwarded HTTP Extension | June 2014 | ProxyFix trust model, X-Forwarded-* headers |
| Flask-WTF CSRF Protection | 1.2.2 | CSRF exemption for JSON Content-Type |
| Werkzeug ProxyFix | 3.1.x | WSGI middleware for proxy header translation |
| Flask-SocketIO | 5.6.1 | WebSocket CORS, Socket.IO protocol |
| Flask-Limiter | 4.1.1 | Rate limiting with `get_remote_address` |
| Flask-Login | 0.6.3 | Session management, `remember=True` |
| PEP 3333 — WSGI | 2011 | Error handling in production WSGI server |

---

## Summary of Findings

| # | Gap Title | Spec/Framework | Severity | Type |
|---|-----------|---------------|----------|------|
| SG-01 | Flask-WTF CSRF exempts JSON Content-Type — all JSON POST endpoints unprotected | Flask-WTF 1.2.2 | **HIGH** | framework-contract |
| SG-02 | Session state self-service — `active_nav` set by unauthenticated client action | Flask Session contract | **MEDIUM** | hidden-control-channel |
| SG-03 | OAuth state parameter missing — Google login lacks CSRF protection per RFC 6749 §10.12 | RFC 6749 §10.12 | **MEDIUM** | missing-check |
| SG-04 | ProxyFix trusts X-Forwarded-* headers without source validation | RFC 7239 §8.1 | **MEDIUM** | proxy-trust |
| SG-05 | Non-constant-time UPDATE_TOKEN comparison | CWE-208 | **MEDIUM** | framework-contract |
| SG-06 | Socket.IO CORS wildcard bypasses browser same-origin policy | RFC 6454 / W3C CORS | **MEDIUM** | framework-contract |
| SG-07 | `X-Requested-With` header controls response format (JSON vs redirect) | HTTP Convention | **LOW** | hidden-control-channel |
| SG-08 | `request.referrer` used as redirect fallback — attacker-controlled | HTTP Convention | **LOW** | hidden-control-channel |

**Excluded from P7** (already in P4 drafts): debug mode (p4-007), Gemini key leak (p4-001), secret key default (p4-002), test-supabase endpoint (p4-011), WebSocket CORS (p4-010), ProxyFix (p4-013), open redirects (p4-003–p4-005), IDOR booking (p4-006), command execution (p4-015), session navigation bypass (p4-018).

---

## Detailed Findings

### SG-01: Flask-WTF CSRF Exempts JSON Content-Type — All JSON POST Endpoints Unprotected

- **Contract**: Flask-WTF 1.2.2 `CSRFProtect` default behavior — `WTF_CSRF_METHODS` defaults to `['POST', 'PUT', 'PATCH', 'DELETE']` but `CSRFProtect._check_csrf()` exempts requests where `request.content_type` is `application/json` (the `is_json` check). This is by design to avoid breaking API-only endpoints, but means any form-submitting page that can be tricked into sending JSON POST (via `fetch()` or `XMLHttpRequest`) bypasses CSRF.
- **Security Assumption**: Application assumes Flask-WTF protects all POST endpoints. In reality, endpoints accepting JSON POST bodies are unprotected.
- **Code Path**: `extensions.py:24` — `csrf = CSRFProtect()`; `app.py:83` — `csrf.init_app(app)`; Multiple endpoint handlers accept `request.get_json()`.
- **Gap Type**: framework-contract
- **Attack Vector**: An attacker on `evil.com` constructs a JavaScript page that sends `fetch("https://target.com/api/tiles/cache/invalidate", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({layer:"heritage"})})`. Since the browser will send session cookies cross-origin for same-site Lax on top-level navigations, but `fetch()` with `Content-Type: application/json` causes a CORS preflight that the server doesn't respond to — however, the preflight itself reveals server availability. More critically: the `POST /notifications/subscribe` and `POST /gamification/api/start-navigation` endpoints accept `application/json` and are CSRF-vulnerable. For form-data endpoints, `POST /auth/google-login` is submitted via Google One Tap which posts form data — CSRF protection applies. The JSON-exempted endpoints include:
  - `POST /api/tiles/cache/invalidate` (unauthenticated)
  - `POST /api/map-feedback` (unauthenticated)
  - `POST /gamification/api/start-navigation` (authenticated)
  - `POST /gamification/api/stop-navigation` (authenticated)
  - `POST /booking/api/reserve` (authenticated)
  - `POST /notifications/mark-read` (authenticated)
- **Exploit Conditions**: Victim must be logged in (for authenticated endpoints) or have an active session. Attacker hosts malicious page that sends JSON POST to target endpoint. Browser's SameSite=Lax allows cookies on top-level navigations but `fetch()` in an iframe/worker is blocked by SameSite. However, the `/api/tiles/cache/invalidate` and `/api/map-feedback` endpoints require NO authentication, so session cookies are not needed.
- **Impact**: Unauthenticated cache invalidation DoS; authenticated state mutations without CSRF tokens.
- **Severity**: **HIGH**
- **Evidence**:
  ```python
  # extensions.py:24
  csrf = CSRFProtect()
  # Flask-WTF 1.2.2 source: _check_csrf() exempts request.is_json
  # core/map_routes.py:249
  @map_bp.route("/cache/invalidate", methods=["POST"])
  @limiter.limit("10 per hour")
  def invalidate_cache():  # No @login_required, no CSRF check for JSON
  ```

### SG-02: Session State Self-Service — `active_nav` Set by Client Action Without Server Validation

- **Contract**: Flask signed sessions are integrity-protected (tamper-evident) but NOT confidentiality-protected for the session cookie value in development (secret key signs but does not encrypt). More critically, Flask sessions are self-service — any authenticated user can set arbitrary session keys via application endpoints that write to `session[]`.
- **Security Assumption**: The `active_nav` session value is trusted as evidence of legitimate navigation state, gating QR check-in access.
- **Code Path**: `modules/gamification/routes.py:86` — `session['active_nav'] = {"id": int(target_id), "type": target_type, ...}`; `modules/gamification/routes.py:48` — session read to gate check-in.
- **Gap Type**: hidden-control-channel
- **Attack Vector**: An authenticated user calls `POST /gamification/api/start-navigation` with `{"id": 1, "type": "attraction"}` to set `session['active_nav']` to any attraction/establishment ID. This bypasses the "must be actively navigating" guard without actually starting map navigation. The user can then access QR check-in pages and (with GPS spoofing) earn badges/check-ins for locations they never visited.
- **Exploit Conditions**: Authenticated user. Knowledge of target_id and type (public information from map).
- **Impact**: Gamification system bypass — earn badges/check-ins without physical presence.
- **Severity**: **MEDIUM**
- **Evidence**:
  ```python
  # modules/gamification/routes.py:86-89
  session['active_nav'] = {
      "id": int(target_id),
      "type": target_type,
      "timestamp": datetime.utcnow().isoformat()
  }
  # modules/gamification/routes.py:48-49
  active_nav = session.get('active_nav')
  if not active_nav or str(active_nav.get('id')) != str(id_) or active_nav.get('type') != type_:
  ```

### SG-03: OAuth State Parameter Missing — Google Login Lacks CSRF Protection

- **RFC/Spec**: RFC 6749, Section 10.12
- **Requirement**: "The client MUST implement CSRF protection for its redirection URI. ... The client SHOULD utilize the 'state' request parameter to deliver this value to the authorization server when making an authorization request." Additionally: "The authorization server MUST implement CSRF protection for its authorization endpoint and ensure that a malicious client cannot obtain authorization without the awareness and explicit consent of the resource owner."
- **Code Path**: `modules/auth/oauth.py:55-68` — `google_login_view()` accepts POST with `credential` form field. No `state` parameter is generated, stored, or verified. The Google Identity Services (One Tap) flow posts the credential directly to the server.
- **Gap Type**: missing-check
- **Attack Vector**: While the Google One Tap/credential flow doesn't use a traditional redirect-based OAuth flow (so the state parameter from RFC 6749 §4.1.1 doesn't directly apply), the `select_role_view()` at `oauth.py:110` creates a new user based solely on `session['oauth_signup']` data. A CSRF attack against the role selection form could force a victim to create an attacker-chosen role for their account. The `select_role` POST form has no CSRF token verification for the role choice.
- **Exploit Conditions**: Victim must have a pending Google OAuth signup session (just authenticated with Google but not yet selected role). Attacker crafts page that auto-submits the role selection form.
- **Impact**: Attacker can force victim into "contributor" role (requiring admin approval) or "business_owner" role instead of intended "user" role.
- **Severity**: **MEDIUM**
- **Evidence**:
  ```python
  # modules/auth/oauth.py:55-68 — no state parameter
  def google_login_view():
      token = request.form.get("credential")
      # ... verifies token, stores in session, redirects to select_role
      session['oauth_signup'] = {'email': email, 'name': name}
      return redirect(url_for("auth.select_role"))
  # modules/auth/oauth.py:110-135 — role selection form, no CSRF on POST
  def select_role_view():
      # POST handler: role = request.form.get("role")
      # Creates user with attacker-chosen role
  ```

### SG-04: ProxyFix Trusts X-Forwarded-* Headers Without Source Validation

- **RFC/Spec**: RFC 7239, Section 8.1
- **Requirement**: "The 'Forwarded' HTTP header field cannot be relied upon to be correct, as it may be modified, whether mistakenly or for malicious reasons, by every node on the way to the server, including the client making the request." The RFC recommends verifying proxy correctness and whitelisting trusted proxies.
- **Code Path**: `app.py:76-77` — `app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)`; `extensions.py:19-22` — `limiter = Limiter(key_func=get_remote_address, ...)`.
- **Gap Type**: proxy-trust
- **Attack Vector**: When `VERCEL` env var is set, ProxyFix trusts exactly one proxy hop. If the application is accessed directly (e.g., Docker deployment on port 5002 exposed to network, or Vercel proxy is bypassed via DNS manipulation), an attacker can set `X-Forwarded-For: 1.2.3.4` and `X-Forwarded-Host: evil.com` to:
  1. Spoof their IP address for rate limiting (different `get_remote_address` per request)
  2. Manipulate `request.host` and URL generation via `X-Forwarded-Host`
  3. Change the URL scheme via `X-Forwarded-Proto`
- **Exploit Conditions**: Application must be directly accessible (bypassing Vercel). On Vercel, Vercel strips/overwrites these headers. On Docker, if port 5002 is exposed without a reverse proxy, this is exploitable.
- **Impact**: Rate limiting bypass enabling brute-force attacks; URL manipulation for phishing.
- **Severity**: **MEDIUM** (conditional on deployment mode)
- **Evidence**:
  ```python
  # app.py:75-77
  if is_vercel:
      app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
  # extensions.py:19-21
  limiter = Limiter(key_func=get_remote_address, ...)
  # RFC 7239 §8.1: headers "cannot be relied upon to be correct"
  ```

### SG-05: Non-Constant-Time UPDATE_TOKEN Comparison

- **Contract**: Secure token comparison requires constant-time algorithms (e.g., `hmac.compare_digest()`) to prevent timing side-channel attacks. Python's `==` operator on strings short-circuits on the first differing character.
- **Security Assumption**: The `UPDATE_TOKEN` comparison is secure because it's compared against an environment variable.
- **Code Path**: `modules/core/update_routes.py:37` — `if expected_token and token != expected_token:` uses `!=` operator (which is `==` negated — same timing behavior).
- **Gap Type**: framework-contract
- **Attack Vector**: An authenticated admin can measure response time differences to extract the `UPDATE_TOKEN` character by character. Each correct character adds ~10-50ns to comparison time. With enough requests (rate limited to 1/min), an attacker with a valid admin session could extract the token.
- **Exploit Conditions**: Authenticated admin user (or compromised admin session). Network latency must be low enough to measure timing differences.
- **Impact**: Extraction of UPDATE_TOKEN enabling RCE via `/pull` endpoint (git pull + file copy to production paths).
- **Severity**: **MEDIUM**
- **Evidence**:
  ```python
  # modules/core/update_routes.py:36-37
  expected_token = os.environ.get("UPDATE_TOKEN")
  if expected_token and token != expected_token:  # Non-constant-time comparison
  ```

### SG-06: Socket.IO CORS Wildcard Bypasses Browser Same-Origin Policy

- **Contract**: The W3C CORS specification and the WebSocket protocol (RFC 6455) define cross-origin restrictions. Socket.IO uses HTTP long-polling as a transport fallback, which IS subject to CORS. The `cors_allowed_origins="*"` tells Socket.IO to respond with `Access-Control-Allow-Origin: *` to ALL origins.
- **Security Assumption**: Application assumes `cors_allowed_origins="*"` is acceptable because chat handlers check authentication.
- **Code Path**: `app.py:84` — `socketio.init_app(app, cors_allowed_origins="*")`; `modules/chat/sockets.py:11-15` — `handle_connect()` allows anonymous connections.
- **Gap Type**: framework-contract
- **Attack Vector**: A malicious page at `evil.com` can:
  1. Establish a Socket.IO connection to the target server (CORS allows it)
  2. Listen to all broadcast messages in public barangay rooms
  3. If the victim has an active session cookie (SameSite=Lax allows top-level navigation cookies), the connection inherits the session
  4. Send messages impersonating the victim in public rooms
- **Exploit Conditions**: Victim must have an active session and visit malicious page. The Socket.IO polling transport sends cookies.
- **Impact**: Chat message interception and impersonation; information leakage of user activity.
- **Severity**: **MEDIUM**
- **Evidence**:
  ```python
  # app.py:84
  socketio.init_app(app, cors_allowed_origins="*")
  # modules/chat/sockets.py:11-15
  @socketio.on('connect')
  def handle_connect():
      if not current_user.is_authenticated:
          pass  # Allows anonymous connection
  ```

### SG-07: `X-Requested-With` Header Controls Response Format

- **Contract**: The `X-Requested-With: XMLHttpRequest` header is a de facto convention for identifying AJAX requests. It's not a security header, but when it controls response format (JSON vs redirect), it becomes a hidden control channel.
- **Security Assumption**: The `X-Requested-With` header is set only by legitimate JavaScript code.
- **Code Path**: `modules/notifications/routes.py:39,44,61,68` — `if request.headers.get("X-Requested-With") == "XMLHttpRequest": return jsonify(...)`.
- **Gap Type**: hidden-control-channel
- **Attack Vector**: An attacker can set this header in a `fetch()` request from a malicious page. However, `X-Requested-With` is a non-simple header, so the browser sends a CORS preflight. Since the server doesn't respond with `Access-Control-Allow-Headers: X-Requested-With`, the preflight fails. This limits exploitation to same-origin or server-side attacks. **Risk is low** because the header only changes response format, not behavior.
- **Exploit Conditions**: Same-origin JavaScript execution or server-side request manipulation.
- **Impact**: Minor — response format switching only.
- **Severity**: **LOW** (below P7 threshold — included for completeness)
- **Evidence**:
  ```python
  # modules/notifications/routes.py:39
  if request.headers.get("X-Requested-With") == "XMLHttpRequest":
      return jsonify({"status": "success", "message": "..."})
  ```

### SG-08: `request.referrer` Used as Redirect Fallback

- **Contract**: The HTTP `Referer` header is set by the browser and can be spoofed by attackers (via `Referer-Policy` or by crafting a request without it). Using it as a redirect target is equivalent to using `request.args.get('next')` without validation.
- **Security Assumption**: `request.referrer` is a trusted value that the user previously visited.
- **Code Path**: `modules/admin_core/content.py:111` — `_next = request.args.get("next") or request.referrer or url_for("admin.reviews_list")`; `content.py:133` — same pattern.
- **Gap Type**: hidden-control-channel
- **Attack Vector**: An attacker crafts a link to `https://target.com/admin/reviews/1/approve?next=https://evil.com` — this is already covered by p4-003/p4-004 (open redirect via `next` parameter). The `request.referrer` fallback is only used if `next` is absent, which requires the attacker to set the `Referer` header. Since `Referer-Policy: strict-origin-when-cross-origin` is set, cross-origin requests omit the Referer, making this path unreachable from external sites. **Risk is low.**
- **Exploit Conditions**: Attacker must control the Referer header (same-origin or HTTPS downgrade).
- **Impact**: Open redirect to attacker-controlled URL.
- **Severity**: **LOW** (below P7 threshold)
- **Evidence**:
  ```python
  # modules/admin_core/content.py:111
  _next = request.args.get("next") or request.referrer or url_for("admin.reviews_list")
  return redirect(_next)
  ```

---

## Framework Contract Challenge Results

### Middleware/Proxy

| Channel | Classification | Security-Relevant? | Findings |
|---------|---------------|-------------------|----------|
| ProxyFix (X-Forwarded-*) | Deployment assumption | YES — rate limiting, URL scheme | SG-04 |
| SocketIO CORS `*` | External input | YES — cross-origin WebSocket | SG-06 |
| CSP `unsafe-eval` + `unsafe-inline` | Already covered in P4 | YES — XSS bypass | p4-012 (existing) |

### Hidden Control Channels

| Channel | Classification | Security-Relevant? | Findings |
|---------|---------------|-------------------|----------|
| `session['active_nav']` | Self-service session state | YES — gamification bypass | SG-02 |
| `session['oauth_signup']` | Self-service session state | YES — user creation trust | p4-014 (existing) |
| `X-Requested-With` header | External input | LOW — response format only | SG-07 |
| `request.referrer` | External input | LOW — redirect fallback | SG-08 |
| `request.is_json` / Content-Type | External input | YES — CSRF exemption | SG-01 |

### Runtime Mode

| Channel | Classification | Security-Relevant? | Findings |
|---------|---------------|-------------------|----------|
| `debug=True` in `__main__` | Deployment assumption | YES — debugger RCE | p4-007 (existing) |
| `VERCEL` env var presence | Deployment assumption | YES — ProxyFix activation | SG-04 |

---

## Spec-to-Code Compliance Matrix

| RFC/Spec | Requirement | Implementation | Status | Gap |
|----------|-------------|---------------|--------|-----|
| RFC 6749 §10.12 | Client SHOULD use `state` parameter for CSRF | No state parameter in Google OAuth flow | **PARTIAL** | SG-03 |
| RFC 7239 §8.1 | Forwarded headers cannot be trusted blindly | ProxyFix trusts without validation | **PARTIAL** | SG-04 |
| RFC 7239 §8.1 | Proxy correctness should be verified | No proxy whitelist, relies on Vercel env var | **WEAKER** | SG-04 |
| Flask-WTF contract | CSRF protection on state-changing requests | JSON requests exempted by default | **WEAKER** | SG-01 |
| Flask Session contract | Sessions are integrity-protected but self-service | `active_nav` set by any authenticated user | **WEAKER** | SG-02 |
| Secure comparison | Token comparisons should use constant-time algorithms | `!=` operator used for token comparison | **WEAKER** | SG-05 |
