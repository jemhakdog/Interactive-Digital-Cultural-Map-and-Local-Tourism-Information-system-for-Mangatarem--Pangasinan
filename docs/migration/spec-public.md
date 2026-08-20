# Migration Spec — `public` User Role (Flask `main` → Next.js)

> Read-only investigation of the **public / guest + Explorer (tourist) + shared auth** surface as it exists on the Flask `main` branch, mapped against the existing FastAPI backend (`backend/app/api/*.py`) and the already-ported React frontend (`frontend/src/app`).
>
> Scope: guest visitors, the "Explorer" (`user`) authenticated role, and shared auth flows (login / register / forgot / reset / Google / business registration / pending-approval / role selection). Public barangay browsing and the announcements bulletin are included. Admin / contributor / business_owner dashboards are out of scope here.

---

## 1. Navigation structure (how the public role is reached)

`base.html` (lines 114–166) chooses the nav partial by `current_user.role`:

| Condition | Nav partial rendered |
|---|---|
| Not authenticated (anonymous / guest) | `includes/guest_nav.html` |
| `role == 'user'` (Explorer) | `includes/user_nav.html` |
| `role == 'admin'` | `includes/admin_nav.html` |
| `role == 'contributor'` | `includes/barangay_nav.html` |
| `role == 'business_owner'` | `includes/business_nav.html` |

### Top nav — Guest (`guest_nav.html`)
| Label | Flask endpoint | Purpose |
|---|---|---|
| Home | `public.index` | Landing / hero |
| Map | `public.map_view` | Interactive map |
| Barangays | `barangay.index` | Barangay directory |
| Events | `events.index` | Public events list |
| Gallery | `gallery.index` | Public gallery |
| Stay & Eat | `business.index` | Approved establishments |
| Login | `auth.login` | Sign in |
| Register | `auth.register` | Sign up (button) |

### Top nav — Explorer (`user_nav.html`)
| Label | Flask endpoint | Purpose |
|---|---|---|
| Dashboard | `user.dashboard` | User home |
| Bookmarks | `user.favorites` | Saved attractions |
| My Visits | `user.visits` | Visit history |
| Passport | `gamification.view_passport` | Tourist passport / gamification |
| **Explore ▾ dropdown** | | Map, Barangays, Events, Gallery, Stay & Eat, Routes (`public.routes`) |
| Logout | `auth.logout` | Sign out |

### Where the other public pages live
- **Announcements** (`/announcements`): NOT in `guest_nav` or `user_nav`. It is linked from the **home page footer/section** (`templates/pagez/index.html:262` → `/announcements`) and from the contributor nav (`barangay.barangay_announcements`). For the public role it is reached only via the home page link / direct URL.
- **Barangay profile** (`barangay.profile`): reached by clicking a barangay card on `barangay.index` (link target `barangay.profile` with `name=barangay.name`).
- **Reset / select-role / pending-approval / register-business**: post-auth or standalone auth pages reached by redirect or direct link from the auth forms.

### Shared partials used by the public role
| Partial | Used by |
|---|---|
| `templates/base.html` | All pages (nav swap, flash messages, footer, mobile-nav JS) |
| `templates/includes/guest_nav.html` | Guest top nav |
| `templates/includes/user_nav.html` | Explorer top nav (incl. `js/components/user-nav.js`) |
| `templates/includes/pagination.html` | Generic paginated lists (present in tree; verify usage) |
| Flash messages pattern (`get_flashed_messages`) | All auth forms (login/register/forgot/reset/register_business) |
| `js/pages/auth.js`, `js/pages/barangays.js`, `js/pages/barangays_mobile.js`, `js/pages/barangay_profile.js`, `js/pages/reset_password.js` | Page behavior (password toggle, view toggle, filters, map) |
| Vendor: Leaflet (`vendor/leaflet/*`), AOS (`vendor/aos/*`) | Map + scroll animations |

> No `public_nav.html` partial exists on `main` (confirmed: `fatal: path 'templates/includes/public_nav.html' does not exist`). Public nav is split into `guest_nav.html` (anonymous) and `user_nav.html` (Explorer).

---

## 2. Feature / page table

Legend: **EXISTING** = a matching FastAPI route already exists in `backend/app/api/*.py`; **MISSING** = no equivalent FastAPI endpoint yet. "Ported?" = React page present under `frontend/src/app`.

### 2.1 Public browsing

| Feature | Main template | Nav location | Purpose | Form fields / data shown | Backend endpoint | Already ported to React? |
|---|---|---|---|---|---|---|
| Barangay directory (desktop) | `pagez/barangays.html` | Top nav "Barangays" (`barangay.index`) | Grid + map directory of 82 barangays with search & category filter | **Data:** `barangays[]` each `{name, image_url, tags[0], attraction_count}`; `barangays-data-store` JSON (full objects incl. `center_latitude/longitude`). **Controls:** `barangaySearch` (text), `categoryFilter` select (all / Nature / History / Food / Festivals), grid/map view toggle. **CTA:** "Login as Contributor" → `auth.login`, "Browse Experiences" → `public.index#experiences`. | **MISSING** (no `barangay.index` list endpoint; `GET /api/search` only returns `barangays_info` when a query/barangay filter is supplied, not a full list) | **No** (`frontend/src/app/barangays` absent) |
| Barangay directory (mobile style) | `pagez/barangays_v1.html` | Same as above | Alt mobile-first layout: sidebar category filter chips + search pill + popular (top-5 by `attraction_count`) + discovery list | **Data:** same `barangays[]`. Client-computed: `code = "BRGY-" + name[:3].upper() + "-" + (len*12+100)`, `class = Urban if attraction_count>3 else Rural`, `eventsCount = (attraction_count*2//3) or 1`. **Controls:** `#mobileBarangaySearch`, filter chips (all/Nature/History/Food/Festivals), bottom-sheet filter. Poblacion uses a hardcoded Wikimedia image. | **MISSING** (same as above) | **No** |
| Barangay profile | `pagez/barangay_profile.html` | Barangay card → `barangay.profile(name=barangay.name)` | Tabbed profile: Cultural / Attractions / Events / Gallery + Leaflet map | **Data:** `barangay_name`; `barangay_info` `{mission, vision, history, unique_features, cultural_assets, traditions, local_practices}`; `attractions[]` `{id, name, category, image_url, description}`; `events[]` `{id, name, category, date, location, image_url}`; `gallery_items[]` `{type(video\|image), url, caption}`; `center_latitude/longitude`; `map_assets`. Each attraction links to `attractions.detail(id)`. | **MISSING** (no `barangay.profile` / barangay-detail endpoint; no route returns a barangay + its attractions/events/gallery) | **No** (`frontend/src/app/barangays` absent; note `heritage` is a different concept) |
| Announcements bulletin | `pagez/announcements.html` | Home page footer link (`/announcements`) — not in top nav | Timeline of LGU + barangay announcements | **Data:** `announcements[]` each `{title, content, created_at, author_name, barangay, barangay_id, barangay_name}`. Badge logic: `barangay_id` null → "LGU Official Notice" (emerald); else `"<barangay_name> Dispatch"` (amber). `created_at` formatted `%B %d, %Y at %I:%M %p`. Empty-state message when none. | **MISSING** (model `ANNOUNCEMENT` exists in `backend/app/models/announcements.py`, but **no GET endpoint** in any `api/*.py`) | **No** (`frontend/src/app/announcements` absent) |

### 2.2 Shared auth flows

| Feature | Main template | Nav location | Purpose | Form fields / data shown | Backend endpoint | Already ported to React? |
|---|---|---|---|---|---|---|
| Login | `auth/login.html` | Nav "Login" (`auth.login`) | Username + password sign-in + Google | **Fields:** `username` (text, required), `password` (password, required), `remember` (checkbox, no backend effect), `csrf_token`. Google: hidden `credential` + `nonce` POSTed to `auth.google_login` (`data-client_id` hardcoded `7945…j1fh.apps.googleusercontent.com`). Flash message area. | **PARTIAL** — `POST /api/auth/login` **EXISTING** but its schema is `email` + `password` (not `username`). `POST /api/auth/google` **EXISTING**. → React must send **email** not username. `remember` has no backend. | **Yes** (`frontend/src/app/auth/login`) — must verify it posts `email` |
| Register (Explorer/Contributor/Business) | `auth/register.html` | Nav "Register" (`auth.register`) | Sign-up with role + conditional barangay | **Fields:** `role` (select, required: `user` / `contributor` / `business_owner`), `barangay` (select, shown only when role=contributor; 82 hardcoded barangay names), `username` (text, required), `email` (email, required), `password` (password, required; hint "8+ chars", no HTML min), `csrf_token`. Google signup → `auth.google_login`. JS `data-action="toggle-barangay"` reveals barangay select. | **EXISTING** `POST /api/auth/register` schema: `email` (EmailStr), `password` (min 6, max 128), `name` (min 2, max 80), `role` (enum, default `user`), `barangay` (str\|None). ⚠ Flask field `username` ↔ FastAPI `name`. Contributor/business_owner set `is_approved=false` server-side. | **Yes** (`frontend/src/app/auth/register`) — must map `username`→`name`, pass `barangay` |
| Forgot password | `auth/forgot_password.html` | Login page "Forgot?" link (`auth.forgot_password`) | Request reset email | **Fields:** `email` (email, required), `csrf_token`. Success/error flash. Links: "Back to Login" (`auth.login`), "Return to Map" (`public.index`). | **EXISTING** `POST /api/auth/forgot-password` (`{email}`) | **Yes** (`frontend/src/app/auth/forgot-password`) |
| Reset password | `auth/reset_password.html` | Email link (`auth.reset_password`, `token=token`) | Set new password via token | **Fields:** `password` (password, required, `minlength=8`), `confirm_password` (password, required, `minlength=8`; client-side match check), `csrf_token`. JS `reset_password.js` enforces: ≥8 chars + match before submit. `token` passed as URL param. | **EXISTING** `POST /api/auth/reset-password` (`{token, password}`, min 6). ⚠ Flask requires min 8 for both; FastAPI only requires min 6 for `password`. `confirm_password` is client-only (drop on submit). | **No dedicated page** — verify `auth/reset-password` exists in React (only `login/register/forgot-password` dirs present) → **likely MISSING** in React |
| Select role (post-Google) | `auth/select_role.html` | Shown mid Google-OAuth registration (`auth.select_role`) | Choose account type after Google auth | **Fields:** hidden `role` (set by JS: `user` / `business_owner` / `contributor`), `csrf_token`. Three interactive cards (Explorer / Merchant / Guardian) with loading spinners; auto-submits after 450 ms. Greets `{{ name or email }}`. | **MISSING** — FastAPI `google_auth` takes `role` directly in the request body; there is no separate select-role step. This page is effectively obsolete in the FastAPI flow. | **No** (not needed — role sent with Google credential) |
| Register business | `auth/register_business.html` | "Stay & Eat" / business CTA (`auth.register_business`) | Standalone business-owner sign-up | **Fields:** `business_name` (text, required), `business_type` (select, required: `inn` / `restaurant` / `cafe` / `fastfood`), `username` (text, required), `email` (email, required), `password` (password, required, `minlength=6`), `csrf_token`. Note: "reviewed by admin before appearing on map." | **MISSING** — no `register_business` endpoint. Business owners register via `POST /api/auth/register` with `role=business_owner`; **`business_name` and `business_type` are NOT captured by the backend** (no establishment created at signup). | **No** (`frontend/src/app/register-business` absent) |
| Pending approval | `auth/pending_approval.html` | Shown after contributor/business registration (no own route; rendered by register flow) | "Account pending review" notice | **No form.** Static notice: 24–48 h manual verification; links "Return to Home Page" (`public.index`) and "Try Logging In Again" (`auth.login`). | **MISSING as a page**, but the *state* is derivable: `UserResponse.is_approved == false` for contributor/business_owner after `POST /api/auth/register`. React should render this screen when `is_approved` is false on the returned user. | **No** (derive from `is_approved` on register response) |

---

## 3. Endpoint mapping summary (FastAPI vs Flask)

All FastAPI routes are mounted under `/api` (see `backend/app/main.py:81-94`).

| Flask endpoint (public role) | HTTP | FastAPI path | Status |
|---|---|---|---|
| `public.index` | GET | `/api/` (homepage data) | **EXISTING** |
| `public.map_view` | GET | `/api/map` | **EXISTING** |
| `public.search` (unified) | GET | `/api/search` | **EXISTING** |
| `public.routes` | — | — | **MISSING** |
| `barangay.index` | GET | (none — list) | **MISSING** |
| `barangay.profile` | GET | (none — by name) | **MISSING** |
| `announcements` (public list) | GET | (none) | **MISSING** |
| `auth.login` | POST | `/api/auth/login` (⚠ uses `email`, not `username`) | **EXISTING (schema differs)** |
| `auth.register` | POST | `/api/auth/register` (⚠ `username`→`name`) | **EXISTING (schema differs)** |
| `auth.google_login` | POST | `/api/auth/google` | **EXISTING** |
| `auth.forgot_password` | POST | `/api/auth/forgot-password` | **EXISTING** |
| `auth.reset_password` | POST | `/api/auth/reset-password` (⚠ min 6 not 8) | **EXISTING (validation differs)** |
| `auth.logout` | POST | `/api/auth/logout` (stateless) | **EXISTING** |
| `auth.refresh` | POST | `/api/auth/refresh` | **EXISTING** |
| `auth.me` | GET | `/api/auth/me` | **EXISTING** |
| `auth.select_role` | POST | (none) | **MISSING** (obsolete in FastAPI) |
| `auth.register_business` | POST | (none) | **MISSING** (`business_name`/`business_type` uncaptured) |
| `auth.pending_approval` | GET | (none, derive from `is_approved`) | **MISSING** (state-based) |
| `events.index` / `gallery.index` / `business.index` | GET | `/api/events`, `/api/gallery`, `/api/business` | **EXISTING** (separate role specs) |

---

## 4. Implementation notes for the Next.js port

1. **Login field rename.** Flask `login.html` posts `username`; FastAPI `LoginRequest` requires `email`. The React `auth/login` page must send the user's email (or the backend must accept either). Confirm which the React page currently posts.
2. **Register field rename + barangay.** Flask `username` → FastAPI `name`. Pass `role` and optional `barangay` (only meaningful for `contributor`). Google signup sends `role` in the Google body directly — there is **no select-role page** in FastAPI.
3. **Business registration gap.** `register_business.html` collects `business_name` + `business_type`, but `POST /api/auth/register` has no such fields. Either extend `RegisterRequest`/add a `POST /api/business` creation step, or drop those fields. Currently the business is **not** created at signup.
4. **New endpoints to build (MISSING):**
   - `GET /api/barangays` — full barangay directory (name, image_url, tags, attraction_count, center lat/lng) for the grid + map views.
   - `GET /api/barangays/{name}` (or `/{id}`) — barangay profile: `barangay_info` text fields + its attractions + events + gallery items + map assets.
   - `GET /api/announcements` — public bulletin (return `title, content, created_at, author_name, barangay_name, barangay_id`; filter LGU vs barangay via `barangay_id`).
5. **Reset-password React page.** Only `auth/login`, `auth/register`, `auth/forgot-password` exist in `frontend/src/app/auth`. A `reset-password` page (consuming `?token=`) is likely still missing — add it; keep client-side confirm + ≥8 char rule to match Flask (note FastAPI only enforces min 6).
6. **Validation parity.** Flask `reset_password` enforces min 8 + match; FastAPI enforces min 6. Decide canonical rule and align both.
7. **Maps/animations.** Both `barangays.html` and `barangay_profile.html` embed Leaflet + a `barangays-data-store` / `map_assets` JSON blob. The React `map` route already exists and can be reused for the directory map view; the profile map needs the per-barangay asset payload from the (missing) profile endpoint.
8. **Announcements placement.** There is no top-nav entry; keep the link on the home page (footer/section) as on Flask, or add it to `guest_nav`/`user_nav` if desired.
9. **Pending-approval state.** After registering as `contributor`/`business_owner`, render the pending screen from `UserResponse.is_approved === false` rather than navigating to a dedicated route.

---

## 5. Ported-vs-missing at a glance (React `frontend/src/app`)

| Page | Flask source | React exists? |
|---|---|---|
| Home | `public.index` | ✅ `page.tsx` |
| Map | `public.map_view` | ✅ `map` |
| Search | `public.search` | ✅ `search` |
| Attractions | `attractions.*` | ✅ `attractions` |
| Events | `events.*` | ✅ `events` |
| Business / Stay & Eat | `business.*` | ✅ `business` |
| Heritage | `heritage.*` | ✅ `heritage` |
| Gallery | `gallery.*` | ✅ `gallery` |
| Login | `auth.login` | ✅ `auth/login` |
| Register | `auth.register` | ✅ `auth/register` |
| Forgot password | `auth.forgot_password` | ✅ `auth/forgot-password` |
| **Barangays directory** | `barangay.index` | ❌ missing |
| **Barangay profile** | `barangay.profile` | ❌ missing |
| **Announcements** | `/announcements` | ❌ missing |
| **Reset password** | `auth.reset_password` | ❌ likely missing (`auth/reset-password` dir absent) |
| **Register business** | `auth.register_business` | ❌ missing |
| **Select role** | `auth.select_role` | ❌ not needed (FastAPI handles in-body) |
| **Pending approval** | `auth.pending_approval` | ❌ derive from `is_approved` |
