# Chapter 2: Methodology and Design

This chapter presents the methodology and design processes employed in developing the Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan. It discusses the software development methodology selected and its justification, identifies the sources of data used in the study, describes the data gathering techniques applied including how, when, and why each technique was used, and presents the structural design of the system through architectural diagrams, flowcharts, dataflow diagrams, and entity-relationship diagrams. The chapter concludes with a detailed implementation plan that outlines the project timeline, deployment strategy, and resource requirements.

## Software Development Methodology

The implementation of a robust Software Development Methodology (SDM) is crucial in software engineering as it provides a structured, repeatable framework for planning, designing, coding, testing, and deploying an information system. A well-defined SDM ensures that development activities are organized, risks are managed, stakeholder expectations are aligned, and the final product is delivered on time and within scope. For the development of the Interactive Digital Cultural Map and Local Tourism Information System, selecting an appropriate SDM ensures that the specific requirements of the Mangatarem LGU and its diverse stakeholders — including tourism officers, barangay representatives, tourists, and researchers — are systematically addressed throughout the development lifecycle.

The methodology chosen for this study is **Rapid Application Development (RAD)**, integrated with the **Participatory GIS (PGIS)** framework. This approach was selected because it emphasizes rapid prototyping, iterative delivery, and continuous stakeholder feedback over rigid, upfront planning. The integration of PGIS ensures that the 'User Design' phase serves as a collaborative platform where community members—rather than just technical developers—actively contribute to the spatial and cultural representation of their barangays, ensuring higher data accuracy and community ownership of the resulting map. Given the dynamic nature of tourism information — where content requirements, user expectations, and municipal priorities may evolve as stakeholders visualize and interact with early versions of the system — RAD allows the developers to quickly adapt to feedback and refine the system without disrupting the overall project timeline or incurring significant rework costs.

Rapid Application Development is an agile-based methodology originally proposed by James Martin in 1991. It is characterized by its flexible, user-centric approach and shortened development cycles. Its key principles and characteristics include: (1) continuous stakeholder engagement, where end-users actively participate in reviewing prototypes and providing feedback; (2) iterative prototyping, where functional models of the system are built and refined in successive cycles rather than being specified entirely upfront; (3) reuse of existing components and frameworks to accelerate development; and (4) time-boxed iterations that enforce disciplined scheduling. This methodology is typically utilized in projects where user interface quality is critical, requirements are expected to evolve as stakeholders interact with prototypes, and rapid delivery of a functional system is prioritized. The primary advantage of RAD is its capability to significantly reduce development time while maintaining high user satisfaction through iterative refinement and early validation.

```mermaid
%%{init: {'theme': 'dark'}}%%
graph LR
    A[Requirements<br>Planning] --> B[User Design<br>/ Prototyping]
    B --> C[Construction]
    C --> D[Cutover]
    D -.->|Feedback| A

    style A fill:#333,stroke:#fff,stroke-width:2px,color:#fff
    style B fill:#333,stroke:#fff,stroke-width:2px,color:#fff
    style C fill:#333,stroke:#fff,stroke-width:2px,color:#fff
    style D fill:#333,stroke:#fff,stroke-width:2px,color:#fff
```
*(Figure 1: RAD Methodology Phases. Replace with an official RAD methodology diagram from defense assets if required by the panel.)*

The phases of the RAD methodology utilized by the developers are broken down as follows:

1. **Requirements Planning:** In this initial phase, the developers conducted meetings and consultations with the LGU Tourism Office staff and potential end-users to identify the core problems of the existing fragmented manual system. Key project objectives, system scope, user roles (Admin, Barangay Representative, Public User, Student/Researcher), and functional requirements were defined and documented. In alignment with the **Community-Based Information System (CBIS)** philosophy, this phase also focused on identifying local gatekeepers of traditional knowledge and ensuring that the system requirements addressed the preservation of both tangible and intangible cultural assets identified by the community. Data gathering techniques such as interviews, observation, and document analysis were applied during this phase to ensure comprehensive requirement capture.

2. **User Design (Prototyping):** Following requirements gathering, the developers created interactive prototypes, wireframes, and mockups of the system's key modules — including the Interactive Digital Cultural Map, the Admin Dashboard, the Contributor Portal, and the Public User interface — using Figma. These prototypes were presented to stakeholders (LGU staff and select barangay representatives) for review and iterative feedback. Based on stakeholder input, the designs were refined and improved to ensure the user interface and user experience aligned with the expectations and technical capabilities of the target users.

3. **Construction:** Upon approval of the finalized prototypes, the actual coding and system building commenced. Utilizing HTML, CSS (Tailwind CSS), and JavaScript for the frontend interface, and Python with the Flask framework and SQLAlchemy for the backend application logic and database management, developers constructed the functional modules in iterative cycles. Each module was continuously tested against the refined requirements, and feedback from internal testing was used to fix bugs and improve features before moving to the next iteration. This phase included the implementation of the interactive map using Mapbox GL JS, comprehensive content submission and moderation workflows for cultural heritage profiling, user authentication via Flask-Login, and a robust database architecture hosted on Supabase.

4. **Cutover (Testing, Deployment, and Maintenance):** The final phase involves comprehensive system testing — including functional testing, performance testing, security testing, usability testing, and user acceptance testing — to ensure the system meets all quality standards and stakeholder requirements. Once testing is complete and all critical issues are resolved, the system will be deployed to the LGU's production environment. This phase also includes user training sessions for Tourism Office staff and Barangay Representatives, the distribution of user manuals, and the establishment of a maintenance and support plan for ongoing technical assistance post-deployment.

## Sources of Data

The primary sources of data for this project are individuals, groups, and locations within the municipality of Mangatarem, Pangasinan that hold crucial tourism, cultural, and historical information relevant to the system. Key data sources include:

- **LGU Tourism Office Staff** — Municipal tourism officers who provide official tourism policies, existing manual records, promotional materials, and municipal-level tourism initiatives. They serve as the authoritative source for content moderation rules, user access policies, and platform governance requirements.
- **Barangay Officials and Representatives** — Designated individuals from each barangay who serve as vital sources for localized cultural data, specific landmark descriptions, community event schedules, and grassroots heritage information that is not centrally documented at the municipal level.
- **Manleluag Spring National Park and Other Tourist Sites** — Physical locations within Mangatarem that serve as points of reference for mapping coordinates, photographic documentation, and on-site observation of existing visitor information systems (e.g., signage, brochures).
- **Municipal Archives and Physical Records** — Existing physical tourism brochures, printed municipal profiles, historical documents, and past tourism reports maintained by the LGU, which serve as secondary data sources to establish the initial database content of the system.

## Data Gathering Techniques

To ensure comprehensive and accurate requirement analysis, the following data gathering techniques were applied during the development of the system:

- **Interviews:** Semi-structured interviews were conducted with the Tourism Office staff and select Barangay Representatives to gather qualitative insights about the current tourism information management workflow. **How:** The developers prepared an interview guide containing open-ended questions about daily operations, pain points, and desired features, and conducted one-on-one or small-group sessions in person at the LGU office. **When:** Interviews were conducted during the Requirements Planning phase of the RAD methodology, prior to any design or prototyping work, to establish a baseline understanding of stakeholder needs. **Why:** This technique was applied to capture detailed, firsthand accounts of the existing process from the people who perform it daily, ensuring that the system requirements reflect real operational challenges rather than developer assumptions.

- **Observation:** The developers observed the daily workflow of the Tourism Office when handling tourist inquiries, processing content updates, and coordinating with barangay officials. **How:** The team visited the LGU Tourism Office and documented the step-by-step process of how tourism data is currently collected, verified, stored, and shared, noting bottlenecks, redundant tasks, and communication delays. **When:** Observation was conducted concurrently with the interview sessions during the Requirements Planning phase, allowing the developers to corroborate interview responses with actual observed behavior. **Why:** This technique was applied to identify inefficiencies and workflow gaps that stakeholders may not have explicitly mentioned during interviews, providing an objective view of the existing process.

- **Document Analysis:** The team analyzed existing physical and digital tourism-related documents to assess the current state of information management. **How:** The developers reviewed municipal tourism brochures, social media posts, event announcements, barangay submitted reports, and any existing digital records to evaluate data formats, consistency, completeness, and accessibility. **When:** Document analysis was performed during the Requirements Planning phase alongside interviews and observation, and continued into the User Design phase to inform the structure of the database and content templates. **Why:** This technique was applied to identify the inconsistencies and gaps in existing data formats, which justified the need for a standardized digital database and informed the design of content submission forms and data fields.

- **Library Research:** The developers conducted library and online research to gather technical knowledge, review related literature, and study best practices in web-based tourism systems and digital cultural mapping platforms. **How:** Academic journals, conference papers, industry reports, and online resources were searched using platforms such as Google Scholar, IEEE Xplore, and Springer Open to identify relevant studies on tourism information systems, interactive mapping technologies, and content management frameworks. **When:** Library research was conducted throughout the project lifecycle — during Requirements Planning to support objective analysis, during User Design to inform feature selection, and during the writing of Chapter 1's Review of Related Literature. **Why:** This technique was applied to ground the project's design decisions in existing research, particularly the frameworks established by Soncuya (2020) regarding NCCA-LGU legal coordination and the technical WebGIS models of Kumar and Singh (2022). Library research allowed the developers to identify a 'policy-practice gap' between national cultural mandates and local implementation, ensuring that the system incorporates proven best practices in community-led mapping and decentralized content management from both local and international contexts.

## System Design

### System Architecture

The System Architecture diagram provides a high-level structural overview of the Interactive Digital Cultural Map and Local Tourism Information System. It defines how the different technological components — from the user's device to the backend database — interact to deliver the system's services. A clear architecture is important because it establishes the blueprint for the system's technical structure, ensuring that all components are properly integrated, scalable, and secure.

```mermaid
graph TB
    subgraph CLIENT LAYER
        A1[Public User<br/>Web Browser]
        A2[Barangay Representative<br/>Web Browser]
        A3[System Administrator<br/>Web Browser]
        A4[Student / Researcher<br/>Web Browser]
    end

    subgraph CLOUD PLATFORM LAYER (Vercel)
        B1[Flask Application Logic<br/>(Serverless Functions)]
        B2[Mapbox API<br/>(Spatial Services)]
    end

    subgraph DATA PERSISTENCE LAYER (Supabase / Upstash)
        C1[(PostgreSQL Database<br/>Heritage Data, Users,<br/>Establishments, Logs)]
        C2[(Redis Cache<br/>Session & Global Cache)]
        C3[Supabase Storage<br/>(Media Assets)]
    end

    A1 & A2 & A3 & A4 -->|HTTPS Requests| B1
    B1 <-->|SQL Queries| C1
    B1 <-->|Cache Access| C2
    B1 <-->|File Upload/Retrieval| C3
    B1 -->|Map Tiles/Data| B2
    B2 -->|Rendered Map| A1 & A2 & A3 & A4
```
*(Figure 2: System Architecture Diagram. The diagram illustrates the client-server model with three logical layers.)*

The architecture follows a modern three-tier cloud-native model. At the **Client Layer**, users — including Public Users, Barangay Representatives, System Administrators, and Students/Researchers — interact with the system through standard web browsers. The user interface is built with HTML, CSS (utilizing the Tailwind CSS framework), and JavaScript, with **Mapbox GL JS** integrated for high-performance spatial visualization. When a user performs an action, the client sends HTTPS requests to the **Cloud Platform Layer**, hosted on **Vercel**. The backend application logic is implemented in **Python** using the **Flask** framework, running as optimized serverless functions. This layer processes requests such as user authentication, cultural heritage form validation, and content moderation workflows. The **Data Persistence Layer** leverages **Supabase** for its primary PostgreSQL database and object storage, and **Upstash** for Redis-based caching. This layer stores all persistent data, including user accounts, detailed heritage profiles (built, natural, and intangible), business establishment records, and system-wide audit logs. This cloud-native architecture ensures a highly available, secure, and performant separation between the interactive interface and the central data repositories.

### Existing Process Flowchart

A flowchart is a graphical representation of a process that uses standardized symbols — such as rectangles for actions, diamonds for decisions, and arrows for flow direction — to illustrate the sequence of steps, decision points, and outcomes. Flowcharts are important in system analysis because they provide a clear, visual understanding of the current (as-is) process, making it easier to identify bottlenecks, redundancies, and inefficiencies that the proposed system must address.

```mermaid
flowchart TD
    Start([Start: Tourist Needs<br/>Tourism Info]) --> A{Where to<br/>get info?}
    A -->|Social Media| B[Search FB Pages /<br/>Unofficial Sources]
    A -->|Visit LGU| C[Travel to Tourism<br/>Office Physically]
    B --> D{Is info<br/>accurate?}
    D -->|No| E[Confusion /<br/>Misinformation]
    D -->|Yes| F[Tourist Gets Info]
    C --> G[LGU Staff Searches<br/>Physical Files]
    G --> H{Is file<br/>available?}
    H -->|No| I[Information<br/>Unavailable]
    H -->|Yes| J[Tourist Gets Info]

    K([Start: Barangay Has<br/>New Event/Info]) --> L[Prepare Physical Report<br/>or Send Text/Message]
    L --> M[Submit to LGU<br/>Tourism Office]
    M --> N[LGU Staff Manually<br/>Consolidates Reports]
    N --> O{Is data<br/>complete?}
    O -->|No| P[Follow-up via<br/>Phone / Text]
    P --> N
    O -->|Yes| Q[LGU Updates Brochure<br/>or Social Media Post]
    Q --> R[Public Sees Updated<br/>Info with Delay]

    style E fill:#ffcdd2
    style I fill:#ffcdd2
    style P fill:#fff9c4
```
*(Figure 3: Existing Process Flowchart — Manual Tourism Information Management. The red nodes indicate problem areas; the yellow node indicates a delay-prone step.)*

The flowchart illustrates the two primary manual processes currently used in Mangatarem, revealing significant gaps in information accessibility and data synchronization. The first process (Top Path) begins when a tourist seeks information. Currently, the tourist is forced to choose between searching unverified social media pages—which often harbor outdated or conflicting details leading to visitor confusion—or traveling physically to the Municipal Tourism Office. At the office, staff must manually browse through paper-bound records and physical files to answer inquiries. If the relevant file is missing or being used by another officer, the information remains unavailable, resulting in a poor visitor experience. 

The second process (Bottom Path) describes the current information reporting workflow from the grassroots level. When a Barangay Representative has a new cultural event or attraction update, they must either prepare a physical report for delivery or send informal messages via text or social media. This non-standardized communication forces LGU Tourism staff to manually consolidate disparate data formats. Any missing information necessitates a repetitive cycle of phone calls and follow-ups, causing significant time lags. By the time the LGU updates its printed brochures or social media posts, the information is often already weeks old. This flowchart demonstrates that the current reliance on manual, physical-first documentation is the root cause of the municipality's fragmented and delay-prone tourism information ecosystem.

### Dataflow Diagram (DFD)

A Dataflow Diagram (DFD) is a graphical tool used to visualize how data moves through a system. It identifies where data originates (external entities), how it is processed (processes), where it is stored (data stores), and the paths it follows (data flows). DFDs are important in system design because they provide a clear, logical representation of the system's data handling without getting into implementation details, making it easier for both developers and stakeholders to validate that all data requirements are covered.

```mermaid
flowchart LR
    EE1[Public User / Tourist]
    EE2[Barangay Representative]
    EE3[System Administrator]
    EE4[Student / Researcher]

    MS((Main System))

    P1[1.0 Process<br/>Search & Browse<br/>Queries]
    P2[2.0 Process<br/>Content Submission]
    P3[3.0 Process<br/>Content Moderation]
    P4[4.0 Process<br/>Data Retrieval<br/>& Display]

    DS1[(D1: User Accounts<br/>& Roles)]
    DS2[(D2: Tourist Spots<br/>& Cultural Data)]
    DS3[(D3: Submission<br/>Logs)]

    EE1 -->|Search Query /<br/>Browse Request| P1
    P1 -->|Query Parameters| MS
    MS -->|Map Data, POI Details,<br/>Cultural Profiles| P4
    P4 -->|Display Results| EE1

    EE2 -->|Content Submission<br/>(Photos, Events, History)| P2
    P2 -->|New Submission Record| DS3
    P2 -->|Pending Content| MS
    MS -->|Pending Item| P3
    P3 -->|Review & Approve/Reject| EE3
    EE3 -->|Approval Status| P3
    P3 -->|Approved Data| DS2
    P3 -->|Rejection Notice| EE2

    EE4 -->|Research Query| P1
    P4 -->|Historical Data,<br/>Barangay Profiles| EE4

    MS <-->|Read/Write| DS1
    MS <-->|Read/Write| DS2
    MS <-->|Read/Write| DS3
```
*(Figure 4: Dataflow Diagram (Level 1). External entities are shown as rectangles, processes as rounded squares, data stores as open-ended rectangles, and data flows as labeled arrows.)*

The DFD details the interactions between the main external entities and the system processes. **Public Users/Tourists (EE1)** send search queries and browse requests to Process 1.0 (Search & Browse), which forwards these to the Main System. Process 4.0 (Data Retrieval & Display) retrieves map data, points of interest details, and cultural profiles from the system and returns them to the user. **Barangay Representatives (EE2)** submit new content — including photos, event details, and historical descriptions — through Process 2.0 (Content Submission), which stores the submission record in Data Store D3 (Submission Logs) and flags it as pending. The **System Administrator (EE3)** interacts with Process 3.0 (Content Moderation), receiving pending submissions for review. The admin sends an approval or rejection decision, which Process 3.0 uses to either commit the approved data to Data Store D2 (Tourist Spots & Cultural Data) or send a rejection notice back to the contributor. **Students/Researchers (EE4)** submit research queries that are processed through the same search and retrieval pipeline, returning structured historical data and barangay profiles. The system also maintains Data Store D1 (User Accounts & Roles) for authentication and access control, which is read and written by all processes that require user verification.

### Entity-Relationship Diagram (ERD)

An Entity-Relationship Diagram (ERD) visually represents the logical structure of a database by defining the entities (tables), their attributes (columns), and the relationships that connect them. ERDs are important in database design because they provide a clear, conceptual blueprint of how data is organized, ensuring data integrity, eliminating redundancy, and establishing the foundation for writing efficient database queries.

```mermaid
erDiagram
    USER {
        int id PK
        string username
        string email
        string password
        string role
        int barangay_id FK
        boolean is_approved
        datetime created_at
    }

    BARANGAY_INFO {
        int id PK
        string name
        text mission
        text vision
        text history
        text cultural_assets
        json map_geo_json
    }

    HERITAGE_PROFILE {
        int id PK
        string asset_type
        string name_of_asset
        int barangay_id FK
        string usage_status
        float latitude
        float longitude
        string status
        int user_id FK
    }

    ATTRACTION {
        int id PK
        string name
        text description
        string category
        float latitude
        float longitude
        int barangay_id FK
        int heritage_profile_id FK
        string status
    }

    EVENT {
        int id PK
        string name
        text description
        datetime date
        string location
        int barangay_id FK
        string category
        string status
    }

    ESTABLISHMENT {
        int id PK
        string name
        string type
        float latitude
        float longitude
        int barangay_id FK
        int owner_id FK
        string status
    }

    ESTABLISHMENT_ROOM {
        int id PK
        int establishment_id FK
        string name
        float price_per_night
    }

    ESTABLISHMENT_MENU_ITEM {
        int id PK
        int establishment_id FK
        string name
        float price
    }

    DATABASE_AUDIT_LOG {
        int id PK
        int user_id FK
        string action
        string table_name
        datetime created_at
    }

    BARANGAY_INFO ||--o{ ATTRACTION : "located_in"
    BARANGAY_INFO ||--o{ EVENT : "hosts"
    BARANGAY_INFO ||--o{ HERITAGE_PROFILE : "contains"
    BARANGAY_INFO ||--o{ ESTABLISHMENT : "contains"
    BARANGAY_INFO ||--o{ USER : "jurisdiction_over"
    
    USER ||--o{ HERITAGE_PROFILE : "submits"
    USER ||--o{ ATTRACTION : "manages"
    USER ||--o{ EVENT : "manages"
    USER ||--o{ ESTABLISHMENT : "owns"
    USER ||--o{ DATABASE_AUDIT_LOG : "triggers"

    HERITAGE_PROFILE ||--o| ATTRACTION : "links_to"
    ESTABLISHMENT ||--o{ ESTABLISHMENT_ROOM : "offers"
    ESTABLISHMENT ||--o{ ESTABLISHMENT_MENU_ITEM : "serves"
```
*(Figure 5: Entity-Relationship Diagram. The diagram reflects the integrated heritage and tourism ecosystem models.)*

The ERD illustrates the comprehensive data structure of the system, which has evolved beyond simple tourism pins to a full heritage and business management ecosystem. The **USER** entity manages role-based access for Admins, Barangay Contributors, and Business Owners, linked to **BARANGAY_INFO** which serves as the geographic and administrative anchor for all content. The **HERITAGE_PROFILE** acts as a central repository for technical documentation (built, natural, and intangible assets), which can be optionally linked to a public **ATTRACTION** entry. The **EVENT** entity manages the municipality's cultural calendar. To support local commerce, the **ESTABLISHMENT** model manages dining and accommodation data, including child entities like **ESTABLISHMENT_ROOM** and **ESTABLISHMENT_MENU_ITEM**. Finally, the **DATABASE_AUDIT_LOG** ensures security and accountability by tracking all administrative actions. This relational structure ensures that cultural data is preserved with high integrity while providing a flexible foundation for tourism promotion.

### Implementation Plan

The successful deployment of the Interactive Digital Cultural Map and Local Tourism Information System requires a structured implementation plan encompassing a project timeline, a deployment strategy, and a clear definition of resource requirements.

#### Project Timeline

The development schedule is organized around the four phases of the RAD methodology, with key milestones and expected completion dates for each phase.

```mermaid
gantt
    title Project Implementation Timeline (13 Weeks)
    dateFormat  W
    axisFormat  Week %W

    section Requirements Planning
    Stakeholder Interviews & Observation   :w1, 2w
    Document Analysis & Requirements Doc   :w2, 1w

    section User Design
    Figma Wireframing & Prototyping        :w3, 2w
    Stakeholder Review & Design Iteration  :w4, 1w

    section Construction
    Database Design & Setup (PostgreSQL)   :w5, 1w
    Frontend Development (Tailwind, Mapbox) :w5, 5w
    Backend Development (Python, Flask API) :w6, 5w
    Heritage & Business Workflows          :w8, 3w
    Internal Integration Testing            :w10, 2w

    section Cutover
    System Testing (Functional, Performance) :w11, 2w
    User Training & Manual Preparation     :w12, 1w
    Deployment to Vercel & Supabase        :w13, 1w
```
*(Figure 6: Gantt Chart — Project Timeline. Critical milestones include prototype approval at Week 4, feature-complete build at Week 10, and deployment at Week 13.)*

#### Deployment Plan

The deployment of the system will follow a phased approach to minimize risk and ensure a smooth transition for all stakeholders:

1. **Pilot Testing (Internal):** The system will first be deployed to a staging environment accessible only to the LGU Tourism Office staff and a select group of 3–5 Barangay Representatives. During this phase, the content moderation workflow will be validated end-to-end — from submission by a barangay representative, through admin review, to publication on the map. Feedback from pilot users will be collected and used to make final adjustments to the user interface, form fields, and notification messages.

2. **Production Deployment:** Following successful pilot testing and resolution of identified issues, the system will be migrated to a live production environment. The production setup utilizes **Vercel** for frontend and serverless backend execution, and **Supabase** for the managed PostgreSQL database and asset storage. The environment will be configured with automated SSL/TLS certification, production-grade security headers, and an optimized caching strategy using **Upstash Redis**. DNS records will be configured to point to the Vercel deployment.

3. **User Training and Launch:** A formal training session will be conducted for System Administrators, Barangay Representatives, and Business Owners. Training will cover account management, heritage profiling procedures, business listing updates, and moderation workflows. Printed and digital user manuals will be distributed. Following training, the system will be officially launched to the public via official municipal channels.

4. **Post-Launch Support:** After the public launch, the development team will provide a defined support period (e.g., 30 days) during which bugs, user-reported issues, and minor adjustments will be addressed. A maintenance schedule will be established for regular database backups, software updates, and monitoring of system performance.

#### Resource Requirements

The following resources are essential for the successful implementation and operation of the system:

**Hardware Resources:**
- Development machines: A minimum of an Intel Core i5 or equivalent processor with 8GB RAM (16GB recommended) and SSD storage for the development team.
- LGU operator workstation: A desktop or laptop with at least Intel Core i5, 8GB RAM, and a stable internet connection for the designated System Administrator at the Tourism Office.
- End-user devices: Standard smartphones, tablets, or personal computers with web browser access for Public Users, Barangay Representatives, and Students/Researchers.

**Software Resources:**
- Development environment: Visual Studio Code, Python 3.12+, Git for version control, and the `uv` package manager for dependency management.
- Design tools: Figma for UI/UX prototyping and wireframing.
- Production environment: Vercel for web hosting and serverless compute, Supabase for PostgreSQL database and object storage, and Upstash for Redis caching.
- End-user software: Updated standard web browsers (Google Chrome, Microsoft Edge, Mozilla Firefox, or Safari).

**Human Resources:**
- Development team: The capstone project developers responsible for system design, coding, testing, and deployment.
- System Administrator: At least one trained LGU Tourism Office staff member or IT personnel designated as the permanent system administrator, responsible for content moderation, user management, and day-to-day platform oversight.
- Barangay Representatives: One designated contributor per barangay, responsible for submitting and updating local tourism and cultural content.
- Project advisor: The capstone project faculty advisor providing academic guidance and validation throughout the development process.
