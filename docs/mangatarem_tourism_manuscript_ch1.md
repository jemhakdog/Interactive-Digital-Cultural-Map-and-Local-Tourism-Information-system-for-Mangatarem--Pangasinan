INTERACTIVE DIGITAL CULTURAL MAP AND LOCAL TOURISM INFORMATION SYSTEM FOR MANGATAREM, PANGASINAN

Members:
[Insert Names Here]

Professor:
[Insert Professor Name Here]

Chapter I
Introduction

The tourism landscape is currently undergoing a significant digital transformation, driven by the increasing reliance on digital platforms for travel planning, navigation, and cultural discovery. In the local setting, Mangatarem, a first-class municipality in the province of Pangasinan, boasts a rich tapestry of cultural heritage and natural attractions, such as the Manleluag Spring National Park, the historic St. Raymund of Peñafort Parish Church, and various local culinary and natural spots. However, promoting and preserving these assets requires transitioning from traditional, localized promotion to an integrated digital approach. 

In the modern era, leveraging technology to promote local tourism and cultural heritage is not just an option but a necessity to boost economic growth and cultural appreciation. The integration of digital mapping and centralized information systems allows municipalities to showcase their attractions to a wider audience while providing tourists with a seamless, informative, and engaging experience. Within the Philippine context, the Department of Tourism actively encourages Local Government Units (LGUs) to embrace ICT-based solutions to enhance tourism delivery, ensure data accessibility, and support local enterprises.

The Municipality of Mangatarem represents a prime candidate for this technological upgrade. Currently, information regarding its cultural and tourist spots is often fragmented, relying heavily on traditional word-of-mouth, physical brochures, or scattered social media posts. This lack of a centralized, interactive digital presence hinders the municipality's potential to attract and accommodate the modern, tech-savvy traveler. Thus, the implementation of an Interactive Digital Cultural Map and Local Tourism Information System is essential to propel Mangatarem's tourism sector into the digital age.

Issues and Challenges Identified
- Fragmented Information: Currently, information regarding tourist spots, historical sites, and local businesses in Mangatarem is scattered across various unofficial social media pages or offline sources, making it difficult for prospective tourists to plan their visits.
- Lack of Interactive Navigation: Tourists often struggle with navigating the municipality to find specific cultural or natural sites due to the absence of a centralized, interactive map tailored to Mangatarem's local tourism.
- Inefficient Local Promotion: Local businesses, artisans, and cultural heritage sites lack a unified digital platform to showcase their offerings, limiting their visibility and economic opportunities.
- Manual Data Management: The local tourism office relies on traditional methods to track tourist inquiries and manage information, which is labor-intensive and limits the ability to analyze tourism trends effectively.

Main Objective / Purpose of the System
The Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem aims to digitize and centralize tourism and cultural data into a secure, accessible web platform. By integrating interactive mapping technologies, it provides tourists with an engaging way to navigate and explore the municipality's landmarks. This system is designed to promote the rich cultural heritage of Mangatarem, boost local economic growth by highlighting local businesses, and enhance the overall efficiency of the LGU's tourism management.

Key Functions
- Interactive Digital Mapping of cultural and tourist sites
- Centralized Tourism Information and Cultural Profiling
- Local business and amenity directory integration
- Admin dashboard for efficient content management and monitoring

Scope of the System
- Cultural & Tourist Spot Information Management – The system covers the management of data relating to heritage sites, natural parks, and other attractions, allowing administrators to add, update, and categorize locations with historical context, operating hours, and media.
- Interactive Mapping System – The system includes an integrated digital map (via Mapbox/Leaflet) that plots the exact locations of attractions, providing tourists with interactive markers, routing, and spatial awareness.
- Local Business Integration – The system features a directory for local enterprises (e.g., restaurants, souvenir shops, accommodations) to promote the local economy alongside tourism.
- Admin Dashboard – The dashboard provides the LGU Tourism Office with a visual summary of listed sites, user engagement, and analytics, allowing for organized content moderation and reporting.
- Responsive Web Interface – The system provides a mobile-responsive web platform ensuring tourists can access the map and information seamlessly on their smartphones while on the go.

Users of the System
- Administrator (LGU Tourism Office) – Has full control over the system, including managing attraction data, approving local business listings, monitoring site analytics, and configuring system settings.
- Tourists / General Public – End-users who access the web application to view the interactive map, search for tourist spots, read historical information, and plan their itineraries.

Stakeholders
- LGU Mangatarem Tourism Office: Will benefit from a centralized platform to easily manage, update, and monitor tourism data, improving their promotional reach and operational efficiency.
- Local Businesses and Artisans: Will gain increased visibility and potential revenue as tourists can easily locate them through the integrated directory.
- Tourists and Visitors: Will experience a vastly improved, convenient, and informative journey through the municipality, supported by accurate navigation and rich cultural context.

Use Cases
- Administrator (Content & System Management): The Administrator is responsible for maintaining the accuracy and richness of the platform. This role involves Full Access to the database to Create, View, Update, and Delete tourist spot profiles, historical data, and business directories. The Admin also utilizes the dashboard to analyze visitor engagement and generate reports for the LGU.
- Tourist (Exploration & Navigation): The Tourist focuses on consuming the platform's content. Their primary function is utilizing the Interactive Map to locate points of interest, filtering attractions by category, viewing detailed cultural profiles, and finding nearby local businesses to enhance their travel experience.

Hardware, Software and Service Requirements
Hardware Requirements
- Processor: Core i5 or higher (for administration and development)
- Memory: Minimum 8GB RAM
Software Requirements
- VS Code (Development)
- Web Browser (Google Chrome, Safari, etc.)
- Git Version Control
Programming Languages & Frameworks
- JavaScript / TypeScript
- React / Next.js
- Tailwind CSS
- Python (Flask/FastAPI for Backend, if applicable)
- PostgreSQL (Database)
Network Requirements
- Stable Internet Connection
- Cloud Hosting Platform (e.g., Vercel, Render)

Methodology
The researchers adopted the Rapid Application Development (RAD) methodology to ensure the efficient and timely delivery of the system. RAD prioritizes rapid prototyping and continuous user feedback, allowing the researchers to refine the interactive map and user interface based on the actual needs of tourists and the LGU.
- Requirements Planning: Gathering functional requirements through interviews with the Mangatarem Tourism Office to understand the current bottlenecks in tourism promotion and the specific data fields needed for cultural profiling.
- User Design: Creating visual prototypes of the interactive map and content dashboard. Involving stakeholders ensures the interface is intuitive for both tourists on mobile devices and admins on desktops.
- Construction: Developing the core system using modern web frameworks (React/Next.js) and integrating Map APIs for spatial representation. This stage involves iterative coding and testing for performance and accurate geolocation.
- Cutover: System deployment to a cloud server, including comprehensive training for the LGU tourism staff to ensure a smooth transition to managing the new digital platform.

Existing Process Flowchart
A flowchart diagram is essential to map out the current manual procedures related to tourism inquiries and promotion. 
Currently, the process begins when a tourist visits the Mangatarem municipal hall or searches fragmented social media groups for information. The tourist requests the location of a specific site. The staff manually provides a physical brochure or gives verbal directions. If the tourist needs to find local dining, the staff provides recommendations from memory. This process highlights the heavy reliance on manual assistance, lack of self-service access, and the difficulty tourists face in navigating without a unified digital guide.

Entity-Relationship Diagram (ERD)
The ERD for the proposed system showcases core entities: Admin Account, Attraction, Category, Local_Business, and Analytics_Log.
- The Admin Account entity holds credentials and roles to securely manage the platform.
- The Attraction entity contains primary data for cultural and tourist spots (name, history, coordinates). It has a many-to-one relationship with the Category entity (e.g., Natural, Historical, Religious).
- The Local_Business entity stores details for nearby enterprises and is linked to the spatial areas of the attractions.
- The Analytics_Log entity tracks user interactions (e.g., page views, map clicks) linked to specific attractions to aid the Admin in generating tourism reports.

Data Flow Diagram (DFD)
- 1.0 Log in/Out: Entry point for the Admin, verifying credentials against the secure database to grant access to the management dashboard.
- 2.0 View Interactive Map: The core process for Tourists. The system retrieves spatial coordinates and basic info from the Attraction data store and plots them onto the map API interface in real-time.
- 3.0 Search & Filter: Tourists input keywords or select categories. The system queries the database and updates the map and list views to show relevant cultural sites or local businesses.
- 4.0 Manage Tourism Content: The Admin interacts with this process to add or edit attraction profiles. The process updates the Attraction and Category data stores, instantly reflecting changes on the public-facing map.

System Architecture Design
The diagram highlights two primary user roles: the Admin and the Tourist. 
Tourists access the Front-End Web Application via mobile or desktop browsers. The Front-End, built with React, interfaces with a Map API (e.g., Mapbox) to render the interactive map. 
The Front-End sends HTTP/HTTPS requests to the Back-End REST API server, which processes business logic. The Back-End server manages data through Cloud Storage (for images and media of attractions) and a Relational Database (SQL) for structured records. 
The Admin accesses a secured route of the Web Application, requiring authentication, to manage the database content. This cloud-based architecture ensures the system is accessible globally, highly available for tourists, and scalable for future municipal expansion.
