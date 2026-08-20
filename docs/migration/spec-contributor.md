# Migration Spec — Contributor (Barangay Representative) Role

**Source:** Flask `main` branch templates (`templates/barangay/*`, `templates/includes/barangay_nav.html`)
**Target:** Next.js React frontend + existing FastAPI backend (`backend/app/api/*.py`)
**Role:** `contributor` = barangay representative / "Barangay Steward".
**Status:** ENTIRELY absent from React. No `frontend/src/app/contributor*` or `*/barangay*` pages exist. (`frontend/src/app/gallery/gallery-view.tsx` contains only static mock `barangay`/`contributor` strings — not a contributor management UI.)

---

## 1. Navigation structure (sidebar)

All contributor pages extend `admin/admin_base.html` and render the sidebar from
`templates/includes/barangay_nav.html`. There is **no** `contributor_nav.html`
(partial does not exist on `main`).

**Sidebar links (in order):**

| Label | Flask endpoint | FastAPI equivalent | Notes |
|-------|----------------|--------------------|-------|
| Dashboard | `barangay.barangay_dashboard` | — (MISSING) | `/barangay/dashboard` |
| Profile | `barangay.barangay_profile_manage` | — (MISSING) | `/barangay/profile` |
| Attractions | `barangay.barangay_attractions` | partial (`/api/attractions/?barangay=` lists only **approved**) | `/barangay/attractions` |
| Events | `barangay.barangay_events` | partial (`/api/events/` lists only **approved**) | `/barangay/events` |
| Gallery | `barangay.barangay_gallery` | partial (`/api/gallery/` lists only **approved**) | `/barangay/gallery` |
| Reviews | `barangay.barangay_reviews` | partial (`/api/attractions/{id}/reviews` per-attraction only) | `/barangay/reviews` |
| (Logout) | `auth.logout` | `/api/auth/logout` (EXISTING) | right-aligned, separated by border |

**Important:** **Announcements is NOT in the sidebar nav.** It is reachable only via its
dedicated route `/barangay/announcements` and its own "Create Announcement" button.
Treat it as an orphan route (likely linked from a top header or entered directly).

The dashboard also exposes two CTAs (not in sidebar): **Add Landmark** → `barangay.barangay_add_attraction`,
**Publish Event** → `barangay.barangay_add_event`. The dashboard "Log Visit" action links to
`analytics_module.log_visitor` (attraction only).

---

## 2. Feature table

Legend: **EXISTING** = working FastAPI path; **PARTIAL** = path exists but not usable as-is for this role; **MISSING** = no usable endpoint.

| Feature | Main template | Nav location | Purpose | Form fields / data shown | Backend endpoint (FastAPI) | React ported? |
|---|---|---|---|---|---|---|
| Contributor dashboard | `barangay/dashboard.html` | Sidebar "Dashboard" | Stats (total/approved/pending/rejected/reviews), recent activity feed, CTAs | Stats cards: `stats.total`, `stats.approved`, `stats.pending`, `stats.rejected`, `stats.reviews`; `recent_activity` (name, type [Attraction\|Event], status, date, id); "Log Visit" link (attraction only); "Add Landmark"/"Publish Event" CTAs; Gallery preview tile | **MISSING** (no contributor stats endpoint; `/api/analytics/summary` is admin-only). "Log Visit" → `POST /api/analytics/log-visitor/attraction/{id}` (**EXISTING**, contributor allowed via `is_rep` check) | No |
| Barangay profile edit | `barangay/profile.html` | Sidebar "Profile" | Edit barangay mission/vision/history/etc. | Textareas: `mission`, `vision`, `history`, `cultural_assets`, `traditions`, `local_practices`, `unique_features` (pre-filled from `BarangayInfo`) | **MISSING** (no `BarangayInfo` GET/PUT endpoint anywhere in API) | No |
| Attractions list | `barangay/attractions.html` | Sidebar "Attractions" | Table of barangay's attractions w/ status + edit/delete | Columns: image, name, submitted-by, category, status badge (approved/rejected/pending), actions (edit/delete) | **PARTIAL**: `/api/attractions/` lists only **approved** and filters by barangay **name**; contributor needs **all statuses** + own barangay_id. Reuse for approved view only. | No |
| Add attraction | `barangay/add_attraction.html` | Dashboard CTA / "Landmarks List" back link | Submit new landmark (pending moderation) | See §3.1 | **MISSING**: `/api/attractions/` POST is `require_admin` and sets `status="approved"`; no contributor/barangay-scoped create | No |
| Edit attraction | `barangay/edit_attraction.html` | Attractions list edit icon | Edit own landmark (re-submitted pending) | Same fields as add, pre-filled; shows current `image_url` | **MISSING**: `/api/attractions/{id}` PUT is `require_admin`; no barangay-ownership guard | No |
| Delete attraction | (list delete action) | Attractions list | Delete own landmark | Confirm dialog | **MISSING**: `/api/attractions/{id}` DELETE is `require_admin`; no barangay-ownership guard | No |
| Events list | `barangay/events.html` | Sidebar "Events" | Table of barangay's events w/ status | Columns: image, name, location, date, status, actions | **PARTIAL**: `/api/events/` lists only **approved**; contributor needs all statuses + own barangay | No |
| Add event | `barangay/add_event.html` | Dashboard CTA / "Events List" back | Publish event (pending moderation) | See §3.2 | **MISSING**: `/api/events/` POST is `require_admin`, sets `status="approved"` | No |
| Edit event | `barangay/edit_event.html` | Events list edit | Edit own event (re-submitted pending) | Same fields pre-filled | **MISSING**: `/api/events/{id}` PUT is `require_admin` | No |
| Delete event | (list delete) | Events list | Delete own event | Confirm dialog | **MISSING**: `/api/events/{id}` DELETE is `require_admin` | No |
| Gallery list | `barangay/gallery.html` | Sidebar "Gallery" | Grid of contributor's own gallery items | Item: type, url, caption, status | **PARTIAL**: `/api/gallery/` lists only **approved** + all users; needs own-user + all-status filter | No |
| Add gallery item | `barangay/add_gallery.html` | "Gallery Items" back link | Upload photo/video (pending) | See §3.3 | **PARTIAL**: `POST /api/gallery/` exists but has **no auth** and takes a raw `url` (no file upload, no barangay/user linkage); sets `status="pending"` | No |
| Edit gallery item | `barangay/edit_gallery.html` | Gallery list | Replace media / edit caption | Current media preview, new file/url, caption | **MISSING** (no gallery PUT/DELETE endpoint) | No |
| Delete gallery item | (list delete) | Gallery list | Delete own item | — | **MISSING** | No |
| Announcements list | `barangay/announcements.html` | **Not in sidebar** | List barangay bulletins w/ status + edit/delete | Columns: title, status (approved/rejected/pending), content (truncated 300), created_at, actions | **MISSING** (no `/api/announcements` router at all; `Announcement` model exists but no API) | No |
| Add announcement | `barangay/add_announcement.html` | Announcements "Create" btn | Post bulletin (pending approval) | See §3.4 | **MISSING** | No |
| Edit announcement | `barangay/edit_announcement.html` | Announcements list | Edit bulletin (re-submitted pending) | title, content pre-filled | **MISSING** | No |
| Delete announcement | (list delete) | Announcements list | Delete own bulletin | Confirm dialog | **MISSING** | No |
| Reviews view + reply | `barangay/reviews.html` | Sidebar "Reviews" | Read barangay's attraction reviews, rating summary, reply | See §3.5 | List: **PARTIAL** (`/api/attractions/{id}/reviews` per-attraction only, no barangay scope). Reply: `POST /api/attractions/{id}/reviews` with `parent_id` (**EXISTING**, active-user; but **no barangay-ownership guard** like Flask has) | No |

---

## 3. Form fields & validation (exact, for rebuild)

### 3.1 Add / Edit Attraction (`add_attraction.html`, `edit_attraction.html`)
Method `POST` to `barangay.barangay_add_attraction` / `barangay_edit_attraction`; `enctype="multipart/form-data"`; CSRF token.

| Field | Input | Rules |
|---|---|---|
| `name` | text | required; `validate_string_input` max_length **200** |
| `category` | select (required) | `Nature`, `Historical`, `Religious`, `Adventure`, `Culture` |
| `description` | textarea (rows 5) | required; sanitized HTML |
| `directions` | textarea (rows 3) | optional; `validate_string_input` max_length **5000**; sanitized |
| `latitude` | number `step="any"` | required; `validate_coordinates` (−90..90); placeholder `15.7xxx` |
| `longitude` | number `step="any"` | required; `validate_coordinates` (−180..180); placeholder `120.2xxx` |
| `image` | file `accept="image/*"` | optional; uploaded via `save_uploaded_file` |
| `image_url` | url | optional; used if no file uploaded |

- **Map picker:** Leaflet (`vendor/leaflet`, `js/map-picker.js`); default center `[15.7889, 120.2986]`, zoom 14; "Pinpoint My Location" geolocation button auto-fills lat/lng inputs; marker drag updates inputs.
- **On submit:** `barangay_id = current_user.barangay_id`, `user_id = current_user.id`, **`status = "pending"`** (Flask). Editing also resets `status="pending"`.
- **Edit:** pre-fills from `attraction.*`; shows current `image_url` preview.
- FastAPI `AttractionCreate` accepts: `name, description, category, latitude, longitude` (required) + `barangay_id, image_url, directions, opening_hours, entrance_fee, contact_info, facilities, physical_status, is_featured` — but is **admin-gated** and forces `status="approved"`.

### 3.2 Add / Edit Event (`add_event.html`, `edit_event.html`)
`POST` `enctype="multipart/form-data"`.

| Field | Input | Rules |
|---|---|---|
| `name` | text | required; min 1 / **max 200**; `validate_string_input` on edit |
| `category` | select (required) | `Civic`, `Religious`, `Entertainment` |
| `date` | date `type=date` | required; parsed `%Y-%m-%d` |
| `location` | text | required |
| `latitude` | number `step="any"` | optional; `validate_coordinates` if provided |
| `longitude` | number `step="any"` | optional; `validate_coordinates` if provided |
| `description` | textarea (rows 5) | required; **max 2000**; sanitized |
| `image` | file `accept="image/*"` | optional |
| `image_url` | url | optional |

- `barangay_id = current_user.barangay_id`, `user_id = current_user.id`, **`status = "pending"`**. Editing resets to pending.
- Edit pre-fills `date` as `%Y-%m-%d`.
- FastAPI `EventCreate` requires `name, description, date, location, category` + optional `latitude, longitude, barangay_id, image_url` — **admin-gated**, forces `status="approved"`.

### 3.3 Add / Edit Gallery (`add_gallery.html`, `edit_gallery.html`)
Add: `POST` `enctype="multipart/form-data"`.

| Field | Input | Rules |
|---|---|---|
| `type` | select (required) | `photo`, `video` (auto-detected from filename if file uploaded) |
| `media_file` | file `accept="image/*,video/*"` | optional; file upload takes precedence over URL |
| `url` | url | required if no file; `sanitize_url` |
| `caption` | textarea (rows 3) | optional; `sanitize_html_input` |

- Add: `user_id = current_user.id`, **`status = "pending"`**.
- Edit: only owner (`gallery_item.user_id == current_user.id`) can edit; new file/url replaces; leaving both empty keeps current; resets `status="pending"`.
- FastAPI `POST /api/gallery/`: body `GalleryItemCreate{type, url (required), caption, user_id}` — **no auth dependency**, no file handling, no barangay ownership; returns `status="pending"`. **Not directly usable** for contributor auth/scope (caller must supply `user_id` and a pre-uploaded URL).
- File uploads (when porting) should use `POST /api/uploads/image` or `/api/uploads/multiple` (EXISTING) then submit the returned URL.

### 3.4 Add / Edit Announcement (`add_announcement.html`, `edit_announcement.html`)
`POST` (no file upload; plain form).

| Field | Input | Rules (Flask) |
|---|---|---|
| `title` | text | required; **min 5 / max 200**; `validate_string_input` |
| `content` | textarea (rows 8) | required; **min 10 / max 5000**; `validate_string_input`; sanitized |

- Add: `user_id = current_user.id`, `barangay_id = current_user.barangay_id`, **`status = "pending"`**.
- Edit: only own barangay; resets `status="pending"`.
- **No FastAPI endpoint exists** (no announcements router, only `Announcement` model + relationships).

### 3.5 Reviews + Reply (`reviews.html`)
- Data: `reviews` = root `AttractionReview` for attractions in contributor's barangay (joined to `Attraction`).
- UI: average rating + star distribution (1..5); each review shows user, date, star badges, linked attraction name, comment, and nested **replies** (with role badge `Barangay Rep`/`Admin`).
- Reply form (`POST barangay.barangay_reply_to_review`): field `comment` (required, sanitized), `parent_id = review.id`, creates reply with `rating=None`, **`status="approved"`** (steward replies auto-approved). Guard: review's attraction must belong to contributor's barangay.
- FastAPI:
  - List: `GET /api/attractions/{attraction_id}/reviews` (approved root reviews + summary). **No barangay-scoped aggregate** — implementation must loop over the barangay's attractions or a new endpoint is needed.
  - Reply: `POST /api/attractions/{attraction_id}/reviews` with `{rating: null, comment, parent_id}`. **EXISTING**, requires `get_current_active_user` (any logged-in user can reply, incl. contributor). **Caveat:** Flask enforces the review belongs to the contributor's barangay; the FastAPI endpoint does **not** — add a barangay-ownership guard when wiring the UI.

### 3.6 Profile (`profile.html`)
`POST` (plain form). Fields (all textareas, pre-filled from `BarangayInfo`, sanitized, max_length **5000** each):
`mission`, `vision`, `history`, `cultural_assets`, `traditions`, `local_practices`, `unique_features`.
Sets `info.user_id = current_user.id` if unset. **No FastAPI endpoint exists** for reading/updating `BarangayInfo`.

---

## 4. Shared partials & utilities

- **Layout:** `admin/admin_base.html` (blocks: `admin_head`, `admin_content`, `scripts`). Contributor pages reuse the admin shell — top header + sidebar `barangay_nav.html`.
- **Sidebar partial:** `templates/includes/barangay_nav.html` (links in §1). Active state via `request.endpoint` match.
- **Maps:** Leaflet (`static/vendor/leaflet/*`) + `static/js/map-picker.js` (`MapPicker` class, `defaultLocation:[15.7889,120.2986]`, zoom 14, geolocation button). Used by attraction + event add/edit.
- **File uploads:** Flask `save_uploaded_file` / `detect_media_type`. FastAPI equivalent: `POST /api/uploads/image`, `POST /api/uploads/multiple` (**EXISTING**).
- **Auth/CSRF:** Flask CSRF token + `@login_required` + `current_user.role == "contributor"` guard on every route. Rate limited `@limiter.limit("10 per minute")` on all POST routes.
- **Moderation model:** Every contributor create/edit sets `status="pending"` (gallery/announcement/attraction/event); admin approves → `approved`; rejection → `rejected` (shows "Correction Required", link to edit). Steward review replies are `approved` immediately.

---

## 5. Backend endpoint gap summary (FastAPI)

**EXISTING & usable as-is:**
- `POST /api/auth/logout`
- `POST /api/uploads/image`, `POST /api/uploads/multiple`
- `POST /api/analytics/log-visitor/attraction/{id}` (contributor-allowed for own barangay attraction)
- `POST /api/attractions/{attraction_id}/reviews` (reply via `parent_id`; needs barangay-ownership guard added)
- `GET /api/attractions/{id}/reviews` (per-attraction; needs barangay aggregation wrapper)
- `GET /api/attractions/?barangay=<name>` and `GET /api/events/`, `GET /api/gallery/?barangay=<id>` — **approved-only lists** (reuse for read-only public-style lists, not for contributor all-status management)

**MISSING (must be built — contributor-scoped, `status="pending"` on submit, barangay ownership guards):**
1. Contributor dashboard stats endpoint (counts by status for `current_user.barangay_id` + review count).
2. Contributor CRUD for Attractions (create/list-all-status/edit/delete) — currently admin-only.
3. Contributor CRUD for Events (create/list-all-status/edit/delete) — currently admin-only.
4. Contributor Gallery edit/delete + authenticated, barangay/user-scoped create (current `/api/gallery/` POST is unauthenticated & url-only).
5. **Full Announcements module** (`/api/announcements`: list/create/edit/delete, barangay-scoped) — no router exists.
6. **BarangayInfo profile GET/PUT** (`mission/vision/history/cultural_assets/traditions/local_practices/unique_features`) — no endpoint exists.
7. Barangay-scoped review aggregate listing + rating summary (per-barangay, all statuses).
8. Add `require_contributor` dependency and barangay-ownership guards (currently only `require_admin` exists; `contributor` is referenced in `booking.py`/analytics but has no dedicated dependency).

---

## 6. Implementation notes
- Reuse the public attraction/event/gallery list endpoints for read-only "approved" browsing, but build **contributor-specific** list endpoints that include `pending`/`rejected` and scope by `current_user.barangay_id`.
- All create/edit must set `status="pending"` (matching Flask moderation flow) — the existing admin endpoints force `status="approved"`, so they are NOT drop-in replacements.
- Add a shared `MapPicker` React component (Leaflet) replicating `js/map-picker.js` behavior for attraction/event geo-pick.
- Use `/api/uploads/*` for image/file handling, then submit returned URLs (Flask mixed file + url; FastAPI gallery currently url-only).
- Announcements and BarangayInfo profile have **zero** API surface — highest build priority.
