# Cultural Content Flowchart

This flowchart documents how users access various cultural content types including events, gallery media, and heritage catalogs.

## Mermaid Diagram

```mermaid
graph TD
    Start([Start]) --> Index[Public Index]
    Index --> Choice{Browse Selection}
    
    Choice -- Events --> IsEvents{Selected Events?}
    IsEvents -- Yes --> ViewEvents[GET /events<br/>Approved Events Catalog]
    
    Choice -- Gallery --> IsGallery{Selected Gallery?}
    IsGallery -- Yes --> ViewGallery[GET /gallery<br/>Approved Media Items]
    
    Choice -- Heritage --> IsHeritage{Selected Heritage?}
    IsHeritage -- Yes --> ViewHeritage[GET /heritage<br/>Heritage Type Catalog]
    ViewHeritage --> SelectType{Select Category?}
    SelectType -- Yes --> ListItems[GET /heritage/type<br/>Specific Heritage List]
```

## Description
1.  **Central Hub**: The homepage acts as the entry point to all cultural data.
2.  **Modular Access**: Users can jump into three distinct content streams:
    - **Events**: Chronological listing of local festivals and activities.
    - **Gallery**: Visual media uploaded by contributors and approved by admins.
    - **Heritage**: A multi-category catalog of tangible and intangible cultural assets.
3.  **Filtered Discovery**: For heritage items, users first browse by type (e.g., Architecture, Traditions) before seeing specific entries.
4.  **Admin Gating**: Only content marked as `approved` is visible in these public views.
