# Port Report — Role Pages TypeScript Build Verification

**Phase:** Verify TypeScript build (agent 13)
**Scope:** Frontend role pages added during the Flask→FastAPI + Next.js migration
**Date:** build verified against current working tree

---

## 1. Build status

| Check | Command | Result |
|---|---|---|
| Type-check | `npx tsc --noEmit` (incremental) | **PASS** — exit 0, 0 errors |
| Type-check (clean) | `npx tsc --noEmit --incremental false` | **PASS** — exit 0, 0 errors |
| Production build | `npm run build` (Next.js) | **PASS** — exit 0, 53 routes generated |

- **TypeScript errors collected: NONE.** No fixes were applied (no errors to fix).
- `npm run build` compiled successfully and prerendered all 53 routes. The only build
  output is a benign warning: *"Next.js inferred your workspace root… set `turbopack.root`
  or remove one of the lockfiles"* — unrelated to our code (environment/monorepo lockfile artifact).
- **No edits were made to `lib/api.ts` or `components/ui/*`** (and none were needed).

> ⚠️ This report covers **compile-time / build-time correctness only**. No live backend was
> available, so runtime behavior, data fetching, and endpoint contracts were **not** exercised.
> "Wired" below means the page calls an endpoint that exists in `backend/app/api/*.py`;
> "placeholder" means the page renders local/empty state because the required FastAPI
> endpoint does not exist (per `CONVENTIONS.md §7` + the role spec files).

---

## 2. Files created per role

Newly-created (untracked) files this round, grouped by role. Pre-existing/committed
supporting files are noted at the end.

### Admin (`admin` role)
- `src/app/admin/analytics/page.tsx`
- `src/app/admin/attractions/new/page.tsx`
- `src/app/admin/attractions/[id]/edit/page.tsx`
- `src/app/admin/bookings/page.tsx`
- `src/app/admin/documents/page.tsx`
- `src/app/admin/establishments/page.tsx`
- `src/app/admin/events/new/page.tsx`
- `src/app/admin/events/[id]/edit/page.tsx`
- `src/app/admin/heritage/page.tsx`
- `src/app/admin/heritage/new/page.tsx`
- `src/app/admin/heritage/[type]/page.tsx`
- `src/app/admin/heritage/[type]/[id]/edit/page.tsx`
- `src/app/admin/newsletter/page.tsx`
- `src/app/admin/reviews/page.tsx`
- `src/app/admin/verify-merchants/page.tsx`
- `src/app/admin/visitor-registry/page.tsx`
- `src/app/admin/visits/page.tsx`
- `src/components/admin/attraction-form.tsx`
- `src/components/admin/event-form.tsx`
- `src/components/admin/heritage-form.tsx`

### Business (`business_owner` role)
- `src/app/business/dashboard/page.tsx`
- `src/app/business/[id]/edit/page.tsx`
- `src/app/business/[id]/menu/page.tsx`
- `src/app/business/[id]/reviews/page.tsx`
- `src/app/business/[id]/rooms/page.tsx`
- `src/app/business/[id]/verify/page.tsx`
- `src/app/business/peers/page.tsx`

### Contributor (`contributor` / barangay steward role)
- `src/app/contributor/layout.tsx`
- `src/app/contributor/dashboard/page.tsx`
- `src/app/contributor/attractions/page.tsx` (list)
- `src/app/contributor/attractions/[id]/page.tsx`
- `src/app/contributor/attractions/new/page.tsx`
- `src/app/contributor/events/page.tsx` (list)
- `src/app/contributor/events/[id]/page.tsx`
- `src/app/contributor/events/new/page.tsx`
- `src/app/contributor/gallery/page.tsx` (list)
- `src/app/contributor/gallery/[id]/page.tsx`
- `src/app/contributor/gallery/new/page.tsx`
- `src/app/contributor/announcements/page.tsx` (list)
- `src/app/contributor/announcements/[id]/page.tsx`
- `src/app/contributor/announcements/new/page.tsx`
- `src/app/contributor/profile/page.tsx`
- `src/app/contributor/reviews/page.tsx`
- `src/components/contributor/nav.tsx`
- `src/components/contributor/types.ts`
- `src/components/contributor/announcement-form.tsx`
- `src/components/contributor/attraction-form.tsx`
- `src/components/contributor/event-form.tsx`
- `src/components/contributor/gallery-form.tsx`

### Tourist (`user` / Explorer role)
- `src/app/chat/[room]/page.tsx`
- `src/app/passport/scan/page.tsx`
- `src/app/reviews/page.tsx`
- *(Pre-existing/committed this round: `src/app/dashboard/page.tsx`, `src/app/passport/page.tsx`,
  `src/app/profile/page.tsx`, `src/app/chat/page.tsx` — already ported earlier, not re-created.)*

### Public / guest role
- `src/app/announcements/page.tsx`
- `src/app/barangays/page.tsx`
- `src/app/barangays/[id]/page.tsx`
- `src/app/auth/pending-approval/page.tsx`
- `src/app/auth/register-business/page.tsx`
- `src/app/auth/reset-password/page.tsx`
- `src/app/auth/select-role/page.tsx`
- `src/components/public/barangay-explorer.tsx`
- `src/components/public/barangay-profile.tsx`
- `src/components/public/newsletter-subscribe.tsx`
- `src/components/public/register-business-form.tsx`
- `src/components/public/reset-password-form.tsx`
- *(Pre-existing/committed supporting files, already in tree: `src/app/auth/auth-constants.ts`,
  `src/app/auth/login/metadata.ts`, `src/app/auth/register/metadata.ts`,
  `src/app/business/business-view.tsx`, `src/app/business/[id]/business-detail-view.tsx`.)*

### Supporting modifications (tracked, edited this round)
- `src/components/layout/navbar.tsx` — role-gated nav links added.
- `src/app/page.tsx` — home page updates (e.g., announcements link).
- `backend/app/models/user.py` — backend model tweak (out of frontend scope; noted for traceability).

---

## 3. Backend gaps — placeholder UI vs wired

Derived from `CONVENTIONS.md §7` + `spec-*.md`, cross-checked against the created pages.
"Placeholder" = page renders local/empty state; required FastAPI endpoint is **MISSING**.

### Admin — partially wired, several placeholders
| Page | Endpoint used | Status |
|---|---|---|
| `admin/analytics` | `GET /api/analytics/summary` (EXISTING, totals only) | **WIRED (partial)** — only total visitors/page-views/7d; period/top-location/comparison are placeholder |
| `admin/attractions/new`, `attractions/[id]/edit` | `POST`/`PUT /api/attractions` (EXISTING) | **WIRED (partial)** — `barangay_id` select needs `GET /api/barangays` (**MISSING**) → dropdown is placeholder |
| `admin/heritage/*` | `GET`/`POST`/`PUT`/`DELETE /api/heritage/*` (EXISTING) | **WIRED** — NCCA Excel/DOCX export (**MISSING**) not wired |
| `admin/establishments` | `GET /api/business` (approved-only) | **PLACEHOLDER** — approve/reject/delete moderation (**MISSING**); list shows approved only |
| `admin/bookings` | `POST /api/booking/admin/update-status` (EXISTING) | **PLACEHOLDER table** — no reservation-read list endpoint (**MISSING**); table is local empty state |
| `admin/documents` | — | **PLACEHOLDER** — entire `/api/documents` router **MISSING** |
| `admin/newsletter` | — | **PLACEHOLDER** — admin newsletter send/list/unsubscribe (**MISSING**) |
| `admin/reviews` | — | **PLACEHOLDER** — admin-wide review list + approve/reject (**MISSING**) |
| `admin/verify-merchants` | — | **PLACEHOLDER** — merchant-verification endpoints (**MISSING**) |
| `admin/visitor-registry` | — | **PLACEHOLDER** — registry read + export (**MISSING**) |
| `admin/visits` | — | **PLACEHOLDER** — per-establishment/attraction history + exports (**MISSING**) |

### Business — mostly wired, two placeholders
| Page | Endpoint used | Status |
|---|---|---|
| `business/dashboard` | `rooms/list`, `menu/list`, `business/{id}` (all EXISTING) | **WIRED (assembled client-side)** |
| `business/[id]/edit` | `PUT /api/business/{id}` (EXISTING, JSON) | **WIRED (partial)** — file upload via `/api/uploads/image` (EXISTING); 1-establishment-per-owner enforced by backend |
| `business/[id]/menu` | `GET`/`POST`/`PUT`/`DELETE /api/business/menu/*` (EXISTING) | **WIRED** |
| `business/[id]/rooms` | `GET`/`POST`/`PUT`/`DELETE /api/business/rooms/*` (EXISTING) | **WIRED** |
| `business/peers` | `GET /api/business` (EXISTING) | **WIRED** (type-filtered public list) |
| `business/[id]/reviews` | `POST /api/business/reviews/{id}/reply` (EXISTING) | **PLACEHOLDER list** — owner all-status review view (**MISSING**) |
| `business/[id]/verify` | — | **PLACEHOLDER** — `POST /api/business/verification` (**MISSING**) |

### Contributor — effectively all placeholder (no contributor-scoped backend)
Every contributor page calls `/api/contributor/*` or relies on endpoints that are
admin-gated / approved-only. **No contributor-scoped FastAPI endpoints exist.**
- `contributor/dashboard` — stats endpoint **MISSING** → placeholder cards.
- `contributor/attractions/*` — contributor create/list-all-status/edit/delete **MISSING** (existing attraction endpoints are admin-gated, force `status="approved"`). Forms render with no submit wired.
- `contributor/events/*` — same as attractions, **MISSING**.
- `contributor/gallery/*` — gallery edit/delete + authenticated/user-scoped create **MISSING** (existing `POST /api/gallery` is unauthenticated, url-only).
- `contributor/announcements/*` — entire `/api/announcements` module **MISSING**.
- `contributor/profile` — `BarangayInfo` GET/PUT **MISSING** → placeholder form, no persistence.
- `contributor/reviews` — barangay-scoped review aggregate **MISSING**; reply endpoint (`POST /api/attractions/{id}/reviews` with `parent_id`) exists but lacks contributor barangay-ownership guard.

### Tourist — wired where endpoints exist; gaps are pre-existing
| Page | Endpoint used | Status |
|---|---|---|
| `chat/[room]` | `GET`/`POST /api/chat/{room_id}` (EXISTING) | **WIRED** — realtime WebSocket missing (FastAPI REST only) |
| `passport/scan` | `POST /api/gamification/checkin` (EXISTING) | **WIRED** (client-only GPS flow) |
| `reviews` | `GET`/`POST /api/attractions/{id}/reviews` (EXISTING) | **WIRED** — review photos upload **MISSING** (`ReviewCreate` JSON-only) |
| `dashboard` (pre-existing) | `GET /api/gamification/passport` (EXISTING) | **PLACEHOLDER stats** — `/api/user` router **MISSING** |
| `profile` (pre-existing) | — | **READ-ONLY** — `GET/PUT /api/user/profile` **MISSING** |

### Public / guest — mixed
| Page | Endpoint used | Status |
|---|---|---|
| `announcements` | — | **PLACEHOLDER** — `GET /api/announcements` **MISSING** |
| `barangays`, `barangays/[id]` | — | **PLACEHOLDER** — `GET /api/barangays` + profile **MISSING** |
| `auth/reset-password` | `POST /api/auth/reset-password` (EXISTING) | **WIRED** (client-side ≥8-char rule; backend enforces min 6) |
| `auth/select-role` | — | **UI only** — obsolete in FastAPI (role sent in Google body); no endpoint needed |
| `auth/pending-approval` | — | **UI only** — derived from `UserResponse.is_approved`; no endpoint needed |
| `auth/register-business` | `POST /api/auth/register` (EXISTING) | **PARTIAL** — `business_name`/`business_type` **uncaptured** by backend; no establishment created at signup |

---

## 4. Anything left unported

### No React route exists yet (true gaps, not placeholders)
- **Tourist Bookmarks** (`/user/favorites`) — no React route; `favorites` list/toggle endpoint **MISSING**.
- **Tourist My Visits** (`/user/visits`) — no React route; visits list/log endpoint **MISSING**.
- **Tourist Profile edit** — only read-only display ported; `GET/PUT /api/user/profile` **MISSING**.
- **Admin heritage NCCA export** (Excel/DOCX) — no export buttons wired (backend export endpoints **MISSING**).

### Backend endpoints still missing (block real functionality)
From `CONVENTIONS.md §7` + spec files, the highest-priority gaps the placeholder UIs depend on:
1. `GET /api/barangays` + `GET /api/barangays/{name}` (admin attraction/event forms, public directory + profile).
2. Admin moderation: approve/reject user, review, establishment; verify-merchants; documents router; newsletter admin; visitor-registry read/export; visits rich analytics; booking reservation-read list.
3. `POST /api/business/verification` (business owner verification).
4. Full contributor scope: dashboard stats, contributor CRUD for attractions/events, gallery edit/delete + authed create, `/api/announcements`, `BarangayInfo` GET/PUT, barangay-scoped review aggregate.
5. `/api/user` router (profile, dashboard stats, favorites, visits) for tourist.
6. Review photo upload (extend `post_review` or pair with `/api/uploads/multiple`).

### Notes
- All placeholder pages are honestly marked in-code with `// TODO: FastAPI … not implemented yet`
  comments and render local/empty state — they compile and build, but will not show live
  data until the corresponding backend endpoints are added.
- The `navbar.tsx` role-gating (admin/business_owner/contributor/user links) was added and
  type-checks cleanly; its runtime visibility depends on `useAuth()` returning the expected
  `role` values (verified shape in `CONVENTIONS.md §3`).

---

## 5. Summary

- **tsc: PASS** (0 errors, verified twice).
- **next build: PASS** (53 routes, 0 failures; one benign monorepo root warning).
- **Fixes applied: none** (nothing to fix).
- **Compiles vs placeholder:** all role pages **compile and build**; however a large share
  is **placeholder UI** waiting on missing FastAPI endpoints (contributor role is entirely
  placeholder; admin has ~7 placeholder modules; business has 2; public has 2; tourist has
  pre-existing gaps). Wired pages use existing endpoints per `CONVENTIONS.md §6`.
- Runtime correctness is **not** asserted (no live backend).
