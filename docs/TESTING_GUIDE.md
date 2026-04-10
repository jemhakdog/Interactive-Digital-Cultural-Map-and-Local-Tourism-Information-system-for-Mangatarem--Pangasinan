# MVT Implementation Testing Guide

This guide walks you through testing the Mapbox Vector Tile (MVT) implementation step-by-step.

## Prerequisites

Before testing, ensure you have:
- ✅ Python 3.12+ with dependencies installed (`pip install -r requirements.txt`)
- ✅ Supabase PostgreSQL database (production)
- ✅ Mapbox access token configured
- ✅ Local development environment running

---

## Phase 1: Enable PostGIS in Supabase

### Step 1.1: Enable PostGIS Extension

1. Go to your Supabase Dashboard: https://supabase.com/dashboard
2. Select your project
3. Navigate to **Database** → **Extensions**
4. Search for "postgis"
5. Click **Enable** on `postgis` extension

### Step 1.2: Run PostGIS Migration Script

1. In Supabase Dashboard, go to **SQL Editor**
2. Click **New Query**
3. Copy the contents of `schema_postgis.sql`
4. Paste and click **Run**
5. Verify success - you should see output like:
   ```
   postgis_version()
   ------------------
   3.4.0 c5870a8...
   ```

### Step 1.3: Verify Geometry Columns

Run this verification query in Supabase SQL Editor:

```sql
-- Check geometry columns exist
SELECT 
    table_name,
    column_name,
    data_type
FROM information_schema.columns
WHERE column_name = 'geom'
  AND table_name IN ('attraction', 'natural_heritage', 'built_heritage');

-- Check spatial indexes
SELECT 
    tablename,
    indexname
FROM pg_indexes
WHERE indexname LIKE 'idx_%_geom';

-- Count records with geometry
SELECT 
    'ATTRACTION' as table_name,
    COUNT(*) as total,
    COUNT(geom) as with_geometry
FROM "ATTRACTION"
WHERE status = 'approved';
```

**Expected Result:**
- Geometry columns listed for each table
- Indexes like `idx_attraction_geom` exist
- Record count matches your approved attractions

---

## Phase 2: Test Tile Endpoints Locally

### Step 2.1: Start the Application

```bash
# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Run the application
python app.py
```

Application should start at `http://localhost:5001`

### Step 2.2: Test Layers Endpoint

```bash
# Test available layers
curl http://localhost:5001/api/tiles/layers
```

**Expected Response:**
```json
{
  "layers": [
    {
      "name": "attractions",
      "table": "ATTRACTION",
      "id_column": "id",
      "name_column": "name",
      "category_column": "category"
    },
    {
      "name": "natural_heritage",
      "table": "NATURAL_HERITAGE",
      ...
    }
  ]
}
```

### Step 2.3: Test Single Tile Endpoint

```bash
# Test tile with headers
curl -I http://localhost:5001/api/tiles/12/500/500.pbf?layer=attractions
```

**Expected Headers:**
```
HTTP/1.1 200 OK
Content-Type: application/x-protobuf
Cache-Control: public, s-maxage=3600, stale-while-revalidate=86400
X-Cache: MISS
ETag: "abc123..."
```

### Step 2.4: Download and Inspect Tile

```bash
# Download tile to file
curl -o test_tile.pbf http://localhost:5001/api/tiles/12/500/500.pbf?layer=attractions

# Check file size (should be > 0 bytes)
ls -lh test_tile.pbf
```

**Expected:** File size between 100 bytes - 50 KB (depending on tile content)

### Step 2.5: Test Combined Tile Endpoint

```bash
# Test multi-layer tile
curl -o combined_tile.pbf "http://localhost:5001/api/tiles/combined/12/500/500.pbf?layers=attractions,natural_heritage"
```

### Step 2.6: Test Cache Invalidation

```bash
# Test cache invalidation endpoint
curl -X POST http://localhost:5001/api/tiles/cache/invalidate \
  -H "Content-Type: application/json" \
  -d '{"layer": "attractions"}'
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "No cached tiles found for this layer",
  "layer": "attractions"
}
```

---

## Phase 3: Test in Browser

### Step 3.1: Open Map Page

1. Open browser to `http://localhost:5001/map`
2. Open DevTools (F12)
3. Go to **Network** tab
4. Filter by "tiles" or type ".pbf"

### Step 3.2: Verify Tile Requests

You should see requests like:
```
/api/tiles/13/730/730.pbf?layer=attractions
/api/tiles/13/731/730.pbf?layer=attractions
/api/tiles/13/730/731.pbf?layer=attractions
```

**Check:**
- [ ] Requests are to `.pbf` endpoint (not GeoJSON)
- [ ] Content-Type is `application/x-protobuf`
- [ ] Response times are < 200ms
- [ ] Tiles load as you pan/zoom

### Step 3.3: Verify Map Rendering

1. **Zoom to Mangatarem** (should auto-center)
2. **Look for colored circles** representing attractions:
   - 🟢 Green = Nature
   - 🟠 Amber = Historical
   - 🟣 Purple = Religious
   - 🔴 Red = Food

3. **Hover over a point** - should show popup with name
4. **Click a point** - should:
   - Fly to location with smooth animation
   - Show place card in sidebar

### Step 3.4: Test Zoom Levels

- **Zoom 10-13**: Points appear as small circles
- **Zoom 14+**: Labels appear next to points
- **Zoom 15+**: 3D buildings should appear (if style supports)

### Step 3.5: Test Category Filters

1. Click category filter buttons (Nature, Historical, etc.)
2. Sidebar list should update
3. Map points should update (may require tile refresh)

---

## Phase 4: Performance Testing

### Step 4.1: Test Response Times

```bash
# First request (cache MISS - slower)
time curl -o /dev/null http://localhost:5001/api/tiles/12/500/500.pbf?layer=attractions

# Second request (should be cached if Redis configured)
time curl -o /dev/null http://localhost:5001/api/tiles/12/500/500.pbf?layer=attractions
```

**Expected:**
- First request: < 200ms (database query)
- Second request: < 50ms (if Redis cached) or < 200ms (Vercel cache)

### Step 4.2: Load Test (Optional)

```bash
# Install Apache Bench (if not installed)
# Test with 100 requests, 10 concurrent
ab -n 100 -c 10 http://localhost:5001/api/tiles/12/500/500.pbf?layer=attractions
```

**Look for:**
- Requests per second
- Average response time
- No failed requests

### Step 4.3: Check Vercel Logs (Production)

After deploying to Vercel:

1. Go to Vercel Dashboard → Your Project → **Logs**
2. Filter by `/api/tiles`
3. Check for:
   - No errors
   - Response times < 200ms
   - Cache HIT ratio increasing

---

## Phase 5: Configure Redis Caching (Optional but Recommended)

### Step 5.1: Create Upstash Redis Database

1. Go to https://upstash.com
2. Sign up / Login
3. Create new Redis database
4. Copy the credentials:
   - `UPSTASH_REDIS_REST_URL`
   - `UPSTASH_REDIS_REST_TOKEN`

### Step 5.2: Add to Environment Variables

**For Local Testing:**
Create `.env` file in project root:
```bash
UPSTASH_REDIS_REST_URL=https://your-namespace.upstash.io
UPSTASH_REDIS_REST_TOKEN=your_token_here
```

**For Vercel:**
1. Vercel Dashboard → Project → **Settings** → **Environment Variables**
2. Add both variables
3. Deploy to apply

### Step 5.3: Test Redis Caching

```bash
# First request (cache MISS)
curl -I http://localhost:5001/api/tiles/12/500/500.pbf?layer=attractions
# Check X-Cache: MISS

# Second request (should be HIT)
curl -I http://localhost:5001/api/tiles/12/500/500.pbf?layer=attractions
# Check X-Cache: HIT and faster response
```

---

## Troubleshooting

### Issue: "PostGIS extension not found"

**Solution:**
```sql
-- Run in Supabase SQL Editor
CREATE EXTENSION IF NOT EXISTS postgis;
```

### Issue: "Tile endpoint returns 500 error"

**Check:**
1. Application logs for SQL errors
2. Verify geometry columns exist:
   ```sql
   SELECT geom FROM "ATTRACTION" LIMIT 1;
   ```
3. Check tile_generator.py imports correctly

### Issue: "Map shows no points"

**Check:**
1. Browser console for JavaScript errors
2. Network tab - are tile requests being made?
3. Tile response size - if 0 bytes, no data in that tile
4. Zoom level - points visible at zoom 10+

### Issue: "X-Cache always MISS"

**Solution:**
- Redis not configured (check environment variables)
- Redis connection failed (check logs)
- This is OK - Vercel Edge Cache will still work

### Issue: "Tiles return empty/no data"

**Check:**
1. Approved attractions exist in database:
   ```sql
   SELECT COUNT(*) FROM "ATTRACTION" WHERE status = 'approved';
   ```
2. Geometry data is valid:
   ```sql
   SELECT id, name, ST_AsText(geom) FROM "ATTRACTION" LIMIT 5;
   ```
3. Tile coordinates are correct for Mangatarem area

---

## Testing Checklist

### Backend Tests
- [ ] PostGIS extension enabled in Supabase
- [ ] Geometry columns created on tables
- [ ] Spatial indexes created
- [ ] `/api/tiles/layers` returns JSON
- [ ] `/api/tiles/12/500/500.pbf` returns binary data
- [ ] Content-Type is `application/x-protobuf`
- [ ] Cache-Control headers present
- [ ] X-Cache header present

### Frontend Tests
- [ ] Map page loads without errors
- [ ] Network tab shows .pbf tile requests
- [ ] Points visible on map (colored circles)
- [ ] Hover shows popup with name
- [ ] Click triggers fly-to animation
- [ ] Category filters work
- [ ] Zoom levels 10-16 display correctly

### Performance Tests
- [ ] First tile request < 200ms
- [ ] Cached tile request < 50ms (with Redis)
- [ ] No JavaScript errors in console
- [ ] Smooth pan/zoom interactions
- [ ] No tile loading flicker

### Production Tests (Vercel)
- [ ] Deployed to Vercel successfully
- [ ] Tile endpoints accessible via production URL
- [ ] Vercel logs show no errors
- [ ] Cache HIT ratio > 50% after warm-up
- [ ] Map loads in < 2 seconds

---

## Success Criteria

✅ **All tests pass if:**
1. Tile endpoint returns `application/x-protobuf` with correct headers
2. Map displays colored points for attractions
3. Interactions (hover, click) work smoothly
4. Response times < 200ms
5. No console errors

🎉 **Ready for production when:**
- All checklist items checked
- PostGIS enabled in production
- Redis caching configured (optional)
- Performance targets met

---

## Next Steps After Testing

1. **Monitor Performance**: Use Vercel Analytics
2. **Set Up Cache Invalidation**: Hook into admin routes
3. **Add More Layers**: Events, heritage sites
4. **Optimize Queries**: Add more spatial indexes if needed
5. **Document Issues**: Update MVT_IMPLEMENTATION.md with any fixes

---

**Questions?** 
- Check `docs/api_reference.md` for endpoint docs
- Review `utils/tile_generator.py` for SQL logic
- See `PLAN-map-concurrency.md` for original requirements
