# Quick Test Commands - MVT Implementation

Copy-paste these commands to test your MVT implementation.

## 1. Start Application

```bash
# Windows
.venv\Scripts\activate
python app.py

# Linux/Mac
source .venv/bin/activate
python app.py
```

---

## 2. Test Endpoints (curl)

### Test Layers Endpoint
```bash
curl http://localhost:5001/api/tiles/layers | jq
```

### Test Single Tile (with headers)
```bash
curl -I http://localhost:5001/api/tiles/12/500/500.pbf?layer=attractions
```

**Expected:**
```
Content-Type: application/x-protobuf
Cache-Control: public, s-maxage=3600, stale-while-revalidate=86400
X-Cache: MISS
```

### Test Tile Download
```bash
curl -o tile.pbf http://localhost:5001/api/tiles/12/500/500.pbf?layer=attractions
ls -lh tile.pbf
```

### Test Combined Layers
```bash
curl -o combined.pbf "http://localhost:5001/api/tiles/combined/12/500/500.pbf?layers=attractions,natural_heritage"
```

### Test Cache Invalidation
```bash
curl -X POST http://localhost:5001/api/tiles/cache/invalidate \
  -H "Content-Type: application/json" \
  -d '{"layer": "attractions"}' | jq
```

---

## 3. Test in Browser

Open: `http://localhost:5001/map`

**DevTools Console (F12) - Paste this to verify MVT:**
```javascript
// Check if map is using vector tiles
console.log('Map sources:', Object.keys(map.getStyle().sources || {}));

// Check for MVT source
const source = map.getSource('mvt-tiles');
if (source) {
    console.log('✅ MVT Source configured:', source.type);
} else {
    console.log('❌ MVT Source not found');
}

// Log tile requests
map.on('sourcedata', (e) => {
    if (e.sourceId === 'mvt-tiles') {
        console.log('Tile loaded:', e.tile?.tileID);
    }
});
```

---

## 4. Supabase SQL Tests

### Verify PostGIS Enabled
```sql
SELECT postgis_version();
```

### Check Geometry Columns
```sql
SELECT table_name, column_name 
FROM information_schema.columns 
WHERE column_name = 'geom' 
  AND table_name IN ('attraction', 'natural_heritage', 'built_heritage');
```

### Check Spatial Indexes
```sql
SELECT tablename, indexname 
FROM pg_indexes 
WHERE indexname LIKE 'idx_%_geom';
```

### Test Tile Generation Query
```sql
SELECT ST_AsMVT(
    (SELECT 
        id,
        name,
        category,
        ST_AsMVTGeom(
            geom,
            ST_MakeEnvelope(120.14, 15.71, 120.37, 15.86, 4326),
            4096, 4096, true, true
        ) AS geom
    FROM "ATTRACTION"
    WHERE status = 'approved'
    LIMIT 10),
    'test',
    4096,
    'geom',
    'id'
) AS mvt;
```

### Count Approved Attractions
```sql
SELECT COUNT(*) as approved_attractions 
FROM "ATTRACTION" 
WHERE status = 'approved';
```

---

## 5. Performance Tests

### Response Time Test
```bash
# First request (uncached)
time curl -o /dev/null http://localhost:5001/api/tiles/12/500/500.pbf?layer=attractions

# Second request (should be faster if cached)
time curl -o /dev/null http://localhost:5001/api/tiles/12/500/500.pbf?layer=attractions
```

**Targets:**
- Uncached: < 200ms
- Cached: < 50ms

### Load Test (Apache Bench)
```bash
# 100 requests, 10 concurrent
ab -n 100 -c 10 http://localhost:5001/api/tiles/12/500/500.pbf?layer=attractions
```

**Look for:**
- Requests per second: > 50
- Failed requests: 0

---

## 6. Check Logs

### Application Logs
```bash
# Watch logs in real-time
tail -f logs/app.log  # If logging to file

# Or check console output when running
```

### Vercel Logs (Production)
```bash
# Install Vercel CLI
npm i -g vercel

# Login and view logs
vercel login
vercel logs your-project-url
```

---

## 7. Quick Validation Script

Save as `test_mvt.py`:

```python
import requests
import time

BASE_URL = "http://localhost:5001"

def test_layers():
    """Test layers endpoint"""
    r = requests.get(f"{BASE_URL}/api/tiles/layers")
    assert r.status_code == 200
    assert "layers" in r.json()
    print("✅ Layers endpoint OK")

def test_tile():
    """Test tile endpoint"""
    r = requests.get(f"{BASE_URL}/api/tiles/12/500/500.pbf?layer=attractions")
    assert r.status_code == 200
    assert r.headers["Content-Type"] == "application/x-protobuf"
    assert "Cache-Control" in r.headers
    print(f"✅ Tile endpoint OK ({len(r.content)} bytes)")
    print(f"   Cache-Control: {r.headers['Cache-Control']}")
    print(f"   X-Cache: {r.headers.get('X-Cache', 'N/A')}")

def test_performance():
    """Test response times"""
    times = []
    for i in range(3):
        start = time.time()
        r = requests.get(f"{BASE_URL}/api/tiles/12/500/500.pbf?layer=attractions")
        elapsed = (time.time() - start) * 1000
        times.append(elapsed)
        print(f"   Request {i+1}: {elapsed:.2f}ms")
    
    avg = sum(times) / len(times)
    print(f"✅ Average response time: {avg:.2f}ms")
    if avg < 200:
        print("   🎯 Performance target met (< 200ms)")
    else:
        print("   ⚠️ Performance target NOT met (> 200ms)")

if __name__ == "__main__":
    print("Testing MVT Implementation...\n")
    test_layers()
    test_tile()
    print("\nPerformance Test:")
    test_performance()
    print("\n✅ All tests complete!")
```

Run it:
```bash
python test_mvt.py
```

---

## 8. Browser Console Checks

Open `http://localhost:5001/map` and paste in console:

```javascript
// 1. Check for MVT source
const source = map.getSource('mvt-tiles');
console.log('MVT Source:', source ? '✅ Found' : '❌ Not Found');
console.log('Source Type:', source?.type);

// 2. Check layers
const layers = map.getStyle().layers.filter(l => l.source === 'mvt-tiles');
console.log('MVT Layers:', layers.map(l => l.id));

// 3. Check for errors
console.log('Any errors above? If no, MVT is working! ✅');
```

---

## 9. Common Issues & Fixes

| Issue | Command to Diagnose | Fix |
|-------|-------------------|-----|
| 500 Error on tile endpoint | Check app logs | Enable PostGIS in Supabase |
| Empty tile (0 bytes) | `curl -o tile.pbf ...` | Add approved attractions |
| No points on map | Browser console | Check tile requests in Network tab |
| X-Cache always MISS | `curl -I ...` twice | Configure Upstash Redis |
| Slow response (>500ms) | `time curl ...` | Add spatial indexes |

---

## 10. Production Deployment Checklist

Before deploying to Vercel:

- [ ] PostGIS enabled in Supabase
- [ ] `schema_postgis.sql` migration run
- [ ] Geometry columns verified
- [ ] Spatial indexes created
- [ ] Local tests pass
- [ ] Mapbox token configured in Vercel
- [ ] Upstash Redis configured (optional)
- [ ] `requirements.txt` includes `upstash-redis`

Deploy:
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

Test production URL:
```bash
curl -I https://your-project.vercel.app/api/tiles/layers
```

---

**📚 Full Documentation:**
- `docs/TESTING_GUIDE.md` - Complete testing guide
- `docs/api_reference.md` - API documentation
- `docs/MVT_IMPLEMENTATION.md` - Implementation details
