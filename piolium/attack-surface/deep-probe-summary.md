# Deep Probe Summary: Manual Attack Surface (P8)

> **Generated**: 2026-08-18 (P8 Manual Probe)  
> **Repository commit**: 30bc3e7f  
> **Mode**: deep — single-team probe  
> **Probes conducted**: 7 findings verified with file:line evidence

---

## Status

**Status**: complete  
**Probe type**: Manual code-level verification + new finding discovery  
**Focus**: Highest-impact slices from KB report, P3-P7 artifacts, and candidates summary

## Findings Summary

| # | ID | Title | Severity | New/Superseding | Verified |
|---|-----|-------|----------|-----------------|----------|
| 1 | p8-001 | `/pull` Token Bypass → RCE via git pull + file copy | **CRITICAL** | Supersedes p5-007, p4-015 | ✓ |
| 2 | p8-002 | Redis KEYS DoS via Cache Invalidation Wildcard Pattern | **HIGH** | **NEW** | ✓ |
| 3 | p8-003 | IDOR in Booking Status Update — No Ownership Verification | **HIGH** | Supersedes p4-006, p5-004 | ✓ |
| 4 | p8-004 | Legacy Redirects Pass Unvalidated `**request.args` | **MEDIUM** | **NEW** | ✓ |
| 5 | p8-005 | Gamification Navigation Guard Bypass via Session Self-Service | **MEDIUM** | Supersedes p4-018, p5-006, p7-002 | ✓ |
| 6 | p8-006 | CSRF JSON Content-Type Bypass on Unauthenticated Write Endpoints | **MEDIUM** | Supersedes p7-001 | ✓ |
| 7 | p8-007 | OAuth Session Trust Chain — Default SECRET_KEY → Account Creation | **MEDIUM** | Supersedes p4-014, p7-003 | ✓ |

### Counts
- **CRITICAL**: 1 (p8-001)
- **HIGH**: 2 (p8-002, p8-003)
- **MEDIUM**: 4 (p8-004, p8-005, p8-006, p8-007)
- **New findings**: 2 (p8-002, p8-004)
- **Superseded/ strengthened**: 5

## New Discoveries (Not in P3-P7)

### 1. Redis KEYS DoS (p8-002)
**Why it was missed**: Prior phases documented the cache invalidation endpoint as "unauthenticated write" (p5-003) and "CSRF bypass" (p7-001), but did not analyze the Redis `KEYS` command usage or the wildcard pattern injection via user-controlled `z`/`x`/`y` parameters. The `KEYS` command is a well-known Redis anti-pattern (O(N) blocking operation), but the connection between user-controlled parameters and the `KEYS` glob pattern was not traced.

**Impact escalation**: The prior finding (p5-003) rated this as "HIGH — cache stampede DoS". The actual impact is higher because:
- Redis `KEYS` blocks the event loop (affects all Redis clients, not just tile serving)
- The wildcard injection allows targeting ALL cached tiles with a single request
- Combined with CSRF JSON bypass (p8-006), this is exploitable from any website

### 2. Legacy Redirect `**request.args` (p8-004)
**Why it was missed**: Prior phases identified open redirect patterns via `request.args.get("next")` (FLOW-01, FLOW-02) but did not examine the `**request.args` spread pattern in the legacy document redirect handlers. The `**request.args` pattern is more subtle — it doesn't create an open redirect but injects arbitrary query parameters into the destination URL.

**Impact**: Medium — parameter pollution, potential for session manipulation via query strings, and attack surface amplification for target handlers that read `request.args`.

## Cross-Chain Analysis

### Chain-1: SECRET_KEY Default → Session Forgery → Admin Account → RCE
```
p8-007 (OAuth session trust, default SECRET_KEY)
  → Forge session with role=admin email
  → _create_google_user() → admin account created
  → Login as admin
  → p8-001 (/pull token bypass when UPDATE_TOKEN unset)
  → subprocess.run(["git", "pull"]) → RCE
```
**Combined severity**: CRITICAL → CRITICAL (chain amplifies from account creation to RCE)

### Chain-2: CSRF Bypass → Redis DoS → Cache Stampede → DB Overload
```
p8-006 (CSRF JSON bypass on unauthenticated endpoints)
  → POST /api/tiles/cache/invalidate with JSON body
  → p8-002 (Redis KEYS DoS with wildcard pattern)
  → All cached tiles wiped
  → 2000/min tile requests hit PostGIS
  → Database overload → potential DoS
```
**Combined severity**: MEDIUM + HIGH = HIGH (CSRF amplifies the DoS impact)

### Chain-3: IDOR → Capacity Manipulation → Double-Booking
```
p8-003 (Booking IDOR, no ownership check)
  → Business_owner A cancels Business_owner B's reservation
  → slot.booked_count decremented
  → Concurrent request re-activates same reservation
  → slot.booked_count incremented
  → Total bookings exceed capacity
```
**Combined severity**: HIGH (IDOR + race condition)

## Verification Method

All findings were verified by:
1. **Reading source files** in full (update_routes.py, map_routes.py, booking/routes.py, admin_core/documents.py, gamification/routes.py, oauth.py, config.py, api_routes.py)
2. **Grep-based evidence extraction** with context lines confirming exact file:line locations
3. **Cross-referencing** with KB report DFDs, source-sink flows, and authz matrix
4. **Code path tracing** from entry point to sink for each finding

## Relation to Prior Phases

| Prior Phase | Finding ID | P8 Relationship |
|-------------|-----------|-----------------|
| P4 SAST | p4-015 (command execution) | p8-001 strengthens with exact bypass path |
| P4 SAST | p4-006 (IDOR booking) | p8-003 strengthens with code path + race condition |
| P4 SAST | p4-014 (OAuth session) | p8-007 strengthens with forge→create chain |
| P5 AuthZ | p5-003 (cache invalidation) | p8-002 is **NEW** — Redis KEYS DoS not identified |
| P5 AuthZ | p5-004 (booking IDOR) | p8-003 strengthens with ownership gap + race |
| P5 AuthZ | p5-006 (session nav bypass) | p8-005 strengthens with full attack chain |
| P5 AuthZ | p5-007 (update token bypass) | p8-001 **supersedes** with RCE chain |
| P6 State | p6-005 (booking no idempotency) | p8-003 confirms with capacity race condition |
| P7 Spec-gap | p7-001 (CSRF JSON bypass) | p8-006 strengthens with specific endpoint enumeration |
| P7 Spec-gap | p7-003 (OAuth missing state) | p8-007 **supersedes** with session forgery chain |
| P7 Spec-gap | p7-005 (update token timing) | p8-001 supersedes — bypass is more impactful than timing |

## Recommendations (Priority Order)

1. **CRITICAL**: Make `UPDATE_TOKEN` required — fail closed if env var not set (p8-001)
2. **CRITICAL**: Make `SECRET_KEY` required — fail if env var not set (p8-007, chains to p8-001)
3. **HIGH**: Add `@login_required` to `/api/tiles/cache/invalidate` + sanitize z/x/y to numeric only (p8-002)
4. **HIGH**: Add ownership verification to `/booking/api/admin/update_status` (p8-003)
5. **MEDIUM**: Remove `**request.args` from all legacy document redirects (p8-004)
6. **MEDIUM**: Add server-side navigation verification for gamification (p8-005)
7. **MEDIUM**: Add explicit CSRF validation for JSON state-changing endpoints (p8-006)
8. **MEDIUM**: Re-verify Google token in `select_role_view` (p8-007)

---

**Artifacts produced**:
- `piolium/attack-surface/manual-attack-surface-inventory.md`
- `piolium/findings-draft/p8-001-pull-token-bypass-rce.md`
- `piolium/findings-draft/p8-002-redis-keys-dos-cache-invalidation.md`
- `piolium/findings-draft/p8-003-idor-booking-status-update.md`
- `piolium/findings-draft/p8-004-legacy-redirect-args-spread.md`
- `piolium/findings-draft/p8-005-gamification-navigation-bypass.md`
- `piolium/findings-draft/p8-006-csrf-json-bypass-unauth-endpoints.md`
- `piolium/findings-draft/p8-007-oauth-session-trust-default-secret.md`
- `piolium/attack-surface/deep-probe-summary.md`
