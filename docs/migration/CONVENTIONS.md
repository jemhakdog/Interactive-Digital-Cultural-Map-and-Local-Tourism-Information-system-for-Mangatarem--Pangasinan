# Conventions — Frontend & Backend API Surface (Source of Truth)

> Extracted during the Flask→FastAPI + Next.js migration. Implementation agents MUST follow these conventions.
> API base: `NEXT_PUBLIC_API_URL` (default `http://localhost:8000`). All backend routes are prefixed `/api`.

---

## 1. Frontend file/folder structure (`frontend/src`)

Next.js App Router. Routes live under `app/`, shared UI under `components/`, data/auth helpers under `lib/`.

```
src/
├── app/                          # Pages (App Router)
│   ├── admin/                    # admin, admin/attractions, admin/events, admin/users
│   ├── attractions/              # list + attractions/[id]
│   ├── auth/                     # login, register, forgot-password
│   ├── business/                 # list + business/[id]
│   ├── chat/
│   ├── dashboard/
│   ├── events/                   # list + events/[id]
│   ├── gallery/
│   ├── heritage/                 # heritage/[type], heritage/[type]/[id]
│   ├── map/
│   ├── passport/
│   ├── profile/
│   ├── search/
│   ├── globals.css               # Tailwind v4 + design tokens (NO tailwind.config file)
│   └── layout.tsx                # Root layout (wraps AuthProvider, Navbar, Footer)
├── components/
│   ├── layout/                   # navbar.tsx, footer.tsx
│   ├── map/                      # map-container, map-sidebar, map-marker-pin, etc.
│   ├── ui/                       # shadcn/Base-UI primitives (see §4)
│   ├── admin-dialogs.tsx
│   ├── auth/google-auth-button.tsx
│   ├── image-upload.tsx
│   ├── map-view.tsx
│   ├── review-form.tsx
│   ├── review-section.tsx
│   └── skeletons.tsx
└── lib/
    ├── api.ts                    # fetchAPI, authAPI, api helpers
    ├── auth.tsx                  # AuthProvider + useAuth()
    ├── validations.ts            # zod schemas (login, register, attraction, event, review)
    └── utils.ts                  # cn() (clsx + tailwind-merge)
```

Conventions:
- Server Components do data fetching; Client Components (`"use client"`) use `useAuth()` + `fetchAPI`.
- Barrel imports use `@/` alias → `src/`. e.g. `@/lib/api`, `@/components/ui/button`.
- UI primitives are **Base UI** (`@base-ui/react`), not Radix. Styled with `cva` + `cn`.

---

## 2. Data fetching

### Server-component pattern (no auth token)
Reads `API_BASE` directly, calls `fetch` with `next: { revalidate }`, and **falls back** to curated/local data on non-OK or empty result.

```ts
const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function getAttractions() {
  try {
    const res = await fetch(`${API_BASE}/api/attractions/`, { next: { revalidate: 60 } });
    if (!res.ok) return Object.values(CURATED_ATTRACTION_METADATA);
    const data = await res.json();
    const items = (data.attractions ?? data.items ?? []);
    return items.length ? items : Object.values(CURATED_ATTRACTION_METADATA);
  } catch {
    return Object.values(CURATED_ATTRACTION_METADATA);
  }
}
```
Ref: `app/attractions/page.tsx`. Keep this fallback shape for any server-fetched list.

### Client pattern (`@/lib/api`)
```ts
import { fetchAPI, authAPI, api } from "@/lib/api";
import { useAuth } from "@/lib/auth";

// Generic fetch with Bearer token + unified error
const data = await fetchAPI<T>("/api/booking/reserve", { method: "POST", body: ... });
```
- **`fetchAPI<T>(path, options?)`** — attaches `Authorization: Bearer <localStorage access_token>`, sends `Content-Type: application/json`, throws `APIError` (status + detail) on `!res.ok`, returns `res.json()` (or `undefined` on 204).
- **`authAPI`** — `login`, `register`, `google`, `forgotPassword`, `me`, `refresh`.
- **`api`** (typed helpers used by pages):
  | helper | endpoint |
  |---|---|
  | `api.home()` | `GET /api/` |
  | `api.attractions(params?)` | `GET /api/attractions?...` → normalizes `attractions|items` → `items` |
  | `api.attraction(id)` | `GET /api/attractions/{id}` |
  | `api.attractionReviews(id)` | `GET /api/attractions/{id}/reviews` |
  | `api.events(params?)` | `GET /api/events?...` → `items` |
  | `api.event(id)` | `GET /api/events/{id}` |
  | `api.business(params?)` | `GET /api/business?...` → `items` (key `businesses|establishments|items`) |
  | `api.businessItem(id)` | `GET /api/business/{id}` |
  | `api.search(q, params?)` | `GET /api/search?q=...` |
  | `api.map(category?)` | `GET /api/map` |
  | `api.heritageTypes()` | `GET /api/heritage/types` |
  | `api.heritageByType(type, params?)` | `GET /api/heritage/{type}?...` |
  | `api.gallery(params?)` | `GET /api/gallery?...` |

---

## 3. Auth

### `useAuth()` shape (`@/lib/auth`)
```ts
interface AuthState {
  user: UserProfile | null;          // null when logged out
  loading: boolean;                   // true during initial token check
  login: (email: string, password: string) => Promise<void>;
  register: (name: string, email: string, password: string, role?: string, barangay?: string) => Promise<void>;
  googleLogin: (credential: string, role?: string) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
}

interface UserProfile {                // returned by /api/auth/me
  id: number;
  email: string;
  name: string;        // maps to backend username
  role: string;        // "admin" | "business_owner" | "contributor" | "user"
  is_approved: boolean;
  created_at: string;
}
```
Access: `const { user, loading, login, logout } = useAuth();` (must be inside `<AuthProvider>`).

### Flow
1. `login` / `register` / `googleLogin` → calls `authAPI.*`, stores `access_token` + `refresh_token` in **localStorage**, then `refreshUser()` → `GET /api/auth/me` populates `user`.
2. Token storage: `localStorage["access_token"]`, `localStorage["refresh_token"]`. `fetchAPI` reads `access_token` and sets `Bearer` header.
3. `logout()`: removes both tokens, sets `user = null`.
4. On app load, `AuthProvider` checks `access_token`; if present, calls `refreshUser()`; on failure clears tokens.
5. `GET /api/auth/logout` exists for symmetry but is stateless (client discards tokens).

### Roles present
`admin`, `business_owner`, `contributor`, `user`.
- `registerSchema` (zod) only allows `role: "user" | "contributor" | "business_owner"` (admin is assigned, not self-registered).
- Only `user` is auto-`is_approved`. `business_owner`/`contributor` default to `is_approved=false` → pending until approved.
- Backend role checks: `require_admin` (strict `role == "admin"`), `get_current_active_user`, `get_current_user`. `booking.update-status` allows `admin|contributor|business_owner`.

---

## 4. Available UI components

Import path: `@/components/ui`. All styled via tokens (`bg-primary`, `text-muted-foreground`, `rounded-xl`, etc.). Based on **Base UI** + `cva`.

| Component file | Exports | Key props / variants |
|---|---|---|
| `button.tsx` | `Button`, `buttonVariants` | `variant`: `default\|outline\|secondary\|ghost\|destructive\|link`; `size`: `default\|xs\|sm\|lg\|icon\|icon-xs\|icon-sm\|icon-lg` |
| `card.tsx` | `Card`, `CardHeader`, `CardFooter`, `CardTitle`, `CardAction`, `CardDescription`, `CardContent` | `Card` prop `size`: `default\|sm` |
| `input.tsx` | `Input` | standard `<input>` props + `type` |
| `textarea.tsx` | `Textarea` | standard `<textarea>` props |
| `badge.tsx` | `Badge`, `badgeVariants` | `variant`: `default\|secondary\|destructive\|outline\|ghost\|link` (pill, `rounded-4xl`) |
| `avatar.tsx` | `Avatar`, `AvatarImage`, `AvatarFallback`, `AvatarGroup`, `AvatarGroupCount`, `AvatarBadge` | — |
| `dialog.tsx` | `Dialog`, `DialogClose`, `DialogContent`, `DialogDescription`, `DialogFooter`, `DialogHeader`, `DialogOverlay`, `DialogPortal`, `DialogTitle`, `DialogTrigger` | — |
| `dropdown-menu.tsx` | `DropdownMenu`, `DropdownMenuPortal`, `DropdownMenuTrigger`, `DropdownMenuContent`, `DropdownMenuGroup`, `DropdownMenuLabel`, `DropdownMenuItem`, `DropdownMenuCheckboxItem`, `DropdownMenuRadioGroup`, `DropdownMenuRadioItem`, `DropdownMenuSeparator`, `DropdownMenuShortcut`, `DropdownMenuSub`, `DropdownMenuSubTrigger`, `DropdownMenuSubContent` | — |
| `navigation-menu.tsx` | `NavigationMenu`, `NavigationMenuContent`, `NavigationMenuIndicator`, `NavigationMenuItem`, `NavigationMenuLink`, `NavigationMenuList`, `NavigationMenuTrigger`, `navigationMenuTriggerStyle`, `NavigationMenuPositioner` | — |
| `separator.tsx` | `Separator` | — |
| `sheet.tsx` | `Sheet`, `SheetTrigger`, `SheetClose`, `SheetContent`, `SheetHeader`, `SheetFooter`, `SheetTitle`, `SheetDescription` | `SheetContent` prop `side`: `right\|left\|top\|bottom` (navbar uses `side="right"`) |
| `table.tsx` | `Table`, `TableHeader`, `TableBody`, `TableFooter`, `TableHead`, `TableRow`, `TableCell`, `TableCaption` | — |
| `tabs.tsx` | `Tabs`, `TabsList`, `TabsTrigger`, `TabsContent`, `tabsListVariants` | — |
| `skeleton.tsx` | `Skeleton` | — |
| `toast.tsx` | `Toaster`, `Toast`, `ToastAction`, `ToastClose`, `ToastContent`, `ToastDescription`, `ToastPortal`, `ToastProvider`, `ToastTitle`, `ToastViewport`, `createToastManager`, `toast`, `useToastManager` | — |
| `map.tsx` | (MapLibre wrapper — large, app-specific) | Not a generic primitive; import only for map features |

Helper: `cn(...)` from `@/lib/utils` (clsx + tailwind-merge) for conditional classes.

---

## 5. Tailwind token classes (primary = GREEN)

Tailwind **v4** — no `tailwind.config` file. Tokens declared via `@theme inline` in `globals.css`, mapping CSS variables. Light tokens in `:root`, dark overrides under `.dark`.

**Colors** (utility = `bg-<name>`, `text-<name>`, `border-<name>`):
- `primary` — **green** `oklch(0.55 0.18 148)` (dark: `0.70 0.18 148`); `primary-foreground` white-ish.
- `secondary` — pale green; `secondary-foreground` dark green.
- `accent` — green (same hue as primary); `accent-foreground` white.
- `muted` / `muted-foreground` — neutral grey-green.
- `card` / `card-foreground`, `popover` / `popover-foreground`.
- `destructive` — red `oklch(0.55 0.2 27)`; `destructive-foreground`.
- `border`, `input`, `ring` — green-tinted greys.
- `chart-1..5`, `sidebar*` — green/teal palette.

**Radius** (base `--radius: 0.625rem`): utilities map to a derived scale:
`--radius-sm` (0.6×), `--radius-md` (0.8×), `--radius-lg` (1× = base), `--radius-xl` (1.4×), `--radius-2xl` (1.8×), `--radius-3xl` (2.2×), `--radius-4xl` (2.6×).
Common usage: `rounded-lg`, `rounded-xl`, `rounded-4xl` (badges/pills).

**Fonts**: `--font-sans` (Geist Sans), `--font-mono` (Geist Mono), `--font-heading` (used by `CardTitle` via `font-heading`).

**Status colors used ad-hoc** (non-token, inline): `text-emerald-500 bg-emerald-500/10`, `text-blue-500`, `text-amber-500`, `text-purple-500` (see admin/dashboard stat cards).

---

## 6. Backend endpoints reference

All routers included in `backend/app/main.py` with `/api` prefix. Auth column: `Public` = no token; `User` = `get_current_user`; `Active` = `get_current_active_user`; `Admin` = `require_admin`; roles noted where narrower.

### `/api/auth` (auth.py)
| Method | Path | Auth | Returns |
|---|---|---|---|
| POST | `/login` | Public | `TokenResponse` (access+refresh) |
| POST | `/register` | Public | `TokenResponse` (201) |
| POST | `/google` | Public | `TokenResponse` |
| POST | `/forgot-password` | Public | `{detail}` |
| POST | `/reset-password` | Public | `{detail}` |
| GET | `/me` | User | `UserResponse` |
| POST | `/refresh` | Public | `TokenResponse` |
| POST | `/logout` | Public | `{detail}` (stateless) |

### `/api` (public.py)
| GET | `/` | Public | homepage (`featured_attractions`, `featured_events`) |
| GET | `/search` | Public | attractions, events, barangays, categories |
| GET | `/map` | Public | markers (approved attractions w/ coords) |

### `/api/attractions` (attractions.py)
| GET | `/` | Public | list (filters: category, barangay, is_featured, lat/lng/radius; pagination) |
| GET | `/{id}` | Public | detail (+ avg rating) |
| POST | `/` | Admin | create |
| PUT | `/{id}` | Admin | update |
| DELETE | `/{id}` | Admin | delete (204) |
| GET | `/{id}/reviews` | Public | reviews + summary + pagination |
| POST | `/{id}/reviews` | Active | post review (rating 1–5, optional parent reply) |

### `/api/events` (events.py)
| GET | `/` | Public | list (status default `approved`; category/status filters) |
| GET | `/{id}` | Public | detail |
| POST | `/` | Admin | create |
| PUT | `/{id}` | Admin | update |
| DELETE | `/{id}` | Admin | delete (204) |

### `/api/business` (business.py)
| GET | `/` | Public | list establishments (filters: type, price_range, barangay, q, featured, lat/lng/radius) |
| GET | `/{establishment_id}` | Public | detail (+ rooms for inn / menu for others / reviews) |
| POST | `/` | `business_owner` | create (status `pending`) |
| PUT | `/{establishment_id}` | owner/Admin | update |
| GET | `/rooms/list` | `business_owner` | owner's rooms |
| POST | `/rooms` | `business_owner` | add room |
| PUT | `/rooms/{room_id}` | `business_owner` | edit room |
| DELETE | `/rooms/{room_id}` | `business_owner` | delete room |
| GET | `/menu/list` | `business_owner` | owner's menu items |
| POST | `/menu` | `business_owner` | add menu item |
| PUT | `/menu/{item_id}` | `business_owner` | edit menu item |
| DELETE | `/menu/{item_id}` | `business_owner` | delete menu item |
| POST | `/{establishment_id}/reviews` | Active | submit review |
| POST | `/reviews/{review_id}/reply` | `business_owner` | reply to review |

### `/api/booking` (booking.py)
| GET | `/availability/{asset_id}` | Public (requires `date` query) | capacity for date |
| POST | `/reserve` | User | create reservation (returns `qr_token`) |
| POST | `/admin/update-status` | `admin|contributor|business_owner` | transition reservation status |
| POST | `/verify-arrival` | User | GPS arrival verification (100m threshold) |

### `/api/chat` (chat.py)
| GET | `/` | User | list rooms for current user |
| GET | `/{room_id}` | User (participant) | messages (paginated) |
| POST | `/{room_id}/messages` | User (participant) | send message |

### `/api/gallery` (gallery.py)
| GET | `/` | Public | list approved (type, barangay filters; pagination; `barangays` list) |
| POST | `/` | Public | submit item (status `pending`) |

### `/api/heritage` (heritage.py)
| GET | `/` | Public | list all (type, search, barangay filters) |
| GET | `/types` | Public | types with counts |
| GET | `/{type}` | Public | list by type (`built|natural|intangible|movable|mixed`) |
| GET | `/{type}/{id}` | Public | detail |
| POST | `/{type}` | Active | create (status `pending`) |
| PUT | `/{type}/{id}` | Active | update |
| DELETE | `/{type}/{id}` | Admin | delete (204) |

### `/api/gamification` (gamification.py)
| POST | `/start-navigation` | User | lock route in Redis (24h TTL) |
| POST | `/stop-navigation` | User | clear route |
| GET | `/active-navigation` | User | current nav session |
| POST | `/checkin` | User | GPS-validated QR check-in (50m threshold; badge unlock) |
| GET | `/passport` | User | passport (badges, coupons, recent check-ins) |

### `/api/notifications` (notifications.py)
| POST | `/subscribe` | Public | newsletter subscribe |
| POST | `/mark-read` | User | mark all read |
| POST | `/mark-read/{id}` | User | mark one read |
| GET | `/` | User | list notifications |
| GET | `/unread` | User | unread count |

### `/api/analytics` (analytics.py)
| POST | `/log-visitor/{target_type}/{target_id}` | Active | log visitor (`target_type`: `attraction|establishment`; perms enforced) |
| GET | `/summary` | Admin | totals (visitors, page views, 7d) |

### `/api/uploads` (uploads.py)
| POST | `/image` | User | upload single image (png/jpg/jpeg/gif, ≤10MB) |
| POST | `/multiple` | User | upload ≤10 images/media (incl. mp4) |

### `/api/admin` (admin.py)
| GET | `/users` | Admin | paginated user list (`users`, `total`, `page`, `per_page`, `pages`) |

### Root (main.py)
| GET | `/health` | Public | `{status:"ok"}` |
| GET | `/` | Public | API info (`docs`: `/docs`) |

---

## 7. MISSING BACKEND list (Flask features → FastAPI status)

Status legend: **EXISTING** = endpoint present; **PARTIAL** = core present, gaps noted; **MISSING** = no endpoint.

| Flask feature | Status | Notes / FastAPI location |
|---|---|---|
| Attractions CRUD | EXISTING | `/api/attractions` |
| Events CRUD | EXISTING | `/api/events` |
| Heritage CRUD | EXISTING | `/api/heritage` |
| Business (menu/rooms) | EXISTING | `/api/business` full CRUD for owner |
| QR check-in | EXISTING | `/api/gamification/checkin` |
| Booking management | **EXISTING (core)** | `/api/booking` reserve/availability/update-status/verify-arrival. **MISSING**: admin list/overview of all reservations; no reservation-read endpoint. |
| Gallery | **PARTIAL** | `/api/gallery` list + submit. **MISSING**: admin moderation (approve/delete pending items) — items created `pending` with no way to flip status. |
| Newsletter | **PARTIAL** | `/api/notifications/subscribe` exists. **MISSING**: full newsletter management (campaigns, admin send/list, unsubscribe). |
| Visitor registry / visits | **PARTIAL** | `/api/analytics/log-visitor` (VisitorLog) + `/api/analytics/summary`. **MISSING**: dedicated visitor registry read/list endpoint (per-establishment/attraction history, export). |
| Announcements | **MISSING** | No `/api/announcements` router. |
| Barangay profiles | **MISSING** | `BarangayInfo` model exists and is used as a JOIN in queries, but there is **no** `GET /api/barangay` or barangay-profile endpoint. |
| Verify merchants | **MISSING** | Establishments are created `status="pending"` but there is **no approve/verify endpoint** for `business_owner` or establishment. Admin cannot flip `pending→approved`. |
| Contributor CRUD | **MISSING** | No `/api/contributor` router. `contributor` role is only used in permission checks (analytics, booking). No contributor profile/CRUD/submission-management endpoints. |
| Documents | **MISSING** | No `/api/documents` router (no doc upload/list/management). |
| Chat | EXISTING | `/api/chat` |
| Notifications | EXISTING | `/api/notifications` |
| Auth | EXISTING | `/api/auth` |
| Gamification (passport/nav) | EXISTING | `/api/gamification` |
| Uploads | EXISTING | `/api/uploads` |
| Admin users | EXISTING | `/api/admin/users` |

**Highest-priority gaps to implement next:** verify_merchants (approve flow), barangay profiles endpoint, announcements, contributor CRUD, gallery moderation, booking admin list.

---

## 8. Current navbar links & where to add role-specific links

File: `components/layout/navbar.tsx` (`"use client"`).

**Current `navLinks` (shown to ALL users, desktop + mobile):**
- `/attractions` — Attractions
- `/events` — Events
- `/business` — Business
- `/map` — Map
- `/heritage` — Heritage
- `/gallery` — Gallery

**Right-side (desktop + mobile Sheet footer):**
- Search icon → `/search` (always).
- If `user`: Dashboard link (`/dashboard`, shows `user.name` + `Admin` Badge when `role==="admin"`) + Logout button.
- Else: Log in (`/auth/login`) + Sign up (`/auth/register`).

**Role gating today:** only an `Admin` **Badge** is shown for admins. Admin management links (`/admin`, `/admin/attractions`, `/admin/events`) appear only inside `DashboardPage` (admin section) and `AdminPage` — **not** in the navbar.

**Where role-specific links should be added:**
- Add them in the **user menu area** (desktop `user` block / mobile `<Sheet>` footer), gated by `user.role === "X"` — same pattern `DashboardPage` already uses for the admin section.
- `business_owner`: needs a link to their establishment management (currently none in navbar). Suggest `/business/manage` (or reuse `/dashboard` business section) — backend owner endpoints exist at `/api/business`.
- `contributor`: needs a contributor dashboard / heritage-submit entry (currently none). Suggest `/contributor` or a "Submit Heritage" link to `/heritage`.
- `admin`: add `/admin` to nav when `user.role === "admin"` (and keep the `Admin` Badge).
- Use `<Badge variant="secondary">` for role indicators (navbar already does for Admin).

**Pattern to copy (from `dashboard/page.tsx`):**
```tsx
{user.role === "admin" && (
  <Link href="/admin"><Button variant="outline" ...>Dashboard</Button></Link>
)}
```
