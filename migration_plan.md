# Migration Plan: Flask + HTML → FastAPI + Next.js

## Current System

**Backend:** Flask (Python) with SQLAlchemy ORM, Flask-Login, Flask-SocketIO, Redis cache, Supabase
**Frontend:** Jinja2 templates + Tailwind CSS + vanilla JS
**Database:** PostgreSQL (via SQLAlchemy)

---

# Part 1: Backend Migration (Flask → FastAPI)

## What Changes

### 1. Framework Swap
| Flask | FastAPI |
|-------|---------|
| `Blueprint` | `APIRouter` |
| `@app.route()` | `@router.get()` / `@router.post()` |
| `render_template()` | `JSONResponse` (API-first) |
| `request` object | `Request` dependency |
| `current_app` | `Depends(get_settings)` |
| `flash()` | Return error response (no server-side sessions) |
| `url_for()` | Hardcode routes or use OpenAPI |

### 2. Auth System
| Flask | FastAPI |
|-------|---------|
| Flask-Login (session cookies) | JWT tokens (access + refresh) |
| `@login_required` | `Depends(get_current_user)` |
| `current_user` | `user: User = Depends(get_current_user)` |
| Session-based | Stateless tokens |

**New auth flow:**
```
Login → returns { access_token, refresh_token }
Every request → Authorization: Bearer <access_token>
Token expires → use refresh_token to get new one
```

### 3. Database Layer
| Flask | FastAPI |
|-------|---------|
| Flask-SQLAlchemy (`db`) | SQLAlchemy async + `AsyncSession` |
| `db.session.query()` | `await session.execute(select(...))` |
| `db.create_all()` | Alembic migrations (already have Flask-Migrate) |
| Sync operations | Async operations |

**Keep:**
- All models (identical structure)
- All relationships
- `to_dict()` methods
- Alembic migration history (just switch runner)

### 4. CSRF Protection
| Flask | FastAPI |
|-------|---------|
| Flask-WTF CSRF | Not needed (JWT stateless) |
| `csrf_token()` in templates | `X-CSRF-Token` header (if double-submit) |

**Remove:** CSRF protection entirely (JWT is sufficient for API).

### 5. Rate Limiting
| Flask | FastAPI |
|-------|---------|
| Flask-Limiter | `slowapi` or custom middleware |

### 6. Real-time (SocketIO)
| Flask | FastAPI |
|-------|---------|
| Flask-SocketIO | `python-socketio` async server |
| Same library, different setup |

### 7. File Structure Change
```
OLD:                              NEW:
modules/                          app/
  auth/                             api/
    routes.py                         auth.py
    models.py                         attractions.py
  attractions/                        events.py
    routes.py                         ... (one file per module)
    models.py                     core/
core/                                 database.py
  public_routes.py                    dependencies.py
app.py                              models/ (keep as-is)
config.py                            schemas/ (new - Pydantic)
```

## What Stays (Keep As-Is)

1. **All models** — Same SQLAlchemy models, just make them async-compatible
2. **Database schema** — No changes
3. **Business logic** — Extract to service layer, keep logic
4. **Redis integration** — Same, just async client (`aioredis`)
5. **Supabase client** — Same Python SDK
6. **Alembic migrations** — Keep history, change runner
7. **Config system** — Same `config.py` structure
8. **Validators** — Same logic, different decorator

## New Required Pieces

### Pydantic Schemas (New)
```python
# schemas/attraction.py
from pydantic import BaseModel
from datetime import datetime

class AttractionResponse(BaseModel):
    id: int
    name: str
    description: str | None
    category: str | None
    latitude: float | None
    longitude: float | None
    status: str
    created_at: datetime | None

    class Config:
        from_attributes = True
```

### Dependencies (New)
```python
# core/dependencies.py
from sqlalchemy.ext.asyncio import AsyncSession

async def get_db():
    async with async_session() as session:
        yield session

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    # Decode JWT, return user
```

### Async Database (New)
```python
# core/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(engine, class_=AsyncSession)
```

## Migration Steps

1. **Add dependencies** — `pip install fastapi uvicorn sqlalchemy[asyncio] aioredis python-jose[cryptography] passlib[bcrypt]`
2. **Create Pydantic schemas** — One per model
3. **Create dependencies** — DB session, auth
4. **Convert routes module by module:**
   - Start with `auth` (login, register, JWT)
   - Then `public_routes` (home, search, map)
   - Then `attractions`, `events`, etc.
   - Finally admin routes
5. **Remove Flask extensions** — CSRF, Flask-Login, Flask-Limiter
6. **Keep models.py and config.py**
7. **Update seed scripts** — Same, just async

---

# Part 2: Frontend Migration (HTML → Next.js + shadcn)

## What Changes

### 1. Template Engine
| Jinja2 | Next.js |
|--------|---------|
| `{% block %}` | Components |
| `{% for %}` | `.map()` |
| `{{ variable }}` | `{variable}` |
| `url_for('route')` | `<Link href="/path">` |
| `csrf_token()` | Not needed (JWT) |

### 2. Routing
| Flask | Next.js |
|-------|---------|
| `@public_bp.route("/")` | `app/page.tsx` |
| `@attractions_bp.route("/<int:id>")` | `app/attractions/[id]/page.tsx` |
| `@auth_bp.route("/login")` | `app/auth/login/page.tsx` |

**New structure:**
```
app/
├── (marketing)/           # Public pages
│   ├── page.tsx           # Home
│   ├── attractions/
│   │   ├── page.tsx       # List
│   │   └── [id]/page.tsx  # Detail
│   ├── events/
│   │   ├── page.tsx
│   │   └── [id]/page.tsx
│   ├── map/page.tsx
│   └── search/page.tsx
├── (auth)/                # Login/Register
│   ├── login/page.tsx
│   └── register/page.tsx
├── (dashboard)/           # Logged-in users
│   ├── dashboard/page.tsx
│   ├── profile/page.tsx
│   └── bookings/page.tsx
├── admin/                 # Admin panel
│   ├── page.tsx
│   ├── attractions/
│   └── events/
├── components/            # Reusable UI
│   ├── ui/               # shadcn components
│   ├── layout/           # Navbar, Footer
│   └── features/         # Domain components
└── lib/                  # Utilities
    ├── api.ts            # API client
    ├── auth.ts           # Auth helpers
    └── utils.ts          # cn(), etc.
```

### 3. Styling
| Current | Next.js + shadcn |
|---------|------------------|
| Tailwind (custom) | shadcn/ui components |
| Manual CSS files | `globals.css` with design tokens |
| Custom classes | Tailwind utilities + shadcn |

**Design tokens to extract:**
```css
:root {
  --background: 0 0% 100%;
  --foreground: 222 47% 11%;
  --primary: 142 76% 36%;        /* Green from current design */
  --primary-foreground: 0 0% 98%;
  --secondary: 210 40% 96%;
  --muted: 210 40% 96%;
  --accent: 210 40% 96%;
  --destructive: 0 84% 60%;
  --border: 214 32% 91%;
  --ring: 142 76% 36%;
  --radius: 0.5rem;
}
```

### 4. Data Fetching
| Flask | Next.js |
|-------|---------|
| Server renders HTML | Server Components (RSC) fetch data |
| `render_template(data)` | `async function Page()` with fetch |
| Forms submit to server | Forms call API or use Server Actions |

**New pattern:**
```tsx
// app/attractions/page.tsx
async function AttractionsPage() {
  const attractions = await fetchAttractions(); // Server-side
  return (
    <div>
      {attractions.map(a => (
        <AttractionCard key={a.id} attraction={a} />
      ))}
    </div>
  );
}
```

### 5. State Management
| Current | Next.js |
|---------|---------|
| Server-side sessions | React Query / SWR for server state |
| `flash()` messages | React toast (sonner) |
| Form validation (server) | Zod + react-hook-form (client) |

## What Stays (Keep As-Is)

1. **All data shapes** — Same JSON from API
2. **Design colors** — Extract to shadcn theme
3. **Page structure** — Same content, different rendering
4. **Images/assets** — Move to `/public`
5. **SEO meta** — Move to `metadata` exports

## Component Mapping

| Template | Component |
|----------|-----------|
| `base.html` | `layout.tsx` (root layout) |
| `admin/admin_base.html` | `admin/layout.tsx` |
| `includes/admin_nav.html` | `<AdminSidebar />` |
| `includes/user_nav.html` | `<UserNav />` |
| `pagez/index.html` | `app/page.tsx` + `<HeroSlider />`, `<FeaturedSection />` |
| `pagez/detail.html` | `app/attractions/[id]/page.tsx` |
| `pagez/map_v2.html` | `app/map/page.tsx` + `<MapView />` |
| `auth/login.html` | `app/auth/login/page.tsx` |
| `admin/dashboard.html` | `app/admin/page.tsx` |
| `admin/attractions.html` | `app/admin/attractions/page.tsx` |

## New Required Pieces

### API Client
```typescript
// lib/api.ts
const API_BASE = process.env.NEXT_PUBLIC_API_URL;

export async function fetchAPI<T>(path: string, options?: RequestInit): Promise<T> {
  const token = getAccessToken();
  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options?.headers,
    },
  });
  if (!res.ok) throw new APIError(res);
  return res.json();
}
```

### Auth Context
```typescript
// lib/auth.ts
export function useAuth() {
  // JWT token management
  // Login/logout functions
  // User state
}
```

### shadcn Components to Install
```
npx shadcn@latest add button card dialog form input label
npx shadcn@latest add table tabs toast dropdown-menu
npx shadcn@latest add navigation-menu sheet separator
npx shadcn@latest add avatar badge calendar command
```

## Migration Steps

1. **Scaffold Next.js** — `npx create-next-app@latest frontend`
2. **Install shadcn** — `npx shadcn@latest init`
3. **Extract design tokens** — From current `main.css` to shadcn theme
4. **Create layout components** — Navbar, Sidebar, Footer
5. **Convert pages one-by-one:**
   - Start with public pages (home, attractions list, detail)
   - Then auth pages (login, register)
   - Then dashboard pages
   - Finally admin pages
6. **Add API client** — Connect to FastAPI backend
7. **Add auth** — JWT token management
8. **Add forms** — Zod validation + react-hook-form
9. **Add real-time** — Socket.io client for chat

---

# Execution Order

## Phase 1: Backend (Week 1-2)
1. Set up FastAPI project structure
2. Port auth module (JWT)
3. Port public routes (home, search, map)
4. Port attractions module
5. Port events module
6. Port remaining modules
7. Test all endpoints

## Phase 2: Frontend (Week 2-4)
1. Scaffold Next.js + shadcn
2. Build layout (navbar, sidebar)
3. Convert public pages
4. Convert auth pages
5. Convert dashboard pages
6. Convert admin pages
7. Connect to API
8. Test full flow

## Phase 3: Polish (Week 4-5)
1. Add loading states
2. Add error handling
3. Add SEO
4. Add PWA support (if needed)
5. Deploy

---

# Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Auth breaks | Keep Flask running until Next.js auth works |
| Data loss | Same database, no schema changes |
| Downtime | Deploy frontend first, then switch backend |
| SEO drop | Use Next.js SSR/SSG for public pages |
| Performance | Next.js is faster than Jinja2 anyway |
