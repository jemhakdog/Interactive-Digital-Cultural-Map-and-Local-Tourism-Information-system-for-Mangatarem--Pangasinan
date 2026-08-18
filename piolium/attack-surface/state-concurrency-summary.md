# State & Concurrency Audit Summary

> **Generated**: 2026-08-18
> **Repository**: jemhakdog/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan
> **Commit**: 30bc3e7f
> **Phase**: P6 — State & Concurrency

---

## Overview

This audit examined every state-mutating code path in the repository for temporal ordering violations (TOCTOU), missing atomicity, state machine violations, double-submit races, idempotency gaps, and lost-update bugs. The codebase runs on Flask + SQLAlchemy 2.0 + PostgreSQL (Supabase) with eventlet for WebSocket support.

**Critical finding**: The codebase contains **zero concurrency primitives** — no `SELECT FOR UPDATE`, no `transaction.atomic()`, no advisory locks, no distributed locks, no `asyncio.Lock`, no `threading.Lock`. Every state mutation is a plain read-then-write pattern with no isolation guarantees beyond PostgreSQL's default READ COMMITTED isolation level.

---

## State-Holding Entities Catalogued

| # | Table | State Columns | Mutation Handlers |
|---|-------|---------------|-------------------|
| 1 | `RESERVATION` | `status` (pending/confirmed/cancelled/attended/no-show) | `reserve_slot()`, `update_status()`, `verify_arrival()` |
| 2 | `BOOKING_SLOT` | `booked_count` (counter) | `reserve_slot()`, `update_status()` |
| 3 | `USER` | `is_approved`, `role`, `reset_token_used` | `approve_user()`, `register_view()`, `reset_password_view()` |
| 4 | `TOURIST_CHECK_IN` | `verified_at` (dedup key) | `verify_checkin()` |
| 5 | `USER_PASSPORT` | `badge_id` (unlock state) | `verify_checkin()` (badge unlock) |
| 6 | `ESTABLISHMENT` | `rating_avg`, `review_count` (counters) | `approve_establishment_review()` |
| 7 | `GALLERY_ITEM` | `status` (pending/approved) | `approve_gallery()`, `reject_gallery()` |
| 8 | `EVENT` | `status` (pending/approved) | `approve_event()`, `reject_event()` |
| 9 | `ANNOUNCEMENT` | `status` (pending/approved/rejected) | `admin_approve_announcement()`, `admin_reject_announcement()` |
| 10 | `REVIEW` | `status` (pending/approved) | `approve_review()`, `reject_review()` |
| 11 | `HERITAGE_PROFILE` | `status` (pending/approved) | `admin_heritage_add()` (auto-approve) |
| 12 | `VISITOR_LOG` | `visit_date` (dedup window) | `verify_arrival()`, `log_visitor()` |
| 13 | `BUSINESS_VERIFICATION` | `status` (pending/approved/rejected) | `approve_merchant_verification()`, `reject_merchant_verification()` |
| 14 | `CHAT_MESSAGE` | `id` (auto-increment, no dedup) | `handle_send_message()` |
| 15 | `NEWSLETTER_SUBSCRIBER` | `is_active` (subscribe/unsubscribe) | `subscribe()` |
| 16 | `MAP_FEEDBACK` | `status` (pending/resolved/dismissed) | unauthenticated writes |
| 17 | `ACHIEVEMENT_BADGE` | `target_locations` (read-only) | (read by badge unlock) |

---

## Concurrency Primitives Observed

| Primitive | Count | Notes |
|-----------|-------|-------|
| `threading.Lock` / `RLock` | 0 | — |
| `asyncio.Lock` | 0 | — |
| `multiprocessing.Lock` | 0 | — |
| `SELECT FOR UPDATE` | 0 | — |
| `transaction.atomic()` | 0 | — |
| Advisory locks (`pg_advisory_lock`) | 0 | — |
| Isolation level overrides | 0 | — |
| Distributed locks (Redis/ZooKeeper) | 0 | — |
| `async-mutex` / `p-queue` | 0 | — |
| `UniqueConstraint` on state entities | 2 | `BOOKING_SLOT(bookable_asset_id, date)`, `RESERVATION.qr_code_token` |

**Total concurrency primitives: 0**

---

## Idempotency Infrastructure

| Channel | Idempotency Key | Dedup Mechanism | Status |
|---------|----------------|-----------------|--------|
| Booking reserve | None | None | **ABSENT** |
| Booking status update | None | None | **ABSENT** |
| Gamification check-in | None | Time-window filter (same day) | **WEAK** (TOCTOU) |
| Newsletter subscribe | None | Unique email constraint only | **WEAK** (TOCTOU) |
| Password reset | None | Token `used` flag (non-atomic) | **WEAK** (TOCTOU) |
| Chat message | None | None | **ABSENT** |
| Visitor log | None | Time-window filter (same day) | **WEAK** (TOCTOU) |
| Registration | None | Unique username/email constraint only | **WEAK** (TOCTOU) |
| Admin approval (all entities) | None | None | **ABSENT** |
| Webhook/payment callbacks | N/A | N/A | No webhooks in codebase |

---

## Findings Filed

| ID | Title | Severity | Class |
|----|-------|----------|-------|
| p6-001 | TOCTOU — Booking slot capacity check-then-act | CRITICAL | toctou |
| p6-002 | TOCTOU — Badge unlock race via concurrent check-in | HIGH | toctou |
| p6-003 | State machine — reversible transitions from terminal states | HIGH | state-machine-violation |
| p6-004 | TOCTOU — Password reset token reuse | MEDIUM | toctou |
| p6-005 | Missing idempotency — booking reserve double-submit | HIGH | idempotency |
| p6-006 | Read-modify-write race — establishment rating | MEDIUM | rmw-no-txn |
| p6-007 | TOCTOU — Registration username/email duplicate check | MEDIUM | toctou |
| p6-008 | State machine — admin approval transitions lack guards | MEDIUM | state-machine-violation |
| p6-009 | TOCTOU — Gamification check-in duplicate guard | MEDIUM | toctou |
| p6-010 | Missing FOR UPDATE — booking status capacity adjustment | HIGH | missing-for-update |
| p6-011 | Double-submit — newsletter subscriber creation | MEDIUM | double-submit |
| p6-012 | TOCTOU — VisitorLog duplicate check on verify-arrival | MEDIUM | toctou |
| p6-013 | Double-submit — WebSocket message dedup | LOW | double-submit |

**Total drafts filed: 13**
- CRITICAL: 1
- HIGH: 4
- MEDIUM: 7
- LOW: 1

**Split by class:**
- toctou: 6
- state-machine-violation: 2
- idempotency: 1
- missing-for-update: 1
- rmw-no-txn: 1
- double-submit: 2

---

## Architectural Observations

### 1. Zero Concurrency Defenses

The most significant finding is systemic: **the entire application has zero concurrency defense mechanisms**. No `SELECT FOR UPDATE`, no `transaction.atomic()`, no advisory locks, no distributed locks. Every state mutation is an unprotected read-then-write.

This is not a collection of individual bugs — it is an architectural gap. The Flask + eventlet + SQLAlchemy stack provides no built-in concurrency guards; the application relies entirely on PostgreSQL's READ COMMITTED isolation, which does not prevent TOCTOU.

### 2. eventlet + SQLAlchemy Thread Safety

The application uses `eventlet` for WebSocket support (cooperative multitasking). While eventlet avoids true thread-level races (no preemption within a greenlet), it does NOT prevent TOCTOU races because:

- Each HTTP request runs in its own greenlet.
- SQLAlchemy sessions are per-request (scoped to the greenlet).
- Two concurrent requests sharing the same database session scope can interleave at `yield` points (I/O operations like `db.session.commit()`).

This means the TOCTOU findings are real even under eventlet's cooperative scheduling.

### 3. GET Methods for State Mutations

Multiple admin approval endpoints use HTTP GET for state-changing operations (approve, reject). This violates REST semantics and has concrete security implications:

- No CSRF protection on GET requests (Flask-WTF only checks POST/PUT/DELETE).
- Browser prefetching, `<img>` tags, and link crawlers can trigger approvals.
- This is a separate class of vulnerability from the concurrency issues but interacts with the state machine violations.

### 4. Missing CHECK Constraints

The database schema lacks critical CHECK constraints:

- `BOOKING_SLOT`: No `CHECK (booked_count <= total_capacity)` constraint. The counter can overflow.
- `BOOKING_SLOT`: No `CHECK (booked_count >= 0)` constraint. The counter can go negative.
- `RESERVATION`: No check constraint on valid status transitions.
- `USER_PASSPORT`: No unique constraint on `(user_id, badge_id)`.
- `TOURIST_CHECK_IN`: No unique constraint on `(user_id, attraction_id, date)`.

These constraints would serve as a safety net even if the application code has TOCTOU bugs.

### 5. Dual Commit Pattern

The `approve_establishment_review()` handler commits twice: once for the review status change, once for the rating recalculation. This creates two separate transaction windows, each independently vulnerable to lost-update races. This pattern should be consolidated into a single transaction.

---

## Recommendations (Priority Order)

1. **Immediate**: Add `CHECK (booked_count >= 0 AND booked_count <= total_capacity)` to `BOOKING_SLOT` as a safety net.
2. **Immediate**: Add `UniqueConstraint('user_id', 'badge_id')` to `USER_PASSPORT`.
3. **Short-term**: Wrap all booking capacity operations in `SELECT FOR UPDATE` or atomic conditional updates.
4. **Short-term**: Add state transition guards to all approve/reject endpoints.
5. **Short-term**: Change all approve/reject endpoints from GET to POST with CSRF.
6. **Medium-term**: Add idempotency keys to booking reserve endpoint.
7. **Medium-term**: Consolidate dual-commit patterns into single transactions.
8. **Long-term**: Implement a centralized state machine framework for all content moderation workflows.
