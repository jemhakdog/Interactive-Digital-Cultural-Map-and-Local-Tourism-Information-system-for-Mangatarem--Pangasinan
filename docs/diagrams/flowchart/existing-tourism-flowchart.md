# Existing Tourism Flowchart (Manual Navigation)

This flowchart documents the legacy manual process tourists follow in Mangatarem, highlighting the dependency on physical visits and paper-based navgation.

## Mermaid Diagram

```mermaid
graph TD
    Start([Start: Tourist Arrives<br/>In Mangatarem]) --> VisitOff[Visit Municipal Tourism Office<br/>(Physical Visit)]
    VisitOff --> ReqInfo[Request Information/<br/>Brochures]
    ReqInfo --> RecPaper[Receive Paper Map /<br/>Verbal Directions]
    RecPaper --> ManNav[Manual Navigation to Site<br/>(No GPS/Digital Map)]
    ManNav --> VisitAttr[Visit Attraction<br/>(Risk: Closed/Hard to Find)]

    style ManNav fill:#f99,stroke:#333,stroke-width:2px,color:black
    style VisitAttr fill:#cfc,stroke:#333,stroke-width:2px,color:black
```

## Description
1.  **Start**: Tourist arrives in town without digital guidance.
2.  **Physical Visit**: Mandatory stop at the Tourism Office for basic data.
3.  **Low-Tech Information**: Dependency on brochures and verbal cues.
4.  **Inefficient Navigation**: Mapping is handled manually without GPS support.
5.  **Outcome Risk**: Tourists may reach attractions only to find them inaccessible or closed.
