# Consolidated Flowchart Explanations

This document provides a comprehensive overview of all system flowcharts and their underlying logic.

---

## 1. Existing Process Flowchart (Legacy)
**Goal**: Visualize the legacy manual data collection method and identify bottlenecks.

### Process Breakdown:
1.  **Manual Field Surveys**: Personnel physically visit sites and fill out paper forms (Forms 01A-07).
2.  **Encoding Phase (Bottleneck)**: Physical data is manually typed into digital documents (Word/Excel), risking human error.
3.  **Physical Submission**: Data is submitted through traditional channels or physical handovers.
4.  **Verification Loop**: Manual approval process. Rejections cause significant return-to-source delays.
5.  **Data Silos**: Approved data is stored in non-interactive, localized databases.

---

## 2. Existing Tourism Flowchart (Manual Navigation)
**Goal**: Highlight the physical dependency and navigation risks of the pre-digital era.

### Process Breakdown:
1.  **Physical Visit**: Requirement to stop at the Municipal Tourism Office.
2.  **Brochure Dependency**: Information limited to printed media or verbal directions.
3.  **Manual Navigation (Bottleneck)**: High risk of getting lost or using inefficient routes without GPS.
4.  **Information Lag**: No real-time status updates for attractions (risk of finding sites closed).

---

## 3. User Registration and Validation
**Goal**: Maintain data integrity and representative accountability during onboarding.

### Critical Decisions:
1.  **Identity Verification**: Uniqueness checks for username and email.
2.  **Role Branching**:
    - **Visitors**: Immediate platform access.
    - **Contributors**: Strict validation required.
3.  **Barangay Representative Constraint**: Only one approved rep per Barangay. Subsequent attempts are blocked.
4.  **Approval Workflow**: New contributors remain "Pending" until Admin verification is complete.

---

## 4. User Login and Authentication
**Goal**: Multi-layered security accommodating different user types.

### Interaction Flows:
1.  **Standard Login**: Primary entry for management roles (Admin/Contributor).
2.  **Google OAuth**: Streamlined "One-Tap" access for general visitors.
3.  **Security Restriction**: High-privilege roles (Admin) cannot use Google login.
4.  **Account Recovery**: Token-based password resets via email.
5.  **Session Management**: Server-side termination upon logout.

---

## 5. Map Exploration
**Goal**: Interactive spatial navigation and tourism discovery.

### Workflow:
1.  **Dynamic Loading**: Fetches approved attractions upon route access.
2.  **Leaflet Visualization**: Renders interactive map markers.
3.  **Barangay Filtering**: Real-time map updates based on locality selection.
4.  **Rich Popups**: Visual thumbnails and quick summaries on click.
5.  **Deep Discovery**: Transition from map to full detail pages.

---

## 6. Cultural Content Navigation
**Goal**: Path-based access to curated cultural repositories.

### Navigation Streams:
1.  **Public Index**: Central hub for all cultural data.
2.  **Events**: Catalog of local festivals and town activities.
3.  **Gallery**: Approved visual media and tourism assets.
4.  **Heritage Catalog**: Categorized browsing for tangible and intangible assets.
5.  **Admin Gating**: Public views are strictly restricted to "Approved" entries.
