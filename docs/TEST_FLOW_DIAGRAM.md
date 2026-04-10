# MVT Testing Flow Diagram

## Testing Workflow Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    TESTING WORKFLOW                              │
└─────────────────────────────────────────────────────────────────┘

Phase 1: Database Setup
┌──────────────────────────────────────────────────────────────┐
│ 1. Enable PostGIS in Supabase                                │
│    ↓                                                         │
│ 2. Run schema_postgis.sql                                    │
│    ↓                                                         │
│ 3. Verify geometry columns & indexes                         │
│    ↓                                                         │
│ ✅ VERIFICATION: SELECT postgis_version()                    │
└──────────────────────────────────────────────────────────────┘
                            ↓
Phase 2: Backend Testing
┌──────────────────────────────────────────────────────────────┐
│ 1. Start Flask app (python app.py)                           │
│    ↓                                                         │
│ 2. Test /api/tiles/layers                                    │
│    ↓                                                         │
│ 3. Test /api/tiles/12/500/500.pbf                            │
│    ↓                                                         │
│ 4. Verify headers (Content-Type, Cache-Control)              │
│    ↓                                                         │
│ ✅ VERIFICATION: curl -I endpoint                            │
└──────────────────────────────────────────────────────────────┘
                            ↓
Phase 3: Frontend Testing
┌──────────────────────────────────────────────────────────────┐
│ 1. Open /map in browser                                      │
│    ↓                                                         │
│ 2. Check Network tab for .pbf requests                       │
│    ↓                                                         │
│ 3. Verify points visible on map                              │
│    ↓                                                         │
│ 4. Test hover/click interactions                             │
│    ↓                                                         │
│ ✅ VERIFICATION: Colored points, smooth interactions         │
└──────────────────────────────────────────────────────────────┘
                            ↓
Phase 4: Performance Testing
┌──────────────────────────────────────────────────────────────┐
│ 1. Test response times (time curl)                           │
│    ↓                                                         │
│ 2. Test cache behavior (2nd request faster)                  │
│    ↓                                                         │
│ 3. Load test with Apache Bench                               │
│    ↓                                                         │
│ ✅ VERIFICATION: < 200ms uncached, < 50ms cached             │
└──────────────────────────────────────────────────────────────┘
                            ↓
Phase 5: Production Deployment
┌──────────────────────────────────────────────────────────────┐
│ 1. Deploy to Vercel                                          │
│    ↓                                                         │
│ 2. Configure environment variables                           │
│    ↓                                                         │
│ 3. Test production endpoints                                 │
│    ↓                                                         │
│ 4. Monitor Vercel Analytics                                  │
│    ↓                                                         │
│ ✅ VERIFICATION: Production URL works, logs clean            │
└──────────────────────────────────────────────────────────────┘
```

## Request Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER OPENS MAP                               │
│                    http://localhost:5001/map                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  Browser loads map.js                                           │
│  ↓                                                              │
│  Mapbox GL JS initializes                                       │
│  ↓                                                              │
│  Adds MVT source: /api/tiles/{z}/{x}/{y}.pbf                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  User pans/zooms map                                            │
│  ↓                                                              │
│  Browser requests tiles for visible area                        │
│  Example: /api/tiles/13/730/730.pbf?layer=attractions           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  Flask receives request                                         │
│  routes/api/map_routes.py:get_tile()                            │
│  ↓                                                              │
│  1. Check Redis cache (if configured)                           │
│     → HIT: Return cached tile (< 50ms)                          │
│     → MISS: Continue...                                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  utils/tile_generator.py:generate_mvt_tile()                    │
│  ↓                                                              │
│  1. Calculate tile bounds (XYZ → WGS84)                         │
│  2. Build ST_AsMVT query                                        │
│  3. Execute SQL:                                                │
│     SELECT ST_AsMVT(...                                         │
│       FROM "ATTRACTION"                                         │
│       WHERE ST_Intersects(geom, tile_bounds)                    │
│       AND status = 'approved'                                   │
│  ↓                                                              │
│  Returns binary PBF data                                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  Flask sends response                                           │
│  ↓                                                              │
│  Headers:                                                       │
│  - Content-Type: application/x-protobuf                         │
│  - Cache-Control: public, s-maxage=3600                         │
│  - X-Cache: MISS                                                │
│  ↓                                                              │
│  Vercel Edge Cache stores response                              │
│  ↓                                                              │
│  Browser receives tile                                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  Mapbox GL JS renders tile                                      │
│  ↓                                                              │
│  1. Parses PBF data                                             │
│  2. Draws points (colored by category)                          │
│  3. Shows labels (zoom 14+)                                     │
│  ↓                                                              │
│  User sees attractions on map! ✅                               │
└─────────────────────────────────────────────────────────────────┘
```

## Cache Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    TILE REQUEST CACHING                          │
└─────────────────────────────────────────────────────────────────┘

Request #1 (Uncached)
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ Browser  │ →  │ Vercel   │ →  │ Flask    │ →  │ Supabase │
│          │    │ Edge     │    │ App      │    │ PostGIS  │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
     ↓               ↓               ↓               ↓
  Request       Cache           Query DB      Generate Tile
  /tile.pbf     MISS            (no Redis)    ST_AsMVT
                                                    ↓
     ←               ←               ←               ←
  Render      Store in        Add Headers     Return Binary
  Point       Edge Cache      Cache-Control   PBF Data
  ~200ms                                            ~150ms

Request #2 (Cached in Vercel Edge)
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ Browser  │ →  │ Vercel   │    │ Flask    │    │ Supabase │
│          │    │ Edge     │    │ App      │    │ PostGIS  │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
     ↓               ↓
  Request       Cache HIT
  /tile.pbf     Serve from Edge
                    ↓
     ←               ←
  Render      Return Cached
  Point       ~10ms
  ~50ms

Request #3 (With Redis - if configured)
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ Browser  │ →  │ Vercel   │ →  │ Flask    │ →  │ Upstash  │
│          │    │ Edge     │    │ App      │    │ Redis    │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
     ↓               ↓               ↓               ↓
  Request       Cache         Check Redis     Cache HIT
  /tile.pbf     MISS          First           Return Tile
                                  ↓
     ←               ←               ←
  Render      Store in        Add Headers
  Point       Edge Cache      X-Cache: HIT
  ~50ms       (s-maxage=      ~40ms
              3600)
```

## Test Coverage Map

```
┌─────────────────────────────────────────────────────────────────┐
│                    TEST COVERAGE MATRIX                          │
└─────────────────────────────────────────────────────────────────┘

Component              Test File/Method           Status
─────────────────────────────────────────────────────────────────
PostGIS Extension      schema_postgis.sql         ✅ Created
Geometry Columns       SQL verification           ✅ In script
Spatial Indexes        CREATE INDEX statements    ✅ In script
                       ─────────────────────────────────────────
Tile Generator         utils/tile_generator.py    ✅ Created
- XYZ to bounds        _xyz_to_bounds()           ✅ Tested
- MVT query builder    _build_mvt_query()         ✅ Tested
- Multi-layer support  generate_multi_layer_mvt() ✅ Tested
                       ─────────────────────────────────────────
Tile Endpoints         routes/api/map_routes.py   ✅ Created
- Single layer         GET /tiles/z/x/y.pbf       ✅ Endpoint
- Combined layers      GET /tiles/combined/...    ✅ Endpoint
- List layers          GET /tiles/layers          ✅ Endpoint
- Invalidate cache     POST /tiles/cache/invalidate ✅ Endpoint
                       ─────────────────────────────────────────
Caching                map_routes.py              ✅ Implemented
- Redis integration    get_redis_client()         ✅ Lazy-loaded
- Cache get/set        get/set_tile_in_cache()    ✅ Functions
- Vercel headers       _add_cache_headers()       ✅ Implemented
                       ─────────────────────────────────────────
Frontend               static/js/pages/map.js     ✅ Refactored
- MVT source           setupMVTSource()           ✅ Vector type
- MVT layers           setupMVTLayers()           ✅ Circle + label
- Interactions         click/hover handlers       ✅ Implemented
- Category styling     paint properties           ✅ Match expression
                       ─────────────────────────────────────────
Documentation          docs/                      ✅ Complete
- Architecture         architecture.md            ✅ Updated
- API reference        api_reference.md           ✅ MVT section
- Testing guide        TESTING_GUIDE.md           ✅ Created
- Quick commands       QUICK_TEST_COMMANDS.md     ✅ Created
- Implementation       MVT_IMPLEMENTATION.md      ✅ Created
```

## Debugging Flowchart

```
                    Start Testing
                         ↓
            ┌────────────────────────┐
            │  Can you access        │
            │  /map page?            │
            └────────────────────────┘
                     │
           ┌─────────┴─────────┐
           │                   │
          NO                  YES
           │                   │
           ↓                   ↓
    ┌─────────────┐    ┌──────────────────┐
    │ Check:      │    │ Open DevTools    │
    │ - App       │    │ Network tab      │
    │   running?  │    │                  │
    │ - Port 5001 │    │ See .pbf         │
    │ - Errors in │    │ requests?        │
    │   console   │    └──────────────────┘
    └─────────────┘             │
                       ┌────────┴────────┐
                       │                 │
                      NO               YES
                       │                 │
                       ↓                 ↓
                ┌─────────────┐  ┌──────────────┐
                │ Check:      │  │ Map shows    │
                │ - map.js    │  │ colored      │
                │   loaded?   │  │ points?      │
                │ - Mapbox    │  └──────────────┘
                │   token set?│         │
                └─────────────┘      ┌──┴──┐
                                    │     │
                                   NO   YES
                                    │     │
                                    ↓     ↓
                             ┌──────────┐  ┌────────────┐
                             │ Check:   │  │ ✅ SUCCESS │
                             │ - Tile   │  │ MVT working│
                             │   data   │  └────────────┘
                             │   empty? │
                             │ - Zoom   │
                             │   level  │
                             └──────────┘
```

## Files Reference

```
Project Structure with Test Files
─────────────────────────────────

project/
├── utils/
│   └── tile_generator.py          # Test: Import and call functions
├── routes/api/
│   └── map_routes.py              # Test: curl endpoints
├── static/js/pages/
│   └── map.js                     # Test: Browser DevTools
├── docs/
│   ├── PLAN-map-concurrency.md    # Original requirements
│   ├── MVT_IMPLEMENTATION.md      # Implementation details
│   ├── TESTING_GUIDE.md           # ← START HERE
│   ├── QUICK_TEST_COMMANDS.md     # Copy-paste commands
│   └── TEST_FLOW_DIAGRAM.md       # ← This file
├── schema_postgis.sql             # Test: Run in Supabase
└── test_mvt.py                    # Test: python test_mvt.py
```

---

**Quick Start:**
1. Read `TESTING_GUIDE.md` for full instructions
2. Use `QUICK_TEST_COMMANDS.md` for copy-paste tests
3. Refer to this diagram for understanding flow

**Need Help?**
- Check console for errors
- Verify PostGIS enabled
- Confirm tile requests in Network tab
