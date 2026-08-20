# Backend Port Report — Missing FastAPI Endpoints

**Workflow:** `build_missing_fastapi_endpoints` (run `build-missing-fastapi-endpoints-mt1luuoc-ifv5xk`)
**Status:** Completed manually after the `be-admin-mod` agent hung post-write (its file was already fully written). Wire (`main.py`) + verify were finished directly.

## Result
- **App imports cleanly** (`from backend.app.main import app` → OK; `/health` → 200, `/` → 200).
- **95 API routes registered**, including all endpoints the ported React placeholder pages depend on.
- **0 import/registration errors.**

## Endpoints added (verified in OpenAPI schema)

### New routers (mounted in `main.py`)
| Prefix | Router file | Endpoints |
|---|---|---|
| `/api/contributor` | `api/contributor.py` | `stats`, `activity`, `attractions` (list/create), `attractions/{id}` (put/delete), `events` (list/create), `events/{id}`, `gallery` (list/create), `gallery/{id}`, `announcements` (list/create), `announcements/{id}`, `profile` (get/put), `reviews`, `reviews/{id}/reply` |
| `/api/user` | `api/user.py` | `profile` (get/put), `stats`, `favorites` (list), `favorites/{attraction_id}` (post/delete), `visits` |
| `/api/documents` | `api/admin_documents.py` | list/create/get/put/delete |
| `/api/newsletter` | `api/admin_newsletter.py` | `subscribers`, `send`, `history` |
| `/api` (visitors) | `api/admin_visitors.py` | `visitor-registry`, `visits` |

### Extended existing routers
- `api/public.py`: `GET /api/barangays`, `GET /api/barangays/{name}`, `GET /api/announcements`
- `api/admin.py`: `reviews` (+`/{id}/moderate`), `merchants/pending`, `merchants/{id}/verify`, `establishments` (+`/{id}/moderate`), `users/pending`, `users/{id}/approve`, `users/{id}/reject`
- `api/business.py`: `POST /verification`, `GET /{id}/reviews`
- `api/booking.py`: `GET /admin/list`

### Shared foundation (one agent)
- `core/dependencies.py`: added `require_roles(*roles)`, `require_contributor`, `require_business_owner`.
- `schemas/`: added `announcements`, `barangay`, `verification`, `document`, `newsletter`, `visitor`, `user`, `contributor`, `moderation`.
- `models/`: added `document.py` (Document) + registered in `models/__init__.py`.

## Caveats (runtime, not build)
- **No live DB / no migrations run.** `init_db()` uses `create_all`, which creates new tables but will NOT alter existing tables. Any model column added to an existing table needs an Alembic migration or a DB recreate before that endpoint works at runtime.
- Runtime data correctness (query logic, relationship joins, response shapes vs what the UI renders) is **not** exercised here — there is no running database. Import + route registration only are verified.
- The smoke test required `SECRET_KEY` in the environment (not present in `.env`); the dev server supplies it via shell env. This is a config prerequisite, not a code defect.

## Files changed (working tree, uncommitted)
New: `api/contributor.py`, `api/user.py`, `api/admin_documents.py`, `api/admin_newsletter.py`, `api/admin_visitors.py`, `models/document.py`, `schemas/{announcements,barangay,verification,document,newsletter,visitor,user,contributor,moderation}.py`.
Modified: `main.py`, `core/dependencies.py`, `models/__init__.py`, `models/business.py`, `api/public.py`, `api/admin.py`, `api/business.py`, `api/booking.py`.
Plus doc: `docs/migration/BACKEND_CONVENTIONS.md`.
