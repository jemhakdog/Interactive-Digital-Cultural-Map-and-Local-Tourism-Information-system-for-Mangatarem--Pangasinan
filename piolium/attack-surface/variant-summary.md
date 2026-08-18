# Phase 12 — Variant Analysis Summary

> **Generated**: 2026-08-18  
> **Audit mode**: deep  
> **Original findings analyzed**: 27 (p10-001 through p10-029, excluding p10-014 false positive)  
> **Variants found**: 27

---

## Variant Statistics

| Category | Count | Severity Breakdown |
|----------|-------|-------------------|
| **Open Redirect / Parameter Injection** (`**request.args` spread) | 3 | HIGH × 3 |
| **Open Redirect** (`next` parameter) | 1 | HIGH |
| **IDOR** (missing ownership check) | 4 | HIGH × 1, MEDIUM × 3 |
| **TOCTOU / Race Conditions** | 9 | HIGH × 2, MEDIUM × 7 |
| **Missing Auth Guard** | 1 | HIGH |
| **Secret / Credential Exposure** | 2 | MEDIUM × 2 |
| **Redis KEYS DoS** | 2 | HIGH × 1, MEDIUM × 1 |
| **State Machine Violations** | 1 | MEDIUM |
| **CSRF on State-Changing GET** | 1 | MEDIUM |
| **Information Disclosure** | 2 | MEDIUM × 1, LOW × 1 |
| **Subprocess in Request** | 1 | LOW |
| **Total** | **27** | **5 HIGH, 18 MEDIUM, 2 LOW** |

---

## Variants by Pattern Family

### Family 1: `**request.args` Spread in Redirects (p10-011 pattern)
All redirect handlers that use `**request.args` to forward query parameters.

| ID | Slug | Location | Auth Required | Severity |
|----|------|----------|--------------|----------|
| p12-001 | args-spread-attractions | `attractions/routes.py:20` | No | HIGH |
| p12-002 | args-spread-barangay-events | `barangay/routes.py:31`, `events/routes.py:10` | No | HIGH |
| p12-003 | args-spread-public-routes | `core/public_routes.py:133` | No | HIGH |

**Note**: The original p10-011 covered `admin_core/documents.py` (10 endpoints, admin-only). These variants extend the pattern to **public/unauthenticated** endpoints, significantly expanding the attack surface.

### Family 2: Open Redirect via `next` Parameter (p10-006/p10-012 pattern)
Unvalidated `next` parameter in redirects.

| ID | Slug | Location | Severity |
|----|------|----------|----------|
| p12-004 | open-redirect-next-params | `visits.py:610,619`, `content.py:111,133` | HIGH |

### Family 3: IDOR — Missing Ownership Verification (p10-007 pattern)
Endpoints that check role but not resource ownership.

| ID | Slug | Location | Severity |
|----|------|----------|----------|
| p12-005 | booking-idor-any-owner | `booking/routes.py:133-160` | HIGH |
| p12-017 | heritage-delete-idor | `heritage/admin_routes.py:275-290` | MEDIUM |
| p12-019 | admin-heritage-edit-idor | `heritage/admin_routes.py:241` | MEDIUM |
| p12-020 | visitor-log-export-idor | `visits.py:182-250` | MEDIUM |

### Family 4: TOCTOU / Race Conditions (p10-021/p10-022/p10-025/p10-026/p10-029 pattern)
Check-then-act without atomicity.

| ID | Slug | Location | Severity |
|----|------|----------|----------|
| p12-006 | booking-toctou-capacity-race | `booking/routes.py:75-88,150-156` | HIGH |
| p12-013 | password-reset-toctou-reuse | `auth/password.py:38-72` | MEDIUM |
| p12-015 | badge-unlock-no-constraint | `gamification/routes.py:130-155` | HIGH |
| p12-016 | gamification-checkin-toctou | `gamification/routes.py:110-125` | MEDIUM |
| p12-023 | registration-toctou-race | `auth/register.py:25-36` | MEDIUM |
| p12-024 | rating-recalc-race | `business/routes.py:207-219` | MEDIUM |
| p12-025 | newsletter-subscribe-toctou | `notifications/routes.py:22-45` | LOW |
| p12-026 | visitor-log-duplicate-toctou | `booking/routes.py:190-205` | MEDIUM |

### Family 5: Missing Auth Guard (p10-009 pattern)
Endpoints with `@login_required` but no role check.

| ID | Slug | Location | Severity |
|----|------|----------|----------|
| p12-009 | missing-role-log-visit | `visits.py:567` | HIGH |

### Family 6: Secret/Credential Exposure (p10-001/p10-002 pattern)
Hardcoded secrets or fail-open defaults.

| ID | Slug | Location | Severity |
|----|------|----------|----------|
| p12-008 | hardcoded-oauth-client-id | `auth/oauth.py:18` | MEDIUM |
| p12-021 | password-reset-email-enumeration | `auth/password.py:17-36` | MEDIUM |

### Family 7: Redis KEYS DoS (p10-018 pattern)
Redis KEYS with user-controlled or wildcard patterns.

| ID | Slug | Location | Severity |
|----|------|----------|----------|
| p12-010 | redis-keys-user-pattern | `map_routes.py:290-297` | HIGH |
| p12-022 | cache-teardown-redis-keys | `map_routes.py:365-375` | MEDIUM |

### Family 8: State Machine / CSRF (p10-023/p10-028 pattern)
Reversible states or CSRF on state-changing endpoints.

| ID | Slug | Location | Severity |
|----|------|----------|----------|
| p12-007 | get-state-change-csrf | `content.py:92,115` | MEDIUM |
| p12-018 | booking-state-reversible-visited | `booking/routes.py:143-160` | MEDIUM |

### Family 9: Session Self-Service (p10-019 pattern)
Client-controlled session state bypasses server guards.

| ID | Slug | Location | Severity |
|----|------|----------|----------|
| p12-011 | gamification-nav-bypass-session | `gamification/routes.py:80-92` | MEDIUM |

### Family 10: PII Exposure (p10-010 pattern)
Data exposure without role restriction.

| ID | Slug | Location | Severity |
|----|------|----------|----------|
| p12-012 | pii-search-unrestricted | `auth/api.py:10-30` | MEDIUM |

### Family 11: Subprocess in Request (p10-008 pattern)
Command execution in web request handlers.

| ID | Slug | Location | Severity |
|----|------|----------|----------|
| p12-014 | subprocess-public-sitemap | `core/public_routes.py:346` | LOW |

### Family 12: IDOR — Admin Data Access (p10-007 pattern)
Admin-only endpoints without ownership verification.

| ID | Slug | Location | Severity |
|----|------|----------|----------|
| p12-027 | admin-heritage-json-idor | `heritage/admin_routes.py:300` | MEDIUM |

---

## High-Severity Variants (5)

1. **p12-001** — `**request.args` spread on public attractions redirect
2. **p12-002** — `**request.args` spread on public barangay/events redirects  
3. **p12-003** — `**request.args` spread on public map redirect
4. **p12-004** — Open redirect via `next` parameter in admin endpoints
5. **p12-005** — Booking IDOR: any business_owner can modify any reservation
6. **p12-006** — Booking TOCTOU: concurrent reservations cause overbooking
7. **p12-009** — Missing role check on visit log POST endpoint
8. **p12-010** — Redis KEYS with user-controlled wildcard pattern
9. **p12-015** — Badge unlock race condition (no unique constraint)

---

## Key Observations

1. **Pattern Amplification**: The original p10-011 (`**request.args` spread) was admin-only. Three new variants (p12-001/002/003) are **unauthenticated**, expanding the attack surface to any anonymous visitor.

2. **Systemic TOCTOU**: 9 TOCTOU variants found across 6 different handlers. The codebase has **zero** `SELECT FOR UPDATE`, **zero** `transaction.atomic()`, and **zero** unique constraints on critical junction tables (UserPassport, TouristCheckIn, VisitorLog).

3. **Inconsistent Access Control**: The `log_visit` endpoint (p12-009) is the third instance of inconsistent auth guards, confirming a systemic pattern of copy-paste omission in the admin module.

4. **Redis DoS Surface**: Two new variants (p12-010, p12-022) confirm that Redis KEYS with wildcard patterns are used both in explicit cache invalidation AND in app teardown hooks, creating a persistent O(N) scan risk.

5. **Redirect Chain Risk**: 14 legacy redirect handlers use `**request.args` spread. While the original finding focused on the 10 admin document redirects, the 4 public redirects are more dangerous due to lack of authentication.

---

## Recommendations

1. **Immediate**: Remove `**request.args` from all redirect handlers; use explicit parameter forwarding only.
2. **Immediate**: Add role check to `log_visit()` endpoint.
3. **Short-term**: Add unique constraints to `UserPassport(user_id, badge_id)` and `TouristCheckIn` duplicate guard.
4. **Short-term**: Replace Redis `KEYS` with `SCAN` in all cache invalidation paths.
5. **Short-term**: Validate `next` parameter against a whitelist of internal paths.
6. **Medium-term**: Implement `SELECT FOR UPDATE` or optimistic locking for all capacity/state mutations.
7. **Medium-term**: Convert GET-based state changes (approve/reject) to POST-only.
