# Defense Presentation Guide: Technical Diagrams Explanation
## Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan

---

## 📋 TABLE OF CONTENTS

1. [Flowchart of Existing Processes](#1-flowchart-of-existing-processes)
2. [Entity-Relationship Diagram (ERD)](#2-entity-relationship-diagram-erd)
3. [Data Flow Diagram (DFD)](#3-data-flow-diagram-dfd)
4. [Software Development Methodology](#4-software-development-methodology)

---

## 1. FLOWCHART OF EXISTING PROCESSES

### 🎯 **What to Show the Panelists**

Display the flowchart diagram (`docs/diagrams/flowchart_p1.png` through `flowchart_p4.png`) showing the current manual heritage data collection process.

### 📝 **Script for Team Member Presentation**

#### **Introduction (30 seconds)**
"Good morning/afternoon, panelists. Let me walk you through our **Flowchart of Existing Processes**, which illustrates how the Tourism Office of Mangatarem currently manages cultural and tourism data collection."

#### **Step-by-Step Explanation (2-3 minutes)**

**Starting Point:**
"The process begins when a user visits the website. However, the real workflow starts with **Manual Heritage Data Collection** - this is where our current system faces its first challenge."

**Current Process Flow:**

1. **Manual Field Survey (Top of Flowchart)**
   - "Tourism officers and barangay representatives physically visit heritage sites"
   - "They fill out **7 different paper forms** (Forms 01A through 07)"
   - "These forms cover: Natural Resources, Buildings, Archaeological Sites, Intangible Heritage, Personalities, Cultural Institutions, and LGU Programs"

2. **Manual Digitization & Encoding**
   - "After collection, data must be manually encoded into digital formats"
   - "This is done using Microsoft Word and Excel"
   - "Each form requires separate data entry"

3. **Barangay Dashboard Submission**
   - "Barangay representatives access the system dashboard"
   - "They create new attraction or event entries"
   - "Information is submitted for approval"

4. **Admin Review Process (Decision Point)**
   - "The Municipal Tourism Office reviews all submissions"
   - "This is a **critical decision point**: Approve or Reject?"
   - "If rejected, comments are added and returned to the submitter"
   - "If approved, content status is set to 'Approved'"

5. **Database Storage**
   - "Approved data is saved to Supabase (PostgreSQL database)"
   - "Data becomes available for public viewing"

6. **Public Access**
   - "Tourists and residents can now browse the interactive map"
   - "They can filter by category or location"
   - "View detailed attraction information"

#### **Highlighting Inefficiencies (1 minute)**

"**Key Bottlenecks We Identified:**

1. **Paper-Based Filing System**
   - Physical forms are prone to damage and loss
   - Requires manual storage and retrieval
   - Time-consuming to search for specific records

2. **Manual Data Entry**
   - High risk of human error during encoding
   - Duplicate entries are common
   - No real-time validation

3. **Error-Prone Retrieval**
   - Finding historical data requires manual searching
   - No centralized search functionality
   - Updates require re-processing entire forms

4. **Approval Delays**
   - Physical submission of forms causes delays
   - No notification system for status updates
   - Contributors don't know if their submission was received

**These inefficiencies established the foundation for developing our proposed digital system.**"

---

## 2. ENTITY-RELATIONSHIP DIAGRAM (ERD)

### 🎯 **What to Show the Panelists**

Display the ERD diagram (`docs/diagrams/erd.drawio` or `erd_v1.drawio`) showing all entities, attributes, and relationships.

### 📝 **Script for Team Member Presentation**

#### **Introduction (30 seconds)**
"Now, let me present our **Entity-Relationship Diagram**, which defines how data is structured and managed within our system. This ERD ensures data integrity and supports all system functionalities."

#### **Entity-by-Entity Explanation (3-4 minutes)**

**1. USER Entity**
- "**Purpose**: Manages all user accounts and authentication"
- "**Key Attributes**:
  - `id` (Primary Key) - Unique identifier for each user
  - `username` (Unique) - User's login name
  - `email` (Unique) - For communication and notifications
  - `password_hash` - Securely stored password
  - `role` - Defines access level (admin, contributor, user)
  - `is_approved` - For contributor approval workflow"
- "**Significance**: Implements role-based access control critical for our multi-tier user system"

**2. ATTRACTION Entity**
- "**Purpose**: Stores all tourism and cultural attraction information"
- "**Key Attributes**:
  - `id` (Primary Key)
  - `name` - Attraction name
  - `description` - Detailed information
  - `latitude`, `longitude` - GPS coordinates for map display
  - `category` - Type of attraction (Historical, Natural, Cultural, etc.)
  - `status` - Approval status (pending/approved/rejected)
  - `created_by` (Foreign Key → User.id) - Who submitted it
  - `barangay_id` (Foreign Key → BarangayInfo.id) - Location reference"
- "**Significance**: Core entity for the interactive map feature"

**3. EVENT Entity**
- "**Purpose**: Manages local festivals and community activities"
- "**Key Attributes**:
  - `id` (Primary Key)
  - `title` - Event name
  - `event_date`, `end_date` - Scheduling information
  - `category` - Religious, Civic, Entertainment
  - `status` - Approval workflow
  - `created_by` (Foreign Key → User.id)"
- "**Significance**: Supports the Events & Festival Directory feature"

**4. BARANGAYINFO Entity**
- "**Purpose**: Stores detailed information about each barangay"
- "**Key Attributes**:
  - `id` (Primary Key)
  - `barangay_name` - Unique barangay identifier
  - `history` - Historical background
  - `traditions` - Cultural practices
  - `cultural_assets` - Notable cultural elements
  - `local_practices` - Community traditions"
- "**Significance**: Provides context for barangay-level cultural data"

**5. GALLERYITEM Entity**
- "**Purpose**: Manages photos and videos of attractions and events"
- "**Key Attributes**:
  - `id` (Primary Key)
  - `file_path` - Location of media file
  - `media_type` - Image or Video
  - `caption` - Description
  - `status` - Content moderation
  - `attraction_id` (Foreign Key → Attraction.id) - Related attraction"
- "**Significance**: Enables the Multimedia Gallery feature"

**6. REVIEW Entity**
- "**Purpose**: User feedback and ratings for attractions"
- "**Key Attributes**:
  - `id` (Primary Key)
  - `rating` - 1-5 star rating
  - `comment` - User review text
  - `user_id` (Foreign Key → User.id)
  - `attraction_id` (Foreign Key → Attraction.id)
  - `status` - Moderation status"
- "**Significance**: Provides quality feedback and user engagement"

**7. FAVORITE Entity**
- "**Purpose**: Tracks user's saved attractions"
- "**Key Attributes**:
  - `id` (Primary Key)
  - `user_id` (Foreign Key → User.id)
  - `attraction_id` (Foreign Key → Attraction.id)
  - `created_at` - When it was favorited"
- "**Significance**: Enhances user experience with bookmarking"

**8. EVENTINTEREST Entity**
- "**Purpose**: Tracks user interest in events"
- "**Key Attributes**:
  - `id` (Primary Key)
  - `user_id` (Foreign Key → User.id)
  - `event_id` (Foreign Key → Event.id)
  - `status` - 'interested' or 'going'"
- "**Significance**: Helps gauge event popularity"

**9. PAGEVIEW Entity**
- "**Purpose**: Analytics tracking"
- "**Key Attributes**:
  - `id` (Primary Key)
  - `page_url` - Which page was viewed
  - `viewed_at` - Timestamp
  - `user_id` (Foreign Key → User.id, nullable) - Track both logged-in and anonymous"
- "**Significance**: Powers the Analytics Dashboard"

#### **Relationships Explanation (1-2 minutes)**

"**Key Relationships:**

1. **USER to ATTRACTION (1:N)**
   - One user can submit multiple attractions
   - Each attraction has one submitter
   - **Cardinality**: Mandatory on both sides

2. **USER to REVIEW (1:N)**
   - One user can write multiple reviews
   - Each review comes from one user

3. **ATTRACTION to REVIEW (1:N)**
   - One attraction can receive multiple reviews
   - Each review is for one attraction

4. **ATTRACTION to GALLERYITEM (1:N)**
   - One attraction can have multiple photos/videos
   - Each gallery item belongs to one attraction

5. **BARANGAYINFO to ATTRACTION (1:N)**
   - One barangay can have multiple attractions
   - Each attraction is located in one barangay

6. **USER to FAVORITE (1:N)**
   - Users can favorite multiple attractions
   - Relationship table enables M:N between USER and ATTRACTION

7. **USER to EVENTINTEREST (1:N)**
   - Users can express interest in multiple events

**All relationships use foreign keys with referential integrity constraints to prevent orphaned records.**"

#### **Alignment with Project Objectives (30 seconds)**

"**How This ERD Supports Our Objectives:**

1. **Efficient Data Management**: Normalized structure reduces redundancy
2. **Scalability**: Designed to handle growth in users and content
3. **Data Integrity**: Foreign keys and constraints ensure consistency
4. **Multi-Role Support**: USER entity supports different access levels
5. **Analytics Ready**: PAGEVIEW entity enables engagement tracking
6. **Content Moderation**: Status fields in multiple entities support approval workflow"

---

## 3. DATA FLOW DIAGRAM (DFD)

### 🎯 **What to Show the Panelists**

Display the DFD Level 1 diagram (`docs/diagrams/dfd-level-1-clean.png`) showing processes, data stores, external entities, and data flows.

### 📝 **Script for Team Member Presentation**

#### **Introduction (30 seconds)**
"Let me now explain our **Data Flow Diagram Level 1**, which illustrates how data moves through our system, showing the interaction between external entities, processes, and data stores."

#### **DFD Components Explanation (1 minute)**

"Before diving into the flows, let me identify the key components:

- **External Entities** (Rectangles): ADMIN, TOURIST, Google OAuth, Mapbox API
- **Processes** (Rounded Squares with Numbers): 1.0 through 8.0
- **Data Stores** (Open Rectangles): User_db, Content_db, Analytics_db, etc.
- **Data Flows** (Arrows): Direction of data movement
- **Main System** (Large Rounded Rectangle): The entire Interactive Digital Cultural Map System"

#### **Process-by-Process Explanation (3-4 minutes)**

**Process 1.0: User Authentication**
- "**Purpose**: Handles user login, registration, and session management"
- "**Data Flows**:
  - ADMIN and TOURIST provide credentials
  - Process validates against **User_db** data store
  - Google OAuth provides external authentication
  - Returns session token for authorized access"
- "**Significance**: Security gateway for the entire system"

**Process 2.0: Content Management**
- "**Purpose**: Allows admins and contributors to create, update, and manage content"
- "**Data Flows**:
  - ADMIN submits attraction/event data
  - Data flows to **Content_db** for storage
  - Retrieves barangay information from **Barangay_db**
  - Media files stored via **Media Storage** external entity"
- "**Significance**: Core content creation workflow"

**Process 3.0: Interactive Map Display**
- "**Purpose**: Renders the interactive cultural map with attraction markers"
- "**Data Flows**:
  - Fetches approved attractions from **Content_db**
  - Mapbox API provides base map tiles
  - Returns rendered map to TOURIST
  - Geo-coordinates flow from attraction data"
- "**Significance**: Primary user interface for exploration"

**Process 4.0: Content Discovery**
- "**Purpose**: Search and filter functionality for attractions and events"
- "**Data Flows**:
  - TOURIST provides search criteria
  - Queries **Content_db** with filters
  - Returns filtered results
  - Supports category, location, and keyword searches"
- "**Significance**: Enables efficient information retrieval"

**Process 5.0: Admin Approval**
- "**Purpose**: Content moderation and approval workflow"
- "**Data Flows**:
  - ADMIN reviews pending submissions
  - Decision flows to **Content_db** (update status)
  - Notification sent to contributor
  - Rejected content returns to submitter with comments"
- "**Significance**: Quality control mechanism"

**Process 6.0: Favorite Management**
- "**Purpose**: Allows users to save attractions for later viewing"
- "**Data Flows**:
  - TOURIST (logged-in) selects attractions
  - Favorites stored in **UserPreferences_db**
  - Retrieves list of saved attractions on demand"
- "**Significance**: Enhances user experience"

**Process 7.0: Analytics & Reporting**
- "**Purpose**: Tracks system usage and generates insights"
- "**Data Flows**:
  - Captures page views from all processes
  - Stores in **Analytics_db**
  - ADMIN can query for reports
  - Provides data on popular attractions and user engagement"
- "**Significance**: Supports data-driven decision making"

**Process 8.0: Review & Feedback**
- "**Purpose**: User ratings and comments on attractions"
- "**Data Flows**:
  - TOURIST submits review with rating
  - Stored in **Feedback_db** with pending status
  - Admin moderation before publication
  - Published reviews flow back to attraction display"
- "**Significance**: Community feedback mechanism"

#### **Data Stores Explanation (1 minute)**

"**Data Stores and Their Roles:**

1. **User_db**: Stores user accounts, roles, sessions
2. **Content_db**: Main repository for attractions, events, gallery items
3. **Barangay_db**: Barangay-specific information and boundaries
4. **Analytics_db**: Page views, user interactions, engagement metrics
5. **UserPreferences_db**: Favorites, event interests, saved data
6. **Feedback_db**: Reviews, ratings, comments with moderation status

**Each data store represents a logical grouping of related data, physically implemented as database tables in Supabase (PostgreSQL).**"

#### **External Entities Interaction (1 minute)**

"**External Entities and Their Interactions:**

1. **ADMIN** (Municipal Tourism Office)
   - Submits and approves content
   - Manages users
   - Views analytics reports

2. **TOURIST** (Visitors, Residents, Students)
   - Browses map and attractions
   - Searches for information
   - Submits reviews and favorites

3. **Google OAuth**
   - Provides authentication service
   - Returns user profile data
   - Enables single sign-on

4. **Mapbox API**
   - Provides map tile rendering
   - Geocoding services
   - Interactive map controls

5. **Media Storage**
   - Cloud storage for images and videos
   - CDN for fast delivery
   - File upload/download services"

#### **Relevance to Project Objectives (30 seconds)**

"**How DFD Supports Project Goals:**

1. **Clear Data Flow**: Shows exactly how heritage data becomes public information
2. **Process Transparency**: Each transformation is visible and traceable
3. **System Boundaries**: Clearly defines what's inside vs. outside the system
4. **Integration Points**: Identifies all external dependencies (OAuth, Mapbox)
5. **Scalability**: Modular processes can be enhanced independently"

---

## 4. SOFTWARE DEVELOPMENT METHODOLOGY

### 🎯 **What to Show the Panelists**

Display an Agile/Scrum methodology diagram showing iterative development cycles.

### 📝 **Script for Team Member Presentation**

#### **Introduction (30 seconds)**
"For our development approach, we adopted the **Agile Software Development Methodology**, specifically a Scrum-based iterative framework. This choice was driven by the evolving nature of requirements and the need for continuous stakeholder feedback."

#### **Why Agile? (1 minute)**

"**Rationale for Choosing Agile:**

1. **Evolving Requirements**: Initial interviews with the Tourism Office revealed new needs as they understood the system's potential
2. **Stakeholder Involvement**: LGU Mangatarem needed to see working features early and provide feedback
3. **Risk Mitigation**: Iterative development allowed us to identify and address issues early
4. **Flexibility**: We could adapt to changes in LGU processes and data collection forms
5. **Continuous Improvement**: Each iteration built upon learnings from the previous one"

#### **Agile Phases Explanation (3-4 minutes)**

**Phase 1: Requirements Gathering & Analysis (Sprint 0)**
- "**Activities**:
  - Conducted interviews with Municipal Tourism Office
  - Analyzed existing manual forms (Forms 01A-07)
  - Documented user stories for each stakeholder type
  - Created initial product backlog"
- "**Deliverables**: Requirements specification, user personas, initial backlog"
- "**Duration**: 2 weeks"

**Phase 2: System Design (Sprint 1-2)**
- "**Activities**:
  - Created ERD and database schema
  - Designed system architecture (Flask + SQLAlchemy)
  - Developed UI/UX mockups
  - Defined API endpoints"
- "**Deliverables**: Architecture documentation, ERD, DFD, UI prototypes"
- "**Duration**: 4 weeks"
- "**Sprint Review**: Presented designs to LGU for feedback"

**Phase 3: Core Development (Sprint 3-8)**
- "**Sprint 3-4: Foundation**
  - Set up Flask application structure
  - Implemented authentication (Flask-Login + Google OAuth)
  - Created database models and migrations
  - Built admin dashboard skeleton"

- "**Sprint 5-6: Content Management**
  - Developed attraction submission forms
  - Implemented event management
  - Built approval workflow
  - Created barangay dashboard"

- "**Sprint 7-8: Public Features**
  - Integrated Leaflet.js interactive map
  - Implemented search and filtering
  - Built multimedia gallery
  - Added review and rating system"

- "**Each Sprint Cycle**:
  - **Sprint Planning**: Selected backlog items
  - **Daily Standups**: 15-minute sync meetings
  - **Development**: Code, test, integrate
  - **Sprint Review**: Demo to team and stakeholders
  - **Sprint Retrospective**: Identify improvements"

**Phase 4: Testing & Quality Assurance (Ongoing + Sprint 9)**
- "**Activities**:
  - Unit testing for models and utilities
  - Integration testing for API endpoints
  - User acceptance testing with Tourism Office
  - Performance testing for map rendering"
- "**Testing Strategy**:
  - Test-Driven Development for critical functions
  - Manual testing for UI/UX
  - Real-world data testing with actual forms"
- "**Duration**: Integrated throughout + dedicated 2-week sprint"

**Phase 5: Deployment & Training (Sprint 10)**
- "**Activities**:
  - Deployed to Vercel (production environment)
  - Migrated from SQLite to Supabase
  - Conducted training sessions for LGU staff
  - Created user documentation and manuals"
- "**Deliverables**: Live system, trained users, documentation"
- "**Duration**: 2 weeks"

**Phase 6: Maintenance & Iteration (Post-Launch)**
- "**Activities**:
  - Monitor system performance
  - Collect user feedback
  - Implement enhancements
  - Fix bugs and issues"
- "**Approach**: Continuous deployment with bi-weekly updates"

#### **Agile Artifacts Used (1 minute)**

"**Agile Artifacts:**

1. **Product Backlog**: Prioritized list of features and improvements
2. **Sprint Backlog**: Tasks selected for each sprint
3. **User Stories**: Feature descriptions from user perspective
   - Example: 'As a barangay representative, I want to submit attractions so that tourists can learn about our heritage'
4. **Burndown Charts**: Track sprint progress
5. **Increment**: Working software at end of each sprint"

#### **How Agile Supported Project Success (1 minute)**

"**Benefits Realized:**

1. **Early Value Delivery**: Core features (authentication, basic map) were available by Sprint 4
2. **Stakeholder Engagement**: LGU could test and provide feedback every 2 weeks
3. **Adaptability**: When Tourism Office requested additional form fields, we incorporated them in the next sprint
4. **Risk Reduction**: Database design issues were caught in Sprint 2, not at deployment
5. **Quality Improvement**: Continuous testing caught bugs early
6. **Team Collaboration**: Daily standups kept everyone aligned despite different schedules"

#### **Visual Representation (Point to Diagram)**

"As shown in our methodology diagram:
- The **outer circle** represents the continuous Agile cycle
- Each **quadrant** shows a major phase
- The **iterative arrows** indicate sprint cycles
- **Feedback loops** show stakeholder input at each stage"

---

## 🎤 GENERAL PRESENTATION TIPS

### For All Diagrams:

1. **Start with Context**: Explain WHY this diagram exists
2. **Use Pointers**: Physically or digitally point to elements as you discuss them
3. **Maintain Flow**: Connect each element to the next logically
4. **Engage Panelists**: Make eye contact, don't just read from notes
5. **Handle Questions**: If interrupted, pause, answer, then resume where you left off
6. **Time Management**: Practice to ensure you don't exceed your allocated time

### Common Panelist Questions & Prepared Answers:

**Q: "Why did you choose this specific methodology?"**
**A:** "Agile allowed us to incorporate continuous feedback from the LGU, which was crucial since they were discovering their own needs as they saw the system's capabilities. A waterfall approach would have locked us into initial requirements that we now know were incomplete."

**Q: "How does your ERD handle scalability?"**
**A:** "Our ERD uses normalization to reduce redundancy, indexed foreign keys for fast joins, and we've designed it to work with PostgreSQL connection pooling in production. The separation of analytics data (PAGEVIEW) from transactional data also improves performance."

**Q: "What was the biggest challenge in mapping the existing process?"**
**A:** "The Tourism Office uses multiple parallel processes - some data goes through email, some through physical forms, and some through verbal reports. Consolidating these into a single coherent flowchart required multiple interview sessions."

**Q: "How does your DFD ensure data security?"**
**A:** "Process 1.0 (User Authentication) acts as a security gateway. All data flows from external entities must pass through authentication before accessing any data store. Additionally, the Admin Approval process (5.0) ensures content moderation before public display."

---

## 📊 TEAM MEMBER ROLE ASSIGNMENTS

**Suggested Distribution:**

- **Member 1**: Flowchart of Existing Processes (4-5 minutes)
- **Member 2**: Entity-Relationship Diagram (5-6 minutes)
- **Member 3**: Data Flow Diagram (5-6 minutes)
- **Member 4**: Software Development Methodology (4-5 minutes)

**Total Technical Diagrams Section: 18-22 minutes**

---

## ✅ PRE-DEFENSE CHECKLIST

- [ ] All diagrams printed in large format or loaded on presentation device
- [ ] Laser pointer or digital highlighting tool ready
- [ ] Each member has practiced their section at least 3 times
- [ ] Team has done at least 2 full run-throughs together
- [ ] Backup copies of diagrams on USB drive and cloud storage
- [ ] Timer set for each section during practice
- [ ] Q&A preparation session conducted
- [ ] All members understand how to transition between sections

---

## 🎯 KEY MESSAGES TO EMPHASIZE

1. **Problem-Solution Fit**: Each diagram shows how we addressed real inefficiencies
2. **Stakeholder-Centric**: LGU Mangatarem's needs drove every design decision
3. **Technical Rigor**: Diagrams follow industry standards and best practices
4. **Scalability**: System designed for growth and future enhancements
5. **User Experience**: All flows prioritize ease of use for all stakeholder types

---

**Good luck with your defense! Remember: You know this system better than anyone. Speak with confidence and clarity.**
