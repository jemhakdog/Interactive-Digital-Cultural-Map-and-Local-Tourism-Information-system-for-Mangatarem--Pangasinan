# Routing & Navigation Architecture

## Overview
The Interactive Cultural Map supports two distinct routing features to help tourists navigate Mangatarem:
1. **Real-Time Point-to-Point Navigation**: Active turn-by-turn driving directions to a single destination using Mapbox.
2. **Multi-Stop Route Optimization**: An itinerary planner that solves the Traveling Salesman Problem (TSP) using OSRM to find the most efficient sequence to visit multiple attractions.

---

## 1. Multi-Stop Route Optimization (OSRM)

The route planner allows tourists to build an itinerary of multiple attractions, which the backend optimizes into the most efficient driving sequence.

### Backend Infrastructure (`modules/routing/`)
- **OSRM Public API**: Uses the open-source Open Source Routing Machine (`router.project-osrm.org`) to solve the Traveling Salesman Problem (TSP) completely free, requiring **no API keys**.
- **Endpoint (`/api/v1/routing/optimize`)**: Accepts an array of attraction IDs and a starting coordinate. It fetches the attractions from PostgreSQL, builds the coordinate string, and calls OSRM's `/trip` endpoint.
- **Caching Layer**: Because the public OSRM server enforces a strict 1 request/second rate limit, optimization results are heavily cached in **Upstash Redis** based on a hashed key of the selected locations. Identical tourist routes are served instantly from the cache.

### Frontend Integration (`map.js`)
- **Interactive Waypoint Manager**: The "Routes" tab contains a dynamic itinerary builder. Users can drag, drop, and manage their selected locations.
- **"Add to Route" Button**: Found on the place details card; pushing it adds the current location to the itinerary builder.
- **GeoJSON Visualization**: When the user clicks "Optimize", the backend returns the optimal sequence and a GeoJSON `LineString`. The frontend renders this on the Mapbox GL JS instance with an animated dashed line and numbered checkpoint markers (1, 2, 3...) showing the visit order.

---

## 2. Real-Time Point-to-Point Navigation (Mapbox)

For users who just want to drive straight to a single location, the map provides real-time active routing.

### Frontend Integration (`map.js`)
- **`isNavigating` State**: A global boolean flag determining if the user is currently navigating.
- **`currentDestination` Object**: Stores the active target destination's coordinates (`lat`, `lng`).
- **Custom User Marker**: Replaces the default Mapbox blue dot with a custom car icon (`car-icon.png`) when active navigation is engaged.
- **Geolocate Event Handler**: The Mapbox `GeolocateControl` `.on('geolocate')` listener tracks `position` updates. The car icon is rotated dynamically according to `position.coords.heading`.

### Mapbox Directions API Integration
The `drawRealTimeRoute(startLat, startLng, destLat, destLng)` function uses the Mapbox Directions API (Driving profile) directly from the client side:
```javascript
const query = await fetch(
    `https://api.mapbox.com/directions/v5/mapbox/driving/${startLng},${startLat};${destLng},${destLat}?geometries=geojson&access_token=${mapboxgl.accessToken}`
);
```
The response geojson is mapped to a `real-time-route` layer on the map with a blue polyline to highlight the driving path.

### User Interface (`map.html`)
The "Directions" / "Stop Navigation" toggle is located on the Place Card popup.
- ID: `start-route-btn`
- When clicked, it checks for geolocation permissions, toggles the `isNavigating` state, hides the Place Card popup, and continuously updates the route to the destination as the user drives.

## Usage Requirements
- **Geolocation Permission**: Users must allow location access for real-time tracking and accurate starting points.
- **Mapbox Token**: Requires a valid Mapbox Access Token configured with permissions to access the Directions API v5 (for single-destination routing).
- **HTTPS**: Browsers require HTTPS to provide geolocation coordinates (except on `localhost`).
