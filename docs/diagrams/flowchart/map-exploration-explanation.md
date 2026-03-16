# Explanation: Map Exploration Flowchart

This flowchart explains the interactive user experience when accessing the digital map of Mangatarem.

### Interactive Workflow:
1.  **Dynamic Loading**: Upon accessing the `/map` route, the system dynamically fetches all verified attractions from the database.
2.  **Visual Representation**: Using **Leaflet.js**, the system renders these results as interactive markers overlaid on the town map.
3.  **Context-Aware Filtering**: Users can utilize a sidebar to filter markers by **Barangay**. This instantly updates the map display to show only relevant points of interest for that specific locality.
4.  **Micro-Interactions**: Clicking a marker triggers a **Popup**, providing a quick snapshot of the location (name, thumbnail, and brief summary).
5.  **Full Discovery**: Users can transition from the map view to a dedicated **Attraction Detail Page** by clicking "View Details," enabling deeper engagement with the town's tourism assets.
