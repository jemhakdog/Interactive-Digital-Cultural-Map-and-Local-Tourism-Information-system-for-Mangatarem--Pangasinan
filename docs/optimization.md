# Performance and Optimization Guide

This guide details the strategies implemented to ensure a high-performance, sub-second response time for the system.

## Server-Side Optimizations (Vercel/Flask)

### 1. Lazy-Loaded Supabase Client
The Supabase client is initialized only when requested, reducing cold start times by 300-500ms.

```python
# utils/db_manager.py
_supabase_client = None

def get_supabase_client():
    global _supabase_client
    if _supabase_client is None:
        _supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _supabase_client
```

### 2. ProxyFix Middleware
Properly handles Vercel's reverse proxy headers for protocol and IP detection.

```python
if "VERCEL" in os.environ:
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
```

---

## Database Optimizations

### 1. Connection Pooling
For production Supabase PostgreSQL, we use connection pooling on port **6543**.

### 2. Field Naming (ERD Aligned)
The system uses `latitude` and `longitude` fields throughout. Avoid using `lat` or `lng` as these are deprecated and can cause schema mismatches during production migrations.

### 3. Caching Strategy
The system uses **Smart Cache Headers** applied globally in `app.py`:

| Content Type | s-maxage | stale-while-revalidate |
|--------------|----------|------------------------|
| Public HTML | 300s (5m) | 600s (10m) |
| Public API | 120s (2m) | 300s (5m) |
| Static Assets | 1 Year | N/A (Immutable) |

---

## Frontend Optimizations

### 1. Leaflet.js Marker Clustering
Prevents browser lag when displaying 100+ map markers by grouping nearby points into clusters.

### 2. Service Worker (PWA)
The `/sw.js` implementation caches core styles and scripts locally, providing instant load times on repeat visits even in low-bandwidth areas (common in rural barangays).

### 3. Tailwind CSS 4.0
Leverages the latest CSS-first engine for minimal bundle size and native-like performance.

---

## Maintenance Tasks

- **Log Rotation**: Ensure logs are managed if running on traditional VPS (though Vercel handles this automatically via Log Drains).
- **Schema Audit**: Periodically run `ANALYZE` on the Supabase database to optimize query planning.