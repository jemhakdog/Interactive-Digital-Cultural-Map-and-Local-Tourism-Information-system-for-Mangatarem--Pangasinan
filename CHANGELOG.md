# Changelog — Flask → Next.js/FastAPI Migration (role features)

This records the work done on branch `feat/react-migration` to port the
Flask `main` branch's per-role features into the React frontend and wire them
to the FastAPI backend.

Two commits landed:

| Commit | Scope |
|--------|-------|
| `87d9de3` | Frontend: port per-role pages from `main` + role-based nav |
| `afc5bfc` | Backend: build the missing FastAPI endpoints + Alembic migration + smoke test |

> Out of scope / deliberately excluded from commits: `user_accounts.md` and
> `docs/chrome-dev-tools.md` (pre-existing, unrelated untracked files).

---

## Commit `87d9de3` — Frontend role-feature port

Ported every role's `main` Flask templates into Next.js App Router pages,
matching existing conventions (`fetchAPI` client, `@/lib/auth`, shadcn/ui
tokens). Nav was role-gated in `navbar.tsx`.

### New pages (`frontend/src/app`)
- **public / guest**: `barangays/`, `barangays/[id]/`, `announcements/`,
  `auth/select-role/`, `auth/reset-password/`, `auth/pending-approval/`,
  `auth/register-business/`
- **tourist (user)**: `passport/scan/` (QR check-in), `chat/[room]/`,
  `reviews/`
- **business_owner**: `business/dashboard/`, `business/[id]/edit/`,
  `business/[id]/menu/`, `business/[id]/rooms/`, `business/[id]/reviews/`,
  `business/[id]/verify/`, `business/peers/`
- **contributor (barangay)** — previously entirely absent: `contributor/`
  (layout + sidebar nav), `dashboard/`, `attractions` (list/new/[id]),
  `events` (list/new/[id]), `gallery` (list/new/[id]),
  `announcements` (list/new/[id]), `profile/`, `reviews/`
- **admin**: `attractions/new/`, `attractions/[id]/edit/`, `events/new/`,
  `events/[id]/edit/`, `establishments/`, `bookings/`, `heritage/`
  (list/new/[type]/[id]/edit), `reviews/`, `verify-merchants/`,
  `visitor-registry/`, `visits/`, `analytics/`, `documents/`, `newsletter/`

### Modified
- `frontend/src/components/layout/navbar.tsx` — role-gated links
  (Admin / My Business / Contributor / Passport) + Barangays & Announcements nav.
- `frontend/src/app/page.tsx` — cosmetic class tweaks only.
- New shared components: `components/admin/*`, `components/contributor/*`,
  `components/public/*`.

### Supporting docs (`docs/migration/`)
- `CONVENTIONS.md`, `spec-public.md`, `spec-tourist.md`, `spec-business.md`,
  `spec-contributor.md`, `spec-admin.md`, `PORT_REPORT.md`.

### Note
A subagent had edited `backend/app/models/user.py` (werkzeug dual-hash
fallback). This was **reverted** as out of scope (unneeded dead code + an
undeclared `werkzeug` dependency for a fresh FastAPI DB) before this commit.

### Verification
- `npx tsc --noEmit` → 0 errors.
- `npm run build` → 53 routes, 0 failures (one benign monorepo-root warning).

---

## Commit `afc5bfc` — Backend endpoint build

Built the FastAPI endpoints the ported placeholder pages depend on. Partitioned
so each subagent owned one router file; shared files (deps, schemas, models,
`main.py`) were handled by dedicated agents.

### New routers (`backend/app/api/`)
- `contributor.py` — stats, activity, attractions/events/gallery/announcements
  CRUD, profile (BarangayInfo), reviews (full CBIS scope)
- `user.py` — profile (get/put), stats, favorites, visits
- `admin_documents.py` — documents CRUD
- `admin_newsletter.py` — subscribers / send / history
- `admin_visitors.py` — visitor-registry, visits

### Extended routers
- `admin.py` — reviews + moderate, merchants/pending + verify, establishments
  + moderate, users/pending + approve/reject
- `public.py` — `GET /barangays`, `/barangays/{name}`, `/announcements`
- `business.py` — `POST /verification`, `GET /{id}/reviews`
- `booking.py` — `GET /admin/list`

### Foundation
- `core/dependencies.py` — added `require_roles(*roles)`,
  `require_contributor`, `require_business_owner`.
- `models/document.py` (new `Document` model) + registered in `models/__init__.py`.
- `models/business.py` — added `verified` column to `Establishment`.
- New schemas: `announcements`, `barangay`, `verification`, `document`,
  `newsletter`, `visitor`, `user`, `contributor`, `moderation`.
- `main.py` — mounted the 5 new routers.

### Migration (`backend/alembic/`)
- New migration `versions/f47ac10b9c3d_add_establishment_verified.py` (idempotent
  `ADD COLUMN verified` on `ESTABLISHMENT`). Applied to `instance/mangatarem.db`
  (backed up first).
- Fixed a **pre-existing** `alembic/env.py` bug: it imported models via the
  `app` path while `models/__init__.py` uses `backend.app`, duplicating `Table`
  metadata → "already defined" errors. Switched `env.py` to the canonical
  `backend.app` path. Also reset a stale `alembic_version` pointer (its
  migration file was missing from the empty `versions/` dir).

### Test (`backend/scripts/smoke_test_endpoints.py`)
Runtime smoke test against a fresh temp DB (seeds one user per role + a
barangay + an establishment). Hits every new endpoint — **41 calls, 0 HTTP 500**.

### Supporting docs (`docs/migration/`)
- `BACKEND_CONVENTIONS.md`, `BACKEND_PORT_REPORT.md`.

### Verification
- App imports cleanly; `/health` → 200; **95 API routes** registered.
- Smoke test: EXIT 0. 401s = correct admin-gating; 404s = missing rows;
  422s = request validation. No server errors.

---

## Known caveats (carried forward)
- Some pages were placeholder UI before this backend work; they are now wired
  to real endpoints and runtime-verified.
- A contributor user not linked to a `BarangayInfo` returns 404 on
  `/api/contributor/profile` — expected until real contributor↔barangay
  linkage/seeding exists (data concern, not a code defect).
- The migration only adds the `verified` column; the `Document` table already
  existed via `create_all`. Any future model-column additions still need their
  own migration (or a DB recreate) since `init_db()` uses `create_all`.
