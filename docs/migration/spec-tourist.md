# Migration Spec — Tourist (User) Role

**Source:** Flask `main` branch templates (`templates/user/*`, `templates/gamification/*`, `templates/chat/*`, `templates/pagez/detail.html`, `templates/includes/user_nav.html`)
**Target:** Next.js React frontend + existing FastAPI backend (`backend/app/api/*.py`)
**Role:** `user` = tourist / visitor ("Visitor Account").
**Status:** PARTIALLY ported. `/dashboard`, `/profile`, `/passport`, `/chat` routes exist in React (room list only). Review form/list exist under `/attractions/[id]`. QR scanner page and chat room view are NOT ported. The Flask `user` blueprint (dashboard/profile/favorites/visits + favorite-toggle + visit-log) has **no FastAPI equivalent** — those endpoints are **MISSING**.

---

## 1. Navigation structure

The tourist nav is rendered by `templates/includes/user_nav.html`, included in `templates/base.html` navbar when `current_user.role == "user"`. There is **no** `templates/includes/tourist_nav.html` (does not exist on `main`) — `user_nav.html` IS the tourist partial.

### Top nav (`user_nav.html`) — desktop + mobile sheet

| Label | Flask endpoint | FastAPI equivalent | Notes |
|-------|----------------|--------------------|-------|
| Dashboard | `user.dashboard` | **MISSING** (passport badges come from `GET /api/gamification/passport`; stats have no endpoint) | `/dashboard` (React exists, minimal) |
| Bookmarks | `user.favorites` | **MISSING** | `/user/favorites` (no React route) |
| My Visits | `user.visits` | **MISSING** | `/user/visits` (no React route) |
| Passport | `gamification.view_passport` | `GET /api/gamification/passport` (**EXISTING**) | `/passport` (React exists) |
| Explore ▾ (dropdown) | `public.map_view`, `barangay.index`, `events.index`, `gallery.index`, `business.index`, `public.routes` | All public/barangay endpoints EXISTING | Map, Barangays, Events, Gallery, Stay & Eat, Routes |
| Logout | `auth.logout` | `POST /api/auth/logout` (**EXISTING**, stateless) | right-aligned, border-separated |

### Entry points NOT in the top nav

- **Community Chat Hubs** (`chat.chat_index` → `GET /api/chat`): reachable by direct URL `/chat`. There is **no** link to it in `user_nav.html`, `base.html`, or any other template (grep of `templates/` found only self-references inside `chat/`). Treat as an orphan route surfaced by the React `/chat` page directly.
- **QR Check-in Scanner** (`gamification.scan_qr` → renders `gamification/qr_scanner.html`): linked from the attraction detail page (`pagez/detail_v1.html`) and establishment detail page (`pagez/establishment_detail.html`) "scan" stamp button: `url_for('gamification.scan_qr', type_=..., id_=...)`. The actual GPS verification calls `gamification.verify_checkin` = `POST /api/gamification/checkin` (**EXISTING**).
- **Write a Review**: lives inside the attraction detail page (`pagez/detail.html`), visible only when `current_user.is_authenticated`; posts to `attractions.post_review` = `POST /api/attractions/{id}/reviews` (**EXISTING**).
- **Favorite / Visited** buttons: on attraction & establishment detail sidebars (`user_actions_modal.html` + `js/pages/user-actions.js`); backed by the **MISSING** `user` blueprint (no favorite-toggle or visit-log FastAPI endpoint).

### React navbar today (`components/layout/navbar.tsx`)
Per `CONVENTIONS.md §8`, the React navbar shows the same links to all users and only gated-links for `admin`. Tourist-specific links (Passport, Bookmarks, My Visits, Chat) are **not** in the React navbar yet — they must be added in the user-menu area gated by `user.role === "user"` (Dashboard already appears when `user` exists).

---

## 2. Feature table

Legend: **EXISTING** = working FastAPI path; **PARTIAL** = path exists but not usable as-is; **MISSING** = no usable endpoint. React: **Yes** = route/component exists; **No** = not ported.

| Feature | Main template | Nav location | Purpose | Form fields / data shown | Backend endpoint (FastAPI) | React ported? |
|---|---|---|---|---|---|---|
| Digital Passport dashboard | `gamification/passport_dashboard.html` | Top nav "Passport" | Show achievement badges + recent stamp log | `badges_data`: `badge.title`, `badge.description`, `badge.badge_image_url`, `is_unlocked`, `completed_reqs`, `total_reqs`, `progress_pct`; `recent_checkins`: attraction/establishment name, `verified_at` (formatted `%b %d, %Y`) | `GET /api/gamification/passport` (**EXISTING**) | **Yes** (`/passport`) |
| QR Check-in scanner | `gamification/qr_scanner.html` | Attraction/establishment detail "scan" btn (`gamification.scan_qr`) | GPS-validated stamp at a landmark (radar HUD, proximity guard) | Client-only: `target_name`, `target_type`, `target_id` (from route); runtime `latitude`, `longitude` from `navigator.geolocation`; hidden manual-verify button; success modal w/ `unlocked_badges[].title/description/badge_image_url` | Page: `gamification.scan_qr` (Next.js page to build). Verify: `POST /api/gamification/checkin` (**EXISTING**) | **No** (no scan page) |
| Chat room list | `chat/index.html` | Direct `/chat` (orphan in nav) | List user's active conversations | `rooms`: `id`, `type` (`barangay`/`business`), `barangay.name`, `establishment.name`, `created_at`; room count badge | `GET /api/chat` (**EXISTING**) | **Yes** (`/chat` list only) |
| Chat room view + send | `chat/room.html` | From room list link (`chat.chat_room`) | View + send messages in a room (Socket.IO realtime) | Hidden `room_id`, `current_user_id`, `csrf_token`; `message-input` textarea (no documented max length). Realtime via Socket.IO | `GET /api/chat/{room_id}` (**EXISTING**, paginated); `POST /api/chat/{room_id}/messages` (**EXISTING**). Realtime WebSocket: **MISSING** (FastAPI has REST only) | **No** (no `/chat/[id]`) |
| Write a review | `pagez/detail.html` (`#review-form`) | Attraction detail (auth-gated) | Submit star rating + comment + photos | `rating` (hidden, required, 1–5 star selector), `comment` (textarea, optional, **max 1000 chars**), `photos` (file, multiple, `accept=image/jpeg,image/png,image/webp`, **up to 5**, max 5MB each, optional); `enctype=multipart/form-data`; CSRF | `POST /api/attractions/{id}/reviews` (**EXISTING**) but accepts **JSON only** `{rating, comment, parent_id}` — **photos NOT handled** (MISSING upload) | **Yes** (`/attractions/[id]` via `review-form.tsx`) |
| Review list | `pagez/detail.html` (`#reviews-feed`) | Attraction detail | Read reviews + rating summary | Review cards; summary avg/stars/distribution; "Load more" (paginated) | `GET /api/attractions/{id}/reviews` (**EXISTING**) | **Yes** (`review-section.tsx`) |
| User dashboard | `user/dashboard.html` | Top nav "Dashboard" | Stats + recent bookmarks, passport badges, visits | `stats.favorites`, `stats.visits`, `stats.events`, `stats.contributions`; `recent_favorites` (attractions+establishments); `badges` (icon, name, desc, unlocked); `recent_visits` (`visit_date`, `target_name`, `target_type`, `notes`) | **MISSING** (no `user` router). Passport badges reuse `GET /api/gamification/passport`; favorites/visits/events/contributions stats have **no** endpoint | **Yes** (minimal: Role/Status/Stamps only from `/api/gamification/passport`) |
| Profile view + edit | `user/profile.html` | Top nav (via Dashboard → "Account Settings") | Manage username/email/interests; password change CTA | `username` (text, required), `email` (email, required), interests checkboxes (`Nature & Adventure`, `Historical Sites`, `Religious Landmarks`, `Food & Dining` — hardcoded pre-checked), "Change Password" button (no endpoint). Submit `POST user.profile` | **MISSING** (no `GET/PUT /api/user/profile`) | **Yes** (read-only display of name/email; no edit form) |
| Bookmarks (Favorites) | `user/favorites.html` | Top nav "Bookmarks" | List saved attractions + establishments | Saved items grid | **MISSING** (no favorites list/toggle endpoint) | **No** |
| My Visits (Travel Log) | `user/visits.html` | Top nav "My Visits" | Grid of logged visits | `visit.visit_date`, `target_name`, `target_type`, `notes`, `created_at`; "Revisit Page" link | **MISSING** (no visits list/log endpoint; check-in creates `TouristCheckIn` but no visit-with-notes endpoint) | **No** |
| Favorite / Visited actions | `includes/user_actions_modal.html` + `js/pages/user-actions.js` | Attraction/establishment detail sidebar | Toggle bookmark; log "Visited" (modal w/ optional notes) | `data-id`, `data-type` (attraction); visit `notes` textarea (optional) | **MISSING** (no favorite-toggle or visit-log endpoint) | **No** |

---

## 3. Form fields & validation (exact, for rebuild)

### 3.1 QR Check-in scanner (`gamification/qr_scanner.html` → `POST /api/gamification/checkin`)
Client-only page. No visible `<form>`; verification is JS-driven.

Context vars injected by Flask (`gamification.scan_qr`, params `type_` + `id_`):
- `target_name` (string, displayed heading), `target_type` (`attraction`|`establishment`), `target_id` (int).

Guard: page reads `localStorage["active_navigation_target"]` (`{id, type}`). If it does **not** match `target_id`/`target_type`, it shows a "Navigation Route Required" block and will not attempt check-in (user must start navigation from the detail page first — see `POST /api/gamification/start-navigation`).

`triggerCheckin(latitude, longitude)` → `fetch("…/verify_checkin", { method:"POST", headers:{ "Content-Type":"application/json", "X-CSRFToken": csrf }, body: JSON.stringify({ type, id, latitude, longitude }) })`.
- `type` (string, required): `attraction` or `establishment`.
- `id` (int, required): target id.
- `latitude` (float, required): from `navigator.geolocation.watchPosition`.
- `longitude` (float, required).
- **Backend validation** (`CheckinRequest`): 50 m Haversine threshold from official coords; `400` if too far or target has no coordinates; `already_checked_in` returned if duplicate; badge unlock computed server-side; response includes `message`, `distance`, `unlocked_badges[{title,description,badge_image_url,reward_promo}]`.

On `200`: show stamp animation + unlock modal (badge image falls back to `/static/img/badges/default.png` if `badge_image_url` null). On fail: reveal manual "Try Manual Verification" button (`verify_manual_btn`).

### 3.2 Chat room (`chat/room.html` → `POST /api/chat/{room_id}/messages`)
`GET /api/chat/{room_id}` returns paginated `messages` (`id`, `sender_id`, `sender_name`, `content`, `created_at`, `is_system_msg`); `has_next`/`has_prev`/`page`. `POST` body (`SendMessageRequest`): `{ "content": string }`. Auth: must be a `ChatParticipant` (or room `type == "barangay"`). Flask used Socket.IO for live push + typing indicator + `csrf_token`; FastAPI has **no WebSocket** — rebuild with polling or a new WS endpoint. `message-input` has no documented max length in template (enforce a sane server cap when adding).

### 3.3 Write a review (`pagez/detail.html` → `POST /api/attractions/{id}/reviews`)
`method="POST"` `action="{{ url_for('attractions.post_review', id=attraction.id) }}"` `enctype="multipart/form-data"`; CSRF hidden field.

| Field | Input | Rules |
|---|---|---|
| `rating` | hidden `<input id="rating-input">` set by star buttons (`data-value` 1–5); required | Must be 1–5; `#rating-error` shown if empty. Backend: `400` if `rating is None or not 1<=rating<=5` (when no `parent_id`). |
| `comment` | `<textarea name="comment" id="review-comment" rows=4>` | Optional; `#char-count` shows `0 / 1000`; client counter caps display at 1000 (enforce server-side max length). |
| `photos` | `<input type="file" name="photos" accept="image/jpeg,image/png,image/webp" multiple>` (drag-drop zone) | Optional, **up to 5**, each ≤ 5 MB, JPG/PNG/WebP. **MISSING in backend**: `ReviewCreate` has no `photos` field; `photos_saved=0` always. Use `POST /api/uploads/multiple` (≤10 images) then attach URLs, or extend `post_review` to accept files. |
| `parent_id` | not in this form (reply path only) | Omit for top-level review. |

Reply (sub-reply) is supported by backend (`parent_id`); validation rejects reply-to-reply and parent/attraction mismatch.

### 3.4 Profile edit (`user/profile.html` → `POST user.profile`)
`method="POST"` `action="{{ url_for('user.profile') }}"`; CSRF hidden field.

| Field | Input | Rules |
|---|---|---|
| `username` | text, `value="{{ current_user.username }}"`, `required` | Required. |
| `email` | email, `value="{{ current_user.email }}"`, `required` | Required, email format. |
| interests (Nature & Adventure) | checkbox, `checked` (hardcoded) | Display-only in Flask; no backend persistence field observed. |
| interests (Historical Sites) | checkbox, `checked` (hardcoded) | Display-only. |
| interests (Religious Landmarks) | checkbox, unchecked (hardcoded) | Display-only. |
| interests (Food & Dining) | checkbox, `checked` (hardcoded) | Display-only. |
| password | "Change Password" button only | **No endpoint** in Flask or FastAPI; stub CTA. |

Note: the template has malformed avatar markup (an unclosed `<button>`/`class="..."` stray line around the avatar) — do not copy verbatim; rebuild cleanly.

### 3.5 Dashboard / Bookmarks / Visits (read-only displays)
- Dashboard stats (`favorites`, `visits`, `events`, `contributions`) require a **new** user-stats endpoint (MISSING). `recent_favorites` need a favorites list endpoint (MISSING). `recent_visits` need a visits list endpoint (MISSING).
- Bookmarks (`user/favorites.html`) and My Visits (`user/visits.html`) are pure list/grid views; both depend on the MISSING favorites/visits endpoints. Visits "Revisit Page" links to `attractions.detail` or `business.detail` by `target_type`.

---

## 4. Shared partials & cross-page assets

| Partial / asset | Role | Used by |
|---|---|---|
| `templates/includes/user_nav.html` | **Tourist top nav** (this role's nav partial) | `base.html` navbar when `role=="user"` |
| `templates/includes/user_actions_modal.html` | Favorite + "Visited" modal (mark-as-visited w/ optional notes) | attraction & establishment detail pages |
| `templates/base.html` | Root layout; switches nav partial by role (`user_nav.html` for `user`) | all pages |
| `templates/includes/guest_nav.html` | Logged-out nav (reference for logged-out state) | `base.html` when anonymous |
| `static/js/pages/user-actions.js` | Wires `#toggle-favorite` + `#open-visit-modal` (MISSING backend) | detail pages |
| `static/js/pages/reviews.js`, `static/js/pages/detail.js` | Review feed + detail map/Leaflet | `pagez/detail.html` |
| `static/js/chat.js` | Socket.IO client (no FastAPI WS equivalent) | `chat/room.html` |
| `static/js/components/user-nav.js` | Dropdown toggle for "Explore" menu | `user_nav.html` |

**Auth includes:** `auth.login` / `auth.logout` / `auth.register` are the login/logout/register flows (see `CONVENTIONS.md §3`). The detail-page review CTA for anonymous users links to `auth.login?next=<url>`.

---

## 5. Backend gaps for the tourist role (add to `CONVENTIONS.md §7`)

| Flask feature | Status | Notes |
|---|---|---|
| Digital Passport | **EXISTING** | `GET /api/gamification/passport` |
| QR check-in (GPS) | **EXISTING** | `POST /api/gamification/checkin` (50 m threshold, badge unlock) |
| Chat list / messages / send | **EXISTING** | `/api/chat`, `/api/chat/{room_id}`, `/api/chat/{room_id}/messages` |
| Reviews (post + list) | **PARTIAL** | `POST/GET /api/attractions/{id}/reviews` exist; **photos upload MISSING** (`ReviewCreate` JSON-only) |
| User dashboard | **MISSING** | No `user` router; stats (favorites/visits/events/contributions) + recent favorites/visits have no endpoint |
| User profile (GET/PUT) | **MISSING** | No `/api/user/profile`; edit username/email/interests/password unbacked |
| Bookmarks / Favorites | **MISSING** | No favorites list or toggle endpoint |
| My Visits (travel log) | **MISSING** | No visits list or visit-log endpoint (with notes) |
| Favorite / Visited actions | **MISSING** | No favorite-toggle or visit-log endpoint for detail-page buttons |
| Chat realtime | **MISSING** | Flask used Socket.IO; FastAPI REST only — needs WebSocket or polling |

**Recommendation:** prioritize a `/api/user` router (profile GET/PUT, dashboard stats, favorites list/toggle, visits list/log) and a review-photo upload path (extend `post_review` or pair with `/api/uploads/multiple`) before porting the dashboard/profile/favorites/visits React pages, since those pages currently have no data source.
