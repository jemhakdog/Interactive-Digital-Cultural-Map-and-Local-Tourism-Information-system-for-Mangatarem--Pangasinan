# Redis Caching & Security System

This document details the Redis-based performance optimization and persistent rate-limiting system implemented for the Mangatarem Cultural Map.

## 🏛️ Architecture Overview

The system leverages **Upstash Redis** (a serverless Redis provider) to provide a shared, persistent state across serverless function invocations. This solves the "memory reset" problem inherent in serverless platforms like Vercel.

### Core Components
1.  **Global Client**: Initialized in `app.py` and attached to `current_app.redis_client`.
2.  **Shared Utility**: Centralized helpers in `utils/cache_helpers.py`.
3.  **Persistent Limiter**: Rate limiter storage migrated from memory to Redis.
4.  **Automatic Invalidation**: Admin-triggered hooks to maintain data consistency.

---

## 🔒 Security: Persistent Rate Limiting

We use `flask-limiter` to protect public routes. In production, it is configured to use Redis to ensure that limits are enforced globally.

- **Storage URI**: Configured via `LIMITER_STORAGE_URI`.
- **Default (Local)**: `memory://` (resets on restart).
- **Production**: `rediss://...` (persists across all Vercel instances).

---

## 🚀 Caching Strategy

We cache data at the **application level** (Python logic) rather than just at the HTTP level. This reduces database load and prevents expensive calculations (like Geo-spatial distances) from running repeatedly.

### Cached Public Routes

| Feature | Cache Key Pattern | TTL | Invalidation Trigger |
| :--- | :--- | :--- | :--- |
| **Barangay Profiles** | `barangay_data:{id}` | 30m | Attraction/Event change in that barangay. |
| **Attractions API** | `api_attractions:{params}` | 5m | Any attraction approval/edit. |
| **Interactive Map** | `map_page_meta` | 10m | Any attraction approval/delete. |
| **Attraction Details** | `attraction_detail_v1:{id}` | 15m | Update to that specific attraction. |
| **Search Results** | `search:{query}:...` | 5m | 5-minute rotation for freshness. |

### Utility Usage (`utils/cache_helpers.py`)

Developers should use the shared helpers to ensure consistency and error handling:

```python
from utils.cache_helpers import cache_get, cache_set

# Retrieve
data = cache_get("my_key")

# Store
cache_set("my_key", {"data": "payload"}, ttl=300)
```

---

## 🧹 Cache Invalidation (Consistency)

To ensure visitors don't see stale information, the Admin Dashboard includes automated invalidation hooks. 

**Whenever an admin performs these actions, the cache is automatically cleared:**
- Approving a pending attraction/event.
- Editing an existing attraction/event.
- Deleting an attraction/event.

**Functions used:**
- `invalidate_attraction_cache(id, barangay_id)`
- `invalidate_event_cache(id, barangay_id)`

---

## ⚙️ Production Configuration (Vercel)

To enable the full system in Vercel, ensure the following environment variables are set:

1.  `UPSTASH_REDIS_REST_URL`: Provided by Upstash.
2.  `UPSTASH_REDIS_REST_TOKEN`: Provided by Upstash.
3.  `LIMITER_STORAGE_URI`: Formatted as `rediss://default:TOKEN@HOST:PORT`.

---

## 🛡️ Guard Rails

1.  **Serialization**: All cached data is stored as JSON. Models must be converted to dictionaries before caching.
2.  **Length Guards**: Search queries longer than 100 characters are **not cached** to prevent malicious actors from filling the Redis memory with unique, junk keys.
3.  **Fallback**: If Redis is unavailable (e.g., maintenance), the system automatically falls back to database queries with no interruption to the user experience.
