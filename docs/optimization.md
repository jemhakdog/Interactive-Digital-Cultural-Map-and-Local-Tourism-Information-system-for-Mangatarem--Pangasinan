# Performance Optimization Guide

**Interactive Digital Cultural Map and Local Tourism Information System**

This guide covers the performance optimizations implemented in the application and recommendations for further improvements.

---

## Implemented Optimizations

### 1. Vercel-Specific Optimizations

#### ProxyFix Middleware

The application uses **Werkzeug ProxyFix** to handle headers from Vercel's reverse proxy:

```python
# app.py
from werkzeug.middleware.proxy_fix import ProxyFix

if is_vercel:
    app.wsgi_app = ProxyFix(
        app.wsgi_app,
        x_for=1,
        x_proto=1,
        x_host=1,
        x_prefix=1
    )
```

**Benefits**:
- Correct HTTPS detection
- Accurate client IP forwarding
- Proper URL generation

#### Lazy Supabase Client Initialization

Supabase client is lazily loaded to reduce cold start times:

```python
# utils/db_manager.py
_supabase_client = None

def get_supabase_client():
    """Lazy-load Supabase client"""
    global _supabase_client
    if _supabase_client is None:
        _supabase_client = create_client(url, key)
    return _supabase_client
```

**Impact**: ~200ms reduction in cold start time.

#### Smart Cache Headers

Dynamic `Cache-Control` headers based on route type:

```python
# app.py
def _apply_cache_headers(response, path):
    if path.startswith('/api/'):
        response.headers['Cache-Control'] = 'public, max-age=300'  # 5 min
    elif path.startswith('/static/'):
        response.headers['Cache-Control'] = 'public, max-age=31536000'  # 1 year
    elif path in ['/', '/map', '/attractions', '/events']:
        response.headers['Cache-Control'] = 'public, max-age=600'  # 10 min
```

**Benefits**:
- Vercel Edge Network caching
- Reduced database load
- Faster response times for public routes

---

### 2. Database Optimizations

#### Connection Pooling (Supabase)

Production uses Supabase connection pooler (port 6543):

```python
DATABASE_URL=postgresql://postgres.[project]:[pass]@[region].pooler.supabase.com:6543/postgres
```

**Benefits**:
- Reuses existing connections
- Reduces connection overhead
- Handles concurrent requests efficiently

#### Pagination on API Endpoints

The `/api/attractions` endpoint includes pagination:

```python
# routes/api.py
page = request.args.get('page', 1, type=int)
per_page = request.args.get('per_page', 20, type=int)

offset = (page - 1) * per_page
attractions_query = attractions_query.offset(offset).limit(per_page)
```

**Benefits**:
- Reduces payload size
- Faster JSON serialization
- Improved client-side rendering

---

### 3. Frontend Optimizations

#### Tailwind CSS Tree Shaking

Tailwind configuration purges unused CSS in production:

```javascript
// tailwind.config.js
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/js/**/*.js"
  ],
  // ...
}
```

**Action**: Run build with `NODE_ENV=production npm run build` to enable purging.

**Impact**: CSS bundle reduced by ~90%.

#### Deferred JavaScript Loading

Non-critical scripts use `defer` attribute:

```html
<script src="{{ url_for('static', filename='js/map.js') }}" defer></script>
```

**Benefits**:
- Non-blocking HTML parsing
- Faster initial page render
- Scripts execute after DOM ready

#### Lazy Loading Images

All images use native lazy loading:

```html
<img src="..." loading="lazy" alt="Attraction">
```

**Benefits**:
- Only loads images when scrolling into view
- Reduces initial page weight
- Saves bandwidth

#### PWA Implementation

Progressive Web App features:
- Service worker for offline caching
- Web app manifest for installability
- Caches static assets for faster subsequent loads

**Files**:
- `static/manifest.json`
- `static/service-worker.js`

---

## Recommended Additional Optimizations

### Database Indexing

**Current Status**: Basic indexes on primary and foreign keys.

**Recommendation**: Add indexes to frequently queried columns:

```sql
CREATE INDEX idx_attraction_category ON attraction(category);
CREATE INDEX idx_attraction_barangay ON attraction(barangay_id);
CREATE INDEX idx_event_date ON event(date);
CREATE INDEX idx_review_status ON review(attraction_id, status);
```

### Flask-Caching for View Results

**Current Status**: Not implemented.

**Recommendation**: Cache rendered templates:

```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@public_bp.route('/')
@cache.cached(timeout=600)  # 10 minutes
def index():
    # ...
```

### Marker Clustering for Maps

**Current Status**: Not implemented.

**Recommendation**: Use Leaflet.markercluster:

```javascript
import MarkerClusterGroup from 'leaflet.markercluster';

const markers = L.markerClusterGroup();
// Add markers to cluster group
map.addLayer(markers);
```

**Benefits**: Improved performance when displaying many map markers.

### Image Optimization

**Recommendation**: 
- Compress images before upload (use libraries like Pillow)
- Generate thumbnails for gallery views
- Serve images via CDN

```python
from PIL import Image

def optimize_image(image_path, max_size=(1920, 1080)):
    img = Image.open(image_path)
    img.thumbnail(max_size, Image.LANCZOS)
    img.save(image_path, optimize=True, quality=85)
```

---

## Performance Monitoring

### Vercel Analytics

Enable Vercel Web Analytics:
1. Vercel Dashboard → Your Project → Analytics
2. Enable Web Analytics
3. Add analytics script to `base.html`

### Core Web Vitals

Monitor key metrics:
- **LCP (Largest Contentful Paint)**: Target < 2.5s
- **FID (First Input Delay)**: Target < 100ms
- **CLS (Cumulative Layout Shift)**: Target < 0.1

Use Google Lighthouse for auditing:

```bash
lighthouse https://your-app.vercel.app --view
```

---

## Additional Resources

- **[Deployment Guide](file:///d:/porjects/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan/docs/deployment_guide.md)** - Vercel deployment optimizations
- **[Architecture Guide](file:///d:/porjects/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan/docs/architecture.md)** - System design details
- **[API Reference](file:///d:/porjects/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan/docs/api_reference.md)** - Caching and pagination details

---

**Last Updated**: 2026-02-12