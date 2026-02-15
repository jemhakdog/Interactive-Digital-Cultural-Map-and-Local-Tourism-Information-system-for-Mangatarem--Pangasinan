# API Reference Documentation

**Interactive Digital Cultural Map and Local Tourism Information System**

This document provides comprehensive documentation for all public API endpoints available in the system.

---

## Overview

The API provides JSON endpoints for accessing approved tourism data. All endpoints are rate-limited for stability and fair usage.

### Base URL

```
/api
```

### Response Format

All API responses follow a consistent JSON structure with appropriate HTTP status codes.

### Rate Limiting

API endpoints are rate-limited to ensure system stability:
- **Default Rate**: 20 requests per minute per IP address
- **Headers**: Rate limit information is included in response headers

---

## Endpoints by Blueprint

### API Blueprint (`/api`)

Public-facing JSON endpoints for accessing tourism data.

---

#### GET `/api/attractions`

Retrieve a paginated list of approved attractions.

**Authentication**: None required (public endpoint)

**Rate Limit**: 20 requests per minute

**Query Parameters**:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | integer | `1` | Page number for pagination |
| `per_page` | integer | `20` | Number of attractions per page (max: 100) |
| `category` | string | `null` | Filter by attraction category (e.g., "Nature", "Historical", "Religious") |
| `barangay` | string | `null` | Filter by barangay name |

**Example Request**:

```bash
GET /api/attractions?page=1&per_page=10&category=Nature
```

**Response Format**:

```json
{
  "attractions": [
    {
      "id": 1,
      "name": "Mount Balungao Hot and Cold Springs",
      "category": "Nature",
      "barangay": "Balungao",
      "description": "Natural hot and cold spring pools...",
      "lat": 15.8965,
      "lng": 120.6543,
      "image": "/static/uploads/balungao_springs.jpg",
      "rating": 4.5
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 45,
    "pages": 5,
    "has_next": true,
    "has_prev": false
  }
}
```

**Response Fields**:

| Field | Type | Description |
|-------|------|-------------|
| `attractions` | array | List of attraction objects |
| `attractions[].id` | integer | Unique attraction identifier |
| `attractions[].name` | string | Attraction name |
| `attractions[].category` | string | Attraction category |
| `attractions[].barangay` | string | Barangay location |
| `attractions[].description` | string | Full description |
| `attractions[].lat` | float | Latitude coordinate |
| `attractions[].lng` | float | Longitude coordinate |
| `attractions[].image` | string | Image URL path |
| `attractions[].rating` | float | Average rating (placeholder: 4.5) |
| `pagination` | object | Pagination metadata |
| `pagination.page` | integer | Current page number |
| `pagination.per_page` | integer | Items per page |
| `pagination.total` | integer | Total number of attractions |
| `pagination.pages` | integer | Total number of pages |
| `pagination.has_next` | boolean | Whether next page exists |
| `pagination.has_prev` | boolean | Whether previous page exists |

**Caching**:

This endpoint includes cache headers:
- `Cache-Control: public, max-age=300`
- `Expires`: 5 minutes from request time

**Status Codes**:

| Code | Description |
|------|-------------|
| `200` | Success |
| `400` | Invalid query parameters |
| `429` | Rate limit exceeded |
| `500` | Internal server error |

**Example cURL**:

```bash
curl -X GET "https://your-domain.vercel.app/api/attractions?page=1&per_page=20&category=Nature" \
  -H "Accept: application/json"
```

**Example JavaScript (Fetch)**:

```javascript
fetch('/api/attractions?page=1&per_page=20&category=Nature')
  .then(response => response.json())
  .then(data => {
    console.log(`Found ${data.pagination.total} attractions`);
    data.attractions.forEach(attraction => {
      console.log(`${attraction.name} - ${attraction.category}`);
    });
  })
  .catch(error => console.error('Error:', error));
```

---

## Authentication

Currently, all public API endpoints do not require authentication. Future versions may include:
- API key authentication for third-party integrations
- OAuth 2.0 for user-specific data access

---

## Error Handling

All API endpoints follow consistent error response format:

**Error Response Structure**:

```json
{
  "error": "Error message description",
  "status": 400
}
```

**Common HTTP Status Codes**:

| Code | Meaning | Description |
|------|---------|-------------|
| `200` | OK | Request successful |
| `400` | Bad Request | Invalid parameters or malformed request |
| `401` | Unauthorized | Authentication required |
| `404` | Not Found | Resource not found |
| `429` | Too Many Requests | Rate limit exceeded |
| `500` | Internal Server Error | Server-side error |

---

## Rate Limiting Details

Rate limiting is implemented using Flask-Limiter with the following configuration:

- **Storage**: In-memory storage (Redis recommended for production scaling)
- **Key**: Client IP address
- **Window**: Rolling window (per minute)
- **Response Headers**:
  - `X-RateLimit-Limit`: Maximum requests allowed
  - `X-RateLimit-Remaining`: Requests remaining in current window
  - `X-RateLimit-Reset`: Time when the rate limit resets (Unix timestamp)

When rate limit is exceeded, the API returns:

```json
{
  "error": "Rate limit exceeded. Please try again later.",
  "status": 429
}
```

---

## Caching Strategy

API responses include appropriate caching headers to optimize performance:

- **Public Endpoints**: `Cache-Control: public, max-age=300` (5 minutes)
- **Vercel Edge Network**: Responses are cached at edge locations for faster access
- **Stale-While-Revalidate**: Used for HTML responses to serve stale content while fetching fresh data

---

## Best Practices

### Pagination

- Always use pagination for large datasets
- Start with reasonable `per_page` values (20-50)
- Maximum `per_page` is capped at 100 to prevent performance issues

### Filtering

- Use specific filters (`category`, `barangay`) to reduce payload size
- Combine filters for more targeted queries

### Caching

- Implement client-side caching to reduce API calls
- Respect `Cache-Control` headers
- Use ETags for conditional requests (if implemented)

### Error Handling

- Always check HTTP status codes
- Implement retry logic with exponential backoff for rate limit errors
- Log errors for debugging and monitoring

---

## Future Endpoints (Planned)

The following endpoints are planned for future releases:

- `GET /api/events` - Retrieve approved events
- `GET /api/barangays` - List all barangays with their information
- `GET /api/gallery` - Retrieve approved gallery items
- `GET /api/attractions/{id}` - Get single attraction details
- `GET /api/search` - Full-text search across attractions and events

---

## Support

For API-related questions or issues:
- **Documentation**: See [architecture.md](file:///d:/porjects/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan/docs/architecture.md)
- **Deployment**: See [deployment_guide.md](file:///d:/porjects/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan/docs/deployment_guide.md)
- **Issues**: Report via project repository

---

**Last Updated**: 2026-02-12
