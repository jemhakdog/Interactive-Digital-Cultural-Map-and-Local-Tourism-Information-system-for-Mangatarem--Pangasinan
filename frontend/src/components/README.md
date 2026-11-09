# Component Package: UI & Geospatial Components (`src/components`)

## Overview
Reusable presentation components, layout shells, form controls, and MapLibre GL interactive mapping interfaces.

## Interface
- `MapContainer`: Geospatial map viewport with Carto basemaps, pins, route polylines, and popups.
- `MapSidebar`: Search and filter sidebar with category selectors, barangay filters, and tour routes.
- `MapDetailSheet`: Slide-over inspection drawer for selected destinations.
- `MapGridView`: Responsive card grid alternative to map view.
- `Navbar` & `Footer`: Global site header and navigation bar with role-based routing.
- `HeroSearch`: Quick-filter and autocomplete search bar for public destinations.
- `Button`, `Card`, `Badge`, `Sheet`: Atomic design system components built on `@base-ui/react`.
- `CURATED_TRAILS`, `DEFAULT_PLACES`: Curated tour data and local landmark fallbacks.
- `calculateDistance`, `resolvePlaceImage`: Coordinate math and media asset fallback helpers.

## Invariants
- MapLibre GL renders with Carto GL basemap styles (`voyager`, `positron`, `dark-matter`).
- Local fallback datasets render gracefully when backend API endpoints are unreachable.

## Side Effects
- Browser Geolocation API invoked on locate action.
- Clipboard copy operations for view-sharing links.

## Verification
- Run: `cd frontend && npm run build`
