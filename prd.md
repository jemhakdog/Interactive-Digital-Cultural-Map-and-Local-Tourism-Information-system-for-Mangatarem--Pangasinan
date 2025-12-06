### **Product Requirements Document (PRD)**

### ---

**1\. Project Overview**

* **Project Name:** Interactive Digital Cultural Map and Local Tourism Information System  
* **Type:** Web Application  
* **Purpose:** This platform helps users find cultural spots and tourism highlights in the city. It consolidates data onto one interactive map to boost local pride, assist tourists, and aid student research.

### **2\. Target Audience**

* **Tourists:** Visitors needing navigation, food recommendations, and attraction details.  
* **Residents:** Locals interested in community events or discovering other barangays.  
* **Students/Researchers:** Users looking for historical data and cultural heritage info.  
* **Admin/Contributors:** Barangay officials or tourism staff who update content.

### **3\. User Stories**

| Role | I want to... | So that I can... |
| :---- | :---- | :---- |
| **Visitor** | click a pin on a map | see photos and details of a tourist spot. |
| **Visitor** | filter map icons | find specific categories like food or historical sites. |
| **Student** | search for a specific festival | get details for school research. |
| **Admin** | login to a dashboard | add new events, approve contributor posts, or update photos. |
| **Admin** | view site statistics | see counts of current attractions and events. |

### **4\. Functional Requirements**

#### **4.1 Interactive Cultural Map**

* **Map Interface:** Base map rendered using **Leaflet.js** centered on Mangatarem.  
* **Pins and Markers:** Color-coded icons for categories (Nature, Historical, Religious, Food).  
* **Pop-up Cards:** Clicking a pin opens a card with the attraction name, description, and link to details.  
* **Navigation:** Zoom/Pan controls; "Fly To" animation when selecting a spot from the sidebar.

#### **4.2 Cultural and Tourism Information Portal**

* **Barangay Profiles:** Dedicated templates displaying history, cultural assets, and unique features per barangay.  
* **Details Page:** Full page view for attractions including Description, Location, and Image.  
* **Categories:** Database categorization for "Eateries," "Landmarks," "Religious Sites," etc.

#### **4.3 Events and Festival Directory**

* **Event List:** Chronological display of upcoming events.  
* **Event Details:** Title, Date, Location, and Description.  
* **Status Indicators:** Logic to display event status (e.g., Pending Approval vs. Approved).

#### **4.4 Multimedia Gallery**

* **Media Grid:** Responsive grid layout for photos and videos.  
* **Uploads:** Contributors can upload images/videos which are stored in the static file system.  
* **Filtering:** Filter media by Barangay or Media Type (Photo/Video).

#### **4.5 Search and Filter Tools**

* **Search Bar:** Text input to filter map results by name or keyword.  
* **Filters:** Buttons/Dropdowns to filter by Category (Nature, Heritage) or specific Barangay.

#### **4.6 Admin and Contributor Module**

* **Role-Based Access Control (RBAC):**  
  * **Admin:** Full access to approve/reject/delete all content.  
  * **Contributor:** Can create/edit their own content; submissions require Admin approval.  
* **Dashboard:** specialized views for Admins (system-wide stats) and Contributors (personal submissions).  
* **Authentication:** Secure login and registration flows.

#### **4.7 Tourist Guide and Suggested Routes**

* **Static Routes:** Informational pages suggesting itineraries (e.g., "Heritage Walk").  
* **Future Scope:** Interactive line drawing on the map.

#### **4.8 Analytics Dashboard**

* **Content Stats:** Counters for Total Attractions, Events, and Gallery items.

### **5\. Non-Functional Requirements**

* **Responsiveness:** Implementation of **Tailwind CSS** to ensure mobile and desktop compatibility.  
* **Performance:** Lazy loading for images and deferred script loading to ensure fast initial paint.  
* **Maintainability:** Code organized into **Flask Blueprints** (Admin, Public, Auth, Barangay) for modularity.

### ---

**6\. Technical Recommendations (Updated)**

This section now reflects the actual implementation found in the repository.

* **Backend Framework:** **Python (Flask)**  
  * *Reasoning:* Lightweight, easy to extend, and handles routing/templating efficiently.  
* **Database:** **SQLite** (via **SQLAlchemy** ORM)  
  * *Reasoning:* Serverless, file-based database ideal for development and small-to-medium scale deployments. No separate database server installation required.  
* **Frontend:**  
  * **Templating:** **Jinja2** (Server-side rendering).  
  * **Styling:** **Tailwind CSS** (Utility-first CSS framework) \+ Custom CSS.  
  * **Interactivity:** **Vanilla JavaScript** (No heavy frontend frameworks like React/Vue required).  
* **Mapping API:** **Leaflet.js** (Open-source)  
  * *Tiles:* OpenStreetMap or CartoDB Voyager.  
  * *Plugins:* Leaflet.markercluster for grouping pins.  
* **Authentication:** **Flask-Login** for session management and user auth.  
* **Hosting Environment:** Any Python-capable host (e.g., PythonAnywhere, Heroku, or a VPS with Gunicorn/Nginx).

### **7\. Assumptions and Constraints**

* **Internet Access:** The application requires an internet connection to load external assets (Tailwind CDN, Map Tiles, FontAwesome).  
* **Database Scalability:** SQLite is currently used. For high-concurrency production use in the future, this can be easily switched to PostgreSQL/MySQL by changing the SQLALCHEMY\_DATABASE\_URI configuration.  
* **Storage:** Images are stored in the local file system (static/uploads). Backups must include the static/uploads folder and the .db file.

---

