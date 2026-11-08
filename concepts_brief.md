# Refined Fix Plan: Municipal Data Seeding, Chat Onboarding, Map Fallbacks, and Form Accessibility

* **Author:** jemhakdog & EGM Synthesizer Swarm
* **Date:** 2026-11-08
* **Status:** Ready for Implementation

## Executive Summary

Live end-to-end testing via Chrome DevTools across all 4 user roles (Tourist, Business Owner, Contributor, Administrator) identified 4 operational and rendering gaps:
1. Empty database tables (`ATTRACTION`, `ESTABLISHMENT`, `EVENT`, and incomplete `BARANGAY_INFO`), causing blank directories and empty admin dashboards.
2. Incomplete fallback in `/map`, which overrides coordinates with an empty array when `/api/map` returns `[]`.
3. Inability for tourists to view or join chat rooms on `/chat` due to participant-only filtering.
4. Missing `id` and `name` attributes on form inputs (specifically the newsletter subscription form).

A multi-lens technical review by the Goldfish swarm uncovered that `DEFAULT_PLACES` was previously omitted from `components/map/data.ts`. This plan provides the exact code changes and idempotent seeding procedures needed to fix all issues cleanly.

---

## Step-by-Step Implementation Milestones

### Milestone 1: Export `DEFAULT_PLACES` (`frontend/src/components/map/data.ts`)
- Build and export `DEFAULT_PLACES: MarkerPlace[]` derived from the 7 canonical landmarks in `CURATED_ATTRACTION_METADATA` and `CURATED_TRAILS`:
  1. Manleluag Spring Protected Landscape (Nature, Malabobo, [15.6667, 120.2833])
  2. Daang Kalikasan (Nature, Malabobo, [15.7000, 120.2500])
  3. St. Raymund de Peñafort Church (Historical, Poblacion, [15.7889, 120.2986])
  4. Timmanguyob Falls (Nature, Cabaluyan, [15.6833, 120.2667])
  5. Pacalat River (Nature, Poblacion, [15.7891, 120.2928])
  6. Canding (Kanding) Falls (Nature, Poblacion, [15.7891, 120.2928])
  7. Municipal Town Plaza (Public Space, Poblacion, [15.7885, 120.2960])

### Milestone 2: Resilient Map Fallback (`frontend/src/app/map/page.tsx`)
- Update `loadMarkers` to use `DEFAULT_PLACES`:
  ```typescript
  const data = await fetchAPI<{ markers: MarkerPlace[] }>("/api/map");
  setAllMarkers(data.markers && data.markers.length > 0 ? data.markers : DEFAULT_PLACES);
  ```
- In the `catch` block, fall back to `DEFAULT_PLACES` as well instead of leaving markers empty:
  ```typescript
  } catch (err) {
    console.error("Failed to load map markers:", err);
    setAllMarkers(DEFAULT_PLACES);
    setError(null);
  }
  ```

### Milestone 3: Public Chat Room Listing & Messaging (`backend/app/api/chat.py` & Frontend)
- In `backend/app/api/chat.py`:
  - Update `list_rooms` to return rooms where `ChatParticipant.user_id == user.id` OR `ChatRoom.type.in_(["public", "general", "barangay"])`.
  - Add descriptive naming:
    ```python
    name = r.barangay.name + " Community" if r.barangay else ("General Visitor Desk" if r.type in ("public", "general") else f"Room {r.id}")
    ```
  - In `get_room_messages` and `send_message`, update authorization to permit access if `is_participant or room.type in ("public", "general", "barangay")`.
- In `frontend/src/app/chat/page.tsx`:
  - Ensure room cards have click handlers navigating to room views: `onClick={() => router.push(`/chat/${room.id}`)}`.

### Milestone 4: Form Accessibility Attributes (`frontend/src/components/public/newsletter-subscribe.tsx`)
- Update the newsletter `<Input>` field with `id="newsletter-email"`, `name="email"`, and `aria-label="Email address for newsletter"`.

### Milestone 5: Idempotent Database Seeding Script (`backend/scripts/seed_initial_data.py`)
- Author an async Python script `.venv/bin/python -m backend.scripts.seed_initial_data`:
  - Ensures a system admin user exists (`admin@mangatarem.gov.ph`).
  - Populates all 82 official barangays into `BARANGAY_INFO`.
  - Seeds the 7 canonical attractions with status `"approved"`.
  - Seeds 3 standard establishments linked to `admin.id` with status `"approved"`.
  - Seeds 3 seasonal events with status `"approved"`.
  - Seeds the "General Community & Visitor Desk" public chat room.

### Milestone 6: Verification via DevTools
- Run `backend/scripts/seed_initial_data.py`.
- Verify `/map` renders 7 markers with active popups.
- Verify `/admin` displays seeded counts.
- Verify `/chat` displays the General Visitor Desk and barangay rooms.
- Verify 0 accessibility warnings in DevTools console.
