# Admin Role — Migration Spec (Flask `main` → Next.js)

Scope: documents every **admin** user-role page/feature from the Flask `main` branch
templates, maps each to an **EXISTING FastAPI endpoint** in `backend/app/api/*.py`,
and records what is already ported to React under `frontend/src/app`.

> API prefix reference (from `backend/app/main.py`):
> `auth=/api/auth`, `public=/api`, `attractions=/api/attractions`, `events=/api/events`,
> `business=/api/business`, `booking=/api/booking`, `heritage=/api/heritage`,
> `analytics=/api/analytics`, `notifications=/api/notifications`, `uploads=/api/uploads`,
> `admin=/api/admin`.

---

## 1. Navigation structure

The admin UI has **two nav surfaces** (both read-only templates).

### 1a. Top nav — `templates/includes/admin_nav.html`
Horizontal bar shown on most admin pages:

| Label | Endpoint (Flask) | Notes |
|---|---|---|
| Dashboard | `admin.admin_dashboard` | |
| Attractions | `admin.admin_attractions` | |
| More ▾ (dropdown) | | contains: |
| ↳ Events | `admin.admin_events` | |
| ↳ Visits | `admin.visits_index` | |
| ↳ Reviews | `admin.reviews_list` | |
| ↳ Documents | `admin.admin_documents` | |
| ↳ Newsletter | `newsletter_admin.index` | |
| ↳ Businesses | `admin.manage_establishments` | |
| View Site | `public.index` | |
| Logout | `auth.logout` | |

### 1b. Sidebar — `templates/admin/admin_base.html` (`<aside id="admin-sidebar">`)
Primary navigation for `role == 'admin'` (this is what actually renders the menu):

| Sidebar label | Endpoint (Flask) |
|---|---|
| Dashboard | `admin.admin_dashboard` |
| Landmarks | `admin.admin_attractions` |
| Local Events | `admin.admin_events` |
| Analytics | `admin.visits_index` |
| Public Reviews | `admin.reviews_list` |
| Newsletters | `newsletter_admin.index` |
| Businesses | `admin.manage_establishments` |
| Verify Merchants | `admin.manage_merchant_verifications` |
| Reservations | `booking.dashboard` |

> **Nav gap worth flagging:** *Heritage* and *Documents* pages exist as admin
> routes (referenced by `templates/includes/admin_breadcrumb.html` and `admin_nav.html`
> "More" dropdown lists "Documents"), but **neither Heritage nor Documents has a
> sidebar or top-nav entry for the `admin` role** in `admin_base.html`. They are
> reached only from within heritage/documents pages (and the "Documents" item in the
> top-nav "More" dropdown). Confirm intended entry point before porting.

### 1c. Breadcrumb partial — `templates/includes/admin_breadcrumb.html`
Auto-builds `Admin / [Section] / [Page]` from `request.endpoint`. Sections:
Attractions, Events, Heritage, Documents, Newsletter, Businesses. Used on
`admin/dashboard.html` (which several feature pages `{% extends %}`).

### 1d. Shared partials / layout
- `admin/admin_base.html` — master layout (sidebar + topbar + mobile drawer).
- `admin/dashboard.html` — `{% extends %}` base for heritage, verify-merchants,
  documents, reviews (provides `admin_header` + `admin_content` blocks).
- `admin/admin_base.css`, `css/pages/admin_dashboard.css`, `css/components/admin-forms.css`,
  `css/pages/admin_add_event.css`, `js/components/admin-nav.js`,
  `js/pages/admin_heritage.js`, `js/pages/admin_documents.js`,
  `js/pages/admin_edit_attraction.js`, `js/pages/visitor-analytics.js`.
- Chart.js (vendor) used on Dashboard (`engagementChart`) and Visits
  (`destinationComparisonChart`).

---

## 2. Feature / page inventory

Legend: ✅ EXISTING (FastAPI path given) · ❌ MISSING (no FastAPI endpoint) ·
⚠️ PARTIAL.

| Feature | Main template | Nav location | Purpose | Backend endpoint (EXISTING path or MISSING) | Ported to React? |
|---|---|---|---|---|---|
| Admin Dashboard | `admin/dashboard.html` | Sidebar "Dashboard" / top-nav | Bento stat cards (attractions, events, gallery, reviews, pending_reviews), engagement chart (7-day), top attractions by views, approval queues (users, gallery, reviews, announcements) | ❌ No single dashboard endpoint. Composed from `GET /api/attractions`, `GET /api/events`, `GET /api/gallery`, `GET /api/attractions/{id}/reviews`, `GET /api/admin/users` (all ✅) — but **approval actions** `approve_user`/`reject_user`/`approve_review`/`reject_review`/`admin_approve_announcement`/`admin_reject_announcement` and **announcements** are ❌ MISSING | ✅ `/admin` (page exists) |
| Attractions — List | (ref `admin/admin_attractions.html`, not in read set) | Sidebar "Landmarks" / top-nav "Attractions" | Grid/list of landmarks with approve/delete/edit | ✅ `GET /api/attractions` (note: returns **approved only**); per-item `PUT`/`DELETE` below | ✅ `/admin/attractions` (list page exists) |
| Attractions — Add | `admin/add_attraction.html` | Breadcrumb Attractions › Add Attraction | Create landmark form | ✅ `POST /api/attractions` (require_admin). ⚠️ `barangay_id` dropdown needs a barangay list — **no `/api/barangays` endpoint exists** | ❌ form not ported (only list) |
| Attractions — Edit | `admin/edit_attraction.html` | Breadcrumb Attractions › Edit Attraction | Edit landmark form (prefilled) | ✅ `PUT /api/attractions/{attraction_id}`; ✅ `DELETE /api/attractions/{attraction_id}` | ❌ form not ported |
| Events — List | (ref `admin/events.html`, not in read set) | Sidebar "Local Events" / top-nav "Events" | Grid/list of events with approve/delete/edit | ✅ `GET /api/events` (approved only) | ✅ `/admin/events` (list page exists) |
| Events — Add | `admin/add_event.html` | Breadcrumb Events › Add Event | Create event form | ✅ `POST /api/events` (require_admin). ⚠️ `barangay_id` dropdown — same missing barangay list | ❌ form not ported |
| Events — Edit | `admin/edit_event.html` | Breadcrumb Events › Edit Event | Edit event form (prefilled) | ✅ `PUT /api/events/{event_id}`; ✅ `DELETE /api/events/{event_id}` | ❌ form not ported |
| Establishments (Business Directory) | `admin/establishments.html` | Sidebar "Businesses" / top-nav "Businesses" | Status-tabbed list (all/pending/approved/rejected) of establishments; approve/reject/delete | ⚠️ `GET /api/business` exists but returns **approved only** (no status filter). ❌ `approve_establishment`/`reject_establishment`/`delete_establishment` (admin moderation) MISSING | ❌ |
| Booking Management | `admin/booking_management.html` | Sidebar "Reservations" (`booking.dashboard`) | Table of reservations (date, asset, tourist, party size, status) with inline status `<select>` that POSTs via fetch | ✅ status update `POST /api/booking/admin/update-status`. ❌ **no GET endpoint to list all reservations** for the table (table data source MISSING) | ❌ |
| Heritage — Dashboard | `admin/heritage_dashboard.html` | Breadcrumb Heritage (no sidebar/top-nav link) | Bento of `type_stats` (total/approved/pending per type) + master registry table of `heritage_types` | ✅ `GET /api/heritage/types`; ✅ `GET /api/heritage` (list all) | ❌ |
| Heritage — List (per type) | `admin/heritage_list.html` | Breadcrumb Heritage › Records List | Searchable/filterable table per `heritage_type`; export Excel/DOCX, edit, delete, pagination | ✅ `GET /api/heritage/{heritage_type}` (list by type); ✅ `PUT`/`DELETE /api/heritage/{heritage_type}/{item_id}`. ❌ `admin_heritage_export_excel` / `admin_heritage_export_docx` (NCCA export) MISSING | ❌ |
| Heritage — Add/Edit form | `admin/heritage_form.html` | Breadcrumb Heritage › Add/Edit Record | **Dynamic form** generated from `config.fields` (each = `field_name, label, field_type, required`; types: text/number/textarea/select/json) | ✅ `POST /api/heritage/{heritage_type}` (create); ✅ `PUT /api/heritage/{heritage_type}/{item_id}` (edit). Field schema must be replicated from Flask `HERITAGE_TYPES` config (not in API — needs re-source) | ❌ |
| Documents (Vault) | `admin/documents_dashboard.html` | top-nav "More › Documents" (no sidebar link) | Folder/category browser, recent activity, structured records, rapid-create, import (.docx), backup/export-all, edit structure, file versions | ❌ **Entire module MISSING** — no `documents` router. Routes used: `admin_documents`, `admin_document_create`, `admin_document_edit`, `admin_document_files`, `admin_document_import`, `admin_document_record_edit`, `admin_documents_export_all`, `admin_document_category_files`, `admin_heritage_export_docx` | ❌ |
| Newsletter — Index | `admin/newsletter/index.html` | Sidebar "Newsletters" / top-nav "Newsletter" | Active-subscriber stat, compose/history shortcuts, subscriber directory table | ❌ **Admin newsletter MISSING** — only public `POST /api/notifications/subscribe` exists. Routes used: `newsletter_admin.index`, `newsletter_admin.compose`, `newsletter_admin.history`, `newsletter_admin.export_subscribers`, `newsletter_admin.delete_subscriber` | ❌ |
| Newsletter — Compose | `admin/newsletter/compose.html` | Breadcrumb Newsletter | Broadcast form: subject, HTML content, recipient checkboxes (all / per-subscriber) | ❌ MISSING | ❌ |
| Newsletter — History | `admin/newsletter/history.html` | Breadcrumb Newsletter | Campaign log table; "Inspect Payload" modal fetches `/admin/newsletter/history/{id}/content` | ❌ MISSING (incl. history-content endpoint) | ❌ |
| Reviews Moderation | `admin/reviews.html` | Sidebar "Public Reviews" / top-nav "Reviews" | Status-tabbed (pending/approved/all) review queue; approve/reject; pagination; reply context | ⚠️ `GET /api/attractions/{id}/reviews` (per-attraction) + `POST /api/attractions/{id}/reviews` exist. ❌ **admin-wide review list + `approve_review`/`reject_review` moderation** MISSING | ❌ |
| Verify Merchants | `admin/verify_merchants.html` | Sidebar "Verify Merchants" | Table of `BusinessVerification` (permit/other docs, submitted_at, status) with approve/reject | ❌ MISSING — `admin.manage_merchant_verifications`, `approve_merchant_verification`, `reject_merchant_verification` (no FastAPI endpoints; `business_verification` relation exists on User model) | ❌ |
| Visitor Registry | `admin/visitor_registry.html` | Sidebar "Analytics" area / "Visitor Registry" | Filtered master table of `VisitorLog` (visitor, age, origin, status, location, date, steward); date/type/id/name filters; export; "Log Walk-in Guest" modal | ⚠️ `POST /api/analytics/log-visitor/{target_type}/{target_id}` (log) ✅; `GET /api/analytics/summary` ✅ (totals only). ❌ `visitor_registry` list, `export_visits` MISSING | ❌ |
| Visits (Tourism Analytics) | `admin/visits.html` | Sidebar "Analytics" / top-nav "Visits" | Period stats (total/month_total/top_location), comparison chart, location audit list, recent logs, log-check-in form, exports (visits/page-views/destination-insights) | ⚠️ `POST /api/analytics/log-visitor/...` ✅; `GET /api/analytics/summary` ✅ (only totals — not period stats/top_location/comparison). ❌ `export_visits`, `export_page_views`, `export_destination_insights` MISSING; `stats`/`location_stats`/`logs`/`comparison_chart_data` list endpoints MISSING | ❌ |
| Log Visitor (public/barangay form) | `analytics/visitor_log.html` | (standalone, from business/barangay dashboards) | Form to log a visitor to a target; user search when "system user" toggled | ✅ `POST /api/analytics/log-visitor/{target_type}/{target_id}`. ❌ `GET /auth/api/users/search` (user-picker) MISSING in FastAPI (`GET /api/auth/me` exists but no search) | ❌ |

---

## 3. Form-field specs (for rebuilding exact forms)

### 3.1 Add Attraction (`admin/add_attraction.html`) — `POST /api/attractions`
- **name** — text, `required`
- **category** — select `required`: `Nature` (Nature & Parks), `Historical` (Historical Landmark), `Religious` (Religious Site), `Adventure` (Adventure & Recreation), `Culture` (Cultural Center)
- **barangay_id** — select `required` (from `barangays`; default id=1). ⚠️ needs barangay source
- **description** — textarea `required`
- **directions** — textarea (optional) "How to Get Here"
- **latitude** — number `step=any` `required`
- **longitude** — number `step=any` `required`
- **physical_status** — select `required`: `Open Public`, `Temporarily Closed`, `Restricted Access`, `Special Events Only`
- **is_verified** — checkbox (value `"true"`, default **checked**)
- **image** — file `accept=image/*` (optional) **OR** **image_url** — url (optional)
- CSRF token (no CSRF in FastAPI — replace with bearer auth)
- ⚠️ Template quirk: add form `action` is a placeholder `url_for('admin.edit_attraction', id=0)`; real submit goes to `add_attraction`.

### 3.2 Edit Attraction (`admin/edit_attraction.html`) — `PUT /api/attractions/{id}`
Same fields, prefilled. Category options include a legacy typo `Culinray` (keep for parity or normalize). `is_verified` checked when `attraction.is_verified`. Image preview from `image_url`; supports new file upload or image_url overwrite.

### 3.3 Add Event (`admin/add_event.html`) — `POST /api/events`
- **name** — text `required`, `maxlength=200`
- **date** — date `required`
- **category** — select `required`: `Civic` (Civic Activity), `Religious` (Religious Tradition), `Entertainment` (Public Entertainment), `Cultural` (Cultural Exhibition)
- **location** — text `required`, `maxlength=300`
- **description** — textarea `required`, `maxlength=2000`
- **barangay_id** — select `required` (default 1) ⚠️ barangay source
- **image** — file `accept=image/*` OR **image_url** — url
- CSRF → bearer auth.

### 3.4 Edit Event (`admin/edit_event.html`) — `PUT /api/events/{id}`
Same fields, prefilled; `date` formatted `%Y-%m-%d`; image_url preview + new upload/url overwrite.

### 3.5 Heritage Add/Edit (`admin/heritage_form.html`) — `POST`/`PUT /api/heritage/{heritage_type}/{item_id?}`
- **Dynamic** — fields come from `config.fields` (a list of `(field_name, label, field_type, required)`).
- `field_type` ∈ `text`, `number`, `textarea`, `select`, `json`.
  - `select` → options from `config[field_name + '_choices']` (title-cased).
  - `json` → textarea, `placeholder='["item1","item2"]'` or `{"key":"value"}`, `tojson` on edit.
  - `textarea`/`json` span full width.
- Hidden `csrf_token`. Submit → `admin_heritage_add` / `admin_heritage_edit`.
- **Migration note:** the `HERITAGE_TYPES` config (field lists, choices, labels, has_coords, name_field, form ids) lives in the Flask app, **not** in the FastAPI API. Must be re-sourced from `main` (`app/modules/heritage/...`) and exposed (or hard-coded in the Next.js client) so the dynamic form can be rebuilt exactly.

### 3.6 Log Visit / Walk-in (`admin/visitor_registry.html`, `admin/visits.html`, `analytics/visitor_log.html`) — `POST /api/analytics/log-visitor/{target_type}/{target_id}`
- **target_type** — `attraction` | `establishment`
- **target_id** — id of the chosen location
- **visitor_count** — number, `min=1`, default 1 (`required`)
- **visit_date** — date (default today)
- **visitor_name** — text (`required` on registry/analytics forms)
- **visitor_age** — number (optional)
- **is_system_user** — checkbox (value `"true"`)
- **visitor_address** — text (optional)
- **notes** — textarea (optional)
- `analytics/visitor_log.html` extra: toggle reveals user search → `GET /auth/api/users/search?q=` (❌ MISSING in FastAPI).

---

## 4. Endpoint status summary (admin features)

### ✅ EXISTING FastAPI endpoints usable as-is
| Feature | Path |
|---|---|
| Attraction CRUD | `POST /api/attractions`, `PUT /api/attractions/{attraction_id}`, `DELETE /api/attractions/{attraction_id}`, `GET /api/attractions` |
| Event CRUD | `POST /api/events`, `PUT /api/events/{event_id}`, `DELETE /api/events/{event_id}`, `GET /api/events` |
| Heritage CRUD + lists | `GET /api/heritage`, `GET /api/heritage/types`, `GET /api/heritage/{heritage_type}`, `GET /api/heritage/{heritage_type}/{item_id}`, `POST /api/heritage/{heritage_type}`, `PUT /api/heritage/{heritage_type}/{item_id}`, `DELETE /api/heritage/{heritage_type}/{item_id}` |
| Booking status update | `POST /api/booking/admin/update-status` |
| Log visitor | `POST /api/analytics/log-visitor/{target_type}/{target_id}` |
| Analytics summary (totals) | `GET /api/analytics/summary` |
| User list (approvals source) | `GET /api/admin/users` |
| Business list (approved) | `GET /api/business` |
| Public newsletter subscribe | `POST /api/notifications/subscribe` |
| Image upload | `POST /api/uploads/image`, `POST /api/uploads/multiple` |

### ❌ MISSING FastAPI endpoints (must be built)
1. **Dashboard aggregation** + approval/moderation actions: `approve_user`, `reject_user`, `approve_review`, `reject_review`, `admin_approve_announcement`, `admin_reject_announcement`, announcements list.
2. **Barangay source** for attraction/event/heritage forms (no `GET /api/barangays`).
3. **Establishment moderation**: `approve_establishment`, `reject_establishment`, `delete_establishment` (and status-filtered list).
4. **Booking reservations list** (GET to populate the management table).
5. **Heritage exports**: `admin_heritage_export_excel`, `admin_heritage_export_docx`.
6. **Documents module** (entire `admin_documents*` + `admin_document_*` + import/export-all/category-files/record-edit).
7. **Newsletter admin**: index/compose/history/export-subscribers/delete-subscriber/history-content.
8. **Reviews moderation**: admin-wide review list + `approve_review`/`reject_review`.
9. **Merchant verification**: `manage_merchant_verifications`, `approve_merchant_verification`, `reject_merchant_verification`.
10. **Visitor Registry list + `export_visits`**; **Visits** `export_page_views`, `export_destination_insights`, and richer `summary` (period totals, `top_location`, `location_stats`, `comparison_chart_data`).
11. **User search** for visitor log: `GET /api/auth/users/search?q=`.

### ⚠️ PARTIAL / caveats
- `GET /api/attractions` and `GET /api/events` return **approved-only** — admin lists that show pending items need an admin-scoped list variant.
- `GET /api/business` returns **approved-only** — no pending/status filter for the Business Directory.
- `GET /api/analytics/summary` returns only `total_visitors`, `total_page_views`, `recent_visitors_7d` — insufficient for the Visits dashboard (needs `stats.total`, `stats.month_total`, `stats.top_location`, `location_stats`, `logs`, `comparison_chart_data`).

---

## 5. React porting status
Already ported (`frontend/src/app`):
- `/admin` — dashboard page (maps to `admin_dashboard.html`)
- `/admin/attractions` — list page (maps to `admin_attractions.html`); **add/edit forms not ported**
- `/admin/events` — list page (maps to `admin_events.html`); **add/edit forms not ported**
- `/admin/users` — user management (partially covers dashboard `pending_users` approval)

**Not ported (all other admin features):** heritage (dashboard/list/form), documents,
newsletter (index/compose/history), reviews moderation, verify merchants, establishments,
booking management, visitor registry, visits analytics, analytics visitor-log form.

---

*Generated by read-only investigation of `main` templates + `backend/app/api/*.py`.
No files were modified.*
