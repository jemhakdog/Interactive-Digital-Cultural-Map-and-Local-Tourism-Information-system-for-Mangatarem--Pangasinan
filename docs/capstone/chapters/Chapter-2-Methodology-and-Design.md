# Chapter 2: Methodology and Design

This chapter presents the methodology and system design adopted in the development of the Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan. It outlines the Rapid Application Development (RAD) model combined with a Participatory GIS (PGIS) framework, chosen to guide the planning, prototyping, construction, and deployment of the platform. Additionally, it details the primary sources of data, the data gathering techniques employed, and the structural design of the system through architectural blueprints, process flowcharts, dataflow diagrams, and entity-relationship diagrams, culminating in a structured project timeline and implementation strategy.

## Software Development Methodology

In software engineering, the use of a well-defined software development methodology (SDM) is crucial for ensuring a structured, efficient, and goal-oriented approach to system development. It serves as a comprehensive framework that guides developers in systematically planning, designing, implementing, testing, and maintaining a software application. For the proposed Interactive Digital Cultural Map and Local Tourism Information System, selecting an appropriate SDM is essential to align the project with the municipal government's specific administrative workflows, spatial data constraints, and development timeframe.

This study adopted the Rapid Application Development (RAD) methodology, integrated with a Participatory GIS (PGIS) framework. RAD was selected due to its iterative nature and strong focus on rapid prototyping and continuous stakeholder feedback over rigid, paper-based planning. Given the fragmented, manual, and delay-prone state of the current tourism reporting workflows in Mangatarem, the RAD model provides the developers with the flexibility to quickly build functional web prototypes (such as the interactive map and content moderation dashboard) and refine them in response to direct feedback from LGU staff. The PGIS framework ensures that local barangay representatives actively participate in defining how their cultural heritage is spatially represented, thereby increasing data accuracy and community ownership of the platform.

The RAD methodology is characterized by short development cycles and continuous user involvement, which minimizes the risk of structural misalignment and ensures that the final computing solution meets the exact needs of its beneficiaries. The development lifecycle is structured into four primary phases: Requirements Planning, User Design, Construction, and Cutover.

1. **Requirements Planning** – During the Requirements Planning phase, the developers conducted consultations and interviews with LGU Tourism Office officers and Barangay Representatives to analyze the current manual communication workflow, define the project boundaries, and establish the core system requirements. The objective was to identify existing bottlenecks, determine the system's target users, and map out the necessary administrative and public modules.
2. **User Design** – The User Design phase involved creating interactive client wireframes and user interface mockups using design tools such as Figma. These mockups—including the full-screen spatial map, barangay submission forms, and administrative moderation screens—were presented to stakeholders for iterative evaluations, ensuring that the navigation logic, layout, and visual accessibility aligned with user expectations.
3. **Construction** – In the Construction phase, the developers converted approved Figma designs into a functional web application. The frontend interface was engineered using HTML5, CSS3 (utilizing the Tailwind CSS framework), Mapbox GL JS for spatial mapping, and JavaScript. The server-side logic was built in Python using the Flask micro-framework, with PostgreSQL serving as the primary relational database, hosted via Supabase Cloud. Unit testing and feature iterations were conducted continuously during this phase to ensure technical compliance.
4. **Cutover** – The final phase, Cutover, involves performing comprehensive system testing, migrating historical cultural data from physical folders into the PostgreSQL database, conducting training seminars for LGU officers and Barangay Representatives, and deploying the completed platform to the live production server (Vercel) for public launch.

## Sources of Data

The sources of data in this study are integral to understanding the operational challenges and user requirements related to managing municipal tourism and cultural data in Mangatarem, Pangasinan. These sources encompass individuals, administrative groups, and localized data archives that provide primary and secondary information:

- **LGU Tourism Office Staff** – Municipal tourism officers and IT staff who provide official tourism guidelines, municipal promotion policies, and administrative moderation rules. They serve as the primary source for content moderation standards and system access parameters.
- **Barangay Officials and Representatives** – Authorized contributors from each barangay who act as vital sources of grassroots historical narratives, localized heritage sites, natural attractions, and community traditions that are not centrally documented.
- **Municipal Archives and Physical Records** – Printed brochures, historical municipal profiles, local heritage reports, and physical document registries maintained by the LGU, which serve as secondary data sources to establish the database's initial cultural inventory.
- **Tourism and Heritage Stakeholders** – Tourists, local residents, and academic researchers whose feedback during surveys and testing provided usability, navigational, and feature expectations for the public-facing interactive map and digital atlas.

## Data Gathering Techniques

To gather comprehensive qualitative and quantitative data for system requirements and post-development evaluation, the developers implemented four distinct data gathering techniques:

**Surveys and Questionnaires**
- *How*: The developers designed and distributed structured survey questionnaires to select tourist visitors, local residents, and academic researchers. The surveys utilized a 5-point Likert scale to assess user expectations regarding information accessibility, preferences for digital spatial mapping, and common difficulties encountered when searching for cultural data.
- *When*: This technique was applied during the early stages of the Requirements Planning phase to establish a quantitative baseline of user needs, and subsequently during the Cutover phase to evaluate system usability.
- *Why*: The quantitative data collected helped the development team prioritize critical public features—such as spatial category filtering and the Digital Cultural Atlas search engine—ensuring the system is highly responsive to public and academic requirements.

**Interviews**
- *How*: Semi-structured, face-to-face interviews were conducted with the central LGU Tourism Office staff and designated Barangay Representatives. The developers utilized an interview guide containing open-ended questions regarding their daily workflows, data submission habits, and system features.
- *When*: Interviews were executed during the first phase of the development lifecycle (Requirements Planning) to gather deep qualitative insights directly from internal users.
- *Why*: This method allowed the developers to analyze the procedural bottlenecks of the legacy manual system, providing the necessary workflow parameters to design the secure Barangay Portal and central Content Moderation Dashboard.

**Observation**
- *How*: The developers conducted direct, non-participant observation of the daily operations at the Municipal Tourism Office, documenting how staff process tourist inquiries, verify incoming cultural updates, and physically catalog historical folders.
- *When*: Direct observations were conducted concurrently with interviews during the Requirements Planning phase.
- *Why*: Witnessing the manual operations firsthand enabled the developers to identify procedural delays, document security risks, and user frustrations that stakeholders might omit during interviews, thereby validating the need for automated moderation.

**Document Analysis**
- *How*: The developers analyzed physical tourism brochures, manual barangay profile folders, local historical documents, and official national heritage guidelines matching NCCA cultural registry forms (Form 01–07).
- *When*: This technique was executed during the prototyping and initial construction stages.
- *Why*: Document analysis provided the exact schema and data fields required for the SQL database, ensuring that the digital forms in the developed system collect accurate, standardized heritage data matching national registry guidelines.

## System Design

### System Architecture

The System Architecture design represents the structural blueprint detailing the components, logical layers, and data transactions of the software system. It defines how users, network protocols, server instances, and data persistence engines are integrated to deliver a secure and highly responsive service.




The architecture follows a modern three-tier client-server model, ensuring a secure and optimized separation of concerns. At the **Client Layer**, users access the system via modern web browsers on mobile phones or desktops. The public-facing interface utilizes HTML5, Tailwind CSS, and vanilla JavaScript, with **Mapbox GL JS** integrated for real-time spatial vector tile rendering. The **Cloud Platform Layer** is hosted on **Vercel**, serving the frontend static files and executing backend application logic written in **Python** using the **Flask** framework as serverless API routes. This layer is responsible for processing requests, managing user authentication via secure cookies, and conducting data validation. The **Data Persistence Layer** is anchored on **Supabase**, hosting the managed **PostgreSQL** database (containing users, heritage profiles, and audit log tables) and Object Storage for high-resolution photography uploads. Additionally, **Upstash Redis** is integrated within this layer to cache georeferenced spatial datasets, reducing database load and ensuring low-latency rendering of map pins on the client interface.

### Existing Process Flowchart

A process flowchart is a graphical representation that utilizes standardized symbols to illustrate the sequential steps, logic checkpoints, and data directions of an operational workflow. In system analysis, a flowchart is critical to visualize the "as-is" manual processes, facilitating the identification of bottlenecks, redundancies, and structural vulnerabilities.


The flowchart delineates the two manual, inefficient workflows currently used in Mangatarem, revealing significant informational delays and data synchronization issues. The tourist inquiry workflow (Left Path) highlights that visitors seeking local information must either browse unverified, fragmented social media pages—which often contain conflicting or outdated details, causing tourist confusion—or travel physically to the Municipal Tourism Office. At the office, staff must manually search through physical binders and handwritten logs. If a document is misplaced or in use, the tourist is left without data, resulting in operational inefficiencies. 

The content reporting workflow (Right Path) illustrates that when a Barangay Representative seeks to update a cultural record or report an upcoming event, they submit physical documents or send unstandardized SMS text messages to the central Tourism Office. This forces central staff to manually sort and transcribe disparate data formats. Any missing details require a repetitive cycle of follow-up phone calls, creating severe time lags. By the time the LGU compiles, verifies, and publishes these updates via printed brochures or social media announcements, the information is often already outdated, highlighting the urgent need for digital automation.

### Dataflow Diagram (DFD)

A Dataflow Diagram (DFD) is a logical design tool used to visualize the flow of information through a system, mapping the inputs, processing routes, data storage components, and outputs. In system design, DFD notation utilizes specific geometric symbols to model data pathways: External Entities are represented as rectangles, Processes as rounded squares, Data Stores as open-ended rectangles, and Data Flows as labeled directional arrows.

The Level-1 Dataflow Diagram details how information moves between external actors, processing modules, and data repositories. **General Public and Academic Users (EE1)** input search parameters and category filters into Process 1.0 (Browse & Spatial Map Search). This process queries Data Store D2 (Tourist Spots & Heritage Data Store) to retrieve georeferenced map coordinates and cultural atlas profiles, rendering them back to the client interface. 

For internal administrative data management, **Barangay Representatives and LGU Administrators (EE2)** interact with Process 2.0 (Content Submission & Moderation). Barangay representatives input structured cultural records and media assets through the secure submission dashboard, which writes temporary records to Data Store D2 in a pending status. The LGU Administrator retrieves these pending submissions, conducts qualitative reviews, and inputs moderation statuses (approve/reject). Once approved, Process 2.0 updates the record status in Data Store D2, making it immediately accessible to Process 1.0 for public rendering. Access permissions, logins, and session audit logs are validated by verifying user credentials against Data Store D1 (User Accounts & Roles Data Store).

### Entity-Relationship Diagram (ERD)

#### 1. Definition, Importance, and Purpose of the ERD

An Entity-Relationship Diagram (ERD) is a structural database design tool that visually maps the logical architecture of a relational database. It defines the core data tables (entities), the specific data fields that characterize them (attributes), and the referential integrity rules (relationships) that connect them. In database engineering, the ERD serves as a conceptual blueprint that bridges abstract user requirements and physical SQL schemas. It prevents data redundancy, guarantees referential integrity through primary and foreign keys, optimizes query join execution paths, and provides a scalable data framework that accommodates future system expansions without database corruption.

#### 2. ERD Illustration

#### 3. Comprehensive Discussion of ERD Content

The system's database schema consists of fifteen highly integrated, normalized tables designed to capture geographic coordinates, cultural records, user privileges, and security audit logs:

##### A. Entities (Uppercase, Singular Form)
1. `USER`: A singular authenticated user account holding a defined role (Admin, Contributor, Public, Guard).
2. `PASSWORD_RESET_TOKEN`: A secure, short-lived verification token linked to a `USER` for password recovery.
3. `BARANGAY_INFO`: The municipal administrative boundary acting as the geographic anchor for all spots and events.
4. `HERITAGE_PROFILE`: The registry file matching national NCCA inventory standards (Form 01–07) for cultural assets.
5. `ATTRACTION`: A georeferenced tourism destination or landmark within the municipality.
6. `EVENT`: A scheduled local cultural festival, religious event, or municipal calendar announcement.
7. `ESTABLISHMENT`: A local hospitality or dining business registered in the tourism directory.
8. `ESTABLISHMENT_ROOM`: A room category or accommodation option offered by a lodging `ESTABLISHMENT`.
9. `ESTABLISHMENT_MENU_ITEM`: A food or beverage selection provided by a dining `ESTABLISHMENT`.
10. `ESTABLISHMENT_REVIEW`: An authenticated customer review, rating, and testimonial submitted for an `ESTABLISHMENT`.
11. `REVIEW_PHOTO`: A multimedia photo upload linked to a specific `ESTABLISHMENT_REVIEW` for visual validation.
12. `USER_FAVORITE_ESTABLISHMENT`: A joining table linking a `USER` to their bookmarked `ESTABLISHMENT` entries.
13. `VISITOR_LOG`: A checkpoint security entry recording visitor entries and exits at landmarks (managed by Guards).
14. `NEWSLETTER_SUBSCRIBER`: A visitor-submitted email subscription powering municipal tourism updates.
15. `DATABASE_AUDIT_LOG`: An immutable chronological trail capturing all administrative changes to ensure accountability.

##### B. Attributes (Characteristics, Primary Keys, and Foreign Keys)
Attributes define the columns or properties characterizing each entity.
* **Primary Keys (PK)**: System-wide unique identifiers that enforce entity integrity, represented first in the attribute list and visually *underlined* (e.g., `id` columns across all tables).
* **Foreign Keys (FK)**: Relational fields referencing a PK in another table to enforce referential integrity.
  * In the `USER` entity, `id` is the underlined PK. The attribute `barangay_id` is an FK referencing the PK of the `BARANGAY_INFO` table, linking the user to a specific jurisdiction.
  * In the `HERITAGE_PROFILE` entity, the primary key `id` is underlined, and `barangay_id` is an FK referencing `BARANGAY_INFO`, while `attraction_id` is an optional FK referencing `ATTRACTION`.
  * In the `ESTABLISHMENT_ROOM` entity, `id` is the underlined PK, and `establishment_id` is an FK referencing `ESTABLISHMENT`, linking room records directly to their business parent.

##### C. Relationships (Cardinality, Optionability, and Labels)
The relational associations within the database are primarily characterized by **one-to-many (1:N)** cardinallity:
1. **`USER` to `PASSWORD_RESET_TOKEN` (1:N)**: A one-to-many relationship where one `USER` can request multiple secure reset tokens. The relationship is *optional* for `USER` but *mandatory* for `PASSWORD_RESET_TOKEN`. **Label**: "requests".
2. **`BARANGAY_INFO` to `USER` (1:N)**: A one-to-many relationship where a barangay can have multiple registered user accounts. The relationship is *optional* for the barangay (as some barangays may not have registered contributors yet) but *mandatory* for user profile association. **Label**: "stewards".
3. **`BARANGAY_INFO` to `HERITAGE_PROFILE` (1:N)**: A one-to-many relationship mapping cultural records to geographic boundaries. It is *mandatory* for `HERITAGE_PROFILE`. **Label**: "contains".
4. **`BARANGAY_INFO` to `ESTABLISHMENT` (1:N)**: A one-to-many relationship mapping local businesses to administrative locations. It is *mandatory* for `ESTABLISHMENT`. **Label**: "locates".
5. **`BARANGAY_INFO` to `EVENT` (1:N)**: A one-to-many relationship where a barangay hosts multiple calendar events. It is *mandatory* for `EVENT`. **Label**: "hosts".
6. **`HERITAGE_PROFILE` to `ATTRACTION` (1:1 / optional 1:N)**: A flexible link where a national heritage record can optionally be mapped to a tourist spot. It is *optional* for `HERITAGE_PROFILE`. **Label**: "promotes".
7. **`ESTABLISHMENT` to `ESTABLISHMENT_ROOM` (1:N)**: A one-to-many relationship mapping rooms to lodging businesses. It is *mandatory* for the room record to point to a parent business. **Label**: "offers".
8. **`ESTABLISHMENT` to `ESTABLISHMENT_MENU_ITEM` (1:N)**: A one-to-many relationship mapping dishes to restaurants. It is *mandatory* for the menu item. **Label**: "serves".
9. **`ESTABLISHMENT` to `ESTABLISHMENT_REVIEW` (1:N)**: A one-to-many relationship mapping public reviews to business listings. It is *mandatory* for the review table. **Label**: "receives".
10. **`ESTABLISHMENT_REVIEW` to `REVIEW_PHOTO` (1:N)**: A one-to-many relationship mapping uploaded images to reviews. It is *optional* for a review to contain a photo, but *mandatory* for the photo to link to a valid review. **Label**: "includes".
11. **`USER` to `USER_FAVORITE_ESTABLISHMENT` (1:N)**: A one-to-many mapping representing bookmarks. It is *mandatory* for the favorite record to point to a valid user. **Label**: "favorites".
12. **`ESTABLISHMENT` to `USER_FAVORITE_ESTABLISHMENT` (1:N)**: A one-to-many association mapping favorited listings back to the business. It is *mandatory*. **Label**: "is_favorited_by".
13. **`USER` to `VISITOR_LOG` (1:N)**: A one-to-many security logging relationship. A verified guard (represented by `USER`) logs multiple guest entries. It is *mandatory* for `VISITOR_LOG`. **Label**: "logs".
14. **`USER` to `DATABASE_AUDIT_LOG` (1:N)**: A one-to-many accountability mapping. Administrative modifications executed by an authenticated `USER` are chronologically audited. It is *mandatory* for `DATABASE_AUDIT_LOG`. **Label**: "audits".

## Implementation Plan

### Project Timeline

The development timeline is structured around the four distinct phases of the RAD methodology, spanning a total of 13 weeks. To align the project timeline with a realistic academic semester, the schedule is mapped from **June 3, 2024, to August 30, 2024**.

```
    Phase 1: Requirements Planning (Week 1 - Week 2: June 3 - June 14, 2024)
    * Conduct interviews with LGU Tourism Office officers.
    * Perform direct observation of manual workflows.
    * Output: Approved Requirements Document.

    Phase 2: User Design (Week 3 - Week 4: June 17 - June 28, 2024)
    * Develop UI/UX mockups and wireframes in Figma.
    * Conduct prototype reviews and feedback sessions with stakeholders.
    * Milestone: Prototype Approval (June 28, 2024).

    Phase 3: Construction (Week 5 - Week 10: July 1 - August 9, 2024)
    * Set up PostgreSQL database tables and Supabase cloud configurations.
    * Code frontend mapping canvas (Mapbox GL JS) and backend APIs (Flask).
    * Perform unit testing and incremental feature integrations.
    * Milestone: Feature-Complete System Build (August 9, 2024).

    Phase 4: Cutover (Week 11 - Week 13: August 12 - August 30, 2024)
    * Execute system testing (functional, performance, security, usability).
    * Migrate manual records from physical folders to database tables.
    * Conduct user training for LGU staff and Barangay Representatives.
    * Deployment & Public Launch: August 30, 2024.
```


### Deployment Plan

The deployment strategy utilizes a phased release model to ensure system reliability and minimize operational risks:

1. **Phased Pilot Launch (Staging)**: The system will initially be deployed to a secure staging environment. Staging access is restricted to the central LGU Tourism staff and a select pilot group of three (3) Barangay Representatives. This phase focuses on validating the multi-role submission and moderation workflow in real-world scenarios.
2. **Production Migration**: Following the successful validation of the pilot test and resolution of user feedback, the software will be migrated to the production environment. Client-side static files and serverless Flask functions will be deployed on **Vercel** with optimized security headers. Relational data tables will be initialized on the production **Supabase (PostgreSQL)** database instance, with caching paths routed through **Upstash Redis**.
3. **Stakeholder Training**: The development team will conduct comprehensive, localized training seminars at the municipal hall. Training will guide LGU administrators through moderation workflows and account management, while Barangay Representatives will learn to digitize NCCA profiles. Customized user manuals will be distributed.
4. **Public Cutover**: Upon completion of training, the DNS records will be modified to point to the live Vercel domain, officially launching the "Interactive Digital Cultural Map" to the public.

### Resource Requirements

The successful development, execution, and long-term operations of the system require the following technical and physical resources:

**Hardware Resources:**
- **Development Workstations**: Workstations equipped with at least an Intel Core i5/AMD Ryzen 5 processor, 16GB of RAM, and a 500GB SSD to run compilers and database tools.
- **LGU Administrator Station**: An office desktop at the Municipal Tourism Office with at least an Intel Core i5, 8GB RAM, and a high-speed, stable internet connection.
- **Client Devices**: Standard smartphones, laptops, or personal computers with modern browser access for public visitors, barangay contributors, and student researchers.

**Software Resources:**
- **Development Tools**: Visual Studio Code, Git Version Control, Python 3.12+, and the `uv` package manager for secure dependency handling.
- **Prototyping Software**: Figma for UI/UX wireframing and design layouts.
- **Hosting and Cloud Infrastructure**: **Vercel** (serverless hosting), **Supabase** (PostgreSQL relational database and asset storage), and **Upstash** (Redis database caching).
- **Web Browser Support**: Modern, updated web browsers including Google Chrome, Microsoft Edge, Mozilla Firefox, or Apple Safari.

**Human Resources:**
- **Development Team**: Capstone developers responsible for frontend coding, backend API scripting, database engineering, and final deployment.
- **LGU Administrators**: Tourism Office IT staff responsible for reviewing submissions, managing contributor credentials, and maintaining data validity.
- **Barangay Contributors**: Designated representatives responsible for uploading historical facts, photography, and event details for their barangays.
- **Academic Advisors**: The capstone project faculty advisor providing technical guidance and structural validation throughout the study.
