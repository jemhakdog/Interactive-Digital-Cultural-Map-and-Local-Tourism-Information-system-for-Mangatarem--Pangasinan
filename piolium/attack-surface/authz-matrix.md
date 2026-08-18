# Authorization Matrix

> **Generated**: 2026-08-18  
> **Phase**: 6 — Authorization & Access Control  
> **Repository**: capstone_system (GoMangatarem)

**Coverage stats**: 134 endpoints discovered | 4 endpoints with no guard detected (missing-guard) | 31 endpoints taking object-id parameter  
**Frameworks covered**: Flask 3.1.2, Flask-Login 0.6.3, Flask-SocketIO 5.6.1, Flask-WTF CSRF  
**Coverage gaps**: WebSocket transport-level auth (anonymous connect allowed, per-event auth); dynamic route registration via `auth_bp.add_url_rule()` (all mapped); no GraphQL/gRPC/Celery

---

## Public Routes (No Auth Required)

| # | Method | Path / Topic / RPC | Handler (file:line) | Layer-1 Guard | In-body Authz | Router/Middleware Guard | Hidden Control Channels | Object-ID Param | Ownership Check? | Tenant Filter? | Expected Scope |
|---|--------|--------------------|---------------------|---------------|---------------|-------------------------|-------------------------|------------------|------------------|----------------|-----------------|
| 1 | GET | `/` | `modules/core/public_routes.py:index` | None | `current_user.is_authenticated` redirect to role dashboard | None | None | No | N/A | N/A | public |
| 2 | GET | `/map` | `modules/core/public_routes.py:map_view` | None | None | None | None | No | N/A | N/A | public |
| 3 | GET | `/search` | `modules/core/public_routes.py:search` | `@limiter.limit("20/min")` + `@validate_query_params` | None | None | None | No | N/A | N/A | public |
| 4 | GET | `/routes` | `modules/core/public_routes.py:routes` | None | None | None | None | No | N/A | N/A | public |
| 5 | GET | `/announcements` | `modules/core/public_routes.py:announcements_public_feed` | None | None | None | None | No | N/A | N/A | public |
| 6 | GET | `/sitemap.xml` | `modules/core/public_routes.py:sitemap` | None | None | None | None | No | N/A | N/A | public |
| 7 | GET | `/robots.txt` | `modules/core/public_routes.py:robots` | None | None | None | None | No | N/A | N/A | public |
| 8 | GET | `/google364b8336ce52ae86.html` | `modules/core/public_routes.py:verify_site` | None | None | None | None | No | N/A | N/A | public |
| 9 | GET | `/test-supabase` | `modules/core/public_routes.py:test_supabase` | **None** | None | None | None | No | No | No | **missing-guard** |
| 10 | GET | `/sw.js` | `core/app_setup.py:serve_sw` | None | None | None | None | No | N/A | N/A | public |
| 11 | GET | `/manifest.json` | `core/app_setup.py:serve_manifest` | None | None | CSRF-exempt (`@csrf.exempt`) | None | No | N/A | N/A | public |
| 12 | GET | `/offline` | `core/app_setup.py:serve_offline` | None | None | None | None | No | N/A | N/A | public |
| 13 | GET | `/logout` | `modules/core/public_routes.py:logout_redirect` | None | None | None | None | No | N/A | N/A | public |
| 14 | GET | `/login` | `modules/core/public_routes.py:login_redirect` | None | None | None | None | No | N/A | N/A | public |
| 15 | GET | `/register` | `modules/core/public_routes.py:register_redirect` | None | None | None | None | No | N/A | N/A | public |
| 16 | GET | `/forgot-password` | `modules/core/public_routes.py:forgot_password_redirect` | None | None | None | None | No | N/A | N/A | public |

## Auth Routes (Partially Public)

| # | Method | Path / Topic / RPC | Handler (file:line) | Layer-1 Guard | In-body Authz | Router/Middleware Guard | Hidden Control Channels | Object-ID Param | Ownership Check? | Tenant Filter? | Expected Scope |
|---|--------|--------------------|---------------------|---------------|---------------|-------------------------|-------------------------|------------------|------------------|----------------|-----------------|
| 17 | GET/POST | `/auth/login` | `modules/auth/routes.py → login_view` | None (GET) | Password check (POST) | `@limiter.limit("5/min")` | None | No | N/A | N/A | public |
| 18 | GET/POST | `/auth/logout` | `modules/auth/routes.py → logout_view` | `@login_required` | None | None | None | No | N/A | N/A | self |
| 19 | GET/POST | `/auth/register` | `modules/auth/routes.py → register_view` | None | `@validate_form_data` | None | None | No | N/A | N/A | public |
| 20 | GET/POST | `/auth/register/business` | `modules/auth/routes.py → register_business_view` | None | `@validate_form_data` | None | No | N/A | N/A | public |
| 21 | GET | `/auth/pending-approval` | `modules/auth/routes.py → pending_approval_view` | None | None | None | No | N/A | N/A | public |
| 22 | POST | `/auth/google-login` | `modules/auth/routes.py → google_login_view` | None | Google OAuth token verification | None | None | No | N/A | N/A | public |
| 23 | GET/POST | `/auth/select-role` | `modules/auth/routes.py → select_role_view` | None | Session `oauth_signup` data trust | None | **Session-stored OAuth data** — `session['oauth_signup']` not re-verified | No | N/A | N/A | public |
| 24 | GET/POST | `/auth/forgot-password` | `modules/auth/routes.py → forgot_password_view` | None | Email lookup | `@limiter.limit("5/min")` | None | No | N/A | N/A | public |
| 25 | GET/POST | `/auth/reset-password/<token>` | `modules/auth/routes.py → reset_password_view` | None | Token validation + expiry | None | None | **Yes** (token) | N/A | N/A | public |
| 26 | GET | `/auth/api/users/search` | `modules/auth/routes.py → api_user_search_view` | `@login_required` | None | None | None | No | No (returns other users' PII) | No | self* |

*`/auth/api/users/search` — returns `id`, `username`, `email`, `barangay` for users matching query. Any authenticated user can enumerate other users' PII.

## Public API Routes (No Auth Required)

| # | Method | Path / Topic / RPC | Handler (file:line) | Layer-1 Guard | In-body Authz | Router/Middleware Guard | Hidden Control Channels | Object-ID Param | Ownership Check? | Tenant Filter? | Expected Scope |
|---|--------|--------------------|---------------------|---------------|---------------|-------------------------|-------------------------|------------------|------------------|----------------|-----------------|
| 27 | GET | `/v1/map` | `modules/api_v1/public.py:map_v2_view` | None | None | None | None | No | N/A | N/A | public |
| 28 | GET | `/v1/map-dashboard` | `modules/api_v1/public.py:map_dashboard_view` | None | None | None | None | No | N/A | N/A | public |
| 29 | GET | `/v1/events` | `modules/api_v1/public.py:events_v2_view` | None | None | None | None | No | N/A | N/A | public |
| 30 | GET | `/v1/lgu-events` | `modules/api_v1/public.py:lgu_events_view` | None | None | None | None | No | N/A | N/A | public |
| 31 | GET | `/v1/attractions/<id>` | `modules/api_v1/public.py:attraction_detail_v1_view` | None | None | None | None | **Yes** (id) | No (public detail) | No | public |
| 32 | GET | `/v1/barangay` | `modules/api_v1/public.py:barangays_v1_view` | None | None | None | None | No | N/A | N/A | public |
| 33 | GET | `/attractions/<id>` | `modules/attractions/routes.py:detail` | None | None | None | None | **Yes** (id) | N/A | N/A | public |
| 34 | GET | `/attractions/api` | `modules/attractions/routes.py:api_list` | `@limiter.limit("20/min")` | None | None | None | No | N/A | N/A | public |
| 35 | GET | `/attractions/<id>/reviews` | `modules/attractions/routes.py:get_reviews` | None | None | None | None | **Yes** (id) | N/A | N/A | public |
| 36 | GET | `/business/` | `modules/business/routes.py:index` | None | None | None | None | No | N/A | N/A | public |
| 37 | GET | `/business/<id>` | `modules/business/routes.py:detail` | None | None | None | None | **Yes** (id) | N/A | N/A | public |
| 38 | GET | `/business/api` | `modules/business/routes.py:api_list` | `@limiter.limit("20/min")` | None | None | None | No | N/A | N/A | public |
| 39 | GET | `/gallery/` | `modules/gallery/routes.py:index` | None | None | None | None | No | N/A | N/A | public |
| 40 | GET | `/heritage/` | `modules/heritage/routes.py:index` | None | None | None | None | No | N/A | N/A | public |
| 41 | GET | `/heritage/<type>` | `modules/heritage/routes.py:type_list` | None | None | None | None | No | N/A | N/A | public |
| 42 | GET | `/heritage/<type>/<id>` | `modules/heritage/routes.py:detail` | None | None | None | None | **Yes** (id) | N/A | N/A | public |
| 43 | GET | `/heritage/api/<type>` | `modules/heritage/routes.py:api_list` | None | None | None | None | No | N/A | N/A | public |
| 44 | GET | `/heritage/api/<type>/<id>` | `modules/heritage/routes.py:api_detail` | None | None | None | None | **Yes** (id) | N/A | N/A | public |
| 45 | GET | `/heritage/api/types` | `modules/heritage/routes.py:api_types` | None | None | None | None | No | N/A | N/A | public |
| 46 | GET | `/events/` | `modules/events/routes.py:index` | None | None | None | None | No | N/A | N/A | public |
| 47 | GET | `/barangay/` | `modules/barangay/routes.py:index` | None | None | None | None | No | N/A | N/A | public |
| 48 | GET | `/barangay/<name>` | `modules/barangay/routes.py:profile` | None | None | None | None | No | N/A | N/A | public |
| 49 | GET | `/booking/api/availability/<id>` | `modules/booking/routes.py:get_availability` | None | None | None | None | **Yes** (id) | No (public info) | No | public |

## Unauthenticated API Endpoints (Anomalous)

| # | Method | Path / Topic / RPC | Handler (file:line) | Layer-1 Guard | In-body Authz | Router/Middleware Guard | Hidden Control Channels | Object-ID Param | Ownership Check? | Tenant Filter? | Expected Scope |
|---|--------|--------------------|---------------------|---------------|---------------|-------------------------|-------------------------|------------------|------------------|----------------|-----------------|
| 50 | GET | `/api/attractions` | `modules/core/api_routes.py:api_attractions` | `@limiter.limit("20/min")` | None | None | None | No | N/A | N/A | public |
| 51 | POST | `/api/map-feedback` | `modules/core/api_routes.py:submit_map_feedback` | **None** | None — writes directly to DB | None | None | No | No | No | **missing-guard** |
| 52 | GET | `/api/gemini/config` | `modules/core/api_routes.py:gemini_config` | **None** | None — returns API key | None | None | No | No | No | **missing-guard** |
| 53 | GET | `/api/gemini/context` | `modules/core/api_routes.py:gemini_context` | None | None | None | None | No | N/A | N/A | public |
| 54 | GET | `/api/tiles/<z>/<x>/<y>.pbf` | `modules/core/map_routes.py:get_tile` | `@limiter.limit("2000/min")` | None | None | None | No | N/A | N/A | public |
| 55 | GET | `/api/tiles/combined/<z>/<x>/<y>.pbf` | `modules/core/map_routes.py:get_combined_tile` | `@limiter.limit("2000/min")` | None | None | None | No | N/A | N/A | public |
| 56 | GET | `/api/tiles/layers` | `modules/core/map_routes.py:get_available_layers` | `@limiter.limit("30/min")` | None | None | None | No | N/A | N/A | public |
| 57 | POST | `/api/tiles/cache/invalidate` | `modules/core/map_routes.py:invalidate_cache` | **None** | None — purges Redis cache | None | None | No | No | No | **missing-guard** |
| 58 | POST | `/api/v1/routing/optimize` | `modules/routing/routes.py:optimize_route` | `@limiter.limit("5/min")` | None | None | None | No | N/A | N/A | public |
| 59 | POST | `/api/v1/routing/directions` | `modules/routing/routes.py:get_directions` | `@limiter.limit("10/min")` | None | None | None | No | N/A | N/A | public |
| 60 | GET | `/api/v1/routing/suggested` | `modules/routing/routes.py:get_suggested` | `@limiter.limit("30/min")` | None | None | None | No | N/A | N/A | public |
| 61 | POST | `/notifications/subscribe` | `modules/notifications/routes.py:subscribe` | None | `@validate_form_data` (email) | None | None | No | N/A | N/A | public |

## Authenticated User Routes

| # | Method | Path / Topic / RPC | Handler (file:line) | Layer-1 Guard | In-body Authz | Router/Middleware Guard | Hidden Control Channels | Object-ID Param | Ownership Check? | Tenant Filter? | Expected Scope |
|---|--------|--------------------|---------------------|---------------|---------------|-------------------------|-------------------------|------------------|------------------|----------------|-----------------|
| 62 | GET | `/user/dashboard` | `modules/core/user_routes.py:dashboard` | `@login_required` + `@user_required` | None | None | None | No | N/A | N/A | self |
| 63 | GET/POST | `/user/profile` | `modules/core/user_routes.py:profile` | `@login_required` + `@user_required` | `current_user` scoped | None | None | No | N/A | N/A | self |
| 64 | GET | `/user/favorites` | `modules/core/user_routes.py:favorites` | `@login_required` + `@user_required` | `current_user.id` filter | None | None | No | Yes | No | self |
| 65 | POST | `/user/favorites/toggle` | `modules/core/user_routes.py:toggle_favorite` | `@login_required` + `@user_required` | `current_user.id` filter | None | None | No | Yes | No | self |
| 66 | GET | `/user/favorites/ids` | `modules/core/user_routes.py:get_favorite_ids` | `@login_required` | `current_user.id` filter | None | None | No | Yes | No | self |
| 67 | GET | `/user/visits/ids` | `modules/core/user_routes.py:get_visited_ids` | `@login_required` | `current_user.id` filter | None | None | No | Yes | No | self |
| 68 | GET | `/user/visits` | `modules/core/user_routes.py:visits` | `@login_required` + `@user_required` | `current_user.id` filter | None | None | No | Yes | No | self |
| 69 | POST | `/user/visits/log` | `modules/core/user_routes.py:log_personal_visit` | `@login_required` + `@user_required` | `current_user.id` as owner | None | None | No | Yes | No | self |
| 70 | GET | `/user/my-events` | `modules/core/user_routes.py:my_events` | `@login_required` + `@user_required` | `current_user.id` filter | None | None | No | Yes | No | self |
| 71 | GET | `/user/contributions` | `modules/core/user_routes.py:contributions` | `@login_required` + `@user_required` | `current_user.id` filter | None | None | No | Yes | No | self |
| 72 | POST | `/notifications/mark-read` | `modules/notifications/routes.py:mark_all_read` | `@login_required` | `current_user.id` filter | None | None | No | Yes | No | self |
| 73 | POST | `/notifications/mark-read/<id>` | `modules/notifications/routes.py:mark_single_read` | `@login_required` | `user_id=current_user.id` filter | None | **Yes** — `id` param | Yes | Yes | No | self |

## Authenticated — Any Role (Multi-Role)

| # | Method | Path / Topic / RPC | Handler (file:line) | Layer-1 Guard | In-body Authz | Router/Middleware Guard | Hidden Control Channels | Object-ID Param | Ownership Check? | Tenant Filter? | Expected Scope |
|---|--------|--------------------|---------------------|---------------|---------------|-------------------------|-------------------------|------------------|------------------|----------------|-----------------|
| 74 | POST | `/booking/api/reserve` | `modules/booking/routes.py:reserve_slot` | `@login_required` | `user_id=current_user.id` on reservation | None | None | No | Yes (reservation) | No | self |
| 75 | GET | `/booking/admin/dashboard` | `modules/booking/routes.py:dashboard` | `@login_required` | Role-filtered query (admin=all, contributor=barangay, business_owner=own) | None | None | No | Partial (role-scoped) | Partial | role-scoped |
| 76 | POST | `/booking/api/admin/update_status` | `modules/booking/routes.py:update_status` | `@login_required` | `role in [admin, contributor, business_owner]` — **no ownership check on reservation** | None | None | **Yes** (reservation_id) | **No** — any business_owner can update any reservation | No | **unknown** |
| 77 | POST | `/booking/api/verify-arrival` | `modules/booking/routes.py:verify_arrival` | `@login_required` | `user_id=current_user.id` on reservations | None | None | No | Yes | No | self |
| 78 | POST | `/attractions/<id>/reviews` | `modules/attractions/routes.py:post_review` | `@login_required` | `user_id=current_user.id` on review | None | None | **Yes** (id) | Yes (on review) | No | self |
| 79 | POST | `/business/<id>/review` | `modules/business/routes.py:submit_review` | `@login_required` | `user_id=current_user.id` on review | None | None | **Yes** (id) | Yes (on review) | No | self |
| 80 | POST | `/chat/` | `modules/chat/routes.py:chat_index` | `@login_required` | `current_user.id` filter on participants | None | None | No | Yes | No | self |
| 81 | GET | `/chat/<id>` | `modules/chat/routes.py:chat_room` | `@login_required` | Participant check or barangay public | None | None | **Yes** (id) | Partial (participant check) | No | self |

## Authenticated — Admin Routes

| # | Method | Path / Topic / RPC | Handler (file:line) | Layer-1 Guard | In-body Authz | Router/Middleware Guard | Hidden Control Channels | Object-ID Param | Ownership Check? | Tenant Filter? | Expected Scope |
|---|--------|--------------------|---------------------|---------------|---------------|-------------------------|-------------------------|------------------|------------------|----------------|-----------------|
| 82 | GET | `/admin/dashboard` | `modules/admin_core/dashboard.py:admin_dashboard` | `@login_required` | `role == "admin"` (in-handler) | None | None | No | N/A | N/A | admin |
| 83 | GET | `/admin/users/approve/<id>` | `modules/admin_core/users.py:approve_user` | `@login_required` | `role == "admin"` (in-handler) | None | None | **Yes** (id) | N/A | N/A | admin |
| 84 | GET | `/admin/users/reject/<id>` | `modules/admin_core/users.py:reject_user` | `@login_required` | `role == "admin"` (in-handler) | None | None | **Yes** (id) | N/A | N/A | admin |
| 85 | GET | `/admin/gallery/approve/<id>` | `modules/admin_core/content.py:approve_gallery` | `@login_required` | `_require_admin()` | None | None | **Yes** (id) | N/A | N/A | admin |
| 86 | GET | `/admin/gallery/reject/<id>` | `modules/admin_core/content.py:reject_gallery` | `@login_required` | `_require_admin()` | None | None | **Yes** (id) | N/A | N/A | admin |
| 87 | GET | `/admin/reviews` | `modules/admin_core/content.py:reviews_list` | `@login_required` | `_require_admin()` | None | None | No | N/A | N/A | admin |
| 88 | GET/POST | `/admin/reviews/approve/<id>` | `modules/admin_core/content.py:approve_review` | `@login_required` | `_require_admin()` | None | **Open redirect via `request.args.get("next")`** | **Yes** (id) | N/A | N/A | admin |
| 89 | GET/POST | `/admin/reviews/reject/<id>` | `modules/admin_core/content.py:reject_review` | `@login_required` | `_require_admin()` | None | **Open redirect via `request.args.get("next")`** | **Yes** (id) | N/A | N/A | admin |
| 90 | GET | `/admin/announcements/approve/<id>` | `modules/admin_core/content.py:admin_approve_announcement` | `@login_required` | `_require_admin()` | None | None | **Yes** (id) | N/A | N/A | admin |
| 91 | GET | `/admin/announcements/reject/<id>` | `modules/admin_core/content.py:admin_reject_announcement` | `@login_required` | `_require_admin()` | None | None | **Yes** (id) | N/A | N/A | admin |
| 92 | GET | `/admin/attractions` | `modules/attractions/admin_routes.py:admin_attractions` | `@login_required` | `role == "admin"` (in-handler) | None | None | No | N/A | N/A | admin |
| 93 | GET/POST | `/admin/attractions/add` | `modules/attractions/admin_routes.py:add_attraction` | `@login_required` | `role in [admin, contributor]` (in-handler) | None | None | No | N/A | N/A | admin/contributor |
| 94 | GET/POST | `/admin/attractions/edit/<id>` | `modules/attractions/admin_routes.py:edit_attraction` | `@login_required` | admin OR contributor with matching barangay OR owner | None | None | **Yes** (id) | Partial (owner/barangay check) | Partial (contributor → barangay) | admin/contributor/owner |
| 95 | GET | `/admin/attractions/delete/<id>` | `modules/attractions/admin_routes.py:delete_attraction` | `@login_required` | admin OR `attraction.user_id == current_user.id` | None | None | **Yes** (id) | Yes | No | admin/owner |
| 96 | GET | `/admin/attractions/approve/<id>` | `modules/attractions/admin_routes.py:approve_attraction` | `@login_required` | `role == "admin"` (in-handler) | None | None | **Yes** (id) | N/A | N/A | admin |
| 97–117 | Various | `/admin/heritage/*` | `modules/heritage/admin_routes.py` | `@login_required` | `_require_admin()` (in-handler) | None | None | Various | N/A | N/A | admin |
| 118–130 | Various | `/admin/v1/documents/*` | `modules/api_v1/documents.py` | `@login_required` | admin check in-handler | None | None | Various | N/A | N/A | admin |
| 131–137 | Various | `/admin/newsletter/*` | `modules/notifications/admin_routes.py` | `@login_required` + `@admin_required` | admin role check (decorator) | None | None | Various | N/A | N/A | admin |
| 138a | GET | `/admin/establishments` | `modules/business/admin_routes.py:manage_establishments` | `@login_required` + `@admin_required` | None | None | None | No | N/A | N/A | admin |
| 138b | POST | `/admin/establishments/<id>/approve` | `modules/business/admin_routes.py:approve_establishment` | `@login_required` + `@admin_required` | None | None | None | **Yes** (id) | N/A | N/A | admin |
| 138c | POST | `/admin/establishments/<id>/reject` | `modules/business/admin_routes.py:reject_establishment` | `@login_required` + `@admin_required` | None | None | None | **Yes** (id) | N/A | N/A | admin |
| 138d | POST | `/admin/establishments/<id>/delete` | `modules/business/admin_routes.py:delete_establishment` | `@login_required` + `@admin_required` | None | None | None | **Yes** (id) | N/A | N/A | admin |
| 138e | GET | `/admin/establishment-reviews` | `modules/business/admin_routes.py:manage_establishment_reviews` | `@login_required` + `@admin_required` | None | None | None | No | N/A | N/A | admin |
| 138f | POST | `/admin/establishment-reviews/<id>/approve` | `modules/business/admin_routes.py:approve_establishment_review` | `@login_required` + `@admin_required` | None | None | None | **Yes** (id) | N/A | N/A | admin |
| 138g | POST | `/admin/establishment-reviews/<id>/reject` | `modules/business/admin_routes.py:reject_establishment_review` | `@login_required` + `@admin_required` | None | None | None | **Yes** (id) | N/A | N/A | admin |
| 138h | GET | `/admin/merchants/verify` | `modules/business/admin_routes.py:manage_merchant_verifications` | `@login_required` + `@admin_required` | None | None | None | No | N/A | N/A | admin |
| 138i | POST | `/admin/merchants/verify/<id>/approve` | `modules/business/admin_routes.py:approve_merchant_verification` | `@login_required` + `@admin_required` | None | None | None | **Yes** (id) | N/A | N/A | admin |
| 138j | POST | `/admin/merchants/verify/<id>/reject` | `modules/business/admin_routes.py:reject_merchant_verification` | `@login_required` + `@admin_required` | None | None | None | **Yes** (id) | N/A | N/A | admin |
| 139a | GET | `/admin/events` | `modules/events/admin_routes.py:admin_events` | `@login_required` | `current_user.role == "admin"` (in-handler) | None | None | No | N/A | N/A | admin |
| 139b | GET | `/admin/events/approve/<id>` | `modules/events/admin_routes.py:approve_event` | `@login_required` | `current_user.role == "admin"` (in-handler) | `@limiter.limit("10 per minute")` | None | **Yes** (id) | N/A | N/A | admin |
| 139c | GET | `/admin/events/reject/<id>` | `modules/events/admin_routes.py:reject_event` | `@login_required` | `current_user.role == "admin"` (in-handler) | `@limiter.limit("10 per minute")` | None | **Yes** (id) | N/A | N/A | admin |
| 139d | GET/POST | `/admin/events/add` | `modules/events/admin_routes.py:add_event` | `@login_required` | `current_user.role == "admin"` (in-handler) | `@limiter.limit("10 per minute")` | None | No | N/A | N/A | admin |
| 139e | GET/POST | `/admin/events/edit/<id>` | `modules/events/admin_routes.py:edit_event` | `@login_required` | `current_user.role == "admin"` (in-handler) | `@limiter.limit("10 per minute")` | None | **Yes** (id) | N/A | N/A | admin |
| 139f | GET | `/admin/events/delete/<id>` | `modules/events/admin_routes.py:delete_event` | `@login_required` | `current_user.role == "admin"` (in-handler) | `@limiter.limit("10 per minute")` | None | **Yes** (id) | N/A | N/A | admin |
| 140a | GET | `/admin/visits` | `modules/admin_core/visits.py:visits_index` | `@login_required` | `current_user.role in [admin, contributor, business_owner]` (in-handler) | None | None | No | N/A | N/A | admin/contributor/business_owner |
| 140b | GET | `/admin/visits/export` | `modules/admin_core/visits.py:export_visits` | `@login_required` | `current_user.role in [admin, contributor, business_owner]` (in-handler) | None | None | No | N/A | N/A | admin/contributor/business_owner |
| 140c | GET | `/admin/visits/export/page-views` | `modules/admin_core/visits.py:export_page_views` | `@login_required` | `current_user.role == "admin"` (in-handler) | None | None | No | N/A | N/A | admin |
| 140d | GET | `/admin/visits/export/destination-insights` | `modules/admin_core/visits.py:export_destination_insights` | `@login_required` | `current_user.role == "admin"` (in-handler) | None | None | No | N/A | N/A | admin |
| 140e | GET | `/admin/visits/registry` | `modules/admin_core/visits.py:visitor_registry` | `@login_required` | `current_user.role in [admin, contributor, business_owner]` (in-handler) | None | None | No | N/A | N/A | admin/contributor/business_owner |
| 140f | POST | `/admin/visits/log` | `modules/admin_core/visits.py:log_visit` | `@login_required` | **None — missing role check** | None | None | No | No | No | **unknown** |

## Authenticated — Business Owner Routes

| # | Method | Path / Topic / RPC | Handler (file:line) | Layer-1 Guard | In-body Authz | Router/Middleware Guard | Hidden Control Channels | Object-ID Param | Ownership Check? | Tenant Filter? | Expected Scope |
|---|--------|--------------------|---------------------|---------------|---------------|-------------------------|-------------------------|------------------|------------------|----------------|-----------------|
| 138 | GET | `/business/dashboard` | `modules/business/routes.py:dashboard` | `@login_required` + `@business_owner_required` | None | None | None | No | N/A | N/A | business_owner |
| 139 | POST | `/business/verify` | `modules/business/routes.py:submit_verification` | `@login_required` + `@business_owner_required` | `user_id=current_user.id` | None | None | No | Yes | N/A | self |
| 140 | GET/POST | `/business/establishment/create` | `modules/business/routes.py:create_establishment` | `@login_required` + `@approved_business_owner_required` | `owner_id=current_user.id` | None | None | No | Yes | No | self |
| 141 | GET/POST | `/business/establishment/edit` | `modules/business/routes.py:edit_establishment` | `@login_required` + `@approved_business_owner_required` | `_get_owner_establishment()` | None | None | No | Yes (owner) | No | self |
| 142–146 | Various | `/business/rooms/*` | `modules/business/routes.py` | `@login_required` + `@approved_business_owner_required` | `_get_owner_establishment()` + ownership check on room | None | Various | Yes (room_id) | Yes (via establishment ownership) | No | self |
| 147–151 | Various | `/business/menu/*` | `modules/business/routes.py` | `@login_required` + `@approved_business_owner_required` | `_get_owner_establishment()` + ownership check on item | None | Various | Yes (item_id) | Yes (via establishment ownership) | No | self |
| 152 | GET | `/business/reviews` | `modules/business/routes.py:view_reviews` | `@login_required` + `@approved_business_owner_required` | `_get_owner_establishment()` | None | None | No | Yes (via establishment) | No | self |
| 153 | POST | `/business/reviews/reply/<id>` | `modules/business/routes.py:reply_to_review` | `@login_required` + `@approved_business_owner_required` | `review.establishment_id == establishment.id` | None | None | **Yes** (id) | Yes | No | self |
| 154 | GET | `/business/browse` | `modules/business/routes.py:browse_peers` | `@login_required` + `@approved_business_owner_required` | None | None | None | No | N/A | N/A | self |

## Authenticated — Contributor (Barangay) Routes

| # | Method | Path / Topic / RPC | Handler (file:line) | Layer-1 Guard | In-body Authz | Router/Middleware Guard | Hidden Control Channels | Object-ID Param | Ownership Check? | Tenant Filter? | Expected Scope |
|---|--------|--------------------|---------------------|---------------|---------------|-------------------------|-------------------------|------------------|------------------|----------------|-----------------|
| 155 | GET | `/barangay/dashboard` | `modules/barangay/routes.py:barangay_dashboard` | `@login_required` | `role == "contributor"` + `barangay_id` filter | None | None | No | N/A | Yes (barangay) | team |
| 156–175 | Various | `/barangay/attractions/*`, `/barangay/events/*`, `/barangay/gallery/*`, `/barangay/announcements/*`, `/barangay/profile`, `/barangay/reviews/*` | `modules/barangay/routes.py` | `@login_required` | `role == "contributor"` + `barangay_id` scoping on all CRUD | None | Various | Yes (id) | Yes (barangay match on all) | Yes | team |

## Update Endpoint

| # | Method | Path / Topic / RPC | Handler (file:line) | Layer-1 Guard | In-body Authz | Router/Middleware Guard | Hidden Control Channels | Object-ID Param | Ownership Check? | Tenant Filter? | Expected Scope |
|---|--------|--------------------|---------------------|---------------|---------------|-------------------------|-------------------------|------------------|------------------|----------------|-----------------|
| 176 | GET/POST | `/pull` | `modules/core/update_routes.py:pull_updates` | `@require_update_token` (admin + env token) | `current_user.role == "admin"` + `UPDATE_TOKEN` comparison | `@limiter.limit("1/min")` | **Token in JSON body** (not header) — if `UPDATE_TOKEN` env var is unset, token check is bypassed | No | N/A | N/A | admin |

## WebSocket Handlers

| # | Method | Path / Topic / RPC | Handler (file:line) | Layer-1 Guard | In-body Authz | Router/Middleware Guard | Hidden Control Channels | Object-ID Param | Ownership Check? | Tenant Filter? | Expected Scope |
|---|--------|--------------------|---------------------|---------------|---------------|-------------------------|-------------------------|------------------|------------------|----------------|-----------------|
| 177 | WS | `connect` | `modules/chat/sockets.py:handle_connect` | **None** | None | `cors_allowed_origins="*"` | **Wildcard CORS** — any origin can connect | No | N/A | N/A | public |
| 178 | WS | `disconnect` | `modules/chat/sockets.py:handle_disconnect` | None | None | None | None | No | N/A | N/A | N/A |
| 179 | WS | `join` | `modules/chat/sockets.py:on_join` | Auth check in-handler | Participant check, barangay public bypass | None | None | Yes (room_id) | Partial | No | self |
| 180 | WS | `send_message` | `modules/chat/sockets.py:handle_send_message` | Auth check in-handler | Participant check, barangay auto-join | None | None | Yes (room_id) | Partial | No | self |
| 181 | WS | `typing` | `modules/chat/sockets.py:handle_typing` | Auth check in-handler | None (broadcasts to room) | None | None | Yes (room_id) | No (broadcasts username) | No | team |
| 182 | WS | `leave` | `modules/chat/sockets.py:on_leave` | None | None | None | None | Yes (room_id) | No | N/A | public |

## Gamification Routes

| # | Method | Path / Topic / RPC | Handler (file:line) | Layer-1 Guard | In-body Authz | Router/Middleware Guard | Hidden Control Channels | Object-ID Param | Ownership Check? | Tenant Filter? | Expected Scope |
|---|--------|--------------------|---------------------|---------------|---------------|-------------------------|-------------------------|------------------|------------------|----------------|-----------------|
| 183 | GET | `/gamification/scan/<type>/<id>` | `modules/gamification/routes.py:scan_qr` | `@login_required` | `session['active_nav']` match required | None | **Session self-set** — `start_navigation` lets user set any target | Yes (type, id) | N/A | N/A | self |
| 184 | POST | `/gamification/api/start-navigation` | `modules/gamification/routes.py:start_navigation` | `@login_required` | None — writes arbitrary target to session | None | **Session self-service** — user sets `active_nav` to any id/type | No | No | No | self* |
| 185 | POST | `/gamification/api/stop-navigation` | `modules/gamification/routes.py:stop_navigation` | `@login_required` | None | None | None | No | N/A | N/A | self |
| 186 | POST | `/gamification/api/checkin` | `modules/gamification/routes.py:verify_checkin` | `@login_required` + `@limiter.limit("10/min")` | `user_id=current_user.id` on checkin | None | None | No (target coords from body) | Yes | No | self |
| 187 | GET | `/gamification/my-passport` | `modules/gamification/routes.py:view_passport` | `@login_required` | `current_user.passports`, `current_user.check_ins` | None | None | No | Yes | No | self |

## Anomaly Summary

| # | Endpoint | Anomaly | Severity |
|---|----------|---------|----------|
| 52 | `GET /api/gemini/config` | **No guard** — returns GEMINI_API_KEY to anonymous visitors | CRITICAL |
| 9 | `GET /test-supabase` | **No guard** — debug endpoint returns DB query results | HIGH |
| 76 | `POST /booking/api/admin/update_status` | **Missing ownership check** — any business_owner can modify any reservation | HIGH |
| 140f | `POST /admin/visits/log` | **Inconsistent guard** — missing role check (all siblings require admin/contributor/business_owner) | HIGH |
| 57 | `POST /api/tiles/cache/invalidate` | **No guard** — anonymous Redis cache invalidation | MEDIUM |
| 51 | `POST /api/map-feedback` | **No guard** — anonymous DB write | MEDIUM |
| 177 | WS `connect` | **Wildcard CORS** — anonymous cross-origin WebSocket | MEDIUM |
| 184 | `POST /gamification/api/start-navigation` | **Session self-service** — bypasses navigation guard | MEDIUM |
| 176 | `GET/POST /pull` | **Token bypass** — if UPDATE_TOKEN env unset, admin-only check still holds but token validation is skipped | MEDIUM |
| 183 | `GET /gamification/scan/<type>/<id>` | **Session-trust guard** — `active_nav` set by user controls access | MEDIUM |
