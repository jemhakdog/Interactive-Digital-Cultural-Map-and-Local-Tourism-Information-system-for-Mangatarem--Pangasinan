# Chapter 3: Results and Discussion

This chapter presents the comprehensive results of the design, development, and system features of the Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan. It encapsulates the logical workflows and multi-role system flowcharts designed to replace fragmented legacy processes, details the operational modules and user interfaces engineered for both public and administrative stakeholders, and outlines the terminal testing and evaluation methodologies. In accordance with Capstone 1 guidelines, this chapter focuses on the design, functional features, and systematic testing plans based on the ISO/IEC 25010 framework, establishing the baseline for full implementation and numerical evaluation in Capstone 2.

## Proposed System Flowchart

The operational workflow of the Interactive Digital Cultural Map and Local Tourism Information System is formalized through a centralized, multi-role system flowchart. Within the context of the Rapid Application Development (RAD) methodology, this flowchart serves as a critical blueprint for aligning functional capabilities with stakeholder expectations during rapid iterations. By mapping the logical pathways of distinct actor groups, the flowchart visualizes the transition from fragmented, legacy manual processes to a synchronized, community-driven digital ecosystem.

The system flowchart is architecturally divided into three role-based user lanes (Swimlanes) and a unified database processing engine, isolating security boundaries and operational concerns. This design guarantees strict data governance, where grassroots data capture is verified through administrative oversight before public exposure.



### Operational Swimlanes and Actor Roles

The workflow partitions responsibilities across four vertical channels to ensure security, usability, and data integrity:

1. **General Public and Academic Users (Visitor Lane)** – Represents the high-concurrency consumer tier. Public users browse the georeferenced municipal map, apply spatial filters to locate attractions, and access verified historical records. Additionally, authenticated public users can submit interactive feedback and reviews for establishments, pushing user-generated ratings to the system database.
2. **Barangay Representatives (Contributor Lane)** – Represents the grassroots data stewardship tier. Contributor accounts are restricted to a single verified representative per barangay. Representatives digitize primary-source historical data, upload local photos, and submit heritage profiles directly through the contributor portal.
3. **LGU Tourism Office Administrators (Admin Lane)** – Represents the administrative moderation and quality assurance tier. Administrators possess high-privilege access to oversee user accounts, publish municipal-wide tourism announcements, and qualitative audits. They manage the moderation queue to verify and authorize all submissions.
4. **Database and Mapping Engine (System Lane)** – Serves as the central repository and transaction coordinator. It manages persistent storage, validates spatial boundaries, records action logs to the database audit registry, and executes PostGIS vector tile generation to serve dynamic map pins to client interfaces.

### Alphanumeric Step-by-Step Workflow Path Mapping

The precise sequential interactions mapped across the proposed system flowchart are structured as follows:

* **General Visitor Workflow Path (V1–V5):**
  * **V1: Access Web Portal**: The visitor initiates a secure web session, loading the public portal containing the map atlas.
  * **V2: Search & Filter Categories**: The visitor applies dynamic taxonomic queries (e.g., natural heritage, built heritage, intangible cultural assets) or filters by barangay boundary.
  * **V3: Explore Interactive Map**: The map coordinates with the backend to render georeferenced visual pins dynamically on the Mapbox GL JS map canvas.
  * **V4: View Attraction/Establishment Details**: Clicking a pin fetches detailed profiles from the database, rendering historical narratives, operating statuses, business menus, and accommodation configurations.
  * **V5: Leave Review / Interactive Feedback**: Authenticated visitors submit community ratings, reviews, and validating media, pushing new interactive feedback to the database engine.
* **Barangay Contributor Workflow Path (C1–C5):**
  * **C1: Secure Login**: The contributor authenticates via a Flask-Login form utilizing secure cookie validation.
  * **C2: Access Barangay Dashboard**: The system redirects the user to their designated dashboard, exposing local stewardship progress metrics.
  * **C3: Digitally Fill Heritage Forms 01–07**: The contributor inputs structured primary-source data conforming to the national cultural heritage inventory protocols.
  * **C4: Upload Photos & Media Assets**: The contributor attaches high-resolution photography and documents to serve as evidentiary support for the heritage profile.
  * **C5: Submit Asset for Review**: Committing the form triggers a transactional save, marking the asset's state as `PENDING` and queuing it in the moderation queue.
* **Tourism Office Admin Workflow Path (A1–A6):**
  * **A1: Secure Login (Admin)**: The administrator authenticates via a high-privilege credentials form.
  * **A2: Access Admin Dashboard**: The admin views active system metrics, active session logs, page views, establishment updates, and the pending moderation queue.
  * **A3: Review Pending Submissions**: The administrator retrieves queued entries from the moderation queue.
  * **A4: Decision Gate (Meets Standards?)**: The administrator conducts a qualitative audit of the metadata, geo-coordinates, and media assets.
  * **A5: Approve & Publish (Yes Branch)**: If the asset meets requirements, the admin approves it. The database updates the state to `APPROVED`, and the mapping engine immediately renders the pin to the general public.
  * **A6: Reject & Send Feedback (No Branch)**: If the asset fails audits, the admin rejects it, logs detailed correction requests, and routes it back to the respective contributor dashboard in a `REJECTED` state for rectification.
* **Database and Mapping Engine System Path (DB1):**
  * **DB1: PostgreSQL & Mapbox Vector Tiles**: Implements strict validation constraints, logs transaction records to the `DATABASE_AUDIT_LOG`, updates caching via Upstash Redis, and serves optimized vector tiles via PostGIS `ST_AsMVT` to visitor interfaces.

### Core Pipelines of the System Flow

The operational workflow transitions through four critical pipelines designed to automate spatial rendering and prevent unauthorized data modifications:

1. **Data Ingestion Pipeline** – Coordinates how incoming data from forms (Jinja2 templates, Flask-WTF validation, and secure upload handlers) is accepted, parsed for geographic coordinates, and written to database tables.
2. **Moderation Queue Pipeline** – Restricts public database queries to only retrieve rows whose status is explicitly marked as `APPROVED`. New contributions from Barangay Representatives are locked in a `PENDING` state, isolated from the public atlas.
3. **Administrative Review Pipeline** – Empowers the LGU Tourism Office with a consolidated moderation portal. The system generates detailed comparison diffs, allowing admins to inspect submitted coordinates against physical boundaries before committing.
4. **Public Publication Pipeline** – Automates the transition of verified data to public visualization. Once approved, caching layers are invalidated, and the new georeferenced coordinates are fed into the Mapbox Vector Tile generation script, achieving real-time, low-latency pin rendering.

## System Features and User Interfaces

The structural capabilities of the Interactive Digital Cultural Map and Local Tourism Information System are rigidly organized around the access privileges and operational requirements of its four primary user roles:

### 1. System Administrator (Tourism Office Staff / IT Staff)
The System Administrator holds the highest level of administrative control and is primarily responsible for system governance, validation, and access control.
- **Content Moderation Module**: A centralized, high-privilege moderation dashboard where administrators retrieve, review, and evaluate pending cultural profiles and media uploads submitted by contributors. The module provides a comparison diff interface and a single-click action to approve and publish the georeferenced coordinates to the public map, or reject the submission and log specific correction notes.
- **User Account Management**: Tools to manage system credentials, verify new contributor profiles, and grant or revoke access privileges to maintain platform integrity.
- **Global Settings and System Auditing**: Access to system-wide audit registries (`DATABASE_AUDIT_LOG`) to monitor modification histories, configure global mapping boundaries, and publish LGU notices.

### 2. Barangay Representative (Contributor)
The Barangay Representative serves as the grassroots data contributor, responsible for digitizing and maintaining the local cultural inventory of their specific jurisdiction.
- **Grassroots Submission Portal**: A secure dashboard restricted to a single verified contributor per barangay, enabling them to draft and submit cultural profiles. The portal provides standardized digital forms matching national NCCA heritage formats.
- **Media Upload Module**: Integrated drag-and-drop secure media handlers to upload high-resolution photography and supporting documents, automatically generating relational links to parent heritage profiles.
- **Status and Revision Tracker**: A progress dashboard displaying the real-time moderation status of their submissions (`PENDING`, `APPROVED`, `REJECTED`). If a submission is rejected, the tracker displays the admin's correction notes, allowing the contributor to edit and resubmit.

### 3. Public User (Tourists / Visitors)
This tier represents the primary public consumer interface, designed with a focus on responsive UI/UX to encourage tourism discovery.
- **Georeferenced Map Canvas**: A dynamic, full-screen map interface (utilizing Mapbox GL JS) displaying custom vector tiles. Public users browse georeferenced pins representing natural heritage sites, local landmarks, and events.
- **Taxonomic Filtering Module**: Advanced filter pickers allowing visitors to segment map pins by category (e.g., historical spots, eco-tourism, local festivals) or filter pins within specific barangay boundaries.
- **Establishment Review and Caching Engine**: Clicking a pin renders a detailed pop-up display with narratives, menu options, or lodging details. Authenticated visitors can submit reviews, ratings, and validation photos, which are processed via an automated validation pipeline.

### 4. Students and Researchers (Academic Users)
Designed specifically to support the academic community, this module provides structured, query-optimized search paths to retrieve cultural and historical archives.
- **Digital Cultural Atlas**: A search-optimized digital database registry providing academic users with comprehensive, read-only access to digitized barangay profiles, historical archives, and traditional heritage accounts.
- **Municipal Archives Retrieval Engine**: A query pipeline allowing researchers to filter the municipal archives by era, category, or keyword, rendering standardized heritage records for academic reference and data gathering, aligned with the primary LGU document repository.

## System Testing and Evaluation

To guarantee technical robustness, compliance with engineering specifications, and organizational usability, a rigorous system evaluation plan has been established under the ISO/IEC 25010 Software Quality Standards. During this terminal phase of Capstone 1, this section outlines the detailed testing plans, execution methodologies, and the customized evaluation instruments designed for each quality characteristic, with actual statistical calculations and final evaluation scores reserved for Capstone 2.



### Functional Testing Plan
The primary objective of Functional Testing is to verify that the system’s modules and logic operate in strict accordance with the defined functional specifications. The testing plan involves executing test cases under simulated user roles to validate the accuracy of database writes, coordinate parsing, and moderation state transitions.
* **Test Case Definition**:
  * *Authentication Security*: Attempting to access the Barangay Contributor Portal or LGU Admin Panel without valid session cookies to verify redirection logic.
  * *Ingestion Validation*: Submitting a heritage profile form with missing geographic coordinates to verify Flask-WTF validation triggers.
  * *Moderation Flow*: Verifying that database records created by contributors are successfully saved in a `PENDING` state and remain invisible on the public map until the status is modified to `APPROVED` by the administrator.
  * *Spatial Search Integrity*: Testing real-time keyword queries and spatial category filters to confirm the client canvas renders only matching coordinate pins.
* **Execution Process**: Testing will be conducted systematically via manual execution on multiple browsers (Google Chrome, Microsoft Edge, Safari) and automated integration tests. The results (Pass/Fail) will be documented in a structured functional matrix.

### Performance Testing Plan
Performance testing evaluates the system's operational efficiency, responsiveness, and stability under varying concurrency levels.
* **Execution Process**: Performance metrics will be gathered using **Google Lighthouse** audits and **Chrome DevTools Performance Traces**. The testing processes focus on measuring:
  * *First Contentful Paint (FCP)*: The time required to render the initial DOM elements on the home screen.
  * *Time to Interactive (TTI)*: The duration before the interactive Mapbox vector map becomes fully responsive to user panning and coordinate filtering.
  * *Database Query Latency*: Measuring API execution times for cached queries (Upstash Redis) compared to raw database queries.
  * *Stress Simulation*: Utilizing load testing utilities to simulate multiple concurrent spatial requests to monitor serverless Flask response times under peak municipal traffic.

### Security Testing Plan
Security testing is executed to validate the system's resilience against unauthorized access, malicious data modification, and common web application vulnerabilities.
* **Execution Process**: The developers will subject the platform to simulated penetration testing and "Red Team" attacks. Testing focuses on:
  * *SQL Injection (SQLi) Prevention*: Input fields, login forms, and search bars will be tested with malicious payloads (e.g., `' OR '1'='1`) to confirm that the SQLAlchemy ORM effectively sanitizes inputs and executes parameterized queries.
  * *Cross-Site Scripting (XSS) Mitigation*: Form submissions containing malicious JavaScript scripts (e.g., `<script>alert("XSS")</script>`) will be entered into content fields to verify that the system sanitizes input string formats using the Python `Bleach` library before storage.
  * *Role-Based Access Control (RBAC) Integrity*: Direct URL access attempts (Insecure Direct Object Reference) to the administrative portal (e.g., `/admin/moderation`) using a standard Public User session will be executed to confirm the server terminates unauthorized sessions and logs the security event.

### Usability and User Acceptance Testing (UAT) Plan
Usability testing evaluates the user-friendliness, navigational clarity, and visual accessibility of the user interfaces, while User Acceptance Testing (UAT) assesses whether the system fulfills the operational needs of LGU staff and contributors.
* **Evaluation Instrument**: The developers will utilize a modified Likert-scale questionnaire based on the ISO/IEC 25010 Usability framework. The instrument is divided into:
  * *Part 1: Demographic Profile*: Collecting role, age group, and computer literacy metrics from respondents.
  * *Part 2: Likert-Scale Statements*: A 5-point scale (ranging from "5 - Strongly Agree" to "1 - Strongly Disagree") to evaluate specific statements regarding navigation ease, visual design clarity, and system friendliness.
  * *Part 3: Qualitative Feedback*: Open-ended queries to gather constructive notes for interface polishing.
* **UAT Execution Process**: During the Cutover phase, the UAT will be administered to a selected sample group of stakeholders (including LGU Tourism Officers, Barangay Representatives, and Academic Users). The numerical data and statistical averages collected will serve as the primary findings of Chapter 3, to be analyzed and discussed during the final Capstone 2 manuscript defense.
