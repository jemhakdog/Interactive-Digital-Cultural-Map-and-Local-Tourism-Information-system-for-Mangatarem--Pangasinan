# API Reference Guide

This document provides a reference for the public and administrative API endpoints available in the system.

## Authentication

Administrative and contributor endpoints require authentication. Use the session cookie provided after a successful login at `/auth/login`.

## Public API Endpoints

### 1. List Attractions
`GET /api/attractions`

Returns a list of all approved attractions with their basic information and coordinates.

**Parameters:**
- `page` (optional): Page number for pagination (default: 1).
- `per_page` (optional): Items per page (default: 20, max: 100).
- `category` (optional): Filter by attraction category (e.g., "Natural", "Religious").
- `barangay` (optional): Filter by barangay name.

**Response:**
```json
{
  "attractions": [
    {
      "id": 1,
      "name": "Manleluag Spring",
      "latitude": 15.7894,
      "longitude": 120.2831,
      "category": "Natural",
      "barangay": "Malabobo",
      "image": "/static/uploads/spring.jpg",
      "description": "Beautiful natural spring",
      "rating": 4.5
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 50,
    "pages": 3,
    "has_next": true,
    "has_prev": false
  }
}
```

**Cache Headers:**
- `Cache-Control: public, max-age=300` (5 minutes)

---

## Mapbox Vector Tiles (MVT) API

High-performance vector tile endpoints for map rendering. Tiles are generated using PostGIS `ST_AsMVT` and cached via Vercel Edge Cache and Redis.

### 6. Single Layer Tile
`GET /api/tiles/<z>/<x>/<y>.pbf`

Returns a Mapbox Vector Tile for the specified coordinates and layer.

**URL Parameters:**
- `z` (required): Zoom level (0-20).
- `x` (required): Tile X coordinate.
- `y` (required): Tile Y coordinate.

**Query Parameters:**
- `layer` (optional): Layer name (default: `attractions`).
  - Available layers: `attractions`, `natural_heritage`, `built_heritage`, `events`

**Response:**
- Content-Type: `application/x-protobuf`
- Binary MVT tile data

**Cache Headers:**
- `Cache-Control: public, s-maxage=3600, stale-while-revalidate=86400`
- `X-Cache: HIT|MISS` (Redis cache status)
- `ETag: "<md5-hash>"` (for conditional requests)

**Example:**
```bash
GET /api/tiles/12/500/500.pbf?layer=attractions
```

**Frontend Usage (Mapbox GL JS):**
```javascript
map.addSource('mvt-tiles', {
    type: 'vector',
    tiles: ['/api/tiles/{z}/{x}/{y}.pbf?layer=attractions'],
    minzoom: 0,
    maxzoom: 20
});
```

### 7. Combined Multi-Layer Tile
`GET /api/tiles/combined/<z>/<x>/<y>.pbf`

Returns a single MVT tile containing multiple named layers.

**URL Parameters:**
- `z` (required): Zoom level (0-20).
- `x` (required): Tile X coordinate.
- `y` (required): Tile Y coordinate.

**Query Parameters:**
- `layers` (optional): Comma-separated list of layer names.
  - Default: all available layers
  - Example: `layers=attractions,natural_heritage`

**Response:**
- Content-Type: `application/x-protobuf`
- Binary MVT tile with multiple layers

**Example:**
```bash
GET /api/tiles/combined/12/500/500.pbf?layers=attractions,built_heritage
```

### 8. List Available Layers
`GET /api/tiles/layers`

Returns metadata for all available tile layers.

**Response:**
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
      "id_column": "id",
      "name_column": "name_of_asset",
      "category_column": "asset_sub_type"
    }
  ]
}
```

### 9. Invalidate Tile Cache
`POST /api/tiles/cache/invalidate`

Invalidates cached tiles for a specific layer. Called automatically when data is updated.

**Request Body (JSON):**
```json
{
  "layer": "attractions",
  "z": 12,        // optional: specific zoom level
  "x": 500,       // optional: specific tile X
  "y": 500        // optional: specific tile Y
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Invalidated 125 cached tiles",
  "layer": "attractions"
}
```

---

## Cultural Heritage Registry API

New endpoints for accessing the structured heritage registry.

### 3. Heritage Types
`GET /api/heritage/types`

Returns the available heritage categories mapping to Forms 01-07.

### 4. Heritage Profiles
`GET /api/heritage/<type>`

Returns profiles filtered by heritage type (e.g., `natural`, `built`, `movable`).

**Supported Types:**
- `natural` (Form 01A)
- `built` (Form 02A)
- `movable` (Form 03A)
- `intangible` (Form 4A)
- `personality` (Form 05)
- `institution` (Form 06)
- `program` (Form 07)

### 5. Heritage Detail
`GET /api/heritage/<type>/<id>`

Returns the full profile and specialized details for a specific heritage entry.

---

## Booking & Proximity API

Proximity-based physical arrival verification and check-in endpoints.

### 10. Verify Arrival & Proximity
`POST /booking/api/verify-arrival`

Accepts current GPS coordinates of the authenticated user to automatically check in today's active reservations and log physical destination arrivals.

**Authentication Required:** Yes (requires session cookie)

**Request Body (JSON):**
* `latitude` (required): Current decimal latitude coordinate (float).
* `longitude` (required): Current decimal longitude coordinate (float).
* `navigated_target_id` (optional): ID of the landmark/asset the user is actively navigating towards (integer).
* `navigated_target_type` (optional): Type of active navigation target (`"attraction"` or `"establishment"`).

**Response (JSON):**
```json
{
  "success": true,
  "booking_attended": true,
  "place_name": "Mangatarem Holy Family Parish",
  "navigated_arrived": true,
  "target_id": 1,
  "target_type": "attraction"
}
```

---

## Rate Limiting

The API is rate-limited to ensure system stability:
- **Default**: 20 requests per minute per IP.
- **Admin**: 100 requests per minute per IP.

Exceeding the limit will return a `429 Too Many Requests` status code.

## Error Responses

| Code | Message | Description |
|------|---------|-------------|
| **400** | Bad Request | Missing or invalid parameters |
| **401** | Unauthorized | Authentication required |
| **404** | Not Found | Resource not found |
| **429** | Rate Limit Exceeded | Too many requests |
| **500** | Server Error | Unexpected system error |
