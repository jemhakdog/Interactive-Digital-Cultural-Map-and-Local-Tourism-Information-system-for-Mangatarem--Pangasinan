# Patch Bypass Summary — Attack Surface

**Repository**: capstone_system (Mangatarem Cultural Map)
**Scan window**: Full 245-commit history (only 1 commit within 60-day window)
**Mode**: Deep

---

## Commit Scan Results

```
MAX_COMMITS=500  |  MAX_AGE="60 days ago"
Total commits in repo: 245
Commits within window: 1 (30bc3e7 — "Add endpoint test script")
Security-relevant commits (full history): 12
```

### Security Commit Timeline

| Date | Commit | Security Relevance |
|------|--------|-------------------|
| 2026-04-10 | `996b9ba` | CSRF protection plan, session cookie hardening, seed refactor |
| 2026-04-11 | `968fc71` | Rate limiting for map routes |
| 2026-04-13 | `939e6d9` | **Core security utilities** — `security.py`, `validators.py`, `template_filters.py`, CSP headers, error sanitization |
| 2026-04-14 | `5f25127` | **Route-level validation** — applied across 12+ route files |
| 2026-04-25 | `a257334` | **Validation decorators** — `@validate_form_data`, `@validate_query_params`, `@validate_json_input` |
| 2026-05-17 | `4224901` | Auth flows (register, login) |
| 2026-05-18 | `388b24f` | Requirements cleanup (security deps) |

### Architecture Refactor

The codebase underwent a major refactoring from flat `routes/` to modular `modules/` structure. Security utilities (`utils/security.py`, `utils/validators.py`) were preserved through the refactor, but **not all routes were migrated with validation intact**. The booking module and some admin routes were added post-refactor without inheriting the validation patterns.

---

## Bypass Attempts & Conclusions

### Bypassed (7 findings)

1. **SECRET_KEY default fallback** — Critical. Enables session forgery if env var unset.
2. **Socket.IO `cors_allowed_origins="*"`** — High. Any origin can connect to chat WebSocket.
3. **CSP `unsafe-eval` + `unsafe-inline`** — High. XSS payloads execute freely.
4. **Open redirect via `next` parameter** — Medium. Admin-only but exploitable via social engineering.
5. **Booking IDOR** — High. Any business_owner can modify any reservation.
6. **Update route optional token** — Critical. RCE possible if `UPDATE_TOKEN` not set.
7. **Booking race condition** — Medium. Overbooking via concurrent requests.

### Sound (3 findings)

1. **SQL injection regex** — Low risk. SQLAlchemy ORM is the primary defense and is sound.
2. **Password reset token** — Low risk. Database-backed validation prevents timing attacks.
3. **Auth rate limiting** — Low risk. 5 req/min on all auth endpoints via Redis-backed limiter.

### Relocated (0 findings)

No instances of a fix merely moving the vulnerability to a different code path.

---

## Cluster Map

```
SEC-UTILS ──┬── security.py (421 lines: sanitize, validate, detect)
             ├── validators.py (248 lines: form/query/json decorators)
             └── template_filters.py (101 lines: Jinja2 filters)
                │
SEC-ROUTES ──┤── admin/attractions.py (validation added)
             ├── admin/events.py (validation added)
             ├── admin/documents.py (JSON validation, file size limits)
             ├── admin/newsletter.py (header injection protection)
             ├── barangay/attractions.py (validation added)
             ├── barangay/events.py (validation added)
             └── barangay/gallery.py (media type checks)
                │
SEC-DECORATORS ── business/routes.py (3 decorated endpoints)
                   core/public_routes.py (search, subscribe)
                   core/user_routes.py (profile update)
                   notifications/routes.py
                │
NOT COVERED ──── booking/routes.py ← New module, no validation
                 chat/routes.py ← No input validation
                 admin_core/visits.py ← Partial validation
                 admin_core/content.py ← Open redirect
```

---

## Key Gap: Booking Module Is a Security Vacuum

The booking module (`modules/booking/routes.py`) was added after the security hardening commits and received **zero validation decorators or manual input checks**. It handles:
- Financial-equivalent operations (reservations)
- Capacity accounting (race condition)
- Physical location verification (GPS spoofing)
- Status modification (IDOR)

This is the highest-priority target for security remediation.
