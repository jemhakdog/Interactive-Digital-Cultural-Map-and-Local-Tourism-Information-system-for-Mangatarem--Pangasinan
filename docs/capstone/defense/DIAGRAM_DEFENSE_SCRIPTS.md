# System Defense Script: DFD & Flowchart

Same with the ERD, the goal is to walk the panel through the diagrams logically.

---

# Part 1: Data Flow Diagram (DFD) Defense Script

**Concept:** Explain how data moves through the PROPOSED system, identifying the **Source** (User), **Process** (Transformation), **Storage** (Database), and **Destination** (Output).

## 1. Context Diagram (Level 0) – The Big Picture

**Discussion by Team Member:**

"Simulan po natin sa **Context Diagram** o Level 0. Dito po makikita natin ang 'Big Picture' ng system."

*   **The Core System:**
    "Sa gitna po, ito ang **Interactive Digital Cultural Map & Tourism Information System**. Ito po ang nagpo-process ng lahat ng data."

*   **External Entities (The Actors):**
    "May limang actors po na nag-iinteract sa system:
    1.  **Tourist / Public User** (kaliwa): Sila ang mga bisita na nagvi-view ng map at impormasyon.
    2.  **Barangay Contributor** (kaliwa): Sila ang nagse-submit ng data galing sa bawat barangay.
    3.  **System Administrator** (kanan): Sila ang nag-aapprove ng content at nagma-manage ng system.
    4.  **Google OAuth Service** (kanan): External service para sa secure login.
    5.  **Mapbox API** (ibaba): External service para sa interactive map tiles."

## 2. Level 1 DFD – Detailed Data Flow

"Ngayon po, tingnan natin ang **Level 1 DFD**. Ito po ang detalyadong flow kung paano pumapasok at lumalabas ang data."

### A. Authentication & User Management (Process 1.0)
"Simulan po natin sa **Process 1.0: User Authentication**.
*   Dito po pumapasok ang login credentials ng Admin, Contributors, at Tourists.
*   Gumagamit tayo ng **Google OAuth** para sa secure at mabilis na login.
*   Kapag na-verify, sine-save sa **User DB**.
*   Mahalaga ito dahil iba-iba ang access levels:
    - Admin: Pwede mag-approve ng content
    - Contributor: Pwede lang mag-submit
    - Tourist: View-only access"

### B. Content Management (Process 2.0)
"Sunod po ay **Process 2.0: Content Management**.
*   Kapag nag-add ang Staff o Contributor ng bagong attraction, event, o barangay info, dadaan ito sa process na ito.
*   Hindi agad lumalabas sa public—kailangan muna ng approval.
*   Naka-save ang data sa:
    - **Attraction DB** (mga pasyalan)
    - **Event DB** (mga darating na events)
    - **Barangay DB** (impormasyon per barangay)"

### C. Heritage Management (Process 9.0)
"Mayroon din po tayong **Process 9.0: Heritage Management** para sa specialized cultural data.
*   Dito po na-e-encode ang mga heritage sites gamit ang modular forms:
    - **Built Heritage** (mga lumang gusali)
    - **Natural Heritage** (mga natural na tanawin)
    - **Movable Heritage** (mga artifact)
    - **Intangible Heritage** (mga tradisyon at kultura)
    - **Cultural Institutions** (mga organisasyon)
    - **LGU Programs** at **Personalities** (mga kilalang tao)
*   Lahat ng ito ay naka-link sa **Heritage Profile** para sa complete record."

### D. Admin Approval (Process 5.0)
"Para sa quality control, may **Process 5.0: Admin Approval**.
*   Lahat ng submitted content (attractions at heritage) ay dadaan sa approval process.
*   Ni-review ng Admin, tapos:
    - **Approved**: Lumalabas na sa public
    - **Rejected**: Ibinabalik sa contributor para i-correct
*   Naka-record lahat sa **Approval Log** para sa tracking."

### E. Public-Facing Processes (Tourist Features)

"**Process 3.0: Interactive Map Display**
*   Ito ang nakikita ng turista.
*   Hinahagil ng system ang data galing sa databases (coordinates, pangalan, images).
*   Pinapakita sa map gamit ang **Mapbox API** na may GPS at directions.

**Process 4.0: Content Discovery**
*   Pwede ang user na mag-search at mag-filter:
    - Ayon sa kategorya (Nature, History, Food)
    - Ayon sa location (per barangay)
    - Ayon sa rating (pinaka-popular)"

### F. User Engagement (Processes 6.0, 7.0, 8.0)

"Para hindi one-way ang system, may engagement features tayo:

**Process 8.0: Review & Feedback**
*   Pwede ang turista na mag-iwan ng rating at comments.
*   Naka-save sa **Review DB**.
*   Nakikita ng ibang users at ng LGU.

**Process 6.0: Favorite Management**
*   Kapag nag-like o nag-save ng place ang user, nare-record sa **Favorite DB**.
*   Nakakatulong ito para sa personalized recommendations.

**Process 7.0: Analytics & Reporting**
*   Kinokolekta ang lahat ng activity:
    - Ilan ang nag-view ng bawat attraction
    - Alin ang pinaka-popular
    - User engagement metrics
*   Naka-generate ng reports para sa LGU decision-making."

### G. Data Stores Summary

"Mayroon tayong **17 data stores** na nag-iimbak ng impormasyon:
- **User DB, Attraction DB, Event DB, Barangay DB** (core data)
- **Heritage Profile + 6 detail tables** (cultural heritage)
- **Review DB, Favorite DB** (user engagement)
- **PageView DB, Reports DB** (analytics)"

---

# Part 2: System Flowchart Defense Script (Existing/Manual Workflow)

**Concept:** Explain the **CURRENT Manual Process** to highlight the pain points and why the new system is needed. Based specifically on the *Existing Workflow Diagram*.

## 1. Organization Workflow (How Data is Collected Today)

**Discussion by Team Member:**

"Sa Flowchart naman po, ipapakita namin ang **Existing Manual Workflow** ng LGU. Dito natin makikita kung bakit kailangan ng digital system."

*   **Step 1: Start & Field Survey**
    "Nagsisimula ang process sa **'Need for Cultural Data'**.
    *   Kasalukuyan, nagko-conduct sila ng **Manual Field Survey** gamit ang physical forms (Forms 01A-07).
    *   Sinusulat nila nang mano-mano ang details ng heritage sites at attractions."

*   **Step 2: Encoding & Submission**
    "Pagkatapos ng survey, may **Manual Encoding**.
    *   Itinatype nila ang data sa Word o Excel. Madaling magkamali ng error at matagal ang process.
    *   Ipinapadala sa **Physical Copy o Email** sa Tourism Office. Walang central database—files lang sa computer o folder."

*   **Step 3: Decision Point (The Bottleneck)**
    "Dito pumapasok ang **Decision Point: Manual Review**.
    *   Tinitingnan ng Tourism Officer ang papel o file.
    *   **Kung 'Return for Correction':** Ibinabalik sa sender, minsan via email o text. Matagal at nakakalito.
    *   **Kung 'Approved':** Saka lang ifi-file."

*   **Step 4: Storage & Retrieval (The Problem)**
    "Kapag na-approve, ang storage ay **Physical Filing** o Local File Storage lang.
    *   Kapag may nag-request ng info (**Manual Retrieval**), kailangan pang galugarin ang cabinet o hanapin sa folders ng PC.
    *   Sobrang bagal ng process na 'to bago maibigay sa public."

---

## 2. Tourist Workflow (The User Experience Today)

"Sa side naman po ng Turista, ganito ang experience nila ngayon—kaya mahirap mag-promote ng tourism."

*   **Step 1: Arrival & Inquiry**
    "Pagdating ng turista sa Mangatarem (**Start**), ang option lang nila ay **Pumunta sa Municipal Tourism Office**.
    *   Kailangan pa nilang pumunta physically para makakuha ng info."

*   **Step 2: Request & Receive**
    "Doon, magre-request sila ng brochures.
    *   Ang ibinibigay ay **Paper Map o Verbal Directions** lang.
    *   Minsan, photocopied map lang o simpleng sketch."

*   **Step 3: Navigation Challenges**
    "Ang ending, **Manual Navigation** ang gagawin nila.
    *   Walang GPS, walang directions sa Waze kung hindi registered.
    *   Kaya madalas, (**End Point**) pagdating nila sa attraction, pwedeng sarado pala, mahirap hanapin, o hindi updated ang info na nakuha nila."

**Closing Statement for Flowchart:**
"Kaya ang proposed system natin ay solusyon sa lahat ng bottlenecks na ito:
- From manual encoding → digital database
- From paper maps → interactive GPS maps
- From one-time visit → accessible anytime online"

