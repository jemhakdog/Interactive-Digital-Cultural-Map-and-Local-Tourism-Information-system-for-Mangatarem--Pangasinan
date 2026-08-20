# Migration Spec — `business_owner` Role (Flask `main` → Next.js)

> Read-only investigation of the Flask `main` branch business-owner features, mapped to
> the **existing** FastAPI backend (`backend/app/api/*.py`) and the **existing** React/Next.js
> frontend (`frontend/src/app`).
>
> Legend:
> - **EXISTING** = a matching FastAPI route already exists (path shown).
> - **MISSING**   = no FastAPI route today; must be built.
> - **PARTIAL**   = exists but does not cover the Flask behavior exactly (note explains gap).

## FastAPI router prefixes (verified in `backend/app/main.py`)

| Router | Prefix |
|--------|--------|
| `business_router` | `/api/business` |
| `auth_router` | `/api/auth` |
| `uploads_router` | `/api/uploads` |
| `public_router` | `/api` |

All `business` write endpoints require `get_current_active_user` and check `user.role == "business_owner"`
(or `admin`) where appropriate.

---

## Feature table

| Feature | Main template | Nav location (link appears) | Purpose | Form fields / data shown | Backend endpoint (EXISTING / MISSING) | Already ported to React? |
|---|---|---|---|---|---|---|
| **Owner Dashboard** | `templates/business/dashboard.html` (extends `admin/admin_base.html`) | Sidebar "Dashboard" → `business.dashboard` (also a card link inside the page) | Hub for the owner's single establishment: status banner, stat cards (rating, room/menu count, review count, approval state), profile summary, action cards (Manage Rooms / Manage Menu / Customer Feedbacks / Log Visitor). Onboarding empty-state when no establishment exists. | Data shown: `establishment` (name, type, status, cover, address, contact_number, email, price_range, lat/long, description), `stats` = `{room_count, menu_count, total_reviews}`, `barangays`, `mapbox_token`. Action links conditionally rendered by `establishment.type`. | **PARTIAL** — Data must be assembled client-side: `GET /api/business/rooms/list` (room_count), `GET /api/business/menu/list` (menu_count), `GET /api/business/{id}` (rating_avg, review_count, status). NO dedicated `/api/business/dashboard` owner-stats endpoint exists. | ❌ No `/business/owner` or dashboard page. Only `/business` (list) and `/business/[id]` (public detail) exist. |
| **Create / Edit Establishment** | `templates/business/edit_establishment.html` (extends `admin/admin_base.html`) | Sidebar "Edit Establishment" → `business.edit_establishment` / `business.create_establishment` | Create a new listing (onboarding) or modify the owner's existing listing. Mapbox picker sets lat/long. | Fields: `name*` (text), `type*` (select: inn/restaurant/cafe/fastfood), `description*` (textarea), `address*` (text), `barangay*` (select from `barangays`), `latitude*` (number, step any, default 15.7900), `longitude*` (number, step any, default 120.2900), `contact_number` (text), `email` (email), `website` (url), `price_range` (select: budget/moderate/premium), `amenities` (checkboxes: wifi, parking, aircon, pool, tv, kitchen, pet_friendly, wheelchair), `cover_image_file` (file image/*), `logo_file` (file image/*), `operating_hours` (7 day rows, `hours_{mon..sun}_open`/`_close` time inputs). CSRF token. Validation: name/type/description/address/barangay/lat/long required; mapbox token from `mapbox_token` context var. | **PARTIAL** — `POST /api/business/` (create, `EstablishmentCreate`) and `PUT /api/business/{id}` (update, `EstablishmentUpdate`) exist as **JSON only**. Gaps: (1) No multipart file upload — `cover_image_file`/`logo_file` must be uploaded via `POST /api/uploads/image` first, then pass `cover_image_url`/`logo_url`. (2) `operating_hours` is a `dict[str,str]`; must be serialized per-day on client. (3) FastAPI create rejects a 2nd establishment (400 "already have an establishment"). (4) Mapbox token must be supplied from config/settings, not a Flask context var. | ❌ Not ported. |
| **Manage Menu (dining only)** | `templates/business/manage_menu.html` (extends `admin/admin_base.html`) | Shown for non-`inn` establishments; sidebar "Manage Menu" → `business.manage_menu` (also dashboard action card) | CRUD menu dishes grouped by category; inline edit modal per item. | Add form: `name*` (text), `price*` (number, step 0.01), `category*` (select: main/appetizer/dessert/drinks/snacks), `description` (textarea), `image_file` (file image/*), `is_available` (checkbox, default checked), `is_bestseller` (checkbox). Edit modal posts same fields + `item_id`. Data shown: `items`, `grouped_items` (by category), `establishment`. | **PARTIAL** — `GET /api/business/menu/list` (list), `POST /api/business/menu` (`MenuItemCreate`), `PUT /api/business/menu/{item_id}` (`MenuItemUpdate`), `DELETE /api/business/menu/{item_id}`. Gaps: (1) No multipart — `image_file` must go through `POST /api/uploads/image` then `image_url`. (2) No "grouped by category" endpoint (client groups the flat list). | ❌ Not ported. |
| **Manage Rooms (inn only)** | `templates/business/manage_rooms.html` (extends `admin/admin_base.html`) | Shown for `inn` establishments; sidebar "Manage Rooms" → `business.manage_rooms` | CRUD room inventory units for an inn. | Add form: `name*` (text), `price_per_night*` (number, step 0.01), `capacity*` (number, min 1, default 2), `description` (textarea), `image_urls` (text, comma-separated), `room_amenities` (checkboxes: wifi, aircon, tv, hot_water, mini_bar, balcony, bathroom), `is_available` (checkbox, default checked). Delete form per room (`room_id`). Data shown: `rooms`, `establishment`. | **EXISTING** — `GET /api/business/rooms/list` (list), `POST /api/business/rooms` (`RoomCreate`), `PUT /api/business/rooms/{room_id}` (`RoomUpdate`), `DELETE /api/business/rooms/{room_id}`. Note: `image_urls` is a JSON list in the schema (Flask sends comma-separated string → must be split client-side). No file upload endpoint needed (URLs only). | ❌ Not ported. |
| **Reviews (owner view + reply)** | `templates/business/reviews.html` (extends `admin/admin_base.html`) | Sidebar "Reviews" → `business.view_reviews` (also dashboard "Customer Feedbacks" card → `business.view_reviews`) | View all reviews for the owner's establishment (approved/pending/rejected) with star rating, status badge, and a collapseable reply form per review. | Data shown: `reviews` (each with `user.username`, `created_at`, `status`, `rating`, `comment`, `replies` list), `establishment`. Reply form: `comment*` (textarea) → `business.reply_to_review`. | **PARTIAL** — Reply exists: `POST /api/business/reviews/{review_id}/reply` (`ReviewReply`, `comment`). Review **viewing** is **MISSING** as a dedicated owner endpoint: `GET /api/business/{id}` returns only `status == "approved"` reviews and only top-level+replies, not pending/rejected, and is a public detail endpoint (no owner-scoped list). A `/api/business/reviews/mine` (or owner-filtered) endpoint is needed to reproduce `view_reviews`. | ❌ Not ported (only public `/business/[id]` detail exists). |
| **Business Verification** | `templates/business/verify.html` (extends `base.html`, includes `business_nav.html`) | Reached from role-gated entry (verify nav in `base.html`); not in the dark admin sidebar | Submit / update business permit & supporting documents for admin approval. Shows pending/rejected banners. | Form (`enctype=multipart/form-data`): `permit_document_file` (file .pdf/image/*), `permit_document_url` (url, OR), `other_document_file` (file, optional), `other_document_url` (url, optional). Pre-filled from `verification.permit_document_url` / `other_document_url`. Posts to `business.submit_verification`. | **MISSING** — No FastAPI business-verification endpoint exists (grep for `verify|verification` in `api/*.py` finds only booking GPS-verify, gamification check-in verify, and auth token verify). A `POST /api/business/verification` (multipart file + url fields) and a `GET` to fetch current status must be created. | ❌ Not ported. |
| **Browse Peer Businesses** | `templates/business/browse_peers.html` (extends `admin/admin_base.html`) | Sidebar "Browse Peers" → `business.browse_peers` (also `business_nav.html`) | Owner-read-only market overview: grid of other approved establishments in Mangatarem, filtered by `type_label`, with cooperative-tourism banner. Each card links to public portal. | Data shown: `peers` (cover_image_url, is_featured, name, address, rating_avg, review_count, price_range, barangay.name), `type_label`, `establishment`. Card link → `business.detail` (public). | **EXISTING** (functional equivalent) — `GET /api/business/?type=<type>&per_page=...` returns approved establishments (`list_establishments`). The Flask `browse_peers` is essentially a type-filtered public list; the shared `/business/` list endpoint covers it. Note: `type_label`/cooperative banner are UI-only. | ⚠️ Partial — public `/business` list + `/business/[id]` detail exist; the owner "Browse Peers" console view (filtered, with banner) is not a dedicated ported page. |
| **Register Business** | `templates/auth/register_business.html` (extends `base.html`) | Public auth page (link from login) | Public sign-up that creates a `business_owner` account + prefilled establishment draft, then routes to admin review. | Fields: `business_name` (text, required), `business_type` (select: inn/restaurant/cafe/fastfood, required), `username` (text, required), `email` (email, required), `password` (password, required, minlength 6). Posts to `auth.register_business`. | **MISSING** (dedicated) — FastAPI has `POST /api/auth/register` (`RegisterRequest`: email, password min 6, name, role default `user`, barangay). Gaps vs Flask: no `business_name`/`business_type` capture (Flask likely auto-creates an establishment draft); role must be set to `business_owner`. A dedicated `/api/auth/register-business` (or extended register accepting business_name + business_type and creating a pending establishment) is needed to reproduce `register_business`. | ⚠️ Only generic `/auth/register` page exists; business-specific register form not ported. |

---

## Navigation structure (role `business_owner`)

There are **two nav contexts** depending on the base template.

### A. Dark admin console shell — `templates/admin/admin_base.html` (sidebar)
Used by: `dashboard`, `edit_establishment`, `manage_menu`, `manage_rooms`, `reviews`, `browse_peers`.
The sidebar has a "Business" section (verified from `admin_base.html`):

| Sidebar link | Flask endpoint | Active-when |
|---|---|---|
| Dashboard | `business.dashboard` | `request.endpoint == 'business.dashboard'` |
| Edit Establishment | `business.edit_establishment` / `business.create_establishment` | endpoint in that set |
| Manage Rooms | `business.manage_rooms` / `business.add_room` / `business.edit_room` | endpoint in that set |
| Manage Menu | `business.manage_menu` / `business.add_menu_item` / `business.edit_menu_item` | endpoint in that set |
| Log Visitor (Visitor Registry) | `admin.visitor_registry` (only when `establishment.status == 'approved'`) | endpoint == `admin.visitor_registry` |
| Reviews | `business.view_reviews` | endpoint == `business.view_reviews` |
| Browse Peers | `business.browse_peers` | endpoint == `business.browse_peers` |

> "Log Visitor" (`admin.visitor_registry`) is rendered on the dashboard action card only when the
> establishment is `approved`; it is an admin-scoped registry, out of scope for this business spec
> but appears in the owner console.

### B. Light public top nav — `templates/includes/business_nav.html` (included in `base.html`)
Used by: `verify`, `register_business` (any page extending `base.html` while logged in as owner).

| Nav link | Flask endpoint |
|---|---|
| Dashboard | `business.dashboard` |
| Browse Peers | `business.browse_peers` |
| Public Directory | `business.index` |
| Map | `public.map_view` |
| (username display) | `current_user.username` |
| Logout | `auth.logout` |

### Shared partials
- `templates/includes/business_nav.html` — horizontal business top-nav, included in `base.html` (lines 120 & 161). Renders Dashboard / Browse Peers / Public Directory / Map / username / Logout.
- `templates/admin/admin_base.html` — dark dashboard shell providing the sidebar above + top bar; the canonical layout for all owner management pages.
- `templates/base.html` — public layout; includes `business_nav.html` for logged-in owners.
- Mapbox GL JS (v3.3.0) loaded in `edit_establishment.html` head for the location picker; requires a Mapbox token (Flask `mapbox_token` context var → must come from FastAPI settings in Next.js).
- CSRF token (`csrf_token()`) used on every Flask POST form — **irrelevant** in FastAPI (token auth / JSON), but note that all write flows become authenticated JSON/multipart calls.

---

## Endpoint coverage summary

| Flask behavior | FastAPI status | Notes |
|---|---|---|
| List establishments / browse peers | EXISTING `GET /api/business/` | type/barangay/q/geo filters supported |
| Establishment detail (public) | EXISTING `GET /api/business/{id}` | approved-only + rooms/menu/reviews |
| Create establishment | EXISTING `POST /api/business/` | JSON; 1-per-owner limit |
| Edit establishment | EXISTING `PUT /api/business/{id}` | JSON; no file upload |
| Rooms list/add/edit/delete | EXISTING `GET/POST/PUT/DELETE /api/business/rooms[/...]` | full CRUD |
| Menu list/add/edit/delete | EXISTING `GET/POST/PUT/DELETE /api/business/menu[/...]` | full CRUD (JSON) |
| Reply to review | EXISTING `POST /api/business/reviews/{review_id}/reply` | owner reply |
| Owner dashboard stats | MISSING (assemble from list endpoints) | no `/dashboard` |
| Owner reviews view (all statuses) | MISSING | only approved via detail |
| Submit business verification | MISSING | no verification route |
| Register business (with draft establishment) | MISSING dedicated | only generic `/api/auth/register` |
| Image/file uploads (cover, logo, dish, permit) | PARTIAL `POST /api/uploads/image`, `/api/uploads/multiple` | must upload-then-pass-URL; establishment/menu update accept `image_url` only |

### Implementation notes for agents
1. **File uploads**: No FastAPI write endpoint accepts `multipart/form-data` for establishment/menu. Pattern: `POST /api/uploads/image` → returns URL → include in `EstablishmentCreate/Update` or `MenuItemCreate/Update` `image_url`/`cover_image_url`/`logo_url`.
2. **One establishment per owner**: `POST /api/business/` returns 400 if owner already has one. The onboarding empty-state (dashboard) must branch: no establishment → show create flow; existing → show edit/management.
3. **Operating hours**: `operating_hours` is `dict[str,str]` (`{"mon":"09:00-17:00", ...}`). Client must pack the 7 day/time inputs.
4. **Mapbox token**: Provide via FastAPI settings/env; expose to the Next.js client (e.g., `/api/config` or public env var) — do not rely on a Flask context var.
5. **Verification & business register**: require new FastAPI routes before the Next.js pages can be wired.
