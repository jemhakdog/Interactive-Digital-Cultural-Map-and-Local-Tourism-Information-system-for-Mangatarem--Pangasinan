# 🗺️ Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan

## 📍 Project Overview

This is a web-based platform designed as a Capstone Project (CP1) to showcase the cultural identity, community highlights, and tourism offerings across the barangays of Mangatarem, Pangasinan.

The primary purpose of the system is to **promote local pride, support educational use, and enhance tourism visibility** for residents, students, and visitors by consolidating cultural and tourism-related information into one accessible digital resource. The project emphasizes problem validation, requirements elicitation, solution scoping, and project planning, which are the focus of Capstone Project 1.

## 🎯 Project Relevance and Objective

This project addresses the issues and challenges faced by beneficiaries (such as the LGU or community organization) that are directly relevant to the study. The stated objective must clearly highlight the system’s significance, feasibility, and potential impact to be compelling for approval.

The system's main objective is to provide an interactive map that allows users to explore local cultural spots, traditions, attractions, events, and significant community features.

## ✨ Key System Features (Modules)

The following modules represent the main components and integral parts of the system, each performing a specific task, which defines the **Scope of the System**:

1.  **Interactive Cultural Map:** Features a clickable map of the City/Municipality, including barangay-level cultural highlights, photos, descriptions, media per location, and zoom/navigation tools.
2.  **Cultural and Tourism Information Portal:** Provides profiles of each barangay's cultural assets, traditions, local practices, and points of interest. It also lists local tourism spots, eateries, and unique community features.
3.  **Events and Festival Directory:** Includes a calendar of local festivities, details on barangay events and citywide celebrations, and announcements of upcoming cultural activities.
4.  **Multimedia Gallery:** Contains photo and video collections of cultural events and allows for uploadable media showcasing local traditions.
5.  **Search and Filter Tools:** Allows quick access to specific cultural or tourism-related information by searching by barangay, cultural category, attraction type, or event.
6.  **Admin and Contributor Module:** Authorized barangay representatives can add or update cultural information, supported by an admin approval workflow for content management and easy content updates for events and photos.
7.  **Tourist Guide and Suggested Routes:** Offers recommended routes for exploring cultural and local tourism spots and itinerary suggestions based on themes (e.g., food tour, historical walk, community landmarks).
8.  **Analytics Dashboard (Optional):** Provides insights on most-viewed locations and attractions, and trends on user engagement (highly recommended for a Capstone).

## ⚙️ Technical Requirements and Stack

The core technology detected for this repository is **Python**. Based on typical Capstone requirements, the system requires defined hardware, software, and service requirements.

### Development Requirements

*   **Programming Language:** Python (and likely PHP, HTML, SQL, CSS, Javascript if web-based, as per Capstone examples).
*   **Database:** (Example: MySQL).
*   **Code Editor:** (Example: Sublime Text).
*   **Operating System:** (Example: Windows 10 OS).
*   **Local Server Stack:** (Example: WAMP).

### Repository Structure Overview

The repository is structured around a typical Python/Flask web application, with several routes defined:

*   `flask_app.py`
*   `models.py` (Contains 7 classes for data modeling).
*   **Routes:** Separate modules handle different user types and functions, including `admin.py`, `barangay.py`, `public.py`, and `auth.py`.
*   **Templates:** Extensive use of templates for administrative interfaces (e.g., `templates/admin/dashboard.html`, `templates/admin/add_event.html`) and public interfaces (e.g., `templates/index.html`, `templates/map.html`).
*   **Static Assets:** Includes CSS (e.g., `hero-slider.css`, `style.css`) and JavaScript (e.g., `map.js`, `animations-optimized.js`).

## 📊 System Design and Artifacts

For the Capstone Project 1 defense, the following diagrams serve as the foundation for the project’s design and must be included in the documentation (Chapter 1-3) and presentation:

*   **Flowchart of Existing Processes:** Depicting the current workflows relevant to the system being developed [4a, 14].
*   **Entity-Relationship Diagram (ERD):** Illustrates the main entities (represented in uppercase and singular form, e.g., STUDENT), their attributes (with Primary Keys underlined and Foreign Keys labeled as FK#), and their relationships (typically 1:N or M:N) [4b, 15, 16, 17].
*   **Data Flow Diagram (DFD):** Maps the flow of data within the system, showing processes (rounded corners), data stores, external entities (rectangles), and data flow lines [4c, 18, 19].
*   **System Architecture Design:** Offers a comprehensive view of how the system will operate, including user types, network devices, services utilized (like cloud services, if applicable), and the developed system [4d, 20].

## 🚀 Performance Optimization Highlights

Efforts have been made to optimize the system's performance, targeting high scores in audits like Chrome DevTools Lighthouse (Target: 90+ score). Key optimization solutions include:

*   Optimizing images and implementing lazy loading using the **Intersection Observer**.
*   Deferring JavaScript and replacing older scripts (`animations.js`) with an optimized version (`animations-optimized.js`) that uses throttled parallax and passive event listeners.
*   Moving large resources like **Leaflet** to map-specific template blocks (`templates/map.html`) to speed up base page loads.

These optimizations are expected to yield significant improvements, such as **65% faster First Contentful Paint** and **55% faster Time to Interactive**.

## 👤 Users and Stakeholders

The project defines the individuals who directly interact with the system (Users) and those who are impacted by its outcomes (Stakeholders):

### Users of the System
This group utilizes the system to accomplish specific tasks. For example (in the context of this tourism system), these might include **System Administrators**, **Barangay Representatives/Contributors**, and **Public Visitors**.

### Stakeholders
This includes all groups or individuals impacted by the development, implementation, or outcomes of the system. For a tourism system, stakeholders could include the **Local Government Unit/Decision-Makers**, **Local Businesses/Beneficiaries** (e.g., eateries, attractions), **Students/Researchers**, and the **Developers of the System**.
