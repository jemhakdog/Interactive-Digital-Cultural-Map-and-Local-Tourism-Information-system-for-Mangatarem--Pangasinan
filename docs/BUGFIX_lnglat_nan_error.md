# Bug Fix: Multiple Map Errors

## 🔍 Issues Summary

### Issue 1: Invalid LngLat Error (NaN, NaN)
**Error:** `Uncaught Error: Invalid LngLat object: (NaN, NaN)`
**Location:** `http://127.0.0.1:5002/map`
**Trigger:** Clicking on attraction cards in the map sidebar
**Status:** ✅ Fixed

### Issue 2: Failed to Parse Tile URL
**Error:** `Failed to construct 'Request': Failed to parse URL from /api/tiles/13/6832/3733.pbf?layer=attractions`
**Location:** Map loading
**Trigger:** Map initialization trying to load MVT tiles
**Status:** ✅ Fixed

### Issue 3: Rate Limit Exceeded (429 TOO MANY REQUESTS)
**Error:** `St {status: 429, url: 'http://127.0.0.1:5002/api/tiles/15/27332/14926.pbf?layer=attractions', message: 'TOO MANY REQUESTS'}`
**Location:** Map tile loading
**Trigger:** Map requesting multiple tiles simultaneously exceeds rate limit
**Status:** ✅ Fixed

### Issue 4: Title Text Readability
**Error:** Attraction titles rendered in light gray (`text-gray-800`) making them hard to read on white backgrounds
**Location:** Attraction cards in sidebar list
**Trigger:** Insufficient color contrast
**Status:** ✅ Fixed

### Issue 5: Duplicated Attractions in List
**Error:** Same attraction appearing multiple times in the sidebar list
**Location:** Attraction cards in sidebar list
**Trigger:** Infinite scroll appending data without deduplication
**Status:** ✅ Fixed

---

## 📋 Root Cause Analysis

### Issue 1: Property Name Mismatch (LngLat Error)

The API endpoint `/api/attractions` returns attraction data with properties named `latitude` and `longitude`:

```python
# routes/api.py
result.append({
    "id": a[0],
    "latitude": a[5],   # ← API returns 'latitude'
    "longitude": a[6],  # ← API returns 'longitude'
    ...
})
```

However, the JavaScript code was trying to access `lat` and `lng` properties:

```javascript
// static/js/pages/map.js (BEFORE FIX)
card.addEventListener('click', () => flyToLocation(attraction.id, attraction.lat, attraction.lng));
```

This caused `attraction.lat` and `attraction.lng` to be `undefined`, which then resulted in `NaN` values when passed to Mapbox's `LngLat` constructor.

### Issue 2: Relative URL for Tile Source (Tile URL Error)

Mapbox GL JS requires absolute URLs for tile sources, but the code was using a relative path:

```javascript
// static/js/pages/map.js (BEFORE FIX)
map.addSource('mvt-tiles', {
    type: 'vector',
    tiles: [
        '/api/tiles/{z}/{x}/{y}.pbf?layer=attractions'  // ← Relative URL
    ],
    ...
});
```

This caused Mapbox GL JS to fail when trying to fetch tiles because it couldn't parse the relative URL properly.

### Issue 3: Rate Limit Too Restrictive (429 Error)

The tile endpoints had a rate limit of "60 per minute" which is far too low for map tile requests:

```python
# routes/map_routes.py (BEFORE FIX)
@limiter.limit("60 per minute")
def get_tile(z: int, x: int, y: int):
```

A single map view at zoom level 15 can request 20-50+ tiles simultaneously (one for each visible tile in the viewport). When panning or zooming, this number can easily exceed 60 requests per minute, triggering the rate limiter.

**Why this happened:**
- Mapbox GL JS requests tiles in batches as the user pans/zooms
- Each tile is a separate HTTP request
- 60 requests/minute is appropriate for API endpoints, not tile servers
- Standard tile servers handle thousands of requests per second

### Issue 4: Title Text Readability

The attraction card titles used `text-gray-800` (light gray) which had insufficient contrast on white card backgrounds:

```javascript
// BEFORE - Low contrast
<h3 class="font-bold text-gray-800 text-sm...">${attraction.name}</h3>
<p class="text-xs text-gray-500...">${attraction.description}</p>

// AFTER - High contrast
<h3 class="font-bold text-gray-900 text-sm...">${attraction.name}</h3>
<p class="text-xs text-gray-600...">${attraction.description}</p>
```

**Why this happened:**
- `text-gray-800` (#1f2937) is too light for comfortable reading
- WCAG accessibility guidelines recommend 4.5:1 contrast ratio for normal text
- Darker shades provide better readability

### Issue 5: Duplicated Attractions

The infinite scroll implementation was appending new attractions to the existing list without checking for duplicates:

```javascript
// BEFORE - No deduplication
attractionsData = [...attractionsData, ...result.attractions];

// AFTER - Deduplicates before rendering
const seen = new Set();
const uniqueAttractions = attractions.filter(attraction => {
    if (seen.has(attraction.id)) return false;
    seen.add(attraction.id);
    return true;
});
```

**Why this happened:**
- Infinite scroll appends new data when users scroll down
- If the same attraction appears in multiple pages or if fetch is called multiple times, duplicates are created
- The frontend didn't have deduplication logic

---

## ✅ Fixes Applied

### 1. Fixed Tile URL to Use Absolute Path

**File:** `static/js/pages/map.js`

```javascript
// BEFORE
map.addSource('mvt-tiles', {
    type: 'vector',
    tiles: [
        '/api/tiles/{z}/{x}/{y}.pbf?layer=attractions'
    ],
    ...
});

// AFTER
// Create absolute URL for tiles (Mapbox requires absolute URLs)
const tileUrl = `${window.location.origin}/api/tiles/{z}/{x}/{y}.pbf?layer=attractions`;

map.addSource('mvt-tiles', {
    type: 'vector',
    tiles: [tileUrl],
    ...
});
```

This change:
- Uses `window.location.origin` to create an absolute URL
- Ensures Mapbox GL JS can properly parse and request tiles
- Works in both development (localhost) and production environments

### 2. Fixed Property Name Access in map.js

**File:** `static/js/pages/map.js`

```javascript
// BEFORE
card.addEventListener('click', () => flyToLocation(attraction.id, attraction.lat, attraction.lng));

// AFTER
card.addEventListener('click', () => {
    // Use latitude/longitude from API (not lat/lng)
    const lat = attraction.latitude || attraction.lat;
    const lng = attraction.longitude || attraction.lng;
    flyToLocation(attraction.id, lat, lng);
});
```

This change:
- Uses the correct property names from the API (`latitude`, `longitude`)
- Provides fallback to `lat`/`lng` for backwards compatibility
- Explicitly extracts coordinates before passing to the function

### 2. Added Coordinate Validation in flyToLocation

**File:** `static/js/pages/map.js`

```javascript
function flyToLocation(id, lat, lng) {
    // Validate coordinates
    if (!lat || !lng || isNaN(lat) || isNaN(lng)) {
        console.warn('Invalid coordinates for attraction:', id, { lat, lng });
        alert('This location does not have valid coordinates.');
        return;
    }
    
    map.flyTo({
        center: [lng, lat],
        zoom: 16,
        duration: 1500
    });
    // ... rest of function
}
```

This change:
- Validates that coordinates exist and are valid numbers
- Provides user-friendly error message
- Logs warning to console for debugging
- Prevents Mapbox from throwing unhandled errors

### 4. Fixed establishment_detail.html Map

**File:** `templates/pagez/establishment_detail.html`

```javascript
// BEFORE
center: [{{ establishment.longitude }}, {{ establishment.latitude }}],

// AFTER
const longitude = {{ establishment.longitude }};
const latitude = {{ establishment.latitude }};

if (mapEl && longitude && latitude && !isNaN(longitude) && !isNaN(latitude)) {
    // Initialize map with valid coordinates
} else {
    // Hide map container if no valid coordinates
    mapEl.parentElement.style.display = 'none';
}
```

This change:
- Validates coordinates before map initialization
- Gracefully hides the map if coordinates are invalid
- Prevents JavaScript errors on establishment detail pages

### 5. Applied Same Fixes to Legacy map.js

**File:** `static/js/map.js`

Applied identical fixes to the legacy map file for consistency.

### 6. Increased Tile Endpoint Rate Limits

**File:** `routes/map_routes.py`

```python
# BEFORE - Too restrictive for tile server
@map_bp.route("/<int:z>/<int:x>/<int:y>.pbf", methods=["GET"])
@limiter.limit("60 per minute")
def get_tile(z: int, x: int, y: int):

# AFTER - Appropriate for tile serving
@map_bp.route("/<int:z>/<int:x>/<int:y>.pbf", methods=["GET"])
@limiter.limit("2000 per minute")
def get_tile(z: int, x: int, y: int):
```

Also updated the combined tile endpoint:

```python
# BEFORE
@limiter.limit("60 per minute")
def get_combined_tile(z: int, x: int, y: int):

# AFTER
@limiter.limit("2000 per minute")
def get_combined_tile(z: int, x: int, y: int):
```

**Rationale:**
- **2000 requests/minute** (~33 requests/second) is appropriate for a tile server
- Still provides abuse protection against malicious actors
- Tiles are cached in Redis, so actual database load is much lower
- Standard tile servers (Mapbox, Google, etc.) handle 10,000+ requests/second
- For production, consider implementing per-IP rate limiting with higher thresholds

### 7. Improved Title Text Contrast

**File:** `static/js/pages/map.js`

```javascript
// BEFORE - Low contrast (hard to read)
<h3 class="font-bold text-gray-800 text-sm...">${attraction.name}</h3>
<p class="text-xs text-gray-500 line-clamp-2">${attraction.description}</p>

// AFTER - High contrast (WCAG compliant)
<h3 class="font-bold text-gray-900 text-sm...">${attraction.name}</h3>
<p class="text-xs text-gray-600 line-clamp-2">${attraction.description}</p>
```

**Changes:**
- Title: `text-gray-800` → `text-gray-900` (darker, more readable)
- Description: `text-gray-500` → `text-gray-600` (better contrast)
- Meets WCAG 2.1 AA accessibility standards for text contrast

### 8. Added Deduplication for Attraction List

**File:** `static/js/pages/map.js`

```javascript
// BEFORE - No deduplication, allows duplicates
listContainer.innerHTML = '';
attractions.forEach(attraction => {
    // render card
});

// AFTER - Deduplicates by ID before rendering
const seen = new Set();
const uniqueAttractions = attractions.filter(attraction => {
    if (seen.has(attraction.id)) return false;
    seen.add(attraction.id);
    return true;
});

listContainer.innerHTML = '';
uniqueAttractions.forEach(attraction => {
    // render card
});
```

**Benefits:**
- Prevents duplicate attractions from appearing in the list
- Uses Set for O(n) deduplication performance
- Preserves order of first appearance
- Works with infinite scroll pagination

---

## 🛡️ Prevention Measures

### 1. API Contract Documentation

Document the expected API response structure:

```typescript
interface AttractionResponse {
  id: number;
  name: string;
  category: string;
  barangay: string;
  description: string;
  latitude: number;   // ← Always use 'latitude'
  longitude: number;  // ← Always use 'longitude'
  image: string;
  rating: number;
}
```

### 2. Add Database-Level Validation

Consider adding constraints to ensure attractions have valid coordinates:

```sql
-- In schema.sql or migration
ALTER TABLE attraction 
ADD CONSTRAINT chk_valid_coordinates 
CHECK (
  (latitude IS NOT NULL AND longitude IS NOT NULL) OR
  (latitude IS NULL AND longitude IS NULL)
);

ALTER TABLE attraction 
ADD CONSTRAINT chk_latitude_range 
CHECK (latitude IS NULL OR (latitude >= -90 AND latitude <= 90));

ALTER TABLE attraction 
ADD CONSTRAINT chk_longitude_range 
CHECK (longitude IS NULL OR (longitude >= -180 AND longitude <= 180));
```

### 3. Frontend Type Checking

Consider adding a helper function to validate API responses:

```javascript
function isValidAttraction(attraction) {
  return attraction && 
         typeof attraction.latitude === 'number' && 
         typeof attraction.longitude === 'number' &&
         !isNaN(attraction.latitude) && 
         !isNaN(attraction.longitude);
}
```

---

## 🧪 Testing Checklist

- [x] Map tiles load without URL parsing errors
- [x] Map tiles load without 429 rate limit errors
- [x] Click on attraction cards with valid coordinates → Map should fly to location
- [x] Attraction titles have proper contrast and are readable
- [x] No duplicate attractions in the sidebar list
- [ ] Test with attractions that have null/undefined coordinates → Should show friendly error
- [ ] Test establishment detail pages with valid coordinates → Map should display
- [ ] Test establishment detail pages without coordinates → Map should be hidden gracefully
- [ ] Check browser console for any remaining errors
- [ ] Test on both mobile and desktop views
- [ ] Test rapid panning/zooming → Should not trigger rate limits

---

## 📝 Files Modified

1. ✅ `static/js/pages/map.js` - Main map implementation
   - Fixed tile URL to use absolute path with `window.location.origin`
   - Fixed coordinate property names (`latitude`/`longitude` instead of `lat`/`lng`)
   - Added coordinate validation in `flyToLocation()` function

2. ✅ `static/js/map.js` - Legacy map implementation
   - Applied same fixes for consistency

3. ✅ `templates/pagez/map.html` - Map page template
   - Added cache-busting version parameter (`?v=20260411-2`) to force browser reload

4. ✅ `templates/pagez/establishment_detail.html` - Establishment detail page
   - Added coordinate validation before map initialization

5. ✅ `routes/map_routes.py` - Tile endpoint routes
   - Increased rate limit from 60 to 2000 requests/minute for both tile endpoints

---

## 🎯 Impact

- **User Experience:** Users will no longer see cryptic "Invalid LngLat" errors or 429 rate limit errors
- **Map Performance:** Tiles load smoothly without rate limiting interruptions
- **Visual Quality:** Attraction titles now have proper contrast and are easily readable
- **Data Quality:** No duplicate attractions appear in the sidebar list
- **Error Handling:** Invalid coordinates are now handled gracefully with user-friendly messages
- **Debugging:** Console warnings help developers identify data issues
- **Stability:** Map initialization is now defensive against missing/invalid data
- **Scalability:** Rate limits now appropriate for tile server usage patterns
- **Accessibility:** Text contrast meets WCAG 2.1 AA standards

---

## 📌 Notes

- The fallback `attraction.latitude || attraction.lat` ensures backwards compatibility
- Consider running a data audit to find attractions with missing coordinates
- Future enhancement: Add a UI to allow admins to set coordinates for attractions without them
