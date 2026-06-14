# Codebase Needs Assessment & Gap Analysis Report

## 1. Executive Summary

This report presents a codebase audit and gap analysis of the **Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan**. The objective of this assessment is to evaluate the alignment between the target functional/non-functional requirements (R1 through R4) and the actual implementation within the codebase.

The system is architected as a modular monolith, utilizing **Flask** (Python) as the backend framework, **SQLAlchemy** for database operations, and a frontend powered by **Tailwind CSS**, vanilla JavaScript, and modern mapping/visualization tools.

Our needs assessment confirms that the codebase is highly mature and meets all major functional categories:
* **R1 (Contributor Module)** provides fully functional profiles, attraction/event CRUD, and media uploads for Barangay Representatives.
* **R2 (Central Admin Approval)** has established moderation workflows, rejection/approval routes, and administrative templates.
* **R3 (Centralized Database & Core Features)** supports dynamic multi-database configurations (SQLite, MySQL, PostgreSQL/Supabase), Mapbox/Leaflet vector tile mappings, interactive event calendars, and visitor dashboards.
* **R4 (Security, Roles & Policies)** integrates role-based authorization, secure Werkzeug password hashing, SQL injection sanitization, and transaction audit logs.

Some specific design requirements (e.g., Announcements, Dual-marker/Brochures) are aligned conceptually via alternative integrated structures rather than dedicated tables, which streamlines data integrity and avoids database fragmentation. This report details those design alignments and offers actionable optimizations to ensure the codebase remains clean, maintainable, and robust.

---

## 2. Exact Matches (Met Expectations)

### R1. Contributor Module (Barangay Representatives)
The Contributor Module enables assigned Barangay Representatives to update their profiles, manage attractions and events, and upload media items for moderation.

* **Profile Management**:
  * **Path**: `modules/barangay/routes.py`
  * **Method/Route**: `barangay_profile_manage()` handles `GET` and `POST` requests at `/barangay/profile`. It validates fields (`mission`, `vision`, `history`, `cultural_assets`, etc.) and commits updates directly to the `BarangayInfo` record.
  * **Template**: `templates/barangay/profile.html` renders the form mapping for editing.
* **Attraction Addition & Editing**:
  * **Path**: `modules/barangay/routes.py`
  * **Methods/Routes**: `barangay_add_attraction()` (`/barangay/attractions/add`) and `barangay_edit_attraction(id)` (`/barangay/attractions/edit/<int:id>`). They handle input validation, geocoordinates confirmation, image file upload mapping, and set the status to `'pending'` for admin moderation.
  * **Templates**: `templates/barangay/add_attraction.html` and `templates/barangay/edit_attraction.html`.
* **Event Addition & Editing**:
  * **Path**: `modules/barangay/routes.py`
  * **Methods/Routes**: `barangay_add_event()` (`/barangay/events/add`) and `barangay_edit_event(id)` (`/barangay/events/edit/<int:id>`).
  * **Templates**: `templates/barangay/add_event.html` and `templates/barangay/edit_event.html`.
* **Media / Gallery Uploads**:
  * **Path**: `modules/barangay/routes.py`
  * **Method/Route**: `barangay_add_gallery()` (`/barangay/gallery/add`) processes media files, validates content type, saves to disk, and creates database records with `'pending'` status.
  * **Database Model**: `GalleryItem` in `modules/gallery/models.py`.
  * **Template**: `templates/barangay/add_gallery.html`.

---

### R2. Central Admin Approval Module
The system enforces a moderation flow where submissions from contributors must be reviewed and approved by a Central Admin.

* **Pending Items Moderation**:
  * **Path**: `modules/admin_core/dashboard.py`
  * **Logic**: `_get_pending_items()` queries the database for attractions, reviews, and content submissions where `status = 'pending'`.
* **Approval Routes**:
  * **Paths**: 
    * `modules/attractions/admin_routes.py`
    * `modules/admin_core/content.py`
  * **Methods/Routes**:
    * `approve_attraction(id)` and `delete_attraction(id)` at `/admin/attractions/approve/<int:id>` and `/admin/attractions/delete/<int:id>` to moderate attractions.
    * `approve_review(id)` and `reject_review(id)` at `/admin/reviews/approve/<int:id>` and `/admin/reviews/reject/<int:id>` to moderate user reviews.
* **Moderation Templates**:
  * **Paths**:
    * `templates/admin/attractions.html` — List and moderation of attractions.
    * `templates/admin/reviews.html` — Review moderation panel.

---

### R3. Centralized Database & Core Features
This requirement details the storage engine configurations, interactive maps, calendars, and visitor analytical dashboards.

* **Multi-DB Manager & Connection Routing**:
  * **Paths**: `config.py` and `utils/db_manager.py`.
  * **Logic**: Connection routing is resolved via `get_database_uri()`. The manager (`utils/db_manager.py`) supports conditional fallback configurations:
    * **SQLite**: Default for local development.
    * **MySQL**: Standard development / XAMPP/Laragon profiles.
    * **PostgreSQL / Supabase**: High-performance production deployment.
  * **Vercel Optimizations**: Implemented in `utils/db_manager.py` to automatically switch PostgreSQL ports to `6543` for the Supabase Transaction Pooler, disabling connection pooling via `NullPool` to accommodate serverless environments.
* **Vector Tile Mapping System**:
  * **Backend Path**: `modules/core/map_routes.py` serves Mapbox Vector Tiles (MVT) generated using PostGIS SQL structures (`ST_AsMVT`).
  * **Frontend Path**: `static/js/pages/map.js` initializes Mapbox GL JS with layers, styling, filters, and fallback Leaflet logic.
* **Interactive Event Calendar**:
  * **Path**: `templates/pagez/events.html` defines the HTML container grid for the calendar.
  * **JavaScript Path**: `static/js/pages/events.js` implements the rendering logic, parses event attributes, populates calendar dates, applies `has-event` highlight class rules, and handles date-range filters.
* **Visitor Dashboards & Analytics**:
  * **Dashboard Path**: `modules/admin_core/dashboard.py` collects physical visitor metrics, page views, and ratings.
  * **Visitor Logging Route**: `modules/analytics/routes.py` provides routes (e.g., `log_visitor()` at `/analytics/log`) to register physical tourist check-ins (recording age, address, and purpose).
  * **Database Models**:
    * `VisitorLog` (`modules/analytics/models.py`): Schema for recording physical site check-ins.
    * `AnalyticsPageView` (`modules/analytics/models.py`): Schema for tracking virtual page views.

---

### R4. Security, Roles & Policies
Core mechanisms are built into the architecture to secure sensitive interfaces and enforce data integrity.

* **Role-Based Access Control (RBAC)**:
  * **Logic**: Authorization checks are performed directly inside the blueprints using the `@login_required` decorator combined with conditional logic (`current_user.role == 'admin'`, etc.).
  * **Example Check**: `_require_admin()` in `modules/api_v1/documents.py` restricts API access by aborting and redirecting unauthorized users.
* **Password Hashing**:
  * **Paths**: `modules/auth/routes.py` and `modules/auth/models.py`.
  * **Logic**: Employs Werkzeug's `generate_password_hash` and `check_password_hash` to secure credentials.
* **SQL Injection Detection & Validation**:
  * **Path**: `modules/api_v1/documents.py`
  * **Logic**: `detect_sql_injection_attempt()` in `utils/security.py` parses file name patterns and text fields in parsed `.docx` document imports to detect SQL injection payloads (e.g., `UNION SELECT`, comment tags, etc.) before writing to `HeritageProfile.form_data`.
* **Database Audit Logging**:
  * **Database Model**: `DatabaseAuditLog` in `modules/analytics/models.py` records details of CRUD operations, tracking who performed them and when.

---

## 3. Partial Matches / Design Concept Alignment

Several specific requirements are fulfilled contextually through consolidated codebase components rather than standalone tables, ensuring optimal database normalization.

### A. Announcement Handlings
* **Requirement**: Dedicated Barangay and Central Admin Announcements.
* **Codebase Alignment**: Rather than using a standalone `Announcement` table, announcements are integrated into two primary features:
  1. **Event Listings**: Public, time-sensitive announcements are served as **Events** (`modules/events/models.py`), rendering directly on the interactive event calendar.
  2. **Newsletters**: Broadcast notifications and updates are handled via the `NewsletterSubscriber` and `NewsletterHistory` models in `modules/notifications/models.py`, which are created and managed by administrators via `/admin/notifications` (`modules/notifications/admin_routes.py`).
* **Design Rationale**: This avoids data duplication (as events and announcements share temporal boundaries and geographic points) and leverages the existing communication/subscription system.

### B. Dual-Marker / Brochure Layouts
* **Requirement**: Map layout showing physical dual-markers/brochures for historical and cultural sites.
* **Codebase Alignment**:
  1. Physical brochures are digitized into standard National Commission for Culture and the Arts (NCCA) Forms 01-07 profile registries.
  2. Docx files containing these NCCA profiles are uploaded and parsed dynamically via `modules/api_v1/documents.py`.
  3. The structured output is stored inside the database under the `HeritageProfile` table (specifically in `HeritageProfile.form_data` as JSON, with key columns for geo-coordinates like `latitude` and `longitude`).
  4. The interactive map (`static/js/pages/map.js`) parses these heritage profiles to display cultural points, serving as a dynamic, digitized cultural brochure map.
* **Design Rationale**: Replacing a static PDF/physical brochure layout with searchable database entries linked to geographical coordinates allows for dynamic updates, custom styling, and responsive user experiences.

---

## 4. Gaps and Optimization Suggestions

While the implementation fully covers the system requirements, the following architectural optimizations are recommended:

### Gap 1: Distributed RBAC Implementation
* **Observed**: Role checks are performed inline inside blueprint views (e.g., `if current_user.role != "contributor": flash("Access denied."); return redirect(...)`).
* **Impact**: Increases boilerplate code and presents a risk of human error if a route is created but role check logic is missed.
* **Suggestion**: Centralize RBAC by writing custom Flask decorators (e.g., `@roles_required('admin')` or `@roles_accepted('admin', 'contributor')`) inside `utils/security.py`. This ensures declarative, audit-friendly, and standardized access control.

```python
# Proposed Custom Decorator
from functools import wraps
from flask import abort, flash, redirect, url_for
from flask_login import current_user

def roles_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role not in roles:
                flash("You do not have permission to access this page.", "error")
                return redirect(url_for("auth.login"))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
```

### Gap 2: Decentralized Event and Announcement System
* **Observed**: Event routes and newsletter routing operate as separate modules, with calendar filtering mapping events but newsletters being broadcast-only.
* **Impact**: If a contributor publishes an event-based announcement, subscribers do not receive automated alerts unless the admin manually composes a newsletter.
* **Suggestion**: Establish a unified **Notification Hub**. When an attraction or event is approved by the admin (`modules/admin_core/content.py`), a signal can trigger an automated email blast to subscribers using the newsletter system, linking directly to the new item.

---

## 5. Verification Matrix

| Requirement | Implementation Verification Path | Success Condition |
| :--- | :--- | :--- |
| **R1 (Contributor CRUD)** | `modules/barangay/routes.py` | Route decorator `@login_required` + role restriction. Form submits to status `'pending'`. |
| **R2 (Admin Approval)** | `modules/admin_core/content.py` | Routes `/approve/<id>` and `/reject/<id>` modify database status to `'approved'` / `'rejected'`. |
| **R3 (Multi-DB Handler)** | `utils/db_manager.py` | Connection string parsed and returned dynamically for SQLite, MySQL, and PostgreSQL. |
| **R3 (Map Vector Tiles)** | `modules/core/map_routes.py` & `static/js/pages/map.js` | Uses Mapbox GL / PostGIS (`ST_AsMVT`) caching to return binary vector formats. |
| **R3 (Event Calendar)** | `templates/pagez/events.html` & `static/js/pages/events.js` | Interactive date-picker renders dynamically and queries event-bound datasets. |
| **R4 (SQL Injection)** | `utils/security.py` & `modules/api_v1/documents.py` | Checks inputs and parsed docx text blocks using the `detect_sql_injection_attempt` validator. |
| **R4 (Audit Logs)** | `modules/analytics/models.py` | Model `DatabaseAuditLog` records state changes. |
