# Security Audit Report: Interactive Digital Cultural Map & Tourism System
## Mangatarem, Pangasinan — Full-Stack Security Assessment

**Repository**: `jemhakdog/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan`  
**Commit**: `30bc3e7f85f14a8c7d4259681c0d2f885ab51337` (branch: `main`)  
**Audit Mode**: Deep (17-phase methodology)  
**Date**: 2026-08-18  
**Framework**: Flask 3.1.2 / Python 3.12 / PostgreSQL (Supabase) / Redis (Upstash)

---

## Executive Summary

This audit assessed a Flask-based modular monolith serving as a digital cultural map and tourism information system for Mangatarem, Pangasinan. The application features public tourism data, user-generated content, gamification (QR/GPS check-ins, badges), a booking/reservation system, and a `/pull` deployment endpoint.

**The audit identified 27 validated vulnerabilities: 2 Critical, 11 High, and 14 Medium.** The most severe findings form an exploit chain: a weak default `SECRET_KEY` enables session forgery, which combined with a bypassed `/pull` endpoint yields unauthenticated remote code execution. A separate Critical finding exposes the Gemini API key to any anonymous visitor. Systemic weaknesses include: zero concurrency primitives across the codebase (no `SELECT FOR UPDATE`, no `transaction.atomic()`, no unique constraints on critical junction tables), pervasive open redirects via `**request.args` spread, multiple IDORs on booking and heritage resources, and an unauthenticated Redis cache invalidation endpoint vulnerable to O(N) KEYS-pattern DoS.

**Risk Level: HIGH.** Immediate remediation is required for the Critical findings and the `SECRET_KEY` chain. The systemic TOCTOU and concurrency issues require architectural changes.

---

## Methodology Summary

- **P1–P3 (Intelligence & Architecture)**: Advisory collection, architecture inventory, dependency analysis, threat modeling with 14 DFD/CFD trust boundary slices, and domain-specific attack research across 8 attack classes (SSTI, Auth, SQLi, File Upload, WebSocket, SSRF, OAuth/JWT, Cryptography).
- **P4–P5 (Static Analysis)**: Candidate scan (1,106 matches across 224 files), CodeQL structural extraction (53 entry points, 14 sink categories, 18 source-to-sink flows), built-in security rulesets (9 categories), and authorization matrix audit (187 endpoints mapped against 5 roles).
- **P6–P7 (State & Concurrency + Spec Gaps)**: State-holding entity catalog (17 entities), concurrency audit (zero locking primitives found), framework contract analysis (6 spec-gap findings), and hidden control channel enumeration (11 channels).
- **P8 (Deep Bug Hunting)**: Manual attack surface probing — 7 high-confidence findings with full code path traces.
- **P9 (Cross-Service)**: Skipped — single-service monolith, no inter-service edges.
- **P10 (Review Chambers)**: 6 adversarial review chambers (secrets-misconfig, authz-access-control, csrf-cors-middleware, unauth-endpoints, concurrency-state, low-severity). 47 hypotheses evaluated; 27 confirmed, 20 rejected (including 1 confirmed false positive via source-code verification of Flask-WTF 1.2.2).
- **P11 (Cold Verification)**: LITE cold verification applied to all 13 Critical/High findings. 1 finding (p10-014 CSRF JSON bypass) was **disproved** by reading the actual Flask-WTF 1.2.2 source code — no content-type exemption exists.
- **P12 (Variant Analysis)**: 27 variant instances identified across 12 pattern families, amplifying the attack surface (e.g., `**request.args` spread extends from admin-only to 4 public unauthenticated endpoints).

**Key artifacts**: [Knowledge Base Report](attack-surface/knowledge-base-report.md) · [Attack Pattern Registry](attack-pattern-registry.json) · [Variant Summary](attack-surface/variant-summary.md) · [Authz Matrix](attack-surface/authz-matrix.md) · [Unauthenticated Surface](attack-surface/unauthenticated-surface.md) · [State & Concurrency Summary](attack-surface/state-concurrency-summary.md)

---

## Summary of Findings

| # | ID | Title | Severity | PoC Status | Adversarial Review |
|---|----|-------|----------|------------|-------------------|
| 1 | p10-001 | Gemini API Key Leaked to Anonymous Visitors | **CRITICAL** | theoretical | CONFIRMED |
| 2 | p10-008 | /pull Token Bypass → RCE via git pull | **CRITICAL** | theoretical | CONFIRMED |
| 3 | p10-002 | SECRET_KEY Weak Default (`your-secret-key-here`) | HIGH | theoretical | CONFIRMED |
| 4 | p10-003 | Debug Supabase Endpoint Exposed | HIGH | theoretical | CONFIRMED |
| 5 | p10-004 | Debug Mode in Production Entry Point | HIGH | theoretical | CONFIRMED |
| 6 | p10-005 | OAuth Session Forgeable Chain (via default SECRET_KEY) | HIGH | theoretical | CONFIRMED |
| 7 | p10-006 | Open Redirect in Admin Review Actions | HIGH | theoretical | CONFIRMED |
| 8 | p10-007 | IDOR in Booking Status Update — Any Owner Can Modify Any Reservation | HIGH | theoretical | CONFIRMED |
| 9 | p10-009 | Inconsistent Auth Guard on /admin/visits/log | HIGH | theoretical | CONFIRMED |
| 10 | p10-012 | Open Redirect in Visit Log Handlers | HIGH | theoretical | CONFIRMED |
| 11 | p10-018 | Redis KEYS DoS via Unauthenticated Cache Invalidation | HIGH | theoretical | CONFIRMED |
| 12 | p10-021 | Booking Slot Overbook — TOCTOU Race Condition | HIGH | theoretical | CONFIRMED |
| 13 | p10-022 | Badge Unlock Race — Duplicate Rewards | HIGH | theoretical | CONFIRMED |
| 14 | p10-010 | Authenticated User Search Exposes PII | MEDIUM | theoretical | — |
| 15 | p10-011 | Legacy Redirect `**request.args` Spread (Admin) | MEDIUM | theoretical | — |
| 16 | p10-013 | Socket.IO CORS Wildcard | MEDIUM | theoretical | — |
| 17 | p10-015 | ProxyFix Trust Bypass (Conditional on Deployment) | MEDIUM | theoretical | — |
| 18 | p10-016 | UPDATE_TOKEN Non-Constant-Time Comparison | MEDIUM | theoretical | — |
| 19 | p10-017 | Unauthenticated Map Feedback DB Write | MEDIUM | theoretical | — |
| 20 | p10-019 | Gamification Navigation Guard Bypass | MEDIUM | theoretical | — |
| 21 | p10-020 | OAuth Missing State Parameter + CSRF on Role Selection | MEDIUM | theoretical | — |
| 22 | p10-023 | Booking State Machine — Reversible Terminal States | MEDIUM | theoretical | — |
| 23 | p10-024 | Booking Reserve — No Idempotency | MEDIUM | theoretical | — |
| 24 | p10-025 | Booking Status Update — No SELECT FOR UPDATE | MEDIUM | theoretical | — |
| 25 | p10-026 | Password Reset Token TOCTOU | MEDIUM | theoretical | — |
| 26 | p10-028 | Admin Approval GET Requests — No CSRF | MEDIUM | theoretical | — |
| 27 | p10-029 | Gamification Check-in Duplicate Guard TOCTOU | MEDIUM | theoretical | — |

> **Note**: All PoC statuses are `theoretical` — the audit was conducted against source code and local deployment; no live production environment was available for exploitation. The adversarial review (P11-LITE) verified each Critical/High finding against actual installed dependency source code where applicable.

> **Rejected finding**: p10-014 (CSRF JSON Content-Type Bypass) was **disproved** by reading Flask-WTF 1.2.2's `csrf.py` source — no `request.is_json` exemption exists. This finding is excluded from the valid count.

---

## Technical Findings Detail

### CRITICAL Findings

---

### p10-001 — Gemini API Key Leaked to Anonymous Visitors
- **Severity**: CRITICAL
- **Summary**: `GET /api/gemini/config` returns the `GEMINI_API_KEY` environment variable as JSON to any anonymous visitor with no authentication, no access control, and default rate limiting only.
- **Impact**: API key theft enabling unauthorized Gemini API usage at the project's expense. Potential broader GCP resource access if the key has elevated permissions.
- **Root Cause**: Endpoint handler directly serializes `os.environ.get('GEMINI_API_KEY')` into the HTTP response without any access control.
- **Key Code Reference**: `modules/core/api_routes.py:127-137` — `gemini_config()`
- **PoC Status**: theoretical
- **Evidence**: No `@login_required`, no role check, no middleware. Single GET request extracts the key.
- **Detailed Report**: `piolium/findings-draft/p10-001-gemini-api-key-leak.md`
- **Adversarial Review**: `piolium/adversarial-reviews/p10-001-gemini-api-key-leak-review.md` — CONFIRMED

---

### p10-008 — /pull Endpoint Token Bypass → RCE via git pull
- **Severity**: CRITICAL
- **Summary**: The `/pull` endpoint's token verification is entirely bypassed when the `UPDATE_TOKEN` environment variable is not set, allowing any authenticated admin to trigger `subprocess.run(["git", "pull"])` and `shutil.copy2()` to production filesystem paths. Chains with p10-002 (default SECRET_KEY) for unauthenticated RCE.
- **Impact**: Remote code execution via git pull (if attacker controls git remote) + arbitrary file copy to production paths (`/home/GoMangatarem/mysite`). Error messages leak internal git remote URLs.
- **Root Cause**: `if expected_token and token != expected_token` — when `UPDATE_TOKEN` env var is unset, `expected_token` is `None`/falsy, short-circuiting the entire token check.
- **Key Code Reference**: `modules/core/update_routes.py:36-37` (token check), `update_routes.py:93` (subprocess.run)
- **PoC Status**: theoretical
- **Attack Chain**: Forge session via p10-002 → POST /pull → git pull executes → files copied to production.
- **Additional Weakness**: Non-constant-time token comparison (`!=` operator) enables timing side-channel extraction (p10-016).
- **Detailed Report**: `piolium/findings-draft/p8-001-pull-token-bypass-rce.md`
- **Adversarial Review**: `piolium/adversarial-reviews/p10-008-pull-token-bypass-rce-review.md` — CONFIRMED

---

### HIGH Findings

---

### p10-002 — SECRET_KEY Weak Default
- **Severity**: HIGH
- **Summary**: `SECRET_KEY` falls back to `"your-secret-key-here"` when the environment variable is unset, allowing any attacker to forge Flask session cookies.
- **Impact**: Session forgery, full account impersonation, CSRF token generation bypass. Chains with p10-005 (OAuth identity bypass) and p10-008 (RCE chain).
- **Key Code Reference**: `config.py:13`
- **Evidence**: `SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key-here")`
- **Adversarial Review**: CONFIRMED

### p10-003 — Debug Supabase Endpoint Exposed
- **Severity**: HIGH
- **Summary**: `GET /test-supabase` queries the PostgreSQL database and returns results as JSON — no authentication.
- **Impact**: Database data exposure, reconnaissance for further attacks (table structure, attraction data).
- **Key Code Reference**: `modules/core/public_routes.py:16-17`
- **Adversarial Review**: CONFIRMED

### p10-004 — Debug Mode in Production Entry Point
- **Severity**: HIGH
- **Summary**: `app.py:140` calls `socketio.run(app, debug=True)`, enabling the Werkzeug interactive debugger in the Docker production entry point.
- **Impact**: Remote code execution via interactive Python console when Docker deployment is internet-accessible and an exception is triggered.
- **Key Code Reference**: `app.py:140`
- **Adversarial Review**: CONFIRMED

### p10-005 — OAuth Session Forgeable Chain
- **Severity**: HIGH
- **Summary**: The Google OAuth flow stores identity in a signed session cookie without re-verifying the Google token. When SECRET_KEY uses the default (p10-002), session forgery enables account creation with attacker-chosen email, name, and role.
- **Impact**: Account impersonation with any email (including government addresses), privilege escalation chain to admin, mass account creation.
- **Key Code Reference**: `modules/auth/oauth.py:58-61` (session store), `oauth.py:110-135` (select_role_view)
- **Adversarial Review**: CONFIRMED

### p10-006 — Open Redirect in Admin Review Actions
- **Severity**: HIGH
- **Summary**: Admin review actions use `request.args.get('next')` to determine post-action redirect without URL validation.
- **Impact**: Admin credential phishing — attacker crafts link with `?next=http://evil.com` that redirects admin after approve/reject action.
- **Key Code Reference**: `modules/admin_core/content.py:111-112`
- **Adversarial Review**: CONFIRMED

### p10-007 — IDOR in Booking Status Update
- **Severity**: HIGH
- **Summary**: Any user with role `admin`, `contributor`, or `business_owner` can modify the status of ANY reservation by ID. No ownership verification. Developer comment at line 152 explicitly acknowledges: *"Needs authorization checks in a real scenario to ensure this user owns the asset."*
- **Impact**: Cross-owner reservation manipulation, capacity fraud (cancel → free capacity → rebook), analytics corruption.
- **Key Code Reference**: `modules/booking/routes.py:128-165`
- **Adversarial Review**: CONFIRMED

### p10-009 — Inconsistent Auth Guard on /admin/visits/log
- **Severity**: HIGH
- **Summary**: `POST /admin/visits/log` has `@login_required` but no role check. Every sibling endpoint in the `/admin/visits/*` group checks `current_user.role`. Any authenticated `user`-role account can log arbitrary visitor data.
- **Impact**: Analytics pollution, inflated/deflated visitor counts, corrupted business metrics.
- **Key Code Reference**: `modules/admin_core/visits.py:567`
- **Adversarial Review**: CONFIRMED

### p10-012 — Open Redirect in Visit Log Handlers
- **Severity**: HIGH
- **Summary**: Visit log handlers use `request.form.get('next')` and `request.args.get('next')` for redirect target without URL validation.
- **Impact**: Credential phishing, session theft via open redirect from authenticated endpoints.
- **Key Code Reference**: `modules/admin_core/visits.py:611,620`
- **Adversarial Review**: CONFIRMED

### p10-018 — Redis KEYS DoS via Unauthenticated Cache Invalidation
- **Severity**: HIGH
- **Summary**: `POST /api/tiles/cache/invalidate` is unauthenticated and accepts user-controlled `z`, `x`, `y` parameters that default to `"*"` and are interpolated into a Redis `KEYS` pattern. Attacker constructs `mvt:attractions:*:*:*` causing O(N) Redis scan and mass cache deletion.
- **Impact**: Redis DoS (blocks event loop), cache stampede (DB load spike), sustained attack (10/hour rate limit still sufficient).
- **Key Code Reference**: `modules/core/map_routes.py:289-297`
- **Adversarial Review**: CONFIRMED

### p10-021 — Booking Slot Overbook TOCTOU
- **Severity**: HIGH
- **Summary**: `reserve_slot()` reads `available_capacity`, checks against `party_size`, then increments `booked_count` — without `SELECT FOR UPDATE`, `transaction.atomic()`, or conditional `UPDATE WHERE`. Two concurrent POSTs for the same slot both pass the capacity check, causing overbooking.
- **Impact**: Overbooking on a tourism system with limited daily capacity. No `CHECK` constraint in DB prevents `booked_count > total_capacity`.
- **Key Code Reference**: `modules/booking/routes.py:80-91`
- **Adversarial Review**: CONFIRMED

### p10-022 — Badge Unlock Race Condition
- **Severity**: HIGH
- **Summary**: `verify_checkin()` reads existing badges, computes new unlocks, and creates `UserPassport` rows without a database lock. Two concurrent check-ins both determine a new badge should unlock, both insert rows (no unique constraint on `(user_id, badge_id)`), resulting in duplicate badge unlocks with duplicate reward redemption.
- **Impact**: Duplicate promo code redemption, economic fraud, leaderboard manipulation.
- **Key Code Reference**: `modules/gamification/routes.py:185-217`
- **Adversarial Review**: CONFIRMED

---

### MEDIUM Findings

---

### p10-010 — Authenticated User Search Exposes PII
- **Summary**: `GET /auth/api/users/search?q=` returns `id`, `username`, `email`, and `barangay` for any matching user. Only `@login_required` — no role restriction. Any authenticated user can enumerate all registered users' PII.
- **Key Code Reference**: `modules/auth/api.py:5`

### p10-011 — Legacy Redirect `**request.args` Spread
- **Summary**: 10 legacy document redirect handlers use `**request.args` to forward query parameters to `url_for()`, enabling parameter injection into redirect URLs. Admin-only but enables parameter pollution and session fixation.
- **Key Code Reference**: `modules/admin_core/documents.py:13-76`
- **Variant Amplification**: p12-001/002/003 extend this pattern to **4 public unauthenticated endpoints** (attractions, barangay/events, map redirects).

### p10-013 — Socket.IO CORS Wildcard
- **Summary**: `cors_allowed_origins="*"` allows any origin to establish WebSocket connections. Cross-site WebSocket hijacking enables chat message interception.
- **Key Code Reference**: `app.py:84`

### p10-015 — ProxyFix Trust Bypass
- **Summary**: When `VERCEL` env var is set, ProxyFix trusts `X-Forwarded-*` headers from one proxy hop. If accessed directly (Docker deployment), attacker spoofs headers to bypass rate limiting and manipulate URL generation.
- **Key Code Reference**: `app.py:75-77`, `extensions.py:19-22`
- **Condition**: Only exploitable when application is directly accessible (not through Vercel).

### p10-016 — UPDATE_TOKEN Non-Constant-Time Comparison
- **Summary**: `require_update_token` uses Python `!=` operator for token comparison, enabling theoretical timing side-channel extraction. Chains with p10-008 (RCE).
- **Key Code Reference**: `modules/core/update_routes.py:37`

### p10-017 — Unauthenticated Map Feedback DB Write
- **Summary**: `POST /api/map-feedback` accepts JSON and writes a `MapFeedback` record directly to the database. No authentication, no CAPTCHA, no input sanitization. Enables spam campaigns.
- **Key Code Reference**: `modules/core/api_routes.py:97`

### p10-019 — Gamification Navigation Guard Bypass
- **Summary**: `POST /gamification/api/start-navigation` sets `session['active_nav']` to any `id`/`type` without server-side verification. Combined with browser geolocation spoofing, users earn check-ins and badges without physical presence.
- **Key Code Reference**: `modules/gamification/routes.py:86-90` (write), `routes.py:42-45` (guard)

### p10-020 — OAuth Missing State Parameter + CSRF on Role Selection
- **Summary**: Google OAuth flow does not implement `state` parameter per RFC 6749 §10.12. The `select_role_view()` POST handler lacks CSRF protection, allowing forced role selection.
- **Key Code Reference**: `modules/auth/oauth.py:55-68`, `oauth.py:110-135`

### p10-023 — Booking State Machine — Reversible Terminal States
- **Summary**: `update_status()` accepts any status regardless of current status. `attended→cancelled` frees consumed capacity. No state machine guard.
- **Key Code Reference**: `modules/booking/routes.py:138-161`

### p10-024 — Booking Reserve — No Idempotency
- **Summary**: `reserve_slot()` creates a new `Reservation` row and increments `booked_count` on every POST. No idempotency key, no unique constraint on `(user_id, booking_slot_id)`. Double-click creates duplicate reservations.
- **Key Code Reference**: `modules/booking/routes.py:57-91`

### p10-025 — Booking Status Update — No SELECT FOR UPDATE
- **Summary**: `update_status()` reads slot capacity for reactivation check and writes `booked_count` without `SELECT FOR UPDATE`. Concurrent status updates lose capacity changes.
- **Key Code Reference**: `modules/booking/routes.py:138-161`

### p10-026 — Password Reset Token TOCTOU
- **Summary**: `reset_password_view()` validates token (checks `used==False`), then sets `used=True` and commits. Two concurrent requests both pass the validity check before either commits.
- **Key Code Reference**: `modules/auth/password.py:72-88`

### p10-028 — Admin Approval GET Requests — No CSRF
- **Summary**: All admin approval/rejection handlers perform direct status assignment via HTTP GET (no CSRF protection). An attacker triggers them via `<img>` tags or link prefetching.
- **Key Code Reference**: `modules/admin_core/content.py:33,102,149`

### p10-029 — Gamification Check-in Duplicate Guard TOCTOU
- **Summary**: Duplicate check-in prevention uses a time-window query (`verified_at >= today`). Two concurrent requests both observe no existing check-in and both create records. No unique constraint on `(user_id, attraction_id, date)`.
- **Key Code Reference**: `modules/gamification/routes.py:178-187`

---

## Attack Chain Analysis

The findings compose several high-impact exploit chains:

### Chain 1: Unauthenticated RCE (Critical)
```
p10-002 (default SECRET_KEY)
  → p10-005 (forge OAuth session cookie with role=admin)
    → p10-008 (bypass /pull token when UPDATE_TOKEN unset)
      → subprocess.run(["git", "pull"]) + shutil.copy2()
        = Remote Code Execution
```
**Preconditions**: `SECRET_KEY` env var unset (default), `UPDATE_TOKEN` env var unset, attacker has network access.  
**Impact**: Full server compromise.

### Chain 2: API Key Theft (Critical)
```
p10-001 (GET /api/gemini/config — no auth)
  → Gemini API key extracted
    → Unauthorized API usage / GCP resource access
```
**Preconditions**: Network access only. No authentication required.

### Chain 3: Admin Account Takeover (High)
```
p10-006 OR p10-012 (open redirect ?next=evil.com)
  → Admin redirected to phishing page
    → Admin credentials harvested
      → Full admin access (all endpoints, heritage, booking, /pull)
```

---

## Attack Surface Summary

The attack surface is documented across multiple artifacts in [`piolium/attack-surface/`](attack-surface/):

| Artifact | Description | Key Statistics |
|----------|-------------|---------------|
| [knowledge-base-report.md](attack-surface/knowledge-base-report.md) | Full architecture model, DFD/CFD slices, threat model, dependency analysis | 14 trust boundaries, 20 attacker-controlled inputs, 15 attack scenarios |
| [authz-matrix.md](attack-surface/authz-matrix.md) | 187-endpoint × 5-role authorization matrix | 65 public + 6 missing-guard + 4 middleware-gap + 21 anomalous |
| [public-routes-authz-matrix.md](attack-surface/public-routes-authz-matrix.md) | Public-routes × role matrix with expected/actual scope | Expected vs actual access control gaps |
| [unauthenticated-surface.md](attack-surface/unauthenticated-surface.md) | 65 pre-authentication entry points | 10 flagged missing-guard/middleware-gap |
| [state-concurrency-summary.md](attack-surface/state-concurrency-summary.md) | 17 state-holding entities, zero locking primitives | 6 TOCTOU, 2 state-machine, 1 idempotency gap |
| [authz-coverage-gaps.md](attack-surface/authz-coverage-gaps.md) | 6 dynamic/unresolved endpoint authorization gaps | Routes not statically analyzable |
| [variant-summary.md](attack-surface/variant-summary.md) | 27 variant instances across 12 pattern families | Pattern amplification analysis |
| [source-sink-flows-all-severities.md](attack-surface/source-sink-flows-all-severities.md) | 18 source-to-sink flow paths, 11 hidden control channels | Taint propagation map |
| [spec-gap-summary.md](attack-surface/spec-gap-summary.md) | 6 framework contract violations | CSRF exemptions, proxy trust, session self-service |
| [patch-bypass-summary.md](attack-surface/patch-bypass-summary.md) | Advisory/patch bypass analysis | Dependency-specific attack paths |
| [advisory-summary.md](attack-surface/advisory-summary.md) | Security advisory collection | CVE-relevant dependencies |
| [sbom.json](attack-surface/sbom.json) | Software bill of materials | All dependencies with versions |

### Attack Pattern Families (6 Confirmed)

| Pattern | Registry ID | Instances | Severity Range |
|---------|------------|-----------|---------------|
| Fail-Open Secret Default | AP-001 | 4 | HIGH–CRITICAL |
| Debug/Dev Endpoint in Production | AP-002 | 1 | HIGH |
| IDOR — No Ownership Verification | AP-003 | 7 | MEDIUM–HIGH |
| CSRF / Open Redirect / Parameter Injection | AP-004 | 9 | MEDIUM–HIGH |
| Redis KEYS Pattern Injection | AP-005 | 3 | MEDIUM–HIGH |
| TOCTOU — Check-Then-Act Without Atomicity | AP-006 | 14 | MEDIUM–HIGH |

---

## Coverage Gaps

The following areas were identified as insufficiently covered by this audit or represent ongoing risk:

| Gap | Impact | Recommendation |
|-----|--------|---------------|
| **No DAST / dynamic testing** | Vulnerabilities only discoverable at runtime (e.g., actual session forgery, debugger activation) may exist | Add OWASP ZAP or similar automated DAST scanning |
| **No dependency vulnerability scanning** | Known CVEs in transitive dependencies undetected | Integrate `pip-audit` or `safety` in CI/CD |
| **No security test suite** | Regression risk — findings may be reintroduced | Add automated tests for auth, CSRF, XSS, SQLi, IDOR |
| **No session revocation mechanism** | Stale sessions persist after password change or account compromise | Add session invalidation on password change, add token blacklist |
| **No rate limiting on auth endpoints beyond login** | Password reset, registration, OAuth flow lack per-endpoint rate limits | Add rate limiting to all authentication endpoints |
| **Gamification GPS verification is client-controlled** | Browser geolocation spoofing defeats the physical-presence requirement | Add server-side GPS trail validation, minimum navigation duration |
| **No audit logging** | Security events (failed auth, privilege escalation attempts) are not recorded | Implement security event logging with alerting |
| **No HTTPS enforcement on Docker deployment** | `ProxyFix` only active when `VERCEL` env var is set | Enforce HTTPS at reverse proxy level for Docker deployment |

---

## Methodology Notes

### Review Chamber Summary

| Metric | Value |
|--------|-------|
| Review Chambers spawned | 6 (secrets-misconfig, authz-access-control, csrf-cors-middleware, unauth-endpoints, concurrency-state, low-severity) |
| Hypotheses evaluated | 47 (30 from Phase 4 + 10 from Phase 5 + 13 from Phase 6 + 7 from Phase 8 − dedup) |
| Findings confirmed | 28 |
| Findings rejected | 19 (14 low-severity, 5 concurrency duplicates/weaknesses, 1 confirmed false positive) |
| False positives disproved | 1 (p10-014: CSRF JSON bypass — Flask-WTF 1.2.2 source code has no content-type exemption) |
| Attack patterns added to registry | 6 |
| Variant findings identified | 27 (Phase 12) |
| Cold verification reviews (P11-LITE) | 14 (all Critical/High) |

### Deduplication

The audit produced findings across 8 analysis phases (P4–P12). Deduplication was performed in the adversarial review chamber (P10):

- **47 raw findings** across phases P4, P5, P6, P7, P8
- **12 duplicate groups** identified (e.g., p4-001/p5-001 → p10-001; p4-015/p5-007/p8-001 → p10-008)
- **27 unique validated findings** surviving adversarial review
- **27 additional variant instances** (Phase 12) extending findings to new code locations
- **19 rejected** as false positives, low-severity, or subsumed by better analysis

### Dependency Verification

Cold verification of Critical/High findings included reading actual installed dependency source code:
- **Flask-WTF 1.2.2** `csrf.py`: Read to verify/disprove CSRF JSON exemption claim (p10-014 — DISPROVED)
- **Flask-Login 0.6.3**: Session regeneration behavior verified
- **SQLAlchemy 2.0.45**: Parameterized query behavior confirmed

### Scope and Limitations

- **In scope**: All application Python code, Flask routes, templates, WebSocket handlers, configuration
- **Out of scope**: Static assets (CSS/JS/images), database migrations, build tooling, Vercel deployment configuration, Supabase cloud infrastructure
- **Not tested**: Actual exploitation in production, social engineering, physical security, mobile client security
- **Environment**: Local development + Docker deployment analysis; no live production access

---

## Conclusion

The application has a **moderate-to-high risk profile**. While the codebase demonstrates awareness of security fundamentals (parameterized queries via SQLAlchemy, `secure_filename` for uploads, `@login_required` on most authenticated routes, CSRF protection via Flask-WTF, rate limiting via Flask-Limiter), systemic architectural weaknesses significantly undermine these controls.

The two Critical findings — API key leakage and the `/pull` endpoint RCE chain — require immediate remediation. The default `SECRET_KEY` issue is the single most impactful vulnerability because it undermines every session-based security control in the application and enables escalation of multiple High findings into RCE.

The systemic absence of concurrency primitives (zero `SELECT FOR UPDATE`, zero `transaction.atomic()`, zero unique constraints on junction tables) creates a class of TOCTOU vulnerabilities across the booking, gamification, and password reset subsystems. These cannot be fixed individually — they require an architectural change to introduce database-level locking or optimistic concurrency control.

The open redirect and `**request.args` spread patterns affect both admin-only and public unauthenticated endpoints, creating a phishing surface that targets the most privileged users (admins) and the most exposed surface (anonymous visitors).

**Priority remediation order**:
1. **Immediate**: Set required `SECRET_KEY` and `UPDATE_TOKEN` environment variables (fail-closed). Remove `/api/gemini/config` endpoint.
2. **Immediate**: Add ownership verification to booking status updates. Add role check to `/admin/visits/log`.
3. **Short-term**: Replace Redis `KEYS` with `SCAN`. Remove `**request.args` from all redirects. Add `next` parameter validation.
4. **Medium-term**: Introduce `SELECT FOR UPDATE` or optimistic locking for all capacity/state mutations. Add unique constraints to junction tables. Restrict Socket.IO CORS origins.
5. **Ongoing**: Add security test suite, DAST scanning, dependency vulnerability scanning, and audit logging.

---

*Report generated by piolium audit system — Phase 15 (Final Report Assembly)*  
*Audit ID: 2026-08-18T03:05:25.733Z | Mode: deep | Run: p15-2026-08-18T03-05-25-733Z-a1-7917cba3*
