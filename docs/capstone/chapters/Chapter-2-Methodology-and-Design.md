# Chapter 2: Methodology and Design

This chapter discusses the methodology and design processes employed in developing the Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem. It details the chosen software development methodology, the sources of data, the data gathering techniques applied, and presents the structural design of the system through architectural diagrams and flowcharts, culminating in a planned implementation strategy.

## Software Development Methodology

The implementation of a robust Software Development Methodology (SDM) is crucial in software engineering as it provides a structured framework for planning, creating, testing, and deploying an information system. For the development of the Interactive Digital Cultural Map and Local Tourism Information System, a well-defined SDM ensures that the specific requirements of the Mangatarem LGU and its stakeholders are met systematically, minimizing risks and ensuring the timely delivery of a functional product.

The methodology chosen for this study is Rapid Application Development (RAD). This approach was selected because it emphasizes rapid prototyping and iterative delivery over strict planning. Given the dynamic nature of tourism information and the need to accommodate the evolving input from various Barangay Representatives and the LGU, RAD allows the developers to quickly adapt to feedback without disrupting the overall project timeline.

Rapid Application Development is an agile-based methodology characterized by its flexible, user-centric approach. Its key principles involve continuous stakeholder engagement, where users actively participate in reviewing prototypes. This methodology is typically utilized in projects where user interface constraints are critical, and requirements might shift as the stakeholders visualize the developing software. The primary advantage of RAD is its capability to significantly reduce development time while maintaining high user satisfaction through iterative refinement.

![RAD Methodology](https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Rapid_Application_Development_%28RAD%29.png/500px-Rapid_Application_Development_%28RAD%29.png)
*(Note: Placeholder generic image for illustration. Replace with the specific RAD image from the defense/design assets.)*

The phases of the RAD methodology utilized by the developers are broken down as follows:

1. **Requirements Planning:** In this initial phase, the developers collaborated with the LGU staff and potential users to identify the core problems of the fragmented manual system. Key objectives, such as centralizing data and establishing user roles (Admin, Barangay Representative, Public User), were defined.
2. **User Design (Prototyping):** Developers created interactive prototypes and wireframes of the Interactive Map, Admin Dashboard, and Contributor Portals using Figma. These designs were presented to stakeholders for iterative feedback, ensuring the UI/UX aligned with tourist and administrative expectations.
3. **Construction:** Following the approval of prototypes, the actual coding commenced. Utilizing HTML, CSS, JavaScript for the frontend and PHP/MySQL for the backend, developers built the functional modules in iterative cycles, continuously testing features against the refined requirements.
4. **Cutover (Testing, Deployment, & Maintenance):** The final phase involves comprehensive functional, usability, and security testing. Once the system meets the quality standards, it will be deployed to the LGU's live environment, followed by user training for the Tourism Officers and Barangay Representatives, and ongoing technical maintenance.

## Sources of Data

The primary sources of data for this project are individuals, groups, and locations within the municipality of Mangatarem that hold crucial tourism and cultural information. Key sources include the **LGU Tourism Office Staff**, who provide the official policies, existing manual records, and municipal-level tourism initiatives. **Barangay Officials and Representatives** serve as vital sources for localized cultural data, specific landmarks, and grassroots community events. Additionally, existing **municipal archives, physical maps, and local historical documents** act as secondary data sources to establish the initial database of the system.

## Data Gathering Techniques

To ensure comprehensive and accurate requirement analysis, the following data gathering techniques were applied:

- **Interviews:** Semi-structured interviews were conducted with the Tourism Office Staff and select Barangay Representatives. This technique was chosen to understand *HOW* the current manual sharing of tourism data operates and *WHY* delays occur. It was applied during the Requirements Planning phase to gather qualitative insights directly from the administrators.
- **Observation:** The developers observed the daily workflow of the Tourism Office when handling inquiries and content updates. This was done to identify the specific bottlenecks in their *traditional communication methods* and to determine the necessary features for the Admin Dashboard.
- **Document Analysis:** The team analyzed existing physical tourism brochures, fragmented social media posts, and municipal records. This technique was used to assess the current inconsistency of data formats, which justified the need for a standardized digital database.

## System Design

### System Architecture

The System Architecture diagram illustrates the high-level structural overview of the Interactive Digital Cultural Map system. It defines how the different technological components interact to deliver the service from the users to the backend database.

*(Note: Insert System Architecture Diagram here)*

The architecture follows a standard client-server model. Users (Admin, Barangay Representatives, Public Users, and Students) interact with the system via web browsers on their devices (Client side). The interface, built with HTML/CSS/JS, sends HTTP requests to the Web Server (handled by Apache/PHP). The application logic processes these requests—such as verifying admin credentials or fetching map coordinates—from the Backend Database (MySQL). Once data is retrieved or stored, the server sends the appropriate response back to the client interface. This architecture ensures a secure separation between the user interface and the sensitive central repository.

### Existing Process Flowchart

The flowchart below illustrates the manual/current process of managing and accessing tourism information before the introduction of the digital system.

*(Note: Insert Existing Process Flowchart here)*

The flowchart begins with an individual seeking tourism information or a barangay attempting to update an event. Tourists typically rely on fragmented social media searches or must physically visit the Tourism Office. For data updates, barangay officials submit physical files or use informal chat channels to notify the LGU. The Tourism Office then manually collates this information, a process that is highly prone to delays and inconsistencies. Ultimately, this results in irregular public updates and a high risk of confusion, visibly demonstrating the inefficiencies of the current workflow.

### Dataflow Diagram (DFD)

A Dataflow Diagram (DFD) is utilized to map out the flow of information for any process or system. It highlights where data originates, how it is processed within the system, and where it is stored or outputted.

*(Note: Insert Data Flow Diagram Level 0/1 here. Ensure compliance with external entity (rectangle), process (rounded square), data store, and flow lines formatting)*

The DFD details the interactions between the main external entities and the system. **Public Users/Tourists** send search queries (requests) to the system and receive map data, cultural profiles, and location details in return. **Barangay Representatives (Contributors)** input new content (photos, history, events) into the system's processing module, which temporarily stores it for review. The **System Administrator** interacts with the moderation process, receiving pending submissions and sending approval/rejection statuses. Approved data is then formatted and committed to the main Central Database (Data Store), making it available to the public interface.

### Entity-Relationship Diagram (ERD)

The Entity-Relationship Diagram (ERD) visually represents the logical structure of the system's database by defining the entities, their attributes, and the relationships connecting them.

*(Note: Insert Entity-Relationship Diagram here. Ensure primary keys are underlined and cardinality is indicated)*

The ERD illustrates the core data tables required for the system. The `USERS` entity stores credentials and role types (Admin, Contributor), dictating access levels. The `BARANGAY_PROFILE` entity holds localized data and has a one-to-many relationship with the `TOURIST_SPOT` and `CULTURAL_EVENT` entities, as one barangay can have multiple spots and events. `TOURIST_SPOT` contains attributes such as `Spot_ID` (Primary Key), `Name`, `Description`, `Latitude`, `Longitude`, and `Media_URL`. The `SUBMISSION_LOG` entity links to both the `USERS` (who submitted it) and the `TOURIST_SPOT`/`CULTURAL_EVENT` to track the status (Pending, Approved, Rejected) executed by the Administrator.

### Implementation Plan

The successful deployment of the Interactive Digital Cultural Map requires a structured implementation plan encompassing a timeline, deployment strategy, and resource allocation.

- **Project Timeline (Gantt Chart overview):** 
  - *Weeks 1-2:* Requirements Planning and initial data gathering.
  - *Weeks 3-4:* User Design and Figma prototyping.
  - *Weeks 5-10:* Construction phase (Frontend and Backend development).
  - *Weeks 11-12:* System Testing (Functional, Usability, Security) and bug fixing.
  - *Week 13:* Cutover, user training, and final deployment.
  *(Note: visually represent this using a Gantt Chart in the final document version).*

- **Deployment Plan:** The deployment will follow a phased approach. Initially, a pilot test will be conducted internally with the Tourism Office and a select few Barangay Representatives to validate the content moderation flow. Following pilot adjustments, the system will be migrated to a live production web hosting server. Finally, a formal launch will be coordinated with the LGU, alongside the distribution of customized training manuals for administrators and contributors.

- **Resource Requirements:** 
  - *Hardware:* A minimum of an Intel Core i5 machine with 8GB RAM for the administrative operator at the LGU; standard smartphones/PCs for Public Users and Contributors.
  - *Software:* A reliable cloud-hosting service with SSL certification (HTTPS) for deployment; MySQL database server; standard updated web browsers (Chrome, Edge, Safari).
  - *Human Resources:* At least one trained IT/Tourism staff member to act as the permanent System Administrator; designated Barangay Representatives committed to content contribution.
