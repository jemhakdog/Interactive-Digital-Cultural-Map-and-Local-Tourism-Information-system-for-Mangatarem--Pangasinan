# Architecture — Entry Points Inventory

> **Generated**: 2026-08-18  
> **Repository**: capstone_system (GoMangatarem)  
> **Purpose**: Reusable entry point map for Phases 4–11 of the piolium deep audit

---

## Public Routes (Unauthenticated)

### Core Pages

| Route | Method | Handler (file:line) | Auth | Rate Limit | Description |
|-------|--------|---------------------|------|------------|-------------|
| `/` | GET | `modules/core/public_routes.py:index` | None | Default 100/min | Home page, redirects authenticated users to role dashboard |
| `/map` | GET | `modules/core/public_routes.py:map_view` | None | Default | Redirect to `/v1/map` |
| `/search` | GET | `modules/core/public_routes.py:search` | None | 20/min | Unified search (attractions, events, barangays) |
| `/routes` | GET | `modules/core/public_routes.py:routes` | None | Default | Tourism routes display |
| `/announcements` | GET | `modules/core/public_routes.py:announcements_public_feed` | None | Default | Public announcements feed |
| `/sitemap.xml` | GET | `modules/core/public_routes.py:sitemap` | None | Default | Dynamic XML sitemap |
| `/robots.txt` | GET | `modules/core/public_routes.py:robots` | None | Default | Robots.txt |
| `/google364b8336ce52ae86.html` | GET | `modules/core/public_routes.py:verify_site` | None | Default | Google Search Console verification |
| `/test-supabase` | GET | `modules/core/public_routes.py:test_supabase` | None | Default | **Debug: Supabase test endpoint** |
| `/sw.js` | GET | `core/app_setup.py:serve_sw` | None | Default | Service worker |
| `/manifest.json` | GET | `core/app_setup.py:serve_manifest` | None | Default | PWA manifest (CSRF-exempt) |
| `/offline` | GET | `core/app_setup.py:serve_offline` | None | Default | Offline page |
| `/logout` | GET | `modules/core/public_routes.py:logout_redirect` | None | Default | Legacy redirect to /auth/logout |
| `/login` | GET | `modules/core/public_routes.py:login_redirect` | None | Default | Legacy redirect to /auth/login |
| `/register` | GET | `modules/core/public_routes.py:register_redirect` | None | Default | Legacy redirect to /auth/register |
| `/forgot-password` | GET | `modules/core/public_routes.py:forgot_password_redirect` | None | Default | Legacy redirect |

### API v1 Public

| Route | Method | Handler (file:line) | Auth | Rate Limit | Description |
|-------|--------|---------------------|------|------------|-------------|
| `/v1/map` | GET | `modules/api_v1/public.py:map_v2_view` | None | Default | Interactive map v2 |
| `/v1/map-dashboard` | GET | `modules/api_v1/public.py:map_dashboard_view` | None | Default | Desktop map dashboard |
| `/v1/events` | GET | `modules/api_v1/public.py:events_v2_view` | None | Default | Events listing v2 |
| `/v1/lgu-events` | GET | `modules/api_v1/public.py:lgu_events_view` | None | Default | Scraped LGU events |
| `/v1/attractions/<id>` | GET | `modules/api_v1/public.py:attraction_detail_v1_view` | None | Default | Attraction detail page |
| `/v1/barangay` | GET | `modules/api_v1/public.py:barangays_v1_view` | None | Default | Barangay directory |

### Domain Module Public

| Route | Method | Handler (file:line) | Auth | Rate Limit | Description |
|-------|--------|---------------------|------|------------|-------------|
| `/attractions/<id>` | GET | `modules/attractions/routes.py:detail` | None | Default | Redirect to /v1/attractions/<id> |
| `/attractions/api` | GET | `modules/attractions/routes.py:api_list` | None | 20/min | Attractions JSON API |
| `/attractions/<id>/reviews` | GET | `modules/attractions/routes.py:get_reviews` | None | Default | Reviews for attraction |
| `/business/` | GET | `modules/business/routes.py:index` | None | Default | Establishment directory |
| `/business/<id>` | GET | `modules/business/routes.py:detail` | None | Default | Establishment detail |
| `/business/api` | GET | `modules/business/routes.py:api_list` | None | 20/min | Establishments JSON API |
| `/gallery/` | GET | `modules/gallery/routes.py:index` | None | Default | Gallery page |
| `/booking/api/availability/<id>` | GET | `modules/booking/routes.py:get_availability` | None | Default | Booking availability check |
| `/notifications/subscribe` | POST | `modules/notifications/routes.py:subscribe` | None | Default | Newsletter subscription |
| `/heritage/` | GET | `modules/heritage/routes.py:index` | None | Default | Heritage directory |
| `/events/` | GET | `modules/events/routes.py:index` | None | Default | Events listing |
| `/barangay/` | GET | `modules/barangay/routes.py:index` | None | Default | Barangay directory |

### API Endpoints (No Auth Required)

| Route | Method | Handler (file:line) | Auth | Rate Limit | Description |
|-------|--------|---------------------|------|------------|-------------|
| `/api/attractions` | GET | `modules/core/api_routes.py:api_attractions` | None | 20/min | Attractions JSON with pagination |
| `/api/map-feedback` | POST | `modules/core/api_routes.py:submit_map_feedback` | None | Default | **Submit map feedback (no auth!)** |
| `/api/gemini/config` | GET | `modules/core/api_routes.py:gemini_config` | None | Default | **Returns GEMINI_API_KEY to any visitor** |
| `/api/gemini/context` | GET | `modules/core/api_routes.py:gemini_context` | None | Default | Gemini system instruction context |
| `/api/tiles/<z>/<x>/<y>.pbf` | GET | `modules/core/map_routes.py:get_tile` | None | 2000/min | Mapbox Vector Tiles |
| `/api/tiles/combined/<z>/<x>/<y>.pbf` | GET | `modules/core/map_routes.py:get_combined_tile` | None | 2000/min | Combined MVT tiles |
| `/api/tiles/layers` | GET | `modules/core/map_routes.py:get_available_layers` | None | 30/min | Tile layer metadata |
| `/api/tiles/cache/invalidate` | POST | `modules/core/map_routes.py:invalidate_cache` | None | 10/hour | **Cache invalidation (no auth!)** |
| `/api/v1/routing/optimize` | POST | `modules/routing/routes.py:optimize_route` | None | 5/min | Route optimization (OSRM) |
| `/api/v1/routing/directions` | POST | `modules/routing/routes.py:get_directions` | None | 10/min | Directions (OSRM) |
| `/api/v1/routing/suggested` | GET | `modules/routing/routes.py:get_suggested` | None | 30/min | Suggested tourism routes |

### Auth Routes (Partially Public)

| Route | Method | Handler (file:line) | Auth | Rate Limit | Description |
|-------|--------|---------------------|------|------------|-------------|
| `/auth/login` | GET/POST | `modules/auth/routes.py:login_view` | None | 5/min | Login page |
| `/auth/logout` | GET/POST | `modules/auth/routes.py:logout_view` | `@login_required` | Default | Logout |
| `/auth/register` | GET/POST | `modules/auth/routes.py:register_view` | None | Default | User registration |
| `/auth/register/business` | GET/POST | `modules/auth/routes.py:register_business_view` | None | Default | Business registration |
| `/auth/pending-approval` | GET | `modules/auth/routes.py:pending_approval_view` | None | Default | Pending approval page |
| `/auth/google-login` | POST | `modules/auth/routes.py:google_login_view` | None | Default | Google OAuth login |
| `/auth/select-role` | GET/POST | `modules/auth/routes.py:select_role_view` | None | Default | OAuth role selection |
| `/auth/forgot-password` | GET/POST | `modules/auth/routes.py:forgot_password_view` | None | 5/min | Password reset request |
| `/auth/reset-password/<token>` | GET/POST | `modules/auth/routes.py:reset_password_view` | None | Default | Password reset form |
| `/auth/api/users/search` | GET | `modules/auth/routes.py:api_user_search_view` | None | Default | User search API |

---

## Authenticated Routes

### Admin Routes (`/admin/*`)

| Route | Method | Handler (file:line) | Auth | Role Check | Description |
|-------|--------|---------------------|------|------------|-------------|
| `/admin/` | GET | `modules/admin_core/dashboard.py:admin_dashboard` | `@login_required` | admin | Admin dashboard |
| `/admin/users/approve/<id>` | GET | `modules/admin_core/users.py:approve_user` | `@login_required` | admin (handler) | Approve contributor |
| `/admin/users/reject/<id>` | GET | `modules/admin_core/users.py:reject_user` | `@login_required` | admin (handler) | Reject/delete contributor |
| `/admin/gallery/approve/<id>` | GET | `modules/admin_core/content.py:approve_gallery` | `@login_required` | admin (handler) | Approve gallery item |
| `/admin/gallery/reject/<id>` | GET | `modules/admin_core/content.py:reject_gallery` | `@login_required` | admin (handler) | Reject gallery item |
| `/admin/reviews` | GET | `modules/admin_core/content.py:reviews_list` | `@login_required` | admin (handler) | Reviews moderation |
| `/admin/reviews/approve/<id>` | GET/POST | `modules/admin_core/content.py:approve_review` | `@login_required` | admin (handler) | Approve review |
| `/admin/reviews/reject/<id>` | GET/POST | `modules/admin_core/content.py:reject_review` | `@login_required` | admin (handler) | Reject review |
| `/admin/announcements/approve/<id>` | GET | `modules/admin_core/content.py:admin_approve_announcement` | `@login_required` | admin (handler) | Approve announcement |
| `/admin/announcements/reject/<id>` | GET | `modules/admin_core/content.py:admin_reject_announcement` | `@login_required` | admin (handler) | Reject announcement |
| `/admin/attractions` | GET | `modules/attractions/admin_routes.py:admin_attractions` | `@login_required` | admin (handler) | Attractions management |
| `/admin/attractions/add` | GET/POST | `modules/attractions/admin_routes.py:add_attraction` | `@login_required` | admin/contributor (handler) | Add attraction |
| `/admin/attractions/edit/<id>` | GET/POST | `modules/attractions/admin_routes.py:edit_attraction` | `@login_required` | admin/owner/contributor (handler) | Edit attraction |
| `/admin/attractions/delete/<id>` | GET | `modules/attractions/admin_routes.py:delete_attraction` | `@login_required` | admin/owner (handler) | Delete attraction |
| `/admin/heritage` | GET | `modules/heritage/admin_routes.py:admin_heritage_dashboard` | `@login_required` | admin (handler) | Heritage dashboard |
| `/admin/heritage/<type>` | GET | `modules/heritage/admin_routes.py:admin_heritage_list` | `@login_required` | admin (handler) | Heritage list |
| `/admin/heritage/<type>/add` | GET/POST | `modules/heritage/admin_routes.py:admin_heritage_add` | `@login_required` | admin (handler) | Add heritage |
| `/admin/heritage/<type>/edit/<id>` | GET/POST | `modules/heritage/admin_routes.py:admin_heritage_edit` | `@login_required` | admin (handler) | Edit heritage |
| `/admin/heritage/<type>/delete/<id>` | POST | `modules/heritage/admin_routes.py:admin_heritage_delete` | `@login_required` | admin (handler) | Delete heritage |
| `/admin/heritage/<type>/json` | GET | `modules/heritage/admin_routes.py:admin_heritage_json` | `@login_required` | admin (handler) | Heritage JSON API |
| `/admin/heritage/export/docx/<id>` | GET | `modules/heritage/admin_routes.py:admin_heritage_export_docx` | `@login_required` | admin (handler) | Heritage DOCX export |
| `/admin/heritage/export/excel/<id>` | GET | `modules/heritage/admin_routes.py:admin_heritage_export_excel` | `@login_required` | admin (handler) | Heritage Excel export |
| `/admin/v1/documents` | GET | `modules/api_v1/documents.py:v1_documents_view` | `@login_required` | admin (handler) | Documents management |
| `/admin/v1/documents/<slug>` | GET | `modules/api_v1/documents.py:v1_document_view` | `@login_required` | admin (handler) | View document |
| `/admin/v1/documents/<slug>/edit` | GET/POST | `modules/api_v1/documents.py:v1_document_edit` | `@login_required` | admin (handler) | Edit document |
| `/admin/v1/documents/<slug>/export` | GET | `modules/api_v1/documents.py:v1_document_export` | `@login_required` | admin (handler) | Export DOCX |
| `/admin/v1/documents/export-all` | GET | `modules/api_v1/documents.py:v1_documents_export_all` | `@login_required` | admin (handler) | Export all as ZIP |
| `/admin/v1/documents/import` | POST | `modules/api_v1/documents.py:v1_document_import` | `@login_required` | admin (handler) | Import DOCX |
| `/admin/v1/documents/create/<slug>` | GET/POST | `modules/api_v1/documents.py:v1_document_create` | `@login_required` | admin (handler) | Create from template |
| `/admin/v1/documents/record/<id>/edit` | GET/POST | `modules/api_v1/documents.py:v1_document_record_edit` | `@login_required` | admin (handler) | Edit record |
| `/admin/v1/documents/download/<file>` | GET | `modules/api_v1/documents.py:v1_document_download` | `@login_required` | admin (handler) | Download DOCX |
| `/admin/newsletter` | GET | `modules/notifications/admin_routes.py:index` | `@login_required` | admin (handler) | Newsletter dashboard |
| `/admin/newsletter/compose` | GET/POST | `modules/notifications/admin_routes.py:compose` | `@login_required` | admin (handler) | Compose newsletter |
| `/admin/newsletter/delete/<id>` | POST | `modules/notifications/admin_routes.py:delete_subscriber` | `@login_required` | admin (handler) | Delete subscriber |
| `/admin/newsletter/export` | GET | `modules/notifications/admin_routes.py:export_subscribers` | `@login_required` | admin (handler) | Export CSV |
| `/admin/newsletter/history` | GET | `modules/notifications/admin_routes.py:history` | `@login_required` | admin (handler) | Campaign history |

### User Routes (`/user/*`)

| Route | Method | Handler (file:line) | Auth | Role Check | Description |
|-------|--------|---------------------|------|------------|-------------|
| `/user/dashboard` | GET | `modules/core/user_routes.py:dashboard` | `@login_required` | user (handler) | User dashboard |
| `/user/profile` | GET/POST | `modules/core/user_routes.py:profile` | `@login_required` | user (handler) | Edit profile |
| `/user/favorites` | GET | `modules/core/user_routes.py:favorites` | `@login_required` | user (handler) | View favorites |
| `/user/favorites/toggle` | POST | `modules/core/user_routes.py:toggle_favorite` | `@login_required` | user (handler) | Toggle favorite (JSON) |
| `/user/favorites/ids` | GET | `modules/core/user_routes.py:get_favorite_ids` | `@login_required` | Default | Get favorite IDs (JSON) |
| `/user/visits` | GET | `modules/core/user_routes.py:visits` | `@login_required` | user (handler) | View visits |
| `/user/visits/ids` | GET | `modules/core/user_routes.py:get_visited_ids` | `@login_required` | Default | Get visited IDs (JSON) |
| `/user/visits/log` | POST | `modules/core/user_routes.py:log_personal_visit` | `@login_required` | user (handler) | Log personal visit |
| `/user/my-events` | GET | `modules/core/user_routes.py:my_events` | `@login_required` | user (handler) | My events |
| `/user/contributions` | GET | `modules/core/user_routes.py:contributions` | `@login_required` | user (handler) | My contributions |

### Business Owner Routes (`/business/*`)

| Route | Method | Handler (file:line) | Auth | Role Check | Description |
|-------|--------|---------------------|------|------------|-------------|
| `/business/dashboard` | GET | `modules/business/routes.py:dashboard` | `@login_required` | business_owner | Business dashboard |
| `/business/verify` | POST | `modules/business/routes.py:submit_verification` | `@login_required` | business_owner | Submit verification |
| `/business/establishment/create` | GET/POST | `modules/business/routes.py:create_establishment` | `@login_required` | approved_business_owner | Create establishment |
| `/business/establishment/edit` | GET/POST | `modules/business/routes.py:edit_establishment` | `@login_required` | approved_business_owner | Edit establishment |
| `/business/rooms` | GET | `modules/business/routes.py:manage_rooms` | `@login_required` | approved_business_owner | Manage rooms |
| `/business/rooms/add` | POST | `modules/business/routes.py:add_room` | `@login_required` | approved_business_owner | Add room |
| `/business/rooms/<id>/edit` | POST | `modules/business/routes.py:edit_room` | `@login_required` | approved_business_owner | Edit room |
| `/business/rooms/<id>/delete` | POST | `modules/business/routes.py:delete_room` | `@login_required` | approved_business_owner | Delete room |
| `/business/menu` | GET | `modules/business/routes.py:manage_menu` | `@login_required` | approved_business_owner | Manage menu |
| `/business/menu/add` | POST | `modules/business/routes.py:add_menu_item` | `@login_required` | approved_business_owner | Add menu item |
| `/business/menu/<id>/edit` | POST | `modules/business/routes.py:edit_menu_item` | `@login_required` | approved_business_owner | Edit menu item |
| `/business/menu/<id>/delete` | POST | `modules/business/routes.py:delete_menu_item` | `@login_required` | approved_business_owner | Delete menu item |
| `/business/reviews` | GET | `modules/business/routes.py:view_reviews` | `@login_required` | approved_business_owner | View reviews |
| `/business/reviews/reply/<id>` | POST | `modules/business/routes.py:reply_to_review` | `@login_required` | approved_business_owner | Reply to review |
| `/business/browse` | GET | `modules/business/routes.py:browse_peers` | `@login_required` | approved_business_owner | Browse peers |
| `/business/<id>/review` | POST | `modules/business/routes.py:submit_review` | `@login_required` | Default | Submit review |

### Booking & Gamification Routes

| Route | Method | Handler (file:line) | Auth | Description |
|-------|--------|---------------------|------|-------------|
| `/booking/api/reserve` | POST | `modules/booking/routes.py:reserve_slot` | `@login_required` | Create reservation |
| `/booking/admin/dashboard` | GET | `modules/booking/routes.py:dashboard` | `@login_required` | Booking management |
| `/booking/api/admin/update_status` | POST | `modules/booking/routes.py:update_status` | `@login_required` | Update reservation status |
| `/booking/api/verify-arrival` | POST | `modules/booking/routes.py:verify_arrival` | `@login_required` | GPS arrival verification |
| `/gamification/scan/<type>/<id>` | GET | `modules/gamification/routes.py:scan_qr` | `@login_required` | QR scanner page |
| `/gamification/api/start-navigation` | POST | `modules/gamification/routes.py:start_navigation` | `@login_required` | Start active navigation |
| `/gamification/api/stop-navigation` | POST | `modules/gamification/routes.py:stop_navigation` | `@login_required` | Stop active navigation |
| `/gamification/api/checkin` | POST | `modules/gamification/routes.py:verify_checkin` | `@login_required` | GPS check-in validation |
| `/gamification/my-passport` | GET | `modules/gamification/routes.py:view_passport` | `@login_required` | Passport dashboard |

### Chat Routes (WebSocket)

| Route | Event | Handler (file:line) | Auth | Description |
|-------|-------|---------------------|------|-------------|
| WebSocket | `connect` | `modules/chat/sockets.py:handle_connect` | **None** | Client connection (allows anonymous) |
| WebSocket | `disconnect` | `modules/chat/sockets.py:handle_disconnect` | None | Client disconnection |
| WebSocket | `join` | `modules/chat/sockets.py:on_join` | Auth check in handler | Join room |
| WebSocket | `send_message` | `modules/chat/sockets.py:handle_send_message` | Auth check in handler | Send message |
| WebSocket | `typing` | `modules/chat/sockets.py:handle_typing` | Auth check in handler | Typing indicator |
| WebSocket | `leave` | `modules/chat/sockets.py:on_leave` | None | Leave room |
| `/chat/` | GET | `modules/chat/routes.py:chat_index` | `@login_required` | Chat interface |
| `/chat/<id>` | GET | `modules/chat/routes.py:chat_room` | `@login_required` | Chat room history |

### Update Endpoint

| Route | Method | Handler (file:line) | Auth | Rate Limit | Description |
|-------|--------|---------------------|------|------------|-------------|
| `/pull` | GET/POST | `modules/core/update_routes.py:pull_updates` | `require_update_token` (admin + token) | 1/min | **Git pull + file copy** |

---

## Attacker-Controlled Sources

| Source | Type | Location | Notes |
|--------|------|----------|-------|
| `request.form` | POST form data | All form handlers | Username, password, email, field values |
| `request.args` | GET query params | Search, filters, pagination | `q`, `category`, `barangay`, `page` |
| `request.get_json()` | JSON body | API endpoints | Routing coords, feedback, booking, chat |
| `request.files` | File upload | Gallery, reviews, documents, business verification | Images, DOCX, PDF |
| `request.headers` | HTTP headers | Auth detection, CSRF | `Accept`, `X-Requested-With` |
| `request.sid` | SocketIO session ID | WebSocket handlers | Session identifier |
| WebSocket `data` | SocketIO event payload | Chat handlers | `room_id`, `content`, `is_typing` |
| `os.environ` | Environment variables | Config, secrets | SECRET_KEY, UPDATE_TOKEN, API keys |
| `session` | Signed cookie session | OAuth flow, navigation | `oauth_signup`, `active_nav` |

---

## High-Value Sinks

| Sink | Location | Description | Risk |
|------|----------|-------------|------|
| `subprocess.run(["git", "pull"])` | `modules/core/update_routes.py:75` | OS command execution | **Critical — RCE** |
| `os.chdir()` | `modules/core/update_routes.py:69` | Directory change | Critical — filesystem access |
| `shutil.copy2()` | `modules/core/update_routes.py:85-100` | File copy | Critical — filesystem write |
| `file.save()` | `utils/file_helpers.py:79` | File upload to disk | High — arbitrary file write |
| `send_from_directory()` | `modules/api_v1/documents.py:265` | File serving | Medium — path traversal risk |
| `send_file()` | `modules/api_v1/documents.py:311,467` | In-memory file serving | Medium — info disclosure |
| `db.session.add()` + `commit()` | All modules | Database writes | Medium — data integrity |
| `requests.get(url)` | `modules/routing/routes.py:67` | External HTTP call | Medium — SSRF |
| `server.sendmail()` | `utils/email_sender.py:71` | Email sending | Medium — SMTP injection |
| `json.loads()` | `modules/api_v1/documents.py:376,406` | JSON parsing | Medium — parse errors |
| `Document()` (python-docx) | `modules/api_v1/documents.py:145` | DOCX parsing | Medium — XXE/DoS |
| `render_template()` | All route handlers | Template rendering | Low — SSTI (if autoescape bypassed) |

---

## Key Source Files

| File | Security Relevance |
|------|-------------------|
| `app.py` | Application factory, ProxyFix, CSRF, session config |
| `config.py` | SECRET_KEY, session cookie settings, CSRF config |
| `extensions.py` | Extension initialization (db, login, limiter, csrf, socketio) |
| `models.py` | Model import hub (shim) |
| `modules/auth/models.py` | User model, password hashing, reset tokens |
| `modules/auth/login.py` | Authentication logic |
| `modules/auth/oauth.py` | Google OAuth integration |
| `modules/auth/password.py` | Password reset flow |
| `modules/core/update_routes.py` | **Critical: subprocess git pull** |
| `modules/core/api_routes.py` | **Critical: Gemini API key leak, map feedback** |
| `modules/core/public_routes.py` | Public pages, search, sitemap |
| `modules/core/map_routes.py` | MVT tile serving, cache invalidation |
| `modules/core/user_routes.py` | User dashboard and profile |
| `modules/api_v1/documents.py` | Document management, DOCX import/export |
| `modules/api_v1/public.py` | Map v2, events, attraction detail |
| `modules/admin_core/content.py` | Content moderation |
| `modules/admin_core/users.py` | User approval |
| `modules/admin_core/documents.py` | Document redirects |
| `modules/attractions/admin_routes.py` | Attraction CRUD (admin) |
| `modules/attractions/routes.py` | Attraction API, reviews |
| `modules/heritage/admin_routes.py` | Heritage CRUD (admin) |
| `modules/heritage/exporter.py` | Excel export |
| `modules/business/routes.py` | Business directory, owner dashboard |
| `modules/chat/sockets.py` | WebSocket handlers |
| `modules/chat/routes.py` | Chat routes |
| `modules/booking/routes.py` | Booking, GPS verification |
| `modules/gamification/routes.py` | QR/GPS check-in, badges |
| `modules/notifications/routes.py` | Newsletter subscription |
| `modules/notifications/admin_routes.py` | Newsletter management |
| `modules/routing/routes.py` | OSRM route optimization |
| `utils/security.py` | Input validation, sanitization |
| `utils/file_helpers.py` | File upload handling |
| `utils/validators.py` | Form/query validation decorators |
| `utils/email_sender.py` | SMTP email sending |
| `core/app_setup.py` | Error handlers, security headers, CSP |
