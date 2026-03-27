# High Concurrency Map Architecture Plan

## Overview
This plan adapts the "1 million concurrent user" map strategy for the Mangatarem Cultural Map. The focus is on handling high read-volumes of geospatial data while staying within the constraints of Vercel's serverless free tier. The primary shift involves moving from sending GeoJSON payloads to generating Mapbox Vector Tiles (MVT) directly in Supabase (PostGIS) and caching them heavily on Vercel's CDN and a Serverless Redis instance (like Upstash).

## Project Type
WEB

## Success Criteria
- Map load and interaction feel instantaneous (under 200ms) even with large numbers of points.
- Mapbox Vector Tile (.pbf) endpoints replace existing GeoJSON endpoints.
- Database load is heavily reduced; most map interaction reads are served via Vercel Edge Cache or Redis.
- Documentation accurately reflects Mapbox usage instead of Leaflet.js.

## Tech Stack
- **Frontend**: Mapbox GL JS (confirmed by user)
- **Backend / Delivery**: Flask on Vercel Serverless (Proxy)
- **Database**: Supabase / PostgreSQL with PostGIS extension (`ST_AsMVT` generation)
- **Caching**: Vercel Edge Caching (Primary) + Upstash Redis (Secondary for dynamic hot-data)

## File Structure
```
.
├── routes/
│   └── api/
│       └── map_routes.py     # New MVT tile endpoints
├── utils/
│   └── tile_generator.py     # PostGIS ST_AsMVT SQL handlers
├── docs/
│   ├── api_reference.md      # Update docs for MVT
│   ├── architecture.md       # Reflect Mapbox over Leaflet
│   └── PLAN-map-concurrency.md
```

## Task Breakdown

### Task 1: Update Frontend Documentation & Architecture
- **Agent**: `frontend-specialist`
- **Skills**: `writing-docs`
- **Priority**: P1
- **Dependencies**: None
- **INPUT**: `README.md` and user confirmation of Mapbox transition.
- **OUTPUT**: Updated `README.md` and `docs/architecture.md` indicating Mapbox GL JS usage instead of Leaflet.js.
- **VERIFY**: Check docs strings; no mentions of "Leaflet.js".

### Task 2: Implement PostGIS Vector Tile (.pbf) Endpoint
- **Agent**: `backend-specialist`
- **Skills**: `database-design`, `api-patterns`
- **Priority**: P0
- **Dependencies**: Task 1
- **INPUT**: Existing data and Flask routes.
- **OUTPUT**: A new Flask route `/tiles/<int:z>/<int:x>/<int:y>.pbf` using SQLAlchemy to execute `ST_AsMVT` functions.
- **VERIFY**: Fetch `/tiles/10/500/500.pbf` and receive `application/x-protobuf` binary data.

### Task 3: Setup Serverless Redis Caching (Upstash) Layer
- **Agent**: `backend-specialist`
- **Skills**: `performance-profiling`
- **Priority**: P1
- **Dependencies**: Task 2
- **INPUT**: MVT Endpoint from Task 2.
- **OUTPUT**: Redis caching layer utilizing Upstash (`upstash-redis` or equivalent) that caches generated tiles before executing DB queries.
- **VERIFY**: Second request to identical tile endpoint is served from Redis (response time < 50ms) without querying Supabase.

### Task 4: Integrate Vercel HTTP Cache Headers (Edge Caching)
- **Agent**: `devops-engineer`
- **Skills**: `deployment-procedures`
- **Priority**: P1
- **Dependencies**: Task 2
- **INPUT**: Tile endpoint in `map_routes.py`
- **OUTPUT**: Update Flask response headers (`Cache-Control: public, s-maxage=3600, stale-while-revalidate=86400`).
- **VERIFY**: Curl endpoint returns appropriate `Cache-Control` header.

### Task 5: Refactor Frontend Mapbox Source to Use MVT
- **Agent**: `frontend-specialist`
- **Skills**: `frontend-design`
- **Priority**: P2
- **Dependencies**: Task 2, Task 4
- **INPUT**: Mapbox implementation in UI.
- **OUTPUT**: Frontend `addSource` uses `type: 'vector'` instead of `geojson`, fetching from the new `.pbf` tile paths.
- **VERIFY**: Browsing the map triggers `/tiles/{z}/{x}/{y}.pbf` network requests instead of `data.json`.

## ✅ PHASE X COMPLETE
- Lint: [ ] Pass
- Security: [ ] No critical issues
- Build: [ ] Success
- Date: [Pending]
