# Handoff

- Last touched: 2026-07-31
- Last model: Pi Coding Agent (Claude)
- Branch: main
- Status: Ponytail batch cleanup and Map V2 mobile fixes completed

## Current task
Ready for commit. All cleanup, bug fixes, Map V2 mobile fixes, and ponytail batch cleanup complete.

## Last concrete action
Performed comprehensive ponytail audit, cleanup, bug fixes, and CRUD verification:

### Ponytail Audit & Cleanup (156 files changed, -12,540 lines)
- Deleted `scratch/` (142 throwaway scripts, 6,829 lines)
- Deleted `db_update_package/` (5 dead migration files)
- Deleted unreferenced JS: `bundle.min.js`, `map.min.js`, `leaflet.js`, `animations*.js`
- Deleted old vendor lib: `static/vendor/leaflet-1.7.1/`
- Deleted 6 duplicate `core/` modules (security, email, validators, template_filters, file_helpers, tile_generator)
- Consolidated imports: `modules/auth/register.py` and `modules/auth/password.py` now use `utils/` instead of `core/`
- Updated `templates/pagez/map_v2.html` to use `vendor/leaflet/leaflet.js`

### Bug Fixes (6 issues)
1. **Admin attraction form action**: Fixed wrong action pointing to list page instead of add endpoint (`templates/admin/add_attraction.html`)
2. **Missing `errors/500.html`**: Created error template based on existing pattern (`templates/errors/500.html`)
3. **PWA z-index**: Lowered from 9999 to 100 to stop covering form submit buttons (`static/js/components/pwa-features.js`)
4. **Business Owner menu edit**: Added edit modal with full form to each menu card (`templates/business/manage_menu.html`)
5. Verified tourist pages work correctly (redirect issue was bad test user with empty role)
6. Verified event form date field is correct HTML `<input type='date'>` (was browser automation filling wrong fields)

### CRUD Verification Across All User Roles
- **Admin** (9 nav items): Full CRUD on Landmarks and Events, read-only on Analytics, Reviews, Newsletters, Businesses, Verify Merchants, Reservations
- **Business Owner** (6 nav items): Create/Update establishment, Create menu items, Read-only on Visitor Registry, Reviews, Reservations
- **Barangay Rep** (7 nav items): Full CRUD on Landmarks and Events, Update Barangay Profile, Read-only on Gallery, Reviews, Reservations
- **Tourist** (10 nav items): Read-only across Dashboard, Passport, Map, Barangays, Events, Gallery, Stay & Eat, Routes

## Last concrete action

### Business dashboard profile seeded + 422 bug fixed (2026-08-23)
- Added `Mangatarem Bangus Grill` (restaurant, `approved`, moderate) for `test_owner` (user id 2) directly in `instance/mangatarem.db` — establishment id 10. test_owner previously had no establishment, so the dashboard showed only the onboarding modal.
- Fixed `?per_page=200` → 422 bug: FastAPI `GET /api/business` caps `per_page` at 100, so all 4 frontend call sites got a hard 422 and no owner's establishment ever appeared on the dashboard. Changed to `per_page=100` in `frontend/src/app/business/dashboard/page.tsx` (x2), `frontend/src/app/business/[id]/edit/page.tsx`, `frontend/src/components/business/business-sidebar.tsx`.
- Verified end-to-end in browser: login test_owner@example.com / password123 → `/business/dashboard` renders the full profile. All three dashboard API calls (list, rooms/list, menu/list) return 200. Public `/api/business/10` returns 200.

### Ponytail Batch Cleanup (2026-07-31)
- Deleted dead tracked artifacts: `archive/`, `code_screenshots/`, `.antigravitycli/`, `tmp/verify_newsletter.py`, `instance/heritage_page.html`, `data/scraped_attractions.json`, `data/scraped_heritage.json`, `build/desktop.py`.
- Deleted duplicate shims: `core/db_manager.py`, `core/geo.py`, `core/logger.py`, `core/session.py`, `utils/session_helper.py`.
- Updated active imports from `core.logger` → `utils.logger_helper` and `core.geo` → `utils.geo` across 8 modules.
- Removed unused validators `validate_json_input()` and `validate_coordinates_fields()` (~110 lines) from `utils/validators.py`.
- Removed unused `DatabaseAuditLog` model from `modules/analytics/models.py`.
- Preserved live `data/scraped_events.json` and deferred higher-risk refactors.

### Map V2 Mobile Touch Fixes (2026-07-31)
Fixed Map V2 mobile touch issues and updated service-worker caching for immediate delivery:
- Removed `touch-action: none` from the bottom sheet so the results list scrolls on mobile.
- Added `touch-action: pan-y` to `#results-section` and refined the gesture-routing logic so swipes scroll the list when the sheet is fully open.
- Bumped SW cache to `gomangatarem-v10` and static version to `map_v2.js?v=1.1.9` so the fixed assets replace stale cached files immediately.
- Confirmed temporary Cloudflare Tunnel is sufficient for mobile testing without a named domain.

Prior session completed a comprehensive ponytail audit, cleanup, bug fixes, and CRUD verification:

## Next concrete step
Commit all changes to main branch.

## Files touched this session
- `templates/pagez/map_v2.html` (leaflet path fix, map_v2.js query version bump)
- `static/js/pages/map_v2.js` (sheet-drag gesture refinement)
- `static/sw.js` (service-worker cache bump to v10)
- `templates/admin/add_attraction.html` (form action fix)
- `templates/errors/500.html` (new file)
- `static/js/components/pwa-features.js` (z-index fix)
- `templates/business/manage_menu.html` (edit modal added)
- `modules/auth/register.py` (import fix)
- `modules/auth/password.py` (import fix)
- `modules/api_v1/public.py` (geo import fix)
- `modules/attractions/routes.py` (geo import fix)
- `modules/auth/login.py` (logger import fix)
- `modules/auth/oauth.py` (logger import fix)
- `modules/business/routes.py` (logger import fix)
- `modules/gallery/routes.py` (logger import fix)
- `modules/heritage/routes.py` (logger import fix)
- `utils/validators.py` (removed dead validators)
- `modules/analytics/models.py` (removed dead model)
- `memory-bank/handoff.md`
- `memory-bank/activeContext.md`
- `memory-bank/progress.md`

## Open questions / blockers
- None.
