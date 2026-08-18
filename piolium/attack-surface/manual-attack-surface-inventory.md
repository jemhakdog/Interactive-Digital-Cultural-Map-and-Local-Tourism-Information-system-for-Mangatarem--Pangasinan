# Manual Attack Surface Inventory

> **Generated**: 2026-08-18 (P8 Manual Probe)
> **Repository commit**: 30bc3e7f
> **Mode**: deep — single-team probe
> **Focus**: Highest-impact slices not fully verified by automated phases

---

## Public Routes / URLs (Pre-Auth)

| # | Method | Path | Handler (file:line) | Auth | Risk |
|---|--------|------|---------------------|------|------|
| 1 | GET | `/test-supabase` | `modules/core/public_routes.py:20` | NONE | **HIGH** — DB data exposure |
| 2 | GET | `/api/gemini/config` | `modules/core/api_routes.py:116` | NONE | **CRITICAL** — API key leak |
| 3 | POST | `/api/map-feedback` | `modules/core/api_routes.py:62` | NONE | MEDIUM — Unauthenticated DB write |
| 4 | POST | `/api/tiles/cache/invalidate` | `modules/core/map_routes.py:200` | NONE | **HIGH** — Redis KEYS DoS + cache wipe |
| 5 | POST | `/api/v1/routing/optimize` | `modules/routing/routes.py:40` | NONE | LOW — SSRF via coords (numeric only) |
| 6 | POST | `/api/v1/routing/directions` | `modules/routing/routes.py:98` | NONE | LOW — SSRF via coords (numeric only) |
| 7 | GET | `/api/tiles/<z>/<x>/<y>.pbf` | `modules/core/map_routes.py:67` | NONE | LOW — Tile serving |
| 8 | GET | `/sitemap.xml` | `modules/core/public_routes.py:300` | NONE | LOW — subprocess.run (hardcoded cmd) |
| 9 | WS  | `connect` | `modules/chat/sockets.py:11` | NONE (transport) | MEDIUM — CORS wildcard |
| 10 | POST | `/auth/login` | `modules/auth/login.py:23` | NONE | LOW — Rate-limited 5/min |
| 11 | POST | `/auth/register` | `modules/auth/register.py:28` | NONE | LOW — Rate-limited 5/min |
| 12 | POST | `/auth/google-login` | `modules/auth/oauth.py:55` | NONE | LOW — Token verified |

## Authenticated Routes (Highest Risk)

| # | Method | Path | Handler (file:line) | Roles | Risk |
|---|--------|------|---------------------|-------|------|
| 13 | POST | `/pull` | `modules/core/update_routes.py:37` | admin + token | **CRITICAL** — RCE via git pull + file copy; token bypass when env unset |
| 14 | POST | `/booking/api/admin/update_status` | `modules/booking/routes.py:150` | admin/contributor/business_owner | **HIGH** — IDOR: no ownership check |
| 15 | POST | `/gamification/api/start-navigation` | `modules/gamification/routes.py:86` | user+ | MEDIUM — Session state self-service |
| 16 | POST | `/admin/v1/documents/import` | `modules/api_v1/documents.py:410` | admin | MEDIUM — DOCX parse via python-docx/lxml |
| 17 | GET | `/admin/documents/<slug>/edit` (legacy) | `modules/admin_core/documents.py:53` | admin | MEDIUM — `**request.args` spread in redirect |
| 18 | POST | `/admin/v1/documents/<slug>/edit` | `modules/api_v1/documents.py:331` | admin | LOW — JSON parse + SQLi regex check |

## Attacker Sources

| # | Source | Location | Attacker Control | Notes |
|---|--------|----------|-----------------|-------|
| S1 | `os.environ.get("UPDATE_TOKEN")` | `update_routes.py:37` | Full if env unset | Token check skipped entirely |
| S2 | `request.get_json().get("token")` | `update_routes.py:33` | Full (JSON body) | Non-constant-time comparison |
| S3 | `data.get("reservation_id")` | `booking/routes.py:163` | Full (any reservation ID) | No ownership verification |
| S4 | `data.get("status")` | `booking/routes.py:164` | Full (any valid status) | Status set directly |
| S5 | `session['oauth_signup']` | `oauth.py:58` | Full if SECRET_KEY default | Session forging |
| S6 | `data.get("layer")` + z/x/y | `map_routes.py:218` | Full (Redis pattern) | KEYS pattern injection |
| S7 | `**request.args` | `admin_core/documents.py:76` | Full (query params) | Extra params in redirect URL |
| S8 | `request.form.get("role")` | `oauth.py:113` | Full (role choice) | After session trust |
| S9 | `data.get("attraction_id")` | `api_routes.py:74` | Full (any ID) | No FK validation on MapFeedback |
| S10 | `file.stream` (DOCX) | `documents.py:419` | Full (file content) | python-docx/lxml parser |

## Sinks

| # | Sink | Location | Type | Impact |
|---|------|----------|------|--------|
| K1 | `subprocess.run(["git", "pull"])` | `update_routes.py:93` | Command execution | RCE if token bypassed |
| K2 | `shutil.copy2()` | `update_routes.py:101,119` | File system write | Arbitrary file overwrite |
| K3 | `reservation.status = new_status` | `booking/routes.py:183` | DB write | Unauthorized state change |
| K4 | `redis_client.keys(pattern)` | `map_routes.py:231` | Redis O(N) scan | DoS via wildcard pattern |
| K5 | `redis_client.delete(*keys)` | `map_routes.py:233` | Redis cache wipe | Cache stampede DoS |
| K6 | `redirect(url_for(..., **request.args))` | `admin_core/documents.py:76` | HTTP redirect | Parameter injection |
| K7 | `session['active_nav'] = {...}` | `gamification/routes.py:89` | Session write | Navigation guard bypass |
| K8 | `_create_google_user(email, name, role)` | `oauth.py:72` | DB write + login | Account creation with forged session |
| K9 | `jsonify({"api_key": key})` | `api_routes.py:125` | HTTP response | API key leakage |
| K10 | `docx.Document(file.stream)` | `documents.py:419` | File parse | XXE/DoS via lxml |

## Hidden Control Channels

| # | Channel | Location | Effect | Condition |
|---|---------|----------|--------|-----------|
| HC1 | `UPDATE_TOKEN` env var presence/absence | `update_routes.py:36` | Skips token verification entirely | Env var not set |
| HC2 | `request.is_json` | `update_routes.py:31` | Controls whether token is extracted | Content-Type header |
| HC3 | `session['oauth_signup']` | `oauth.py:58` | Trust boundary for user creation | Session cookie (forgeable with default SECRET_KEY) |
| HC4 | `X-Forwarded-For` via ProxyFix | `app.py:40` | Rate limit key spoofing | Direct access (Docker) |
| HC5 | `request.args` spread | `admin_core/documents.py:76` | Extra query params in redirect URL | Legacy redirect handlers |
| HC6 | `cors_allowed_origins="*"` | `app.py:55` | Any origin can connect to WebSocket | Always |

## Trust Chain Gaps

| Gap | Description | Severity | Priority Target |
|-----|-------------|----------|----------------|
| **GAP-1** | `UPDATE_TOKEN` env var absence → token check skipped → RCE via `/pull` | CRITICAL | YES |
| **GAP-2** | Default `SECRET_KEY` → session forging → OAuth role selection → account creation with attacker-chosen role | HIGH | YES |
| **GAP-3** | `POST /api/tiles/cache/invalidate` → no auth → `redis.keys(user_pattern)` → DoS | HIGH | YES |
| **GAP-4** | `POST /booking/api/admin/update_status` → role check only → no ownership → IDOR | HIGH | YES |
| **GAP-5** | `**request.args` in legacy document redirects → parameter injection | MEDIUM | YES |
| **GAP-6** | `session['active_nav']` self-service → navigation guard bypass → gamification fraud | MEDIUM | YES |
| **GAP-7** | `GET /api/gemini/config` → API key leaked to all visitors | CRITICAL | Already documented (p5-001) |
| **GAP-8** | `GET /test-supabase` → DB data exposed without auth | HIGH | Already documented (p5-002) |
| **GAP-9** | CSRF exempt on JSON endpoints → unauthenticated mutations on cache invalidation, map feedback | MEDIUM | YES |

## Exploit-Relevant Paths

### Path-1: Token Bypass → RCE Chain
```
Attacker (any authenticated admin) → POST /pull with JSON body (no "token" field)
  → require_update_token: current_user.is_authenticated ✓, role=="admin" ✓
  → token = None (no "token" in JSON)
  → expected_token = os.environ.get("UPDATE_TOKEN") → None if env unset
  → expected_token is falsy → token check SKIPPED
  → pull_updates() executes:
    → os.chdir("/home/GoMangatarem/...") 
    → subprocess.run(["git", "pull"]) 
    → shutil.copy2() to production paths
```

### Path-2: Session Forgery → Account Creation Chain
```
Attacker forges session cookie with SECRET_KEY = "your-secret-key-here"
  → session['oauth_signup'] = {'email': 'victim@example.com', 'name': 'Victim'}
  → POST /auth/select-role with role=contributor
  → _create_google_user("victim@example.com", "Victim", "contributor")
  → is_approved = False (needs admin approval) → limited impact
  → OR role=user → is_approved = True → immediate account with victim's email
```

### Path-3: Redis KEYS DoS Chain
```
Anonymous attacker → POST /api/tiles/cache/invalidate
  Content-Type: application/json (CSRF-exempt)
  Body: {"layer": "attractions", "z": "*", "x": "*", "y": "*"}
  → layer_name = "attractions" (valid, passes LAYER_CONFIG check)
  → pattern = "mvt:attractions:*:*:*"
  → redis_client.keys("mvt:attractions:*:*:*") → O(N) full scan
  → redis_client.delete(*all_matching_keys) → complete cache wipe
  → Cache stampede on next tile request → DB overload
```

### Path-4: IDOR → Unauthorized Booking Status Change
```
Business_owner A → POST /booking/api/admin/update_status
  Body: {"reservation_id": <any_ID>, "status": "cancelled"}
  → current_user.role == "business_owner" → passes role check
  → Reservation.query.get_or_404(res_id) → fetches ANY reservation
  → reservation.status = "cancelled" → reservation.slot.booked_count -= reservation.party_size
  → No check: does this user own the attraction linked to this reservation?
```

### Path-5: Legacy Redirect Parameter Injection
```
Admin → GET /admin/documents/create/natural?next=/admin/documents/built
  → admin_document_create("natural") 
  → redirect(url_for("v1_docs.v1_document_create", slug="natural", next="/admin/documents/built"), 302)
  → Response: 302 Location: /admin/v1/documents/create/natural?next=%2Fadmin%2Fdocuments%2Fbuilt
  → Target handler (v1_document_create) does NOT use `next` parameter → no open redirect
  → BUT: any query params from request.args are injected into redirect URL as free params
```
