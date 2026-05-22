# Real-Time Routing & Navigation

## Overview
The Interactive Cultural Map supports real-time routing and navigation using the Mapbox Directions API. When a user selects a destination on the map, they can start active navigation which updates their location in real-time, displays a custom user marker (a car icon), and draws a calculated route on the map.

## Key Components

### 1. Frontend Integration (`map.js`)
The `map.js` script handles the frontend logic for real-time routing and updating the UI:
- **`isNavigating` State**: A global boolean flag that determines if the user is currently navigating to a destination.
- **`currentDestination` Object**: Stores the active target destination's coordinates (`lat`, `lng`).
- **Custom User Marker (`customUserMarker`)**: Replaces the default Mapbox blue dot with a custom car icon (`car-icon.png`) when active navigation is engaged.
- **Geolocate Event Handler**: The Mapbox `GeolocateControl` `.on('geolocate')` event listener listens to `position` updates. If `isNavigating` is true, the car icon's position is updated, and it is rotated according to `position.coords.heading`.

### 2. Directions API Integration
The `drawRealTimeRoute(startLat, startLng, destLat, destLng)` function uses the Mapbox Directions API (Driving profile) to retrieve the shortest route:
```javascript
const query = await fetch(
    `https://api.mapbox.com/directions/v5/mapbox/driving/${startLng},${startLat};${destLng},${destLat}?geometries=geojson&access_token=${mapboxgl.accessToken}`
);
```
The response geojson is dynamically mapped to a `real-time-route` layer on the map with a blue polyline to highlight the driving path.

### 3. User Interface (`map.html`)
The "Start Route" / "Stop Navigation" toggle is implemented in the Place Card popup. 
- ID: `start-route-btn`
- When clicked, it checks for `currentDestination` and geolocation permissions, toggles the `isNavigating` state, hides the Place Card popup, and calls `drawRealTimeRoute()`.

## Usage Requirements
- **Geolocation Permission**: Users must allow location access for real-time tracking to work.
- **Mapbox Token**: Requires a valid Mapbox Access Token configured with permissions to access the Directions API v5.
- **HTTPS**: Browsers require HTTPS to provide geolocation coordinates (except on `localhost`).
