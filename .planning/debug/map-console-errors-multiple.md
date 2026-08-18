---
slug: map-console-errors-multiple
status: investigating
trigger: "Multiple console errors on map page: SW Response conversion failures, 401 Unauthorized on auth-gated APIs, Mapbox POST failures, place selection broken after select/cancel/refresh"
created: 2026-07-30
updated: 2026-07-30
tdd_mode: false
goal: find_and_fix
---

## Symptoms

- **Expected:** Map page loads cleanly with no console errors; place selection works after selecting, canceling, or refreshing
- **Actual:** Multiple console errors:
  1. `Uncaught (in promise) TypeError: Failed to convert value to 'Response'.` from sw.js:1 (3 occurrences)
  2. `POST http://localhost:5002/passport/api/stop-navigation 401 (UNAUTHORIZED)`
  3. `POST http://localhost:5002/booking/api/verify-arrival 401 (UNAUTHORIZED)` + `[Arrival Verification Error]`
  4. `POST https://events.mapbox.com/events/v2?... net::ERR_FAILED` (multiple)
  5. Place selection not available after selecting, canceling, or refreshing the browser
- **Error messages:** See above — all from browser console
- **Timeline:** First time seeing them. Map loads but has place selection bugs.
- **Reproduction:** Visit map page while logged out. Place selection breaks after select/cancel/refresh.
- **Auth state:** Logged out (anonymous/guest)

## Current Focus

- **Hypothesis:** SW catch handler returns non-Response value (undefined/cached mismatch); 401s are expected when logged out but client shouldn't call auth-gated endpoints; place selection bug may be related to SW caching stale state
- **Test:** Inspect sw.js fetch handler return paths, check auth-gated API call guards, check place selection JS logic
- **Expecting:** Find the SW code path that returns non-Response, find missing auth checks in client code, find place selection state management issue
- **Next action:** Gather initial evidence — read sw.js, map.js, and relevant route files

## Evidence

_(none yet)_

## Eliminated

_(none yet)_
