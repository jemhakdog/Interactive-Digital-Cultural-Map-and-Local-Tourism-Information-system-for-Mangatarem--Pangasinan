# API Reference Guide

This document provides a reference for the public and administrative API endpoints available in the system.

## Authentication

Administrative and contributor endpoints require authentication. Use the session cookie provided after a successful login at `/auth/login`.

## Public API Endpoints

### 1. List Attractions
`GET /api/attractions`

Returns a list of all approved attractions with their basic information and coordinates.

**Parameters:**
- `category` (optional): Filter by attraction category (e.g., "Natural", "Religious").
- `barangay` (optional): Filter by barangay name.

**Response:**
```json
[
  {
    "id": 1,
    "name": "Manleluag Spring",
    "latitude": 15.7894,
    "longitude": 120.2831,
    "category": "Natural",
    "barangay": "Malabobo",
    "image_url": "/static/uploads/spring.jpg"
  }
]
```

### 2. Search Events
`GET /api/events`

Returns a list of upcoming community events.

**Parameters:**
- `status` (optional): Defaults to "approved".
- `type` (optional): Filter by event type.

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
