# Tourist App — React Native Migration Plan

## Overview

A **city guide + itinerary companion** for tourists visiting a destination. Core value: **discover, plan, navigate, and remember** — all in one offline-capable app.

---

## Feature Set

### 1. **Discover** (home feed)
- GPS-based feed of nearby attractions, restaurants, cafes, hidden gems
- Categories: History, Food, Nature, Art, Shopping, Nightlife
- Each item: photo, rating, distance, quick description, open hours
- "Near me now" + "Popular today" tabs

### 2. **Itinerary Builder**
- Drag-and-drop day planner
- Auto-suggests optimal routes (minimize backtracking)
- Time-aware: shows what's open now, alerts before closing
- Share itinerary with travel companions

### 3. **Map & Navigate**
- Offline maps (download city packs)
- Walking directions, public transport info
- Custom markers: saved spots, itinerary pins, photo spots
- "Show me the nearest [coffee/restroom/ATM/pharmacy]"

### 4. **Local Info Hub**
- Emergency numbers (police, ambulance, embassy)
- Currency + tipping customs
- Cultural dos/don'ts
- Public transport guide (cards, apps, routes)
- Visa/entry requirements summary

### 5. **Translation**
- Camera translate (signs, menus)
- Phrasebook with audio pronunciation
- Favorites/saved phrases

### 6. **Budget Tracker**
- Log expenses by category
- Currency conversion (live rates)
- Daily/total spending overview

### 7. **Memory Book**
- Photo journal with location tags
- Notes per day
- Export as PDF/share to social

### 8. **Social**
- Follow friends' itineraries
- Tips/reviews from other tourists
- "Ask a local" Q&A (or AI chatbot for instant answers)

---

## Architecture

```
┌─────────────────────────────────────────┐
│              React Native App           │
├─────────────────────────────────────────┤
│  Screens:                               │
│  ├── Home (Discover feed)               │
│  ├── Map (offline-capable)              │
│  ├── Itinerary (day planner)            │
│  ├── Place Detail (reviews, photos)     │
│  ├── Local Info (emergency, customs)    │
│  ├── Translate (camera + phrasebook)    │
│  ├── Budget (expense tracker)           │
│  ├── Memory Book (journal)              │
│  └── Profile / Settings                 │
├─────────────────────────────────────────┤
│  State: Zustand (light, fast)           │
│  Navigation: React Navigation           │
│  Maps: react-native-maps + offline tiles│
│  Storage: SQLite (offline) + Firebase   │
│  Auth: Firebase Auth (Google/Apple)     │
│  API: Firebase Functions / Express      │
└─────────────────────────────────────────┘
```

---

## Data Flow

```
User opens app
    ↓
GPS location acquired → fetch nearby places (or load offline cache)
    ↓
User taps "Add to itinerary" → saved to local SQLite
    ↓
User opens Map → shows itinerary pins + nearby
    ↓
User taps place → detail screen (reviews, hours, photos)
    ↓
Offline? → app works from cached data, syncs when back online
```

---

## Offline Strategy

- Download **city packs** (tiles + place data) before trip
- SQLite stores: places, itineraries, expenses, journal entries
- Sync queue: pending reviews/photos upload when online
- Maps use pre-downloaded OSM tiles (no Google dependency)

---

## Tech Choices

| Layer | Choice | Why |
|-------|--------|-----|
| Framework | React Native (Expo) | Cross-platform, fast dev |
| Navigation | React Navigation 6 | Mature, bottom tabs + stack |
| State | Zustand | Minimal, no boilerplate |
| Maps | react-native-maps + OSMDroid | Offline support, free |
| Local DB | SQLite (expo-sqlite) | Offline-first, reliable |
| Backend | Firebase (auth, functions, storage) | Quick setup, scales |
| Cache | AsyncStorage + file system | City packs, images |
| i18n | i18next | Multi-language support |

---

## MVP Scope (v1)

1. ✅ Discover feed (hardcoded city data → later API)
2. ✅ Place detail screen
3. ✅ Itinerary builder (local only)
4. ✅ Basic map with pins
5. ✅ Local info page (static content)
6. ✅ Budget tracker
7. ❌ Translation (v2)
8. ❌ Social features (v2)
9. ❌ Memory book (v2)

---

## Workflow

1. **Scaffold** Expo project, set up navigation
2. **Build** Home screen + Place detail
3. **Build** Itinerary screen (SQLite CRUD)
4. **Add** Map with markers
5. **Add** Local info (static data)
6. **Add** Budget tracker
7. **Polish** offline mode, error handling
8. **Test** on device, optimize performance
9. **Ship** v1 to Play Store

---

## File Structure (Proposed)

```
tourist-app/
├── app/                    # Expo Router screens
│   ├── (tabs)/
│   │   ├── index.tsx       # Home/Discover
│   │   ├── map.tsx         # Map view
│   │   ├── itinerary.tsx   # Day planner
│   │   ├── budget.tsx      # Expense tracker
│   │   └── profile.tsx     # Settings
│   ├── place/[id].tsx      # Place detail
│   └── local-info.tsx      # Emergency, customs, etc.
├── components/
│   ├── PlaceCard.tsx
│   ├── ItineraryItem.tsx
│   ├── ExpenseRow.tsx
│   └── MapMarker.tsx
├── lib/
│   ├── db.ts               # SQLite setup + queries
│   ├── places.ts           # Place data / API calls
│   ├── offline.ts          # City pack download
│   └── sync.ts             # Online sync queue
├── assets/
│   └── city-packs/         # Offline map tiles
└── package.json
```
