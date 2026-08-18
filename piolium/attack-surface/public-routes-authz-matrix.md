# Public Routes × Role Authorization Matrix

> **Generated**: 2026-08-18  
> **Phase**: 5 — Authorization & Access Control  
> **Repository**: capstone_system (GoMangatarem)  
> **Supersedes**: Phase P3 best-effort public route inventory

**Coverage**: 87 public/unauthenticated routes + 6 WebSocket events + 3 non-route entry points  
**Auth model**: Flask-Login session cookies; `@login_required` decorator (Layer 1); in-handler `current_user.role` checks (Layer 2); no global middleware (Layer 3). CSRF via Flask-WTF (JSON Content-Type exempt by default). Rate limiting via Flask-Limiter with `get_remote_address` key (spoofable via X-Forwarded-For when ProxyFix active).  
**Frameworks**: Flask 3.1.2, Flask-Login 0.6.3, Flask-SocketIO 5.6.1, Flask-WTF CSRF 1.2.2, Flask-Limiter 4.1.1

---

## How to Read This Matrix

- **Roles**: `anon` = anonymous/unauthenticated, `user` = any authenticated role, `admin` = admin-only, `contributor` = contributor+barangay, `business_owner` = business owner, `approved` = approved business owner
- **Expected Scope** column: What roles *should* access this endpoint by design
- **Actual Scope** column: What roles *can* access it based on code analysis
- **Anomaly** column: `✓` if expected matches actual; `⚠` if discrepancy found
- **Finding** column: Cross-reference to finding draft if anomaly detected

---

## Section A: Core Public Pages (by-design public — no auth expected)

| # | Method | Path | Handler (file:line) | Expected Scope | Actual Scope | Layer-1 Guard | In-Body Authz | Hidden Channels | Anomaly | Finding |
|---|--------|------|---------------------|----------------|-------------|---------------|---------------|-----------------|---------|---------|
| 1 | GET | `/` | `public_routes.py:index` | public | public | None | None | None | ✓ | — |
| 2 | GET | `/map` | `public_routes.py:map_view` | public | public | None | None | None | ✓ | — |
| 3 | GET | `/search` | `public_routes.py:search` | public | public | `@limiter("20/min")` + `@validate_query_params` | None | None | ✓ | — |
| 4 | GET | `/routes` | `public_routes.py:routes` | public | public | None | None | None | ✓ | — |
| 5 | GET | `/announcements` | `public_routes.py:announcements_public_feed` | public | public | None | None | None | ✓ | — |
| 6 | GET | `/sitemap.xml` | `public_routes.py:sitemap` | public | public | None | `subprocess.run(["git","log"])` (hardcoded) | None | ✓ | — |
| 7 | GET | `/robots.txt` | `public_routes.py:robots` | public | public | None | None | None | ✓ | — |
| 8 | GET | `/google364b8336ce52ae86.html` | `public_routes.py:verify_site` | public | public | None | None | None | ✓ | — |
| 9 | GET | `/sw.js` | `app_setup.py:serve_sw` | public | public | None | None | None | ✓ | — |
| 10 | GET | `/manifest.json` | `app_setup.py:serve_manifest` | public | public | None | None | CSRF-exempt | ✓ | — |
| 11 | GET | `/offline` | `app_setup.py:serve_offline` | public | public | None | None | None | ✓ | — |
| 12 | GET | `/logout` | `public_routes.py:logout_redirect` | public | public | None | None | Redirect only | ✓ | — |
| 13 | GET | `/login` | `public_routes.py:login_redirect` | public | public | None | None | Redirect only | ✓ | — |
| 14 | GET | `/register` | `public_routes.py:register_redirect` | public | public | None | None | Redirect only | ✓ | — |
| 15 | GET | `/forgot-password` | `public_routes.py:forgot_password_redirect` | public | public | None | None | Redirect only | ✓ | — |

## Section B: Auth Routes (public by design — identity-establishing)

| # | Method | Path | Handler (file:line) | Expected Scope | Actual Scope | Layer-1 Guard | In-Body Authz | Hidden Channels | Anomaly | Finding |
|---|--------|------|---------------------|----------------|-------------|---------------|---------------|-----------------|---------|---------|
| 16 | GET/POST | `/auth/login` | `auth/login.py:login_view` | public | public | `@limiter("5/min")` | Password check → session create | None | ✓ | — |
| 17 | GET/POST | `/auth/logout` | `auth/login.py:logout_view` | self | self | `@login_required` | Session destroy | None | ✓ | — |
| 18 | GET/POST | `/auth/register` | `auth/register.py:register_view` | public | public | None | `@validate_form_data` | None | ✓ | — |
| 19 | GET/POST | `/auth/register/business` | `auth/register.py:register_business_view` | public | public | None | `@validate_form_data` | None | ✓ | — |
| 20 | GET | `/auth/pending-approval` | `auth/register.py:pending_approval_view` | public | public | None | None | None | ✓ | — |
| 21 | POST | `/auth/google-login` | `auth/oauth.py:google_login_view` | public | public | None | `verify_oauth2_token` | None | ✓ | — |
| 22 | GET/POST | `/auth/select-role` | `auth/oauth.py:select_role_view` | public | public | None | Session `oauth_signup` trust (no re-verify) | Session-stored OAuth data not re-verified | ✓* | — |
| 23 | GET/POST | `/auth/forgot-password` | `auth/password.py:forgot_password_view` | public | public | `@limiter("5/min")` | Email lookup → token create | None | ✓ | — |
| 24 | GET/POST | `/auth/reset-password/<token>` | `auth/password.py:reset_password_view` | public | public | None | Token validation + expiry | None | ✓ | — |
| 25 | GET | `/auth/api/users/search` | `auth/api.py:api_user_search_view` | admin? | **user** (any authenticated) | `@login_required` | None — returns other users' email/barangay | **PII leak**: any auth user can enumerate all approved users | ⚠ | **p5-010** |

> *Row 22: `select_role_view` trusts session data set during OAuth flow without re-verifying the Google token. If SECRET_KEY is weak (default: `"your-secret-key-here"`), session forging is possible. See `config.py`.

## Section C: Public API v1 Pages (by-design public)

| # | Method | Path | Handler (file:line) | Expected Scope | Actual Scope | Layer-1 Guard | In-Body Authz | Hidden Channels | Anomaly | Finding |
|---|--------|------|---------------------|----------------|-------------|---------------|---------------|-----------------|---------|---------|
| 26 | GET | `/v1/map` | `api_v1/public.py:map_v2_view` | public | public | None | None | None | ✓ | — |
| 27 | GET | `/v1/map-dashboard` | `api_v1/public.py:map_dashboard_view` | public | public | None | None | None | ✓ | — |
| 28 | GET | `/v1/events` | `api_v1/public.py:events_v2_view` | public | public | None | None | None | ✓ | — |
| 29 | GET | `/v1/lgu-events` | `api_v1/public.py:lgu_events_view` | public | public | None | None | None | ✓ | — |
| 30 | GET | `/v1/attractions/<id>` | `api_v1/public.py:attraction_detail_v1_view` | public | public | None | None | None | ✓ | — |
| 31 | GET | `/v1/barangay` | `api_v1/public.py:barangays_v1_view` | public | public | None | None | None | ✓ | — |
| 32 | GET | `/attractions/<id>` | `attractions/routes.py:detail` | public | public | None | None | Redirect → `/v1/attractions/<id>` | ✓ | — |
| 33 | GET | `/attractions/api` | `attractions/routes.py:api_list` | public | public | `@limiter("20/min")` | None | None | ✓ | — |
| 34 | GET | `/attractions/<id>/reviews` | `attractions/routes.py:get_reviews` | public | public | None | None | None | ✓ | — |
| 35 | GET | `/business/` | `business/routes.py:index` | public | public | None | None | None | ✓ | — |
| 36 | GET | `/business/<id>` | `business/routes.py:detail` | public | public | None | None | None | ✓ | — |
| 37 | GET | `/business/api` | `business/routes.py:api_list` | public | public | `@limiter("20/min")` | None | None | ✓ | — |
| 38 | GET | `/gallery/` | `gallery/routes.py:index` | public | public | None | None | None | ✓ | — |
| 39 | GET | `/heritage/` | `heritage/routes.py:index` | public | public | None | None | None | ✓ | — |
| 40 | GET | `/heritage/<type>` | `heritage/routes.py:type_list` | public | public | None | None | None | ✓ | — |
| 41 | GET | `/heritage/<type>/<id>` | `heritage/routes.py:detail` | public | public | None | None | None | ✓ | — |
| 42 | GET | `/heritage/api/<type>` | `heritage/routes.py:api_list` | public | public | None | None | None | ✓ | — |
| 43 | GET | `/heritage/api/<type>/<id>` | `heritage/routes.py:api_detail` | public | public | None | None | None | ✓ | — |
| 44 | GET | `/heritage/api/types` | `heritage/routes.py:api_types` | public | public | None | None | None | ✓ | — |
| 45 | GET | `/events/` | `events/routes.py:index` | public | public | None | None | Redirect → `/v1/events` | ✓ | — |
| 46 | GET | `/barangay/` | `barangay/routes.py:index` | public | public | None | None | Redirect → `/v1/barangay` | ✓ | — |
| 47 | GET | `/barangay/<name>` | `barangay/routes.py:profile` | public | public | None | None | None | ✓ | — |
| 48 | GET | `/booking/api/availability/<id>` | `booking/routes.py:get_availability` | public | public | None | None | None | ✓ | — |

## Section D: Public Data APIs (by-design public)

| # | Method | Path | Handler (file:line) | Expected Scope | Actual Scope | Layer-1 Guard | In-Body Authz | Hidden Channels | Anomaly | Finding |
|---|--------|------|---------------------|----------------|-------------|---------------|---------------|-----------------|---------|---------|
| 49 | GET | `/api/attractions` | `core/api_routes.py:api_attractions` | public | public | `@limiter("20/min")` | None | None | ✓ | — |
| 50 | GET | `/api/gemini/context` | `core/api_routes.py:gemini_context` | public | public | None | None | None | ✓ | — |
| 51 | GET | `/api/tiles/<z>/<x>/<y>.pbf` | `core/map_routes.py:get_tile` | public | public | `@limiter("2000/min")` | None | None | ✓ | — |
| 52 | GET | `/api/tiles/combined/<z>/<x>/<y>.pbf` | `core/map_routes.py:get_combined_tile` | public | public | `@limiter("2000/min")` | None | None | ✓ | — |
| 53 | GET | `/api/tiles/layers` | `core/map_routes.py:get_available_layers` | public | public | `@limiter("30/min")` | None | None | ✓ | — |
| 54 | POST | `/api/v1/routing/optimize` | `routing/routes.py:optimize_route` | public | public | `@limiter("5/min")` | None | None | ✓ | — |
| 55 | POST | `/api/v1/routing/directions` | `routing/routes.py:get_directions` | public | public | `@limiter("10/min")` | None | None | ✓ | — |
| 56 | GET | `/api/v1/routing/suggested` | `routing/routes.py:get_suggested` | public | public | `@limiter("30/min")` | None | None | ✓ | — |
| 57 | POST | `/notifications/subscribe` | `notifications/routes.py:subscribe` | public | public | None | `@validate_form_data` (email) | None | ✓ | — |

## Section E: ANOMALOUS Endpoints — Should Require Auth But Don't

| # | Method | Path | Handler (file:line) | Expected Scope | Actual Scope | Layer-1 Guard | In-Body Authz | Hidden Channels | Anomaly | Finding |
|---|--------|------|---------------------|----------------|-------------|---------------|---------------|-----------------|---------|---------|
| 58 | GET | `/test-supabase` | `core/public_routes.py:test_supabase` | **admin** (debug) | **anon** — any visitor | **None** | None — returns Supabase query results | None | ⚠ **CRITICAL** | **p5-002** |
| 59 | POST | `/api/map-feedback` | `core/api_routes.py:submit_map_feedback` | user/auth | **anon** — any visitor | **None** | None — writes `MapFeedback` to DB | None | ⚠ **MEDIUM** | **p5-008** |
| 60 | GET | `/api/gemini/config` | `core/api_routes.py:gemini_config` | **admin/secret** | **anon** — any visitor | **None** | None — returns `GEMINI_API_KEY` | None | ⚠ **CRITICAL** | **p5-001** |
| 61 | POST | `/api/tiles/cache/invalidate` | `core/map_routes.py:invalidate_cache` | **admin** | **anon** — any visitor | `@limiter("10/hour")` only | None — purges Redis tile cache | Rate limit on destructive action | ⚠ **HIGH** | **p5-003** |

## Section F: Authenticated Endpoints with Guard Anomalies

| # | Method | Path | Handler (file:line) | Expected Scope | Actual Scope | Layer-1 Guard | In-Body Authz | Hidden Channels | Anomaly | Finding |
|---|--------|------|---------------------|----------------|-------------|---------------|---------------|-----------------|---------|---------|
| 62 | POST | `/admin/visits/log` | `admin_core/visits.py:log_visit` | admin/contributor/biz_owner | **user** (any auth) | `@login_required` | **None** — no role check | None | ⚠ **HIGH** — inconsistent with all `/admin/visits/*` siblings | **p5-009** |
| 63 | POST | `/booking/api/admin/update_status` | `booking/routes.py:update_status` | admin/contributor/biz_owner (own) | admin/contributor/biz_owner (**any**, no ownership check) | `@login_required` | Role check only (`admin`/`contributor`/`business_owner`) — **no ownership filter on reservation** | None | ⚠ **HIGH** — IDOR/BOLA | **p5-004** |

## Section G: Authenticated Endpoints — Correctly Guarded (sample)

| # | Method | Path | Handler (file:line) | Expected Scope | Actual Scope | Layer-1 Guard | In-Body Authz | Hidden Channels | Anomaly | Finding |
|---|--------|------|---------------------|----------------|-------------|---------------|---------------|-----------------|---------|---------|
| 64 | GET | `/admin/dashboard` | `admin_core/dashboard.py:admin_dashboard` | admin | admin | `@login_required` | `role == "admin"` | None | ✓ | — |
| 65 | GET/POST | `/admin/attractions/add` | `attractions/admin_routes.py:add_attraction` | admin/contributor | admin/contributor | `@login_required` | `role in [admin, contributor]` | None | ✓ | — |
| 66 | GET | `/admin/attractions/edit/<id>` | `attractions/admin_routes.py:edit_attraction` | admin/owner/contributor | admin/owner/contributor | `@login_required` | admin OR owner OR contributor(barangay) | None | ✓ | — |
| 67 | GET | `/admin/heritage/<type>/add` | `heritage/admin_routes.py:admin_heritage_add` | admin | admin | `@login_required` | `_require_admin()` | None | ✓ | — |
| 68 | GET | `/user/dashboard` | `core/user_routes.py:dashboard` | user | user | `@login_required` + `@user_required` | None | None | ✓ | — |
| 69 | POST | `/user/favorites/toggle` | `core/user_routes.py:toggle_favorite` | self | self | `@login_required` + `@user_required` | `current_user.id` filter | None | ✓ | — |
| 70 | POST | `/booking/api/reserve` | `booking/routes.py:reserve_slot` | self | self | `@login_required` | `user_id=current_user.id` on reservation | None | ✓ | — |
| 71 | POST | `/business/establishment/create` | `business/routes.py:create_establishment` | self (approved) | self (approved) | `@login_required` + `@approved_business_owner_required` | `owner_id=current_user.id` | None | ✓ | — |
| 72 | POST | `/business/rooms/add` | `business/routes.py:add_room` | self (approved) | self (approved) | `@login_required` + `@approved_business_owner_required` | `_get_owner_establishment()` + ownership check | None | ✓ | — |
| 73 | GET/POST | `/admin/heritage/<type>/edit/<id>` | `heritage/admin_routes.py:admin_heritage_edit` | admin | admin | `@login_required` | `_require_admin()` | None | ✓ | — |
| 74 | POST | `/admin/heritage/<type>/delete/<id>` | `heritage/admin_routes.py:admin_heritage_delete` | admin | admin | `@login_required` | `_require_admin()` | None | ✓ | — |
| 75 | GET/POST | `/admin/v1/documents/import` | `api_v1/documents.py:v1_document_import` | admin | admin | `@login_required` | admin check in-handler | None | ✓ | — |
| 76 | POST | `/gamification/api/checkin` | `gamification/routes.py:verify_checkin` | self | self | `@login_required` + `@limiter("10/min")` | `user_id=current_user.id` on checkin | None | ✓ | — |
| 77 | GET | `/gamification/my-passport` | `gamification/routes.py:view_passport` | self | self | `@login_required` | `current_user.passports` | None | ✓ | — |
| 78 | GET | `/chat/<id>` | `chat/routes.py:chat_room` | self | self (partial) | `@login_required` | Participant check | None | ✓ | — |
| 79 | GET | `/admin/visits` | `admin_core/visits.py:visits_index` | admin/contributor/biz_owner | admin/contributor/biz_owner | `@login_required` | Role check in-handler | None | ✓ | — |
| 80 | GET | `/admin/visits/export` | `admin_core/visits.py:export_visits` | admin/contributor/biz_owner | admin/contributor/biz_owner | `@login_required` | Role check in-handler | None | ✓ | — |
| 81 | GET | `/admin/visits/registry` | `admin_core/visits.py:visitor_registry` | admin/contributor/biz_owner | admin/contributor/biz_owner | `@login_required` | Role check in-handler | None | ✓ | — |
| 82 | POST | `/pull` | `core/update_routes.py:pull_updates` | admin+token | admin+token (bypassable) | `@require_update_token` + `@limiter("1/min")` | Admin role + token comparison | **Token bypass** if `UPDATE_TOKEN` env unset | ⚠ **MEDIUM** | **p5-007** |
| 83 | GET | `/admin/establishments` | `business/admin_routes.py:manage_establishments` | admin | admin | `@login_required` + `@admin_required` | None | None | ✓ | — |
| 84 | POST | `/admin/establishments/<id>/approve` | `business/admin_routes.py:approve_establishment` | admin | admin | `@login_required` + `@admin_required` | None | None | ✓ | — |

## Section H: WebSocket Events

| # | Event | Handler (file:line) | Expected Scope | Actual Scope | Layer-1 Guard | In-Body Authz | Hidden Channels | Anomaly | Finding |
|---|-------|---------------------|----------------|-------------|---------------|---------------|-----------------|---------|---------|
| 85 | `connect` | `chat/sockets.py:handle_connect` | **anon** (allows) | **anon** — any origin | **None** — `cors_allowed_origins="*"` | None | **Wildcard CORS** — any origin can connect | ⚠ **MEDIUM** | **p5-005** |
| 86 | `disconnect` | `chat/sockets.py:handle_disconnect` | N/A | N/A | None | None | None | ✓ | — |
| 87 | `join` | `chat/sockets.py:on_join` | self (participant) or public (barangay) | self (participant) or public (barangay) | In-handler: `is_authenticated` check | Participant check; barangay auto-join | Barangay rooms auto-join for authenticated users | ✓ | — |
| 88 | `send_message` | `chat/sockets.py:handle_send_message` | self (participant) | self (participant) | In-handler: `is_authenticated` check | Participant check | None | ✓ | — |
| 89 | `typing` | `chat/sockets.py:handle_typing` | team (room members) | team (room members) | In-handler: `is_authenticated` check | None (broadcasts username) | None | ✓ | — |
| 90 | `leave` | `chat/sockets.py:on_leave` | **public** (any can leave) | **public** — no auth check | **None** | None | None | ✓ | — |

## Section I: Non-Route Entry Points

| # | Kind | Entry point (file:line) | Expected Scope | Actual Scope | Guard | Hidden Channels | Anomaly | Finding |
|---|------|-------------------------|----------------|-------------|-------|-----------------|---------|---------|
| 91 | Session self-service | `gamification/routes.py:start_navigation` | self (authed) | self (authed) but **self-trusting** | `@login_required` | `session['active_nav']` set by user — no server-side verification of navigation state | ⚠ **MEDIUM** | **p5-006** |
| 92 | Session self-service | `gamification/routes.py:scan_qr` | self (authed, nav guard) | self (authed, nav guard) | `@login_required` + `session['active_nav']` match | Guard depends on session value set by #91 | ⚠ (depends on #91) | — (covered by p5-006) |
| 93 | Cookie config | `config.py` (SECRET_KEY default) | secret | **default**: `"your-secret-key-here"` | Environment variable with fail-open default | If default used, session forging → full auth bypass | ⚠ **HIGH** | **p4-002** (already filed) |
| 94 | Debug mode | `app.py:135` `debug=True` | dev only | dev+production (Docker entry) | None | Werkzeug debugger in production entry point | ⚠ **HIGH** | **p4-007** (already filed) |
| 95 | Proxy header trust | `app.py:40` `ProxyFix` | Vercel only | Vercel + direct access | None | `X-Forwarded-For` spoofable → rate limit bypass | ⚠ **MEDIUM** | **p4-013** (already filed) |
| 96 | CORS wildcard | `app.py:55` `cors_allowed_origins="*"` | internal | public | None | Cross-site WebSocket hijacking | ⚠ **MEDIUM** | **p5-005** (already filed) |

---

## Anomaly Summary

| # | Endpoint | Anomaly Class | Severity | Finding ID |
|---|----------|---------------|----------|------------|
| 1 | `GET /api/gemini/config` | missing-guard (API key leak) | **CRITICAL** | p5-001 |
| 2 | `GET /test-supabase` | missing-guard (debug endpoint) | **HIGH** | p5-002 |
| 3 | `POST /api/tiles/cache/invalidate` | missing-guard (cache DoS) | **HIGH** | p5-003 |
| 4 | `POST /booking/api/admin/update_status` | IDOR — no ownership check | **HIGH** | p5-004 |
| 5 | `POST /admin/visits/log` | inconsistent-guard (sibling group) | **HIGH** | p5-009 |
| 6 | `GET /auth/api/users/search` | excessive PII exposure | **MEDIUM** | **p5-010** (new) |
| 7 | `POST /api/map-feedback` | missing-guard (unauth DB write) | **MEDIUM** | p5-008 |
| 8 | WebSocket `connect` | CORS wildcard + anon | **MEDIUM** | p5-005 |
| 9 | `POST /gamification/api/start-navigation` | session self-trust | **MEDIUM** | p5-006 |
| 10 | `GET/POST /pull` | token bypass (env unset) | **MEDIUM** | p5-007 |
| 11 | `config.py` SECRET_KEY default | fail-open secret | **HIGH** | p4-002 |
| 12 | `app.py` debug=True entry | debug in production | **HIGH** | p4-007 |
| 13 | `ProxyFix` header trust | rate limit bypass | **MEDIUM** | p4-013 |

---

## Role × Endpoint Coverage Matrix (Compact View)

| Role | Read-only public data | Write operations | Admin operations | IDOR risk |
|------|----------------------|-----------------|-----------------|-----------|
| **anon** | 48 routes (Sections A-D) | 4 endpoints (Section E: map-feedback, cache/invalidate, gemini/config leak, test-supabase) | 0 (but gemini/config leaks secret) | N/A |
| **user** | All anon + 25 (Section G user routes) | 1 anomalous: `/admin/visits/log` (Section F #62) | 0 (but visits/log is anomalous) | N/A |
| **contributor** | All user + `/admin/attractions/add` | `/admin/visits/log` (no ownership check) | Heritage CRUD (admin-only by `_require_admin`) | Low — barangay-scoped |
| **business_owner** | All user + `/business/*` public | `/admin/visits/log` + `/booking/api/admin/update_status` (**no ownership**) | 0 | **HIGH** — any biz_owner can modify any reservation |
| **admin** | Everything | Everything | Everything + `/pull` (token bypass risk) | None — admin has full access by design |
