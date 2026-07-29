# Active Context

## Current focus

- All cleanup, bug fixes, and CRUD verification complete. Ready for commit.

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

## Next step

- Commit all changes to main branch.