# Explorer Findings: Barangay Directory Analysis

This report maps out the components, routing, layouts, styling sheets, scripts, and configurations relevant to restyling the Barangay Directory page.

---

## 1. Routing & Page Component Entries

* **Legacy Route Redirect**: 
  * **File**: `modules/barangay/routes.py` (lines 27–31)
  * **Endpoint**: `/barangay/`
  * **Behavior**: Returns a `302` redirect pointing to `public_v1.barangays_v1_view`.
* **Modern Active Route**: 
  * **File**: `modules/api_v1/public.py` (lines 273–347)
  * **Endpoint**: `/v1/barangay` (registered under the `public_v1` blueprint prefix `/v1`)
  * **Function**: `barangays_v1_view()`
  * **Behavior**: Queries all active barangay contributor IDs, fetches approved attractions to aggregate tags and representative images, maps the results, and renders `pagez/barangays_v1.html`.
* **Page Template File**: 
  * **File**: `templates/pagez/barangays_v1.html`

---

## 2. Layouts, Navbars, Sidebars, and Default Themes

* **Base Template Layout**:
  * **File**: `templates/base.html`
  * **Components**: 
    * **Navbar**: Sticky global header (lines 85–171) styled with `bg-sapphire-black/95` and sky-blue accents (`#38bdf8` / `text-sky-500`).
    * **Footer**: Detailed global footer (lines 183–350) styled with `bg-sapphire-black` and topographic SVG background decorations.
* **Page Layout (`templates/pagez/barangays_v1.html`)**:
  * **Desktop Sidebar**: Sticky panel (lines 70–101) containing name headers and experience type category filters (`filter-chip`). Currently styled with a white background (`bg-white`) and light borders (`border-F1F5F9`).
  * **Main Content Area**: Holds the header, search bars, "Popular Barangays" horizontal slider, and the "Discovery" grid container.
* **Current Styling Theme**:
  * **Page Background**: Light grey/off-white (`#F8F9FB`).
  * **Card Panels**: White background (`bg-white`) with soft shadows (`box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05)`).
  * **Accent Color**: Sky blue (`#0ea5e9` or `#38bdf8`) used for active filter states and badge tags.
  * **Text Colors**: Dark charcoal/grey text hierarchy (`text-gray-900`, `text-gray-800`, `text-gray-700`).

---

## 3. Style Configurations, CSS, JavaScript, and Data Queries

* **Tailwind Configuration**:
  * **File**: `tailwind.config.js`
  * **Configured Colors**:
    * `primary` palette: Sky blue colors (`#f0f9ff` to `#082f49`).
    * `accent`: Gold (`#D4AF37`).
    * `sapphire-black`: `#0f172a`.
    * `premium-blue`: `#38bdf8`.
    * `royal-blue`: `#1d4ed8`.
* **CSS Files**:
  * **Global CSS**: `static/css/main.css`, `static/css/style.css`.
  * **Page-Specific Styles**: `static/css/pages/barangays_mobile.css` (contains the root variables and explicit layout/card classes for mobile and desktop viewport variations).
* **Frontend JavaScript**:
  * **File**: `static/js/pages/barangays_mobile.js`
  * **Behavior**: Parses JSON data from the `#barangays-data-store` DOM element and handles client-side instant searches and filter selections for categories across the list grid.
* **Backend Data Query / Payload**:
  * Fetches `User.barangay_id` with role `contributor` who are approved.
  * Fetches approved attractions to determine tags (`attraction.category`) and counts.
  * Represents each Barangay with `BarangayInfo.image_url` or falls back to the first available attraction image.
  * Outputs data array into the HTML via a JSON store element: `<div id="barangays-data-store" data-barangays='{{ barangays | tojson | safe }}' class="hidden"></div>`.
