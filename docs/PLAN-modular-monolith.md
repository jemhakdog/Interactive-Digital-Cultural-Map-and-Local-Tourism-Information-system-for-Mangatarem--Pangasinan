# PLAN: Modular Monolith Refactoring
**Task Slug:** `modular-monolith`
**Project Type:** BACKEND (Flask/Python Web App)
**Agent:** `backend-specialist`
**Date:** 2026-04-25

---

## Overview

The current codebase is a Flask application that already uses Blueprints and has some logical grouping, but suffers from **cross-cutting concerns** — all models live in one `models.py`, utilities are flat in `utils/`, and there is no enforced boundary between domain areas. This plan reorganizes the codebase into a true **Modular Monolith** where each business domain (module) owns its routes, models, services, and schemas — while sharing infrastructure (extensions, config, app factory) from the root.

The goal is **zero feature changes** — this is a pure structural refactor. The app deploys as one process, one codebase.

---

## Identified Domain Modules

After analyzing the codebase, the natural domain boundaries are:

| Module | Current Files | Owns |
|--------|--------------|------|
| **auth** | `routes/auth.py` | `User`, `PasswordResetToken`, login, registration, password reset |
| **attractions** | `routes/public.py` (partial), `routes/admin/attractions.py`, `routes/barangay/attractions.py` | `Attraction`, `AttractionReview`, `UserFavoriteAttraction` |
| **events** | `routes/admin/events.py`, `routes/barangay/events.py` | `Event`, `UserEventInterest` |
| **heritage** | `routes/admin/heritage.py`, `routes/admin/documents.py`, `heritage_models/` | `HeritageProfile` + 7 sub-form models |
| **business** | `routes/business.py`, `routes/admin/establishments.py` | `Establishment`, `EstablishmentRoom`, `EstablishmentMenuItem`, `EstablishmentReview` |
| **barangay** | `routes/barangay/` | `BarangayInfo` |
| **gallery** | `routes/barangay/gallery.py`, `routes/admin/content.py` | `GalleryItem` |
| **analytics** | `routes/admin/dashboard.py`, `routes/map_routes.py` | `AnalyticsPageView` |
| **notifications** | `routes/admin/newsletter.py` | `NewsletterSubscriber` |
| **core** (shared) | `app.py`, `extensions.py`, `config.py`, `utils/` | Infrastructure only |

---

## Target Directory Structure

```
capstone_system/
│
├── app.py                  # Application factory (unchanged interface)
├── extensions.py           # Shared Flask extensions (db, login_manager, etc.)
├── config.py               # Configuration (unchanged)
│
├── modules/                # ← NEW: All domain modules live here
│   │
│   ├── auth/
│   │   ├── __init__.py     # Blueprint definition
│   │   ├── models.py       # User, PasswordResetToken
│   │   ├── routes.py       # ← MOVE FROM: routes/auth.py
│   │   ├── services.py     # ← EXTRACT: email logic, token logic
│   │   └── validators.py   # ← EXTRACT: auth-specific validators from utils/validators.py
│   │
│   ├── attractions/
│   │   ├── __init__.py
│   │   ├── models.py       # Attraction, AttractionReview, UserFavoriteAttraction
│   │   ├── routes/
│   │   │   ├── public.py   # ← EXTRACT FROM: routes/public.py (attraction sections)
│   │   │   ├── admin.py    # ← MOVE FROM: routes/admin/attractions.py
│   │   │   └── barangay.py # ← MOVE FROM: routes/barangay/attractions.py
│   │   └── services.py     # ← EXTRACT: attraction business logic
│   │
│   ├── events/
│   │   ├── __init__.py
│   │   ├── models.py       # Event, UserEventInterest
│   │   ├── routes/
│   │   │   ├── admin.py    # ← MOVE FROM: routes/admin/events.py
│   │   │   └── barangay.py # ← MOVE FROM: routes/barangay/events.py
│   │   └── services.py
│   │
│   ├── heritage/
│   │   ├── __init__.py
│   │   ├── models/
│   │   │   ├── __init__.py         # HeritageProfile base
│   │   │   ├── natural.py          # ← MOVE FROM: heritage_models/natural_heritage.py
│   │   │   ├── built.py            # ← MOVE FROM: heritage_models/built_heritage.py
│   │   │   ├── movable.py          # ← MOVE FROM: heritage_models/movable_heritage.py
│   │   │   ├── intangible.py       # ← MOVE FROM: heritage_models/intangible_heritage.py
│   │   │   ├── personality.py      # ← MOVE FROM: heritage_models/personality_profile.py
│   │   │   ├── institution.py      # ← MOVE FROM: heritage_models/cultural_institution.py
│   │   │   └── lgu_program.py      # ← MOVE FROM: heritage_models/lgu_culture_program.py
│   │   ├── routes/
│   │   │   ├── admin.py            # ← MERGE FROM: routes/admin/heritage.py + documents.py
│   │   │   └── contributor.py      # ← EXTRACT FROM: routes/public.py (heritage forms)
│   │   └── services.py
│   │
│   ├── business/
│   │   ├── __init__.py
│   │   ├── models.py       # Establishment, Room, MenuItem, Review
│   │   ├── routes/
│   │   │   ├── owner.py    # ← MOVE FROM: routes/business.py
│   │   │   └── admin.py    # ← MOVE FROM: routes/admin/establishments.py
│   │   └── services.py
│   │
│   ├── barangay/
│   │   ├── __init__.py
│   │   ├── models.py       # BarangayInfo
│   │   ├── routes/
│   │   │   ├── dashboard.py # ← MOVE FROM: routes/barangay/dashboard.py
│   │   │   ├── gallery.py   # ← MOVE FROM: routes/barangay/gallery.py
│   │   │   └── profile.py   # ← MOVE FROM: routes/barangay/profile.py
│   │   └── services.py
│   │
│   ├── gallery/
│   │   ├── __init__.py
│   │   ├── models.py       # GalleryItem
│   │   ├── routes/
│   │   │   └── admin.py    # ← MOVE FROM: routes/admin/content.py
│   │   └── services.py
│   │
│   ├── analytics/
│   │   ├── __init__.py
│   │   ├── models.py       # AnalyticsPageView, DatabaseAuditLog
│   │   ├── routes/
│   │   │   ├── admin.py    # ← MOVE FROM: routes/admin/dashboard.py
│   │   │   └── map.py      # ← MOVE FROM: routes/map_routes.py
│   │   └── services.py
│   │
│   └── notifications/
│       ├── __init__.py
│       ├── models.py       # NewsletterSubscriber
│       ├── routes/
│       │   └── admin.py    # ← MOVE FROM: routes/admin/newsletter.py
│       └── services.py     # ← EXTRACT: email_sender logic from utils/email_sender.py
│
├── core/                   # ← NEW: Shared infrastructure utilities
│   ├── __init__.py
│   ├── security.py         # ← MOVE FROM: utils/security.py
│   ├── db_manager.py       # ← MOVE FROM: utils/db_manager.py
│   ├── file_helpers.py     # ← MOVE FROM: utils/file_helpers.py
│   ├── geo.py              # ← MOVE FROM: utils/geo.py
│   ├── logger.py           # ← MOVE FROM: utils/logger_helper.py
│   ├── validators.py       # ← MOVE FROM: utils/validators.py (shared rules only)
│   ├── template_filters.py # ← MOVE FROM: utils/template_filters.py
│   ├── session.py          # ← MOVE FROM: utils/session_helper.py
│   └── tile_generator.py   # ← MOVE FROM: utils/tile_generator.py
│
└── utils/                  # ← KEEP but emptied as alias (backward compat during transition)
    └── __init__.py         # Re-exports from core/ for backward compat
```

---

## Key Rules After Refactoring

> These are the "walls between rooms" — must be enforced via code review or linting.

1. **Modules NEVER import from each other's `models.py` directly** — they reference the shared `db` via `extensions.py`.
2. **Cross-module data access** is done via a module's public `services.py` interface only.
3. **Shared infrastructure** (`extensions`, `config`, `core/`) is the ONLY allowed cross-cutting import.
4. **`models.py` at root level** stays as a **re-export shim** so existing migrations don't break.

---

## Task Breakdown

### Phase 1 — Foundation (No Code Changes, Setup Only)

#### TASK-1.1: Create module directory scaffolding
- **Agent:** `backend-specialist`
- **Input:** Target structure above
- **Output:** All `modules/` and `core/` directories created with empty `__init__.py`
- **Verify:** `ls modules/` shows all 9 module folders

#### TASK-1.2: Create `core/` directory from `utils/`
- **Agent:** `backend-specialist`
- **Input:** `utils/` directory (10 files)
- **Output:** Each `utils/*.py` file copied to `core/*.py` with renamed file as noted above
- **Verify:** All `core/` files exist; old `utils/` still intact
- **Rollback:** Delete `core/`, restore `utils/` imports

---

### Phase 2 — Model Migration (Most Critical)

#### TASK-2.1: Migrate `auth` models
- **Files to Edit:**
  - **CREATE** `modules/auth/models.py`
  - **MOVE** `User`, `PasswordResetToken` classes FROM `models.py` lines 8–63
- **Code to Move:**
  ```python
  # FROM: models.py lines 1-63
  # TO: modules/auth/models.py
  from extensions import db
  from flask_login import UserMixin
  from werkzeug.security import generate_password_hash, check_password_hash
  from datetime import datetime, timedelta
  import secrets
  
  class User(...): ...
  class PasswordResetToken(...): ...
  ```
- **After Move — Edit `models.py`:** Replace moved classes with import shim:
  ```python
  # models.py (shim - keeps migrations working)
  from modules.auth.models import User, PasswordResetToken
  ```
- **Verify:** `from models import User` still works; migrations unaffected

#### TASK-2.2: Migrate `attractions` models
- **Files to Edit:**
  - **CREATE** `modules/attractions/models.py`
  - **MOVE** `Attraction`, `AttractionReview`, `UserFavoriteAttraction` FROM `models.py` lines 103–240
- **After Move — Edit `models.py`:** Add shim:
  ```python
  from modules.attractions.models import Attraction, AttractionReview, UserFavoriteAttraction
  ```
- **Verify:** `from models import Attraction` still works

#### TASK-2.3: Migrate `events` models
- **MOVE** `Event`, `UserEventInterest` FROM `models.py` lines 142–229
- **CREATE** `modules/events/models.py`
- **Edit `models.py`:** Add shim

#### TASK-2.4: Migrate `business` models
- **MOVE** `Establishment`, `EstablishmentRoom`, `EstablishmentMenuItem`, `EstablishmentReview` FROM `models.py` lines 256–333
- **CREATE** `modules/business/models.py`
- **Edit `models.py`:** Add shim

#### TASK-2.5: Migrate `barangay` model
- **MOVE** `BarangayInfo` FROM `models.py` lines 175–198
- **CREATE** `modules/barangay/models.py`
- **Edit `models.py`:** Add shim
- **⚠️ WARNING:** `BarangayInfo` is referenced by FKs in almost EVERY other model. The shim in `models.py` is critical here.

#### TASK-2.6: Migrate `analytics` models
- **MOVE** `AnalyticsPageView`, `DatabaseAuditLog` FROM `models.py` lines 201–370
- **CREATE** `modules/analytics/models.py`
- **Edit `models.py`:** Add shim

#### TASK-2.7: Migrate `gallery`, `notifications` models
- **MOVE** `GalleryItem` → `modules/gallery/models.py`
- **MOVE** `NewsletterSubscriber` → `modules/notifications/models.py`
- **Edit `models.py`:** Add shims

#### TASK-2.8: Migrate `heritage` models
- **MOVE** entire `heritage_models/` → `modules/heritage/models/`
- **Rename files** per target structure
- **MOVE** `HeritageProfile` FROM `models.py` lines 66–100 → `modules/heritage/models/__init__.py`
- **Edit `models.py`:** Add shim:
  ```python
  from modules.heritage.models import HeritageProfile
  from modules.heritage.models.natural import NaturalHeritage
  # ... etc
  ```
- **Verify:** All existing imports of heritage models still work

---

### Phase 3 — Route Migration

#### TASK-3.1: Migrate `auth` routes
- **MOVE** `routes/auth.py` → `modules/auth/routes.py`
- **Edit Blueprint name:** No change needed (already `auth_bp`)
- **Edit `routes/__init__.py`:**
  ```python
  # BEFORE:
  from .auth import auth_bp
  # AFTER:
  from modules.auth.routes import auth_bp
  ```

#### TASK-3.2: Migrate `attractions` routes
- **MOVE** `routes/admin/attractions.py` → `modules/attractions/routes/admin.py`
- **MOVE** `routes/barangay/attractions.py` → `modules/attractions/routes/barangay.py`
- **EXTRACT** attraction-related handlers FROM `routes/public.py` → `modules/attractions/routes/public.py`
- **Edit `routes/__init__.py`:** Update imports

#### TASK-3.3: Migrate `events` routes
- **MOVE** `routes/admin/events.py` → `modules/events/routes/admin.py`
- **MOVE** `routes/barangay/events.py` → `modules/events/routes/barangay.py`

#### TASK-3.4: Migrate `heritage` routes
- **MOVE** `routes/admin/heritage.py` → `modules/heritage/routes/admin.py`
- **MOVE** `routes/admin/documents.py` → merge into `modules/heritage/routes/admin.py`

#### TASK-3.5: Migrate `business` routes
- **MOVE** `routes/business.py` → `modules/business/routes/owner.py`
- **MOVE** `routes/admin/establishments.py` → `modules/business/routes/admin.py`

#### TASK-3.6: Migrate `barangay` routes
- **MOVE** `routes/barangay/*.py` → `modules/barangay/routes/`

#### TASK-3.7: Migrate `gallery`, `analytics`, `notifications` routes
- **MOVE** `routes/admin/content.py` → `modules/gallery/routes/admin.py`
- **MOVE** `routes/admin/dashboard.py` → `modules/analytics/routes/admin.py`
- **MOVE** `routes/map_routes.py` → `modules/analytics/routes/map.py`
- **MOVE** `routes/admin/newsletter.py` → `modules/notifications/routes/admin.py`

---

### Phase 4 — Service Extraction (Value-Add Step)

> This phase extracts business logic currently embedded in route handlers into dedicated `services.py` per module. This is optional but highly recommended for clean module isolation.

#### TASK-4.1: Extract `auth` services
- **Extract FROM** `modules/auth/routes.py`:
  - Token generation/validation logic → `modules/auth/services.py`
  - Email sending calls → `modules/auth/services.py` (wraps `core/email_sender.py`)

#### TASK-4.2: Extract `attractions` services
- **Extract FROM** route handlers: search/filter logic, status update logic → `modules/attractions/services.py`

#### TASK-4.3: Extract remaining module services
- Same pattern for `events`, `heritage`, `business`, `barangay`

---

### Phase 5 — Wiring & Cleanup

#### TASK-5.1: Update `app.py` blueprint registration
- **Edit `app.py`** — the `register_blueprints` call stays the same but `routes/__init__.py` now imports from `modules/`:
  ```python
  # routes/__init__.py (updated)
  def register_blueprints(app):
      from modules.auth.routes import auth_bp
      from modules.attractions.routes.public import attractions_public_bp
      from modules.attractions.routes.admin import attractions_admin_bp
      # ... etc
  ```

#### TASK-5.2: Update `utils/` to re-export from `core/`
- **Edit `utils/__init__.py`** to re-export all symbols from `core/` for backward compat:
  ```python
  # utils/__init__.py — backward compat shim
  from core.security import *
  from core.db_manager import *
  # ... etc
  ```

#### TASK-5.3: Update `models.py` shim — final cleanup
- Ensure `models.py` is now **100% shim imports** (no class definitions)
- All existing migration files reference `models.py` — this keeps Flask-Migrate working

#### TASK-5.4: Delete old route files
- After confirming all blueprints are re-registered via `modules/`:
  - Delete `routes/auth.py`, `routes/business.py`, `routes/map_routes.py`, `routes/update.py`, `routes/user.py`
  - Delete `routes/admin/attractions.py`, `routes/admin/events.py`, etc.
  - Delete `heritage_models/` directory
  - Delete `utils/*.py` (after shim is in place)

---

## File-by-File Change Summary

| File | Action | What Changes |
|------|--------|-------------|
| `models.py` | EDIT (becomes shim) | Remove all class definitions, replace with `from modules.X.models import ...` |
| `app.py` | NO CHANGE | Interface stays the same |
| `extensions.py` | NO CHANGE | Still shared infrastructure |
| `config.py` | NO CHANGE | Still shared infrastructure |
| `routes/__init__.py` | EDIT | Update all imports to point at `modules/` |
| `routes/auth.py` | MOVE → `modules/auth/routes.py` | Path change only |
| `routes/business.py` | MOVE → `modules/business/routes/owner.py` | Path change only |
| `routes/map_routes.py` | MOVE → `modules/analytics/routes/map.py` | Path change only |
| `routes/admin/attractions.py` | MOVE → `modules/attractions/routes/admin.py` | Path change only |
| `routes/admin/events.py` | MOVE → `modules/events/routes/admin.py` | Path change only |
| `routes/admin/heritage.py` | MOVE → `modules/heritage/routes/admin.py` | Path change only |
| `routes/admin/documents.py` | MERGE → `modules/heritage/routes/admin.py` | Merge into heritage admin |
| `routes/admin/establishments.py` | MOVE → `modules/business/routes/admin.py` | Path change only |
| `routes/admin/dashboard.py` | MOVE → `modules/analytics/routes/admin.py` | Path change only |
| `routes/admin/content.py` | MOVE → `modules/gallery/routes/admin.py` | Path change only |
| `routes/admin/newsletter.py` | MOVE → `modules/notifications/routes/admin.py` | Path change only |
| `routes/barangay/attractions.py` | MOVE → `modules/attractions/routes/barangay.py` | Path change only |
| `routes/barangay/events.py` | MOVE → `modules/events/routes/barangay.py` | Path change only |
| `routes/barangay/gallery.py` | MOVE → `modules/gallery/routes/barangay.py` | Path change only |
| `routes/barangay/dashboard.py` | MOVE → `modules/barangay/routes/dashboard.py` | Path change only |
| `routes/barangay/profile.py` | MOVE → `modules/barangay/routes/profile.py` | Path change only |
| `heritage_models/*.py` | MOVE → `modules/heritage/models/*.py` | Path + rename |
| `utils/security.py` | MOVE → `core/security.py` | Path change only |
| `utils/db_manager.py` | MOVE → `core/db_manager.py` | Path change only |
| `utils/email_sender.py` | MOVE → `core/email_sender.py` | Path change only |
| `utils/file_helpers.py` | MOVE → `core/file_helpers.py` | Path change only |
| `utils/geo.py` | MOVE → `core/geo.py` | Path change only |
| `utils/logger_helper.py` | MOVE → `core/logger.py` | Path + rename |
| `utils/validators.py` | MOVE → `core/validators.py` | Path change only |
| `utils/template_filters.py` | MOVE → `core/template_filters.py` | Path change only |
| `utils/session_helper.py` | MOVE → `core/session.py` | Path + rename |
| `utils/tile_generator.py` | MOVE → `core/tile_generator.py` | Path change only |

---

## Critical Gotchas & Risks

> [!WARNING]
> **BarangayInfo is a cross-cutting FK.** Every model references it. NEVER import `BarangayInfo` from another module's `models.py`. Always use the shim via `models.py` or directly via `modules.barangay.models`.

> [!WARNING]
> **Flask-Migrate / Alembic.** The migration files in `migrations/` reference `models.py` tablenames (strings like `'ATTRACTION'`). Since we use `__tablename__` strings (not Python class paths), migrations will NOT break as long as `models.py` re-exports all models. Do NOT change `__tablename__` values.

> [!WARNING]
> **Blueprint URL prefixes.** When moving routes, the Blueprint's `url_prefix` and `name` must remain identical to what was registered before. Only the Python import path changes.

> [!CAUTION]
> **Circular imports.** When module A's `services.py` calls module B's `services.py`, this must go through the shared `core/` layer or use Flask's `current_app` proxy. Never do direct cross-module model imports.

> [!NOTE]
> **Do Phase 2 (Models) BEFORE Phase 3 (Routes).** Routes import models. If models aren't in their new location first, route migration will fail on import.

---

## Execution Order (Dependency Graph)

```
TASK-1.1 (scaffold dirs)
    └── TASK-1.2 (core/ from utils/)
            └── TASK-2.x (model migrations, in order: auth → barangay → rest)
                    └── TASK-3.x (route migrations)
                            └── TASK-4.x (service extraction) [optional]
                                    └── TASK-5.x (wiring & cleanup)
```

---

## Success Criteria

- [ ] App starts with `python app.py` without import errors
- [ ] All existing routes respond correctly (no 404/500 regressions)
- [ ] `from models import User` still works (shim intact)
- [ ] Flask-Migrate `flask db migrate` produces empty migration (schema unchanged)
- [ ] Each module folder is self-contained: models + routes + services
- [ ] No module imports directly from another module's `models.py`

---

## Verification Plan

### Automated
```powershell
# 1. Start the app
python app.py

# 2. Run existing tests
python -m pytest tests/ -v

# 3. Security scan
python .agent/skills/vulnerability-scanner/scripts/security_scan.py .

# 4. Check for circular imports
python -c "from app import create_app; app = create_app(); print('OK')"
```

### Manual
- [ ] Browse all major pages: `/`, `/map`, `/admin`, `/auth/login`, `/business`
- [ ] Submit a heritage form → verify it saves to DB
- [ ] Log in as admin, approve an attraction → verify status changes
- [ ] Confirm Flask-Migrate shows no schema changes after refactor

---

## Phase X: Final Verification Checklist

- [ ] Lint: `ruff check .` passes
- [ ] No purple/violet hex codes in templates
- [ ] Socratic Gate was respected
- [ ] All tasks marked `[x]`
- [ ] `flask db migrate` produces no schema changes
- [ ] All tests pass

---

*Plan created by `project-planner` agent | 2026-04-25*
