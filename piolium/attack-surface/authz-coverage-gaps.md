# Authorization Coverage Gaps

> **Generated**: 2026-08-18  
> **Phase**: 6 — Authorization & Access Control

## Endpoints Requiring Manual Chamber Review

The following endpoints have **Expected Scope = unknown** or involve framework-specific behavior that the systematic enumeration could not fully verify. Phase 10 chambers must review these.

| # | Endpoint | Issue | Recommendation |
|---|----------|-------|----------------|
| 1 | `/auth/api/users/search` | Authenticated user can search other users' PII (email, barangay) without any authorization beyond `@login_required`. No role restriction. | Verify if this should be admin-only or if it exposes excessive PII. |
| 2 | WebSocket `connect` event | Anonymous connections allowed; per-event auth in `join`/`send_message` but no transport-level auth. `leave` event has no auth at all. | Verify if anonymous WebSocket access is required or if it should be restricted. |
| 3 | `/pull` endpoint | Admin + token check, but token validation is conditional on `UPDATE_TOKEN` env var. If unset, any admin can trigger `git pull` + file copy. | Verify if this is intentional for development or a production risk. |
| 4 | `debug=True` in `app.py:135` | Werkzeug interactive debugger is enabled when running via `python app.py`. Combined with the `/pull` endpoint and default admin credentials, this could enable RCE. | Verify if debug mode is gated by environment. |
| 5 | `/auth/select-role` | Session-stored `oauth_signup` data is trusted without re-verifying the Google token. An attacker who controls the session can set arbitrary user identity data. | Verify if session forging is possible (depends on SECRET_KEY strength). |
| 6 | `ProxyFix` in `app.py:42` | On Vercel, `X-Forwarded-For` is trusted for rate limiting. If the app runs outside Vercel, an attacker can spoof IP addresses and bypass rate limits. | Verify if the Vercel env var is always set in production. |

## Dynamic / Reflection-Based Endpoints

No dynamically-registered or reflection-based routes were detected. All routes are explicitly defined via Flask Blueprints and `add_url_rule()`. The codebase does not use:
- Flask plugin-based auto-discovery
- `@app.before_request` for routing (only for session permanence)
- Dynamic Blueprint registration from database/config

## WebSocket Event Handlers

| Event | Handler | Auth Pattern | Coverage Status |
|-------|---------|--------------|-----------------|
| `connect` | `sockets.py:handle_connect` | None (anonymous allowed) | Covered — see p5-005 |
| `disconnect` | `sockets.py:handle_disconnect` | None | Covered — no auth needed |
| `join` | `sockets.py:on_join` | In-handler auth check | Covered — partial (barangay auto-join) |
| `send_message` | `sockets.py:handle_send_message` | In-handler auth check | Covered |
| `typing` | `sockets.py:handle_typing` | In-handler auth check | Covered |
| `leave` | `sockets.py:on_leave` | **None** | Covered — no auth needed for leaving |

## Notes on Probe Corroboration

No `probe-workspace/*/probe-summary.md` files were found. Phase 6 findings are independently derived from source code analysis. If Phase 5 Deep Probe later emits authz-adjacent hypotheses for the same endpoints, the following overlap is expected:

- `p5-001` (Gemini API key) may overlap with any probe finding on `api_routes.py`
- `p5-004` (booking IDOR) may overlap with p4-006 (`p4-006-idor-booking-status.md`) which was filed in Phase 4 SAST. Phase 6 filing is retained because it provides the complete guard-stack analysis.
- `p5-005` (WebSocket CORS) may overlap with p4-010 (`p4-010-websocket-cors-wildcard.md`)
- `p5-009` (inconsistent guard on `/admin/visits/log`) is uniquely discovered in Phase 6 systematic sweep — no SAST or probe overlap expected
