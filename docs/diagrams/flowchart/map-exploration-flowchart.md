# Map Exploration Flowchart

This flowchart documents how users interact with the interactive digital map to discover attractions and culture.

## Mermaid Diagram

```mermaid
graph TD
    Start([Start]) --> GetMap[GET /map]
    GetMap --> Fetch[Fetch Approved Attractions]
    Fetch --> Render[Render Leaflet Map & Markers]
    Render --> UserAction{User Action}
    
    UserAction -- Filter Barangay --> FilterBrgy{Selected Barangay?}
    FilterBrgy -- Yes --> UpdateMap[Filter Visible Markers]
    UpdateMap --> UserAction
    
    UserAction -- Explore Map --> ClickMarker{Click Marker?}
    ClickMarker -- Yes --> ShowPopup[Show Attraction Popup]
    ShowPopup --> ClickDetails{Click 'View Details'?}
    
    ClickDetails -- Yes --> DetailPage[Redirect /attraction/id]
    ClickDetails -- No --> UserAction
```

## Description
1.  **Initial Load**: The system fetches all approved attractions and renders them as markers on a Leaflet.js map.
2.  **Interaction Loop**: The user can choose between two primary actions:
    - **Filter**: Narrow down attractions by selecting a specific barangay.
    - **Explore**: Click on markers to see a brief summary (popup).
3.  **Discovery**: From any popup, users can deep-dive into the full attraction details page.
4.  **Real-time Response**: Filtering is handled client-side/via AJAX for a smooth UX.
