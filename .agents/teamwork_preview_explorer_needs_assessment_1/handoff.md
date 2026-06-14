# Codebase Analysis & Needs Assessment Report

This report evaluates the **Mangatarem Cultural Map & Local Tourism Information System** codebase, assessing the location, presence, and completeness of core requirements.

---

## 1. Observation

### R1. Contributor Module Alignment
*   **Barangay Profile Updates**:
    *   *Path*: `modules/barangay/routes.py:231-262` (`barangay_profile_manage` controller action).
    *   *Template*: `templates/barangay/profile.html` (form mapping updates to `BarangayInfo` fields).
*   **Attraction Addition & Editing**:
    *   *Path*: `modules/barangay/routes.py:79-141` (`add_attraction` action) and `modules/barangay/routes.py:143-227` (`edit_attraction` action).
    *   *Templates*: `templates/barangay/add_attraction.html` and `templates/barangay/edit_attraction.html`.
*   **Event Addition & Editing**:
    *   *Path*: `modules/barangay/routes.py:265-316` (`add_event` action) and `modules/barangay/routes.py:318-372` (`edit_event` action).
    *   *Templates*: `templates/barangay/add_event.html` and `templates/barangay/edit_event.html`.
*   **Media / Gallery Uploads**:
    *   *Path*: `modules/gallery/routes.py:46-77` (`upload_photo` action).
    *   *Model*: `GalleryItem` in `modules/gallery/models.py:5-24`.
    *   *Template*: `templates/gallery/upload.html`.
*   **Announcements**:
    *   No dedicated "announcement" database table exists. Instead, announcements are represented as public **Event / festival calendar listings** (handled via `modules/events/routes.py`) and administrative **Newsletters** sent to subscribers.
    *   *Model*: `NewsletterSubscriber` and `NewsletterHistory` in `modules/notifications/models.py:5-32`.
    *   *Admin Compose Controller*: `modules/notifications/admin_routes.py:34-108`.

---

### R2. Central Admin Approval Module
*   **Pending Items Moderation**:
    *   *Path*: `modules/admin_core/dashboard.py:110-156` (`_get_pending_items` query logic fetches reviews, content submissions, and attractions with `status='pending'`).
    *   *Admin Approval Routes*:
        *   **Attractions/Establishments**: `modules/admin_core/content.py:84-142` (`admin_approve_item` and `admin_reject_item` route actions update status to `'approved'` or `'rejected'`).
        *   **Reviews**: `modules/admin_core/content.py:144-190` (`admin_approve_review` and `admin_reject_review` route actions).
    *   *Admin Moderation Templates*:
        *   `templates/admin/pending_items.html`
        *   `templates/admin/review_moderation.html`

---

### R3. Centralized Database & Core Features
*   **Database Configuration**:
    *   *Path*: `config.py:27-33` (loads database URI via `get_database_uri()`).
    *   *Provider Settings*: `utils/db_manager.py:199-232` handles conditional initialization of **SQLite** (local default), **MySQL** (standard & XAMPP/Laragon configs), and **Supabase (PostgreSQL)**.
    *   *Vercel Optimization*: `utils/db_manager.py:97-101` automatically switches PostgreSQL ports to `6543` for the Supabase Transaction Pooler when run under Vercel, and tunes connections via `NullPool` (`utils/db_manager.py:255-261`).
*   **Interactive Map System**:
    *   *MVT Backend Route*: `modules/core/map_routes.py` (serves Vector Tiles using PostGIS `ST_AsMVT` and Redis caching).
    *   *Frontend Integration*: `static/js/pages/map.js` (initializes Mapbox GL JS, handles layers, fallback Leaflet logic, and custom styling).
    *   *Concept of "Dual-marker/Brochures"*: Legacy physical brochures are replaced digitally by standard NCCA (National Commission for Culture and the Arts) Forms 01-07 parsed via `modules/api_v1/documents.py` into JSON and saved to the database. There is no custom visual layer or map toggle specifically named "dual-marker/brochures".
*   **Event Calendar Integration**:
    *   *Path*: `templates/pagez/events.html:120-138` (defines the HTML container structure for the calendar widget).
    *   *Calendar Rendering Logic*: `static/js/pages/events.js:66-187` (parses date attributes, populates days, flags dates containing events with `has-event`, and updates filters dynamically).
*   **Visitor Dashboard & Performance**:
    *   *Path*: `modules/admin_core/dashboard.py:28-66` aggregates metrics for page views (`AnalyticsPageView`), review ratings, and registered visitor check-ins (`VisitorLog`).
    *   *Visitor Logging Route*: `modules/analytics/routes.py:12-83` (`log_visitor` records physical visitor counts, age, and addresses).
    *   *Visitor Logging Schema*: `modules/analytics/models.py:63-103` (`VisitorLog`).
    *   *Page View Analytics Schema*: `modules/analytics/models.py:5-22` (`AnalyticsPageView`).

---

### R4. Security, Roles, & LGU Policies
*   **Role-Based Access Control (RBAC)**:
    *   Authorization checks are executed inside blueprint routes via `@login_required` combined with conditional role logic (`current_user.role == 'admin'`, `'contributor'`, etc.).
    *   For example, `_require_admin` in `modules/api_v1/documents.py:377-383` blocks access to non-admin roles.
*   **Password Hashing**:
    *   Implemented via Werkzeug security primitives (`generate_password_hash` and `check_password_hash`) in `modules/auth/routes.py` and `modules/auth/models.py`.
*   **Data Privacy & SQL Injection Protection**:
    *   Dynamic forms validation in `modules/api_v1/documents.py:702-722` uses `detect_sql_injection_attempt` to prevent injection vectors in parsed `.docx` document imports.
    *   Database transactions are audited using `DatabaseAuditLog` (`modules/analytics/models.py:23-61`).

---

## 2. Logic Chain

1.  **R1 (Contributor Portal)** is **Fully Implemented**. The code in `modules/barangay/routes.py` directly handles additions and edits of attractions and events by barangay representatives, mapping them to templates under `templates/barangay/` and database tables (`ATTRACTION`, `EVENT`, `BARANGAY_INFO`).
2.  **R2 (Central Admin Approval)** is **Fully Implemented**. The core files `modules/admin_core/content.py` and `modules/admin_core/dashboard.py` implement moderation actions for pending items, routing updates back to update status flags (`status = 'approved'`).
3.  **R3 (Central Database & Features)** is **Fully Implemented**. 
    *   Database configuration handles multiple providers (Postgres, SQLite, MySQL) dynamically.
    *   Event Calendar includes both HTML structure and interactive JS date-binding logic.
    *   Visitor Dashboard aggregates metrics from page view trackers and logged physical visits.
    *   *Concept Clarification*: The "dual-marker/brochure" is a design methodology concept referencing the replacement of physical brochures with digital NCCA registry profiles. It does not exist as a map-specific custom code component or UI element.
4.  **R4 (Security, Roles, & Policies)** is **Fully Implemented**. Hashing, RBAC checks inside routes, SQL injection detection on inputs, and database audit logs are actively utilized.

---

## 3. Caveats
*   The system uses implicit role checks inside view functions rather than standard Flask-Principal or Flask-Security extension wrappers. This is lightweight but requires manual inspection across all blueprints to ensure consistency.
*   "Announcements" are handled contextually as newsletters or public event listings rather than a dedicated announcement table.

---

## 4. Conclusion
The system implementation matches all key requirements mapped in the capstone documentation. The features (Contributor portal, Admin moderation, Event calendar, Visitor analytics, Multi-provider database routing) are successfully coded and integrated.

---

## 5. Verification Method

To verify these routes locally:
1.  **Database Connection Routing**: Inspect `utils/db_manager.py` and print the output of `get_database_uri()` to verify local SQLite/MySQL/PostgreSQL fallback.
2.  **Access Control**: Try to access `/admin/documents` using a contributor account or anonymous session. The system will throw a 403 / redirect to the login/index page via the `_require_admin()` hook.
3.  **Interactive Calendar**: Open `templates/pagez/events.html` and verify that `events.js` loads and correctly binds event filtering to calendar clicks.
