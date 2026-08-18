# Unauthenticated Attack Surface

> **Supersedes**: Phase P3 best-effort version (route-matrix-derived, exhaustive)  
> **Generated**: 2026-08-18  
> **Phase**: 5 — Authorization & Access Control

Reachable by an anonymous attacker — no valid session, token, or API key.

**Coverage**: 65 entry points | 55 by-design public | 6 missing-guard | 4 middleware-gap  
**Auth model**: Flask-Login session cookies via `@login_required` decorator and `login_manager.unauthorized_handler` (redirect to `/auth/login` or 401 JSON for AJAX/API requests). Role-based guards via `current_user.role` checks in handler bodies (not decorators). CSRF via Flask-WTF (JSON Content-Type exempt by default). Rate limiting via Flask-Limiter with `get_remote_address` key (spoofable via X-Forwarded-For when ProxyFix active). Google OAuth2 via `google.oauth2.id_token.verify_oauth2_token`. WebSocket auth enforced per-event in handler, not at transport level (`cors_allowed_origins="*"`).  
**Coverage gaps**: WebSocket `connect` event allows anonymous connections (transport-level auth gap); `/test-supabase` debug endpoint; `/api/gemini/config` exposes API key; `/api/tiles/cache/invalidate` has no auth; `SECRET_KEY` has fail-open default; `debug=True` in production entry point.

---

## Pre-Auth HTTP / API Routes

### Core Pages (by-design public)

| # | Method | Path | Handler (file:line) | Why pre-auth | Notable inputs / sinks | Blast radius |
|---|--------|------|---------------------|--------------|------------------------|--------------|
| 1 | GET | `/` | `modules/core/public_routes.py:index` | by-design | Public home page, Redis cache reads | Low |
| 2 | GET | `/map` | `modules/core/public_routes.py:map_view` | by-design | Redirect to `/v1/map` | None |
| 3 | GET | `/search` | `modules/core/public_routes.py:search` | by-design | `q` param → ILIKE query; `category`, `barangay` filters; rate-limited 20/min | Low |
| 4 | GET | `/routes` | `modules/core/public_routes.py:routes` | by-design | Static template render | None |
| 5 | GET | `/announcements` | `modules/core/public_routes.py:announcements_public_feed` | by-design | DB query for approved announcements | Low |
| 6 | GET | `/sitemap.xml` | `modules/core/public_routes.py:sitemap` | by-design | `subprocess.run(["git", "log"])` — hardcoded command, no user input | Low |
| 7 | GET | `/robots.txt` | `modules/core/public_routes.py:robots` | by-design | Static response | None |
| 8 | GET | `/google364b8336ce52ae86.html` | `modules/core/public_routes.py:verify_site` | by-design | Google verification template | None |
| 9 | GET | `/sw.js` | `core/app_setup.py:serve_sw` | by-design | Static file | None |
| 10 | GET | `/manifest.json` | `core/app_setup.py:serve_manifest` | by-design | Static file, CSRF-exempt | None |
| 11 | GET | `/offline` | `core/app_setup.py:serve_offline` | by-design | Static template | None |
| 12 | GET | `/logout` | `modules/core/public_routes.py:logout_redirect` | by-design | Redirect to `/auth/logout` | None |
| 13 | GET | `/login` | `modules/core/public_routes.py:login_redirect` | by-design | Redirect to `/auth/login` | None |
| 14 | GET | `/register` | `modules/core/public_routes.py:register_redirect` | by-design | Redirect to `/auth/register` | None |
| 15 | GET | `/forgot-password` | `modules/core/public_routes.py:forgot_password_redirect` | by-design | Redirect to `/auth/forgot-password` | None |

### Auth Routes (Pre-Auth — by-design)

| # | Method | Path | Handler (file:line) | Why pre-auth | Notable inputs / sinks | Blast radius |
|---|--------|------|---------------------|--------------|------------------------|--------------|
| 16 | GET/POST | `/auth/login` | `modules/auth/login.py:login_view` | by-design | Login form, `username`/`password` → DB check; rate-limited 5/min | Low |
| 17 | GET/POST | `/auth/register` | `modules/auth/register.py:register_view` | by-design | Registration form → DB write | Low |
| 18 | GET/POST | `/auth/register/business` | `modules/auth/register.py:register_business_view` | by-design | Business registration → DB write | Low |
| 19 | GET | `/auth/pending-approval` | `modules/auth/register.py:pending_approval_view` | by-design | Static page | None |
| 20 | POST | `/auth/google-login` | `modules/auth/oauth.py:google_login_view` | by-design | Google OAuth `credential` → token verification | Low |
| 21 | GET/POST | `/auth/select-role` | `modules/auth/oauth.py:select_role_view` | by-design | Session `oauth_signup` data trust — **session-stored identity not re-verified** | Low* |
| 22 | GET/POST | `/auth/forgot-password` | `modules/auth/password.py:forgot_password_view` | by-design | Email → reset token; rate-limited 5/min | Low |
| 23 | GET/POST | `/auth/reset-password/<token>` | `modules/auth/password.py:reset_password_view` | by-design | Token validation → password change | Low |

> *Row 21: `select_role_view` trusts session data set during OAuth flow. If `SECRET_KEY` uses default value (`"your-secret-key-here"`), session forging is possible → full account creation with attacker-chosen role.

### Public API v1 Pages (by-design)

| # | Method | Path | Handler (file:line) | Why pre-auth | Notable inputs / sinks | Blast radius |
|---|--------|------|---------------------|--------------|------------------------|--------------|
| 24 | GET | `/v1/map` | `modules/api_v1/public.py:map_v2_view` | by-design | Map template render | Low |
| 25 | GET | `/v1/map-dashboard` | `modules/api_v1/public.py:map_dashboard_view` | by-design | Dashboard template | Low |
| 26 | GET | `/v1/events` | `modules/api_v1/public.py:events_v2_view` | by-design | DB query for approved events | Low |
| 27 | GET | `/v1/lgu-events` | `modules/api_v1/public.py:lgu_events_view` | by-design | Static JSON file read | Low |
| 28 | GET | `/v1/attractions/<id>` | `modules/api_v1/public.py:attraction_detail_v1_view` | by-design | Attraction detail, Redis cache | Low |
| 29 | GET | `/v1/barangay` | `modules/api_v1/public.py:barangays_v1_view` | by-design | Barangay directory | Low |
| 30 | GET | `/attractions/<id>` | `modules/attractions/routes.py:detail` | by-design | Redirect to `/v1/attractions/<id>` | None |
| 31 | GET | `/attractions/api` | `modules/attractions/routes.py:api_list` | by-design | JSON API with pagination; rate-limited 20/min | Low |
| 32 | GET | `/attractions/<id>/reviews` | `modules/attractions/routes.py:get_reviews` | by-design | Reviews JSON with rating summary | Low |
| 33 | GET | `/business/` | `modules/business/routes.py:index` | by-design | Establishment directory | Low |
| 34 | GET | `/business/<id>` | `modules/business/routes.py:detail` | by-design | Establishment detail page | Low |
| 35 | GET | `/business/api` | `modules/business/routes.py:api_list` | by-design | JSON API; rate-limited 20/min | Low |
| 36 | GET | `/gallery/` | `modules/gallery/routes.py:index` | by-design | Gallery page | Low |
| 37 | GET | `/heritage/` | `modules/heritage/routes.py:index` | by-design | Heritage catalog | Low |
| 38 | GET | `/heritage/<type>` | `modules/heritage/routes.py:type_list` | by-design | Heritage type listing | Low |
| 39 | GET | `/heritage/<type>/<id>` | `modules/heritage/routes.py:detail` | by-design | Heritage detail page | Low |
| 40 | GET | `/heritage/api/<type>` | `modules/heritage/routes.py:api_list` | by-design | JSON API | Low |
| 41 | GET | `/heritage/api/<type>/<id>` | `modules/heritage/routes.py:api_detail` | by-design | JSON API detail | Low |
| 42 | GET | `/heritage/api/types` | `modules/heritage/routes.py:api_types` | by-design | Types metadata | Low |
| 43 | GET | `/events/` | `modules/events/routes.py:index` | by-design | Redirect to `/v1/events` | None |
| 44 | GET | `/barangay/` | `modules/barangay/routes.py:index` | by-design | Redirect to `/v1/barangay` | None |
| 45 | GET | `/barangay/<name>` | `modules/barangay/routes.py:profile` | by-design | Barangay profile page | Low |
| 46 | GET | `/booking/api/availability/<id>` | `modules/booking/routes.py:get_availability` | by-design | Booking availability check | Low |

### Public Data APIs (by-design)

| # | Method | Path | Handler (file:line) | Why pre-auth | Notable inputs / sinks | Blast radius |
|---|--------|------|---------------------|--------------|------------------------|--------------|
| 47 | GET | `/api/attractions` | `modules/core/api_routes.py:api_attractions` | by-design | JSON API; rate-limited 20/min | Low |
| 48 | GET | `/api/gemini/context` | `modules/core/api_routes.py:gemini_context` | by-design | Attraction data for Gemini context | Low |
| 49 | GET | `/api/tiles/<z>/<x>/<y>.pbf` | `modules/core/map_routes.py:get_tile` | by-design | Map tile coordinates → PostGIS; rate-limited 2000/min | Low |
| 50 | GET | `/api/tiles/combined/<z>/<x>/<y>.pbf` | `modules/core/map_routes.py:get_combined_tile` | by-design | Combined map tiles; rate-limited 2000/min | Low |
| 51 | GET | `/api/tiles/layers` | `modules/core/map_routes.py:get_available_layers` | by-design | Tile layer metadata; rate-limited 30/min | Low |
| 52 | POST | `/api/v1/routing/optimize` | `modules/routing/routes.py:optimize_route` | by-design | `attraction_ids`, `start` coords → OSRM call; rate-limited 5/min | Low |
| 53 | POST | `/api/v1/routing/directions` | `modules/routing/routes.py:get_directions` | by-design | `coordinates` → OSRM call; rate-limited 10/min | Low |
| 54 | GET | `/api/v1/routing/suggested` | `modules/routing/routes.py:get_suggested` | by-design | Suggested routes from DB; rate-limited 30/min | Low |
| 55 | POST | `/notifications/subscribe` | `modules/notifications/routes.py:subscribe` | by-design | `email` → DB write + email send | Low |

### Anomalous Pre-Auth Endpoints (missing-guard / middleware-gap)

| # | Method | Path | Handler (file:line) | Why pre-auth | Notable inputs / sinks | Blast radius | Classification | Finding |
|---|--------|------|---------------------|--------------|------------------------|--------------|----------------|---------|
| 56 | GET | `/test-supabase` | `modules/core/public_routes.py:test_supabase` | **missing-guard** | `supabase.table('attraction').select("*")` → JSON response | **High — DB data exposure** | missing-guard | p5-002 |
| 57 | POST | `/api/map-feedback` | `modules/core/api_routes.py:submit_map_feedback` | **missing-guard** | `message`, `type`, `attraction_id` → **DB write (MapFeedback)** | **Medium — spam/data pollution** | missing-guard | p5-008 |
| 58 | GET | `/api/gemini/config` | `modules/core/api_routes.py:gemini_config` | **missing-guard** | Returns `GEMINI_API_KEY` env var as JSON | **Critical — API key leaked** | missing-guard | p5-001 |
| 59 | POST | `/api/tiles/cache/invalidate` | `modules/core/map_routes.py:invalidate_cache` | **middleware-gap** | `layer` → Redis cache invalidation; rate-limited 10/hour but **no auth** | **High — cache stampede DoS** | middleware-gap | p5-003 |

---

## Other Unauthenticated Entry Points

### Non-Route Entry Points

| Kind | Entry point (file:line) | Why pre-auth | Classification | Notes | Finding |
|------|-------------------------|--------------|----------------|-------|---------|
| **Debug endpoint** | `modules/core/public_routes.py:test_supabase` | **missing-guard** | missing-guard | `GET /test-supabase` queries Supabase and returns results. No auth. Exposes DB contents. | p5-002 |
| **API key exposure** | `modules/core/api_routes.py:gemini_config` | **missing-guard** | missing-guard | `GET /api/gemini/config` returns `GEMINI_API_KEY` to any visitor. | p5-001 |
| **Cache invalidation** | `modules/core/map_routes.py:invalidate_cache` | **middleware-gap** | middleware-gap | `POST /api/tiles/cache/invalidate` purges Redis cache. No auth. | p5-003 |
| **Anonymous DB write** | `modules/core/api_routes.py:submit_map_feedback` | **missing-guard** | missing-guard | `POST /api/map-feedback` writes feedback to DB without auth. | p5-008 |
| **Subprocess execution** | `modules/core/public_routes.py:sitemap` | by-design | — | `GET /sitemap.xml` → `subprocess.run(["git", "log"])`. Hardcoded command, no user input. Low risk. | — |
| **WebSocket pre-handshake** | `modules/chat/sockets.py:handle_connect` | **middleware-gap** | middleware-gap | SocketIO `connect` event allows anonymous connections (`cors_allowed_origins="*"`). Per-event auth enforced for join/message but not at transport. | p5-005 |
| **WebSocket cross-origin** | `app.py:55` `cors_allowed_origins="*"` | **middleware-gap** | middleware-gap | Any origin can connect to WebSocket. Enables cross-site hijacking if victim has session. | p5-005 |
| **Static file server** | `core/app_setup.py:serve_sw`, `serve_manifest` | by-design | — | Service worker and manifest served without auth. Standard PWA. | — |
| **Redirect handlers** | `modules/core/public_routes.py:login_redirect`, `logout_redirect`, etc. | by-design | — | Legacy path redirects to modular auth routes. No security impact. | — |
| **Fail-open SECRET_KEY** | `config.py` — `os.environ.get("SECRET_KEY", "your-secret-key-here")` | **missing-guard** | missing-guard | If env var unset, sessions signed with default key → session forging | p4-002 |
| **Debug mode entry** | `app.py:135` — `socketio.run(app, debug=True)` | **middleware-gap** | middleware-gap | Werkzeug interactive debugger exposed when run via `python app.py` | p4-007 |

### Pre-Auth WebSocket Events

| Event | Handler (file:line) | Why pre-auth | Classification | Notes | Finding |
|-------|---------------------|--------------|----------------|-------|---------|
| `connect` | `modules/chat/sockets.py:handle_connect` | **middleware-gap** | middleware-gap | Allows anonymous connections. `cors_allowed_origins="*"` enables cross-origin. | p5-005 |
| `leave` | `modules/chat/sockets.py:on_leave` | **missing-guard** | missing-guard | No auth check at all. Any connected client can leave any room. | p5-005 |

---

## Summary of Pre-Auth Findings

| # | Finding | Severity | Entry Point | Classification | Finding ID |
|---|---------|----------|-------------|----------------|------------|
| 1 | Gemini API key leaked | **Critical** | `GET /api/gemini/config` | missing-guard | p5-001 |
| 2 | Debug Supabase endpoint exposed | **High** | `GET /test-supabase` | missing-guard | p5-002 |
| 3 | Map tile cache invalidation | **High** | `POST /api/tiles/cache/invalidate` | middleware-gap | p5-003 |
| 4 | Unauthenticated map feedback DB write | **Medium** | `POST /api/map-feedback` | missing-guard | p5-008 |
| 5 | WebSocket CORS wildcard + anon connect | **Medium** | SocketIO `connect` event | middleware-gap | p5-005 |
| 6 | Fail-open SECRET_KEY default | **High** | `config.py` | missing-guard | p4-002 |
| 7 | Debug mode in production entry | **High** | `app.py:135` | middleware-gap | p4-007 |
| 8 | ProxyFix header trust | **Medium** | `app.py:40` | middleware-gap | p4-013 |
| 9 | Gamification session navigation bypass | **Medium** | `POST /gamification/api/start-navigation` | middleware-gap | p5-006 |
| 10 | Update token bypass when env unset | **Medium** | `GET/POST /pull` | middleware-gap | p5-007 |

**By-design public**: 55 entry points (core pages + auth + API v1 + data APIs)  
**Missing-guard**: 6 entry points (test-supabase, gemini/config, map-feedback, user search PII, SECRET_KEY default, WebSocket leave)  
**Middleware-gap**: 4 entry points (cache/invalidate, WebSocket connect+CORS, debug mode, ProxyFix)
