# Active Context

## Current focus

- Seeded business profile for test_owner; fixed dashboard 422 bug (per_page=200 → 100).
- Previous: all cleanup, bug fixes, and CRUD verification complete. Ready for commit.

## Recent changes (2026-07-29)

### Ponytail Audit & Cleanup
- Performed full-repo over-engineering audit using ponytail-audit skill.
- Deleted 142 throwaway scripts in `scratch/` (6,829 lines).
- Deleted `db_update_package/` (5 dead migration files).
- Deleted unreferenced JS bundles: `bundle.min.js` (40KB), `map.min.js` (13KB), `leaflet.js` (148KB), `animations*.js`.
- Deleted old vendor library: `static/vendor/leaflet-1.7.1/` (284KB).
- Consolidated 6 duplicate `core/` modules into `utils/` (security, email_sender, validators, template_filters, file_helpers, tile_generator).
- Fixed imports in `modules/auth/register.py` and `modules/auth/password.py` to use `utils/` instead of `core/`.
- Updated `templates/pagez/map_v2.html` to use `vendor/leaflet/leaflet.js`.
- **Net: 156 files changed, -12,540 lines removed.**

### Bug Fixes
- Fixed admin attraction form action pointing to list page instead of add endpoint.
- Created missing `errors/500.html` template to prevent server crashes on unhandled exceptions.
- Lowered PWA install prompt z-index from 9999 to 100 to stop covering form submit buttons.
- Added edit modal with full form to Business Owner menu items (previously missing edit UI).

### CRUD Verification (All User Roles)
- **Admin** (9 nav items): Full CRUD on Landmarks and Events, read-only on Analytics, Reviews, Newsletters, Businesses, Verify Merchants, Reservations.
- **Business Owner** (6 nav items): Create/Update establishment, Create menu items (now with edit), Read-only on Visitor Registry, Reviews, Reservations.
- **Barangay Rep** (7 nav items): Full CRUD on Landmarks and Events, Update Barangay Profile, Read-only on Gallery, Reviews, Reservations.
- **Tourist** (10 nav items): Read-only across Dashboard, Passport, Map, Barangays, Events, Gallery, Stay & Eat, Routes.

## Recent changes (2026-07-31)

### Map V2 Mobile Touch Fixes
- Removed `touch-action: none` from `.bottom-sheet` and added `touch-action: pan-y` to `#results-section` so the landmark list scrolls by finger.
- Refined the results-list touchstart handler to only hijack the gesture when the sheet is not already fully open.
- Bumped SW cache to `gomangatarem-v10` and static query version to `map_v2.js?v=1.1.9` so mobile browsers load the corrected files immediately.
- Added PWA install HUD mobile layout adjustment (`bottom: 260px`) so it no longer overlaps the sheet handle.

### Ponytail Audit Batch Cleanup
- Deleted dead files: `archive/`, `code_screenshots/`, `.antigravitycli/`, `tmp/verify_newsletter.py`, `instance/heritage_page.html`, `data/scraped_attractions.json`, `data/scraped_heritage.json`, `build/desktop.py`.
- Deleted duplicate `core/` shims: `core/db_manager.py`, `core/geo.py`, `core/logger.py`, `core/session.py`, `utils/session_helper.py`.
- Updated active imports from `core.logger` → `utils.logger_helper` and `core.geo` → `utils.geo` across 8 modules.
- Removed unused validators: `validate_json_input()` and `validate_coordinates_fields()` from `utils/validators.py` (~110 lines).
- Removed dead `DatabaseAuditLog` model from `modules/analytics/models.py`.
- Preserved `data/scraped_events.json` (live) and skipped riskier refactors: auth module merge, seed consolidation, `.kilo/worktrees/`, backward-compat model aliases.

## Recent changes (2026-08-19)

### Visions of Mangatarem Multimedia Gallery Redesign
- Redesigned and modernized `/gallery` in Next.js with the "Visions of Mangatarem" visual archive system.
- Implemented rich Hero section with cultural badges, metric highlights, and quick actions.
- Added interactive control bar with category pills (Landscapes & Nature, Historical & Heritage, Agro-Tourism & Farms, Festivals & Celebrations, Flavors & Local Life), live search, barangay dropdown, sorting, and view mode switcher (Masonry, Grid, Editorial).
- Built full-screen cinematic Lightbox with keyboard arrow navigation, like/appreciation counter, copy share link, open high-res image, and bottom filmstrip thumbnail ribbon.
- Added community media contribution modal for locals and visitors to submit photo/video stories.
- Updated `backend/app/api/gallery.py` with expanded serialization and submission support.
- Verified with Playwright test suite (16/16 public page tests passing).