# Chapter 3: Results and Discussion

*(Note: As per the BCC BSIT Capstone Project Guide Revised 2025, Capstone 1 focuses exclusively on Chapters 1, 2, and the system design/features of Chapter 3. The actual implementation results, deployment findings, and final evaluation scores will be completed during Capstone 2. This chapter currently outlines the expected system features per user role and the planned testing and evaluation methodologies.)*

## System Features and Modules

The Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan is designed to address the challenges of fragmented manual tourism processes. The system is divided into specific modules tailored to the needs and access privileges of its key stakeholders.

### 1. System Administrator (Tourism Office Staff / IT Staff)
The System Administrator represents the highest level of access and is the core regulatory body of the platform, ensuring all published data is accurate and appropriate.
* **Content Moderation Module:** A centralized dashboard where the Admin receives, reviews, and either approves or rejects cultural and tourism data submissions from Barangay Representatives.
* **User Assessment and Management:** Ability to manage user accounts, assign or revoke access permissions for Contributors, and monitor audit logs of system activity.
* **Platform Operations:** Tools to oversee general platform maintenance, configure map settings, and update global LGU announcements or emergency tourism notices.

### 2. Barangay Representative (Contributor)
The Barangay Representative acts as the localized data source, bridging the gap between grassroots cultural events and the municipal database.
* **Content Submission Portal:** A dedicated interface allowing representatives to draft and submit proposals detailing local history, new attractions, and upcoming community events within their specific jurisdiction.
* **Media Upload Capabilities:** Features enabling the secure upload of localized photos and videos to visually enhance the cultural profile of their barangay.
* **Update and Edit Tracking:** Ability to request updates to previously approved information to ensure the interactive map remains current with real-world changes.

### 3. Public User (Tourists / Visitors)
This module focuses heavily on UI/UX to ensure tourists have an engaging, accessible, and informative experience without requiring an account.
* **Interactive Digital Cultural Map:** A dynamic, visually engaging geographic map that allows users to navigate the municipality and locate specific attractions (e.g., Manleluag Spring).
* **Search and Filter Functions:** Tools to easily query specific points of interest based on categories (e.g., historical sites, nature, dining) or general keywords.
* **Pop-up Details and Routing:** Clicking on a map pin reveals rich multimedia pop-up details, cultural background information, and suggested routes/directions to the landmark.

### 4. Students and Researchers (Academic Users)
Designed to support the academic community, this module provides structured access to the municipality's heritage records.
* **Historical Data Archives:** Access to detailed barangay profiles, historical data, and cultural traditions specifically formatted for academic research and data gathering.
* **Heritage Study Tools:** Capabilities to read comprehensive articles regarding local practices and community history, ensuring reliable educational resources are readily available.

## Evaluation Results

*(Note: This section will remain a placeholder detailing the **Evaluation Plan** for Capstone 1. The actual statistical results and interpretation will be conducted in Capstone 2).*

### Testing Plan
The evaluation of the system is a critical component to ensure the computing solution resolves the identified problems effectively. The testing plan is designed to validate the system against the objectives set in Chapter 1. The evaluation will utilize the ISO/IEC 25010 Software Quality Standards as the primary framework.

The following quality characteristics will be tested:
1. **Functional Suitability:** To evaluate if the interactive map correctly filters locations, if the submission portal accurately transmits data to the Admin, and if the moderation module effectively publishes approved content. User Acceptance Testing (UAT) will be conducted involving actual Tourism Office staff and Barangay officials to verify these workflows.
2. **Performance Efficiency:** To assess the loading speed of the interactive map and multimedia pop-ups under typical traffic loads. Stress testing will simulate multiple concurrent public users accessing the map simultaneously.
3. **Usability:** To measure the user-friendliness of both the public map interface and the backend Admin Dashboard. The System Usability Scale (SUS) will be administered to a sample group of tourists and local administrators to gather quantitative feedback.
4. **Security:** To ensure the Contributor Portal and Admin Dashboard are protected against unauthorized access, and that content cannot be published without proper LGU approval.

### Evaluation Instrument
The primary evaluation instrument will be a modified Likert-scale questionnaire based on the ISO/IEC 25010 criteria. The questionnaire will target the specific user groups (Admin, Contributors, Tourists, and Students). 

- **Part 1:** Demographic profile of the respondents (e.g., Role, Age, Technical Proficiency).
- **Part 2:** Assessment of Functional Suitability, Performance Efficiency, Usability, and Security, structured as statements where respondents indicate their level of agreement (e.g., "5 - Strongly Agree" to "1 - Strongly Disagree").
- **Part 3:** Open-ended section for qualitative suggestions and feedback regarding the interactive map's features and the content contribution process.

*(The findings, statistical treatment of data, and interpretation of these evaluation results will proudly constitute the core of Chapter 3 during the final Capstone 2 defense).*
