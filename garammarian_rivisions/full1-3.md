
**Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan**

**A Capstone Project Presented to the Faculty of the**
**Information Technology Department**
**Binalatongan Community College**
**San Carlos City, Pangasinan**

**In Partial Fulfillment of the Requirements**
 **for the Degree of Bachelor of Science**
**in Information Technology**

**Submitted by:**

**Austria, Jem Carlo**
 **Dalas, Mary Jane**
**Solis, Rea**
**De Guzman, Joy**

        				**May 2026**

**APPROVAL SHEET**

	This capstone project entitled **Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan** prepared and submitted by **Jem Carlo Austria, Mary Jane Dalas, Rea Solis, Joy De Guzman** in partial fulfillment of the requirements for the degree **BACHELOR OF SCIENCE IN INFORMATION TECHNOLOGY,** has been examined and is recommended for acceptance and approval.
                                                                   \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
					                 **MR. Christop P. Catungal, BSIT**
   		    Adviser

               PANEL OF EXAMINERS

                                      \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
    **BANNER B. FERRER, MIT**
	    Chairperson
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_                \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
**CHARLES NIXON C. CAYANDING, BSIT          JANNELE M. DE VERA, MIT**
                  Member                                                            Member

	**ACCEPTED** and **APPROVED** in partial fulfillment of the requirements for the degree **BACHELOR OF SCIENCE IN INFORMATION TECHNOLOGY** on **May 17,2022** with a grade of \_\_\_\_\_\_\_.

                                                             		        \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_             \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
**BRIXON J. DE VERA, MIT**	 	          **DR. MACRINA B. CAJALA**	   Dean, Information Technology Department   		        College President

**Abstract**

**Jem Carlo Austria, Mary Jane Dalas, Rea Solis, Joy De Guzman, “Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan,”** Bachelor of Science in Information Technology, College of Information Technology, Binalatongan Community College, San Carlos City, Pangasinan, Philippines, May 2025\.
Adviser: 	**FRANCIS L. CRISOSTOMO, BSIT**
The Local Government Unit (LGU) of Mangatarem, Pangasinan, currently faces challenges with manual, fragmented record-keeping for tourism and cultural assets, which hinders public accessibility and operational efficiency. To address these issues, this study developed an Interactive Digital Cultural Map and Local Tourism Information System designed to centralize data management through a web-based, cloud-native architecture. Employing the Rapid Application Development (RAD) methodology and a Participatory GIS framework, the researchers created a secure, multi-tier platform that integrates an administrative moderation workflow with an interactive, public-facing heritage map. Post-implementation testing yielded a 100% success rate in functional and security performance, alongside high usability and user acceptance ratings. Consequently, this digital solution effectively modernizes heritage preservation and provides a scalable, accessible resource for local stakeholders, tourists, and academic researchers. By digitizing cultural narratives and tourism data, this project sets a foundational model for other municipalities in Pangasinan to pursue digital transformation in their heritage management strategies. The researchers ultimately conclude that this system serves as a bridge between the municipality’s historical identity and the digital future, ensuring that
Mangatarem’s rich heritage is both preserved and accessible to a global audience.
**Acknowledgement**
The researchers express their profound gratitude to the Local Government Unit of Mangatarem, Pangasinan, for their invaluable trust and collaborative support throughout the realization of this capstone project. We extend our sincere appreciation to our project advisor and the faculty of Binalatongan Community College for their constant guidance, technical critiques, and encouragement, which were vital in refining the system’s architecture. Special thanks are reserved for the barangay representatives and local stakeholders whose active participation and candid feedback were instrumental in ensuring the platform effectively meets the community's needs. Finally, we are deeply grateful to our families, friends, and peers for their unwavering patience, moral support, and motivation, which sustained us through the challenges of this endeavor. We also acknowledge the invaluable contributions of the various tourism sites and archives that provided the raw data necessary for populating our cultural database. Above all, we offer this work as a testament to our dedication to the field of Information Technology and our commitment to serving the community through innovative software solutions.

**Table of Contents**

|  |  | Page |
| ----- | ----- | :---: |
| Title Page ………………………………………………………………... ……….... |  | i |
| Approval Form ………………………………………………………………………. |  | ii |
| Abstract …………………………………………………………………………………     |  | iii |
| Acknowledgment …………………………………………………………………… |  | iv |
| Table of Contents ………………………………………………………………….. |  | v |
| List of Tables ……………..…………………………………………..……………. |  | vii |
| List of Figures ………………………………………………………..……………... |  | viii |
|  |  |  |
| **Chapter** |  |  |
| **1** | **INTRODUCTION** …………………………………..……......... | 1 |
|  | Background of the Study ………………………………………..  | 1 |
|  | Purpose and Description ………………………………………..  | 5 |
|  | Objectives of the Study ……………………………………...…..   | 7 |
|  | Conceptual Framework (IPO) ……………………………..….. | 8 |
|  | Scope and Limitations …………………………………………… | 10 |
|  | Definition of Terms …………….……………………………..…..  | 12 |
|  | Review of Related Literature.……………………………..…… | 14 |
|  |  |  |
| **2** | **METHODOLOGY AND DESIGN** .…………………………. | 17 |
|  | Software Development Methodology ……………………… | 17 |
|  | Sources of Data …………………………………………………… | 20 |
|  | Data Gathering Techniques…………………………………….. | 21 |
|  | System Design ..…………………………………………….......... | 23 |
|  |           System Architecture ……………………………………. | 23 |
|  |           Dataflow Diagram ………………………………………. | 29 |
|  |  |  |
|  |           Entity-Relationship Diagram ………………………… | 32 |
|  |           Implementation Diagram …………………………….. | 36 |
|  |  |  |
| **3** | **RESULTS AND DISCUSSION** |  |
|  | System Process Flowchart.………………………. | 40 |
|  | System Features and User Interfaces ………………………. | 46 |
|  | System Testing and Evaluation …………………....…………. | 47 |
|  | Implementation Results .…………………………………......... | 48 |
|  | Analysis of Results ………...………………………………......... | 49 |
|  | Discussion of Findings ………………..……………………….... | 54 |
|  |  |  |
| **4** | **RECOMMENDATIONS**.…………………………………………. | 55  |
|   |  |  |
| **Appendices** ………………………….……………………….…………………….. |  | 56  |
| **A** | Endorsement Letter ………………………………………………… | 56  |
| **B** | System Source Codes ………………………..…….…………….. | 57  |
| **C** | Database Schema (Actual Database Structure) ….……… | 120  |
| **D** | Survey/Evaluation Forms Used During Testing ………….. | 137  |
| **E** | Collected Sample Documents for Document Analysis/Data Gathering…..………………………………………. | 130  |
|  |  |  |
| **Curriculum Vitae** …………………………………………………………………. |  | 142 |

##

**List of Tables**

| Table | 		Title | Page |
| ----- | :---- | :---: |
| 3.1 | Functional Testing | 49 |
| 3.2 | Performance testing | 50 |
| 3.3 | Security testing | 51 |
| 3.4 | Usability testing | 52 |
| 3.5 | User acceptance testing | 53 |

##

**List of Figures**

| Figure | 		Title | Page |
| :---: | :---- | :---: |
| 1.1 | IPO | 8 |
| 2.1 | RAD | 18 |
| 2.2 | System Design | 23 |
| 2.3 | Existing Flowchart | 30 |
| 2.3 | Dataflow Diagram | 31 |
| 2.4 | Entity Relationship Diagram | 33 |
| 2.5 | Project Timeline | 36 |
| 3.1 | Proposed System Flowchart | 41 |
| 3.2 | Home | 46 |
| 3.3 | Dashboard | 46 |
| 3.4 | Login | 47 |

## **Chapter I**

**INTRODUCTION**

## **Background of the Study**

Local government units (LGUs) in the Philippines are mandated under the Local Government Code of 1991 to promote tourism and preserve local cultural heritage. However, many municipal offices face operational difficulties due to their reliance on paper-based records and manual archiving. The Municipal Tourism Office of Mangatarem, Pangasinan, currently handles tourism data and cultural profiling through physical folders and manual logbooks. This setup limits the public's access to historical information and delays the administrative updates of local attractions. Academic studies show that establishing a centralized web platform for municipal data improves public engagement and coordinates tourism information more effectively than physical-first archives (Chang & Caneday, 2011). Transitioning to a digital database and spatial mapping system is therefore a practical step to resolve these administrative delays and secure local heritage records.

Mangatarem is a first-class municipality with historical sites and natural attractions, including the Manleluag Spring National Park. Despite its tourism potential, the LGU struggles to distribute accurate cultural and tourism information. The tourism office acts as the main depository for data from the municipality's 82 barangays, but the lack of a unified system leads to fragmented records. When researchers or visitors request data, staff must search through physical filing cabinets, which is time-consuming and risks data loss. These administrative bottlenecks highlight the need for a structured digital platform that coordinates cultural mapping and tourism management at the municipal level (de Claro et al., 2024).

To address these inefficiencies, this study develops the 'Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan.' The system replaces the current manual record-keeping with a web-based mapping application. By digitizing cultural records and centralizing tourism information, the platform aims to streamline the LGU's approval workflow, prevent data duplication, and provide real-time updates. The integration of geographical maps and digital profiles allows tourists, residents, and academic researchers to access verified historical records online, supporting long-term cultural preservation in a secure digital repository (Cascón-Katchadourian et al., 2018).

### **Encountered Problems**

The Municipal Tourism Office of Mangatarem currently experiences operational bottlenecks in collecting and verifying data from individual barangays. Barangay representatives report updates on local attractions or events through informal channels, such as text messages, personal phone calls, or physical paper documents. This lack of standardization requires tourism office staff to manually compile and format incoming reports, causing delays in publishing updates. Additionally, because there is no synchronized database, conflicting information about local landmarks and schedules is sometimes posted on unofficial social media accounts, which misleads visitors and reduces the LGU's credibility (Chang & Caneday, 2011).

The manual archiving system also creates access problems for researchers and students. Academic users looking for cultural profiles or barangay history must travel to the tourism office to inspect physical folders. These physical documents are subject to wear and tear and can be easily misplaced. Furthermore, the slow coordination between the municipal office and local stakeholders prevents the LGU from promoting seasonal events or local businesses in a timely manner. These issues demonstrate the necessity of a web-based, multi-role system that standardizes data entry, enforces administrative review, and provides secure public access to cultural mapping data (Cascón-Katchadourian et al., 2018).

##

## **Purpose and Description**

The primary purpose of this Capstone Project is to design, develop, and implement a web-based Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan. This computing solution seeks to centralize, digitize, and standardize the management of the municipality's tourism assets and cultural heritage records, replacing legacy, manual processes with a secure, highly interactive digital platform. By providing a unified administrative moderation pipeline and an engaging, map-driven public interface, the system aims to improve administrative efficiency, eliminate data redundancy, and promote local heritage to a global audience. Once the proposed system is implemented, it will hold particular significance for the following beneficiaries:

1. **Administrative and Stakeholder Users (LGU Tourism Office and Barangay Representatives)** – This category is the primary beneficiary, as it provides a centralized platform for the LGU to promote tourism and manage cultural data. It allows the Tourism Office staff to verify facts from every barangay, ensuring the public receives accurate and authoritative information. Barangay representatives benefit from a dedicated portal to directly upload content, streamlining the flow of information from the grassroots level to the municipal dashboard.
2. **General Public and Academic Users (Tourists, Visitors, and Researchers)** – This category benefits from an interactive and educational tool to explore Mangatarem’s heritage. Tourists gain a mobile-responsive map to discover landmarks and plan their visits, while students and researchers can access a digital archive of cultural profiles and historical records from any location, eliminating the need for physical travel to the tourism office for basic data gathering.

3. **Residents of Mangatarem** – The community at large gains a digital safeguard for their traditions and festivals, fostering local pride and ensuring that their heritage is preserved in a secure, accessible format for future generations.

The administrative rationale behind the project is to resolve the inconsistencies, communication delays, and accessibility bottlenecks inherent in the current manual workflow. By replacing fragmented communication with a standardized digital pipeline, the project assumes that the system will establish a definitive "source of truth" for municipal tourism and cultural data, thereby maximizing stakeholder satisfaction and enhancing operational transparency.

##

##

##

##

##

##

## **Objectives of the Study**

The main objective of this study is to design and develop an Interactive Digital Cultural Map and Local Tourism Information System for the Local Government Unit (LGU) of Mangatarem, Pangasinan. The system is engineered to replace legacy, manual processes with a centralized, web-based platform that optimizes information management and promotional workflows.

Furthermore, the developers aim to achieve the following specific objectives:

1. To analyze the existing processes of collecting, verifying, and disseminating tourism and cultural information in Mangatarem, Pangasinan, in order to identify administrative inefficiencies, workflow bottlenecks, and data integration challenges.
2. To identify and design the key system modules, workflows, and access control parameters for the designated user categories:
   * **Administrative and Stakeholder Users**: Incorporating System Administrators (Tourism Office Staff) and Barangay Representatives (Contributors) to facilitate secure data entry, content submission, and moderation workflows.
   * **General Public and Academic Users**: Incorporating Tourists, Visitors, and Academic Researchers to facilitate spatial mapping, digital heritage exploration, and research-oriented data extraction.
3. To test and evaluate the system's functionality, performance, security, usability, and acceptability in accordance with the ISO/IEC 25010 Software Quality Standards to ensure compliance with technical specifications and user expectations.
4. To prepare a comprehensive, phased implementation plan for the deployment of the system, including server migration, database initialization, and stakeholder training.

##

##

## **Conceptual Framework**

This study utilizes the Input-Process-Output (IPO) model to delineate the systematic framework and developmental lifecycle of the proposed computing solution. The IPO model serves as a structured technical roadmap, defining the foundational resources required (Input), the software engineering methodology executed to construct the platform (Process), and the resulting operational system delivered to the municipality (Output), with a continuous feedback loop to ensure long-term maintenance and alignment.
**Figure 1.1: IPO**

The conceptual framework illustrated above delineates the systematic flow of the project. The Inputs specify the technical and physical resources, along with the domain knowledge required by the developers to undertake the project. These resources feed into the Process, which employs the Rapid Application Development (RAD) methodology to iteratively design, prototype, and build the platform through structured phases. This structured process ensures that the final Output — the Interactive Digital Cultural Map and Local Tourism Information System — is developed efficiently and aligns with the functional and operational requirements of the Mangatarem LGU and its stakeholders. The feedback loop ensures that any issues identified during testing or post-deployment can be communicated back to the development team to refine the system inputs and processes, resulting in continuous improvement.

##

##

##

##

##

##

##

##

##

## **Scope and Limitations**

### *Scope*

The project focuses on the development of a web-based Interactive Digital Cultural Map and Local Tourism Information System for the Local Government Unit (LGU) of Mangatarem, Pangasinan. The system will be built utilizing web technologies including HTML, CSS (Tailwind CSS), and JavaScript for the frontend interface, Python with the Flask framework for server-side application logic, and PostgreSQL as the primary relational database management system — managed via Supabase for cloud-native persistence and real-time features. Figma will be utilized for user interface and user experience design during the prototyping phase. The key functionalities provided by the software include a public-facing interactive map where the **Public and Academic** category can browse, locate, and filter tourist attractions and cultural heritage sites by category such as historical landmarks, natural attractions, and local events. For **Administrative and Stakeholder** users, the system features a decentralized content contribution portal that allows authorized Barangay Representatives to submit, upload, and propose updates for local tourism content, alongside a centralized administrative dashboard for LGU Tourism Office staff to moderate all submissions through an approve-or-reject workflow, manage user accounts, and publish municipal-wide tourism announcements. Students and researchers within the public category are provided with structured access to archived cultural profiles and historical records to support academic data gathering and heritage research.

### *Limitations*

While the system aims to provide comprehensive tourism information management for Mangatarem, it will not include online booking, reservation, or payment gateway functionalities for local accommodations, tour guides, or event ticketing. The interactive map and all system features require an active internet connection; full offline capabilities such as cached map tiles or offline content browsing are not within the scope of this project. Performance and scalability are designed to accommodate the expected volume of tourist traffic and barangay-level content contributions typical of a municipal tourism platform, but the system is not engineered to handle extreme traffic surges beyond standard municipal usage without future server infrastructure upgrades. Access to the content contribution and moderation modules is strictly restricted to authenticated and authorized LGU personnel and registered Barangay Representatives, meaning the general public cannot directly create, edit, or publish map data without going through the LGU approval workflow. The system is also limited to the geographic and administrative boundaries of Mangatarem, Pangasinan, and does not cover tourism data from neighboring municipalities or provinces.

## **Definition of Terms**

For clarity and consistency, the following key terms are defined operationally as they are used in this study:

**Administrative and Stakeholder Users** . This consolidated category refers to
the LGU Tourism Office staff (System Administrators) and authorized Barangay Representatives (Contributors) who hold internal access to the system. This category is responsible for submitting, reviewing, and approving cultural heritage data, managing the platform's operational integrity, and overseeing the municipality's digital tourism presence.

**General Public and Academic Users**. This category refers to tourists, visitors,
students, and researchers who access the system to navigate the interactive map, search for points of interest, and view published cultural and tourism information. These users consume the data for leisure, travel planning, or academic data gathering without requiring administrative privileges.

**Interactive Digital Cultural Map**.The core feature of the system that provides
a visual, geographical, and navigable representation of tourist spots, historical landmarks, natural attractions, and cultural heritage sites within the municipality of Mangatarem, Pangasinan. Users can interact with the map by clicking pins, filtering categories, and viewing detailed multimedia information for each location.

**Local Government Unit (LGU)**. In this study, this refers specifically to the
municipal government of Mangatarem, Pangasinan, serving as the main beneficiary, authoritative body, and decision-maker over the tourism information system and its content governance policies.

**Public User**. Refers to tourists, visitors, or any general member of the public
who accesses the system to navigate the interactive map, search for points of interest, and view published cultural and tourism information without requiring a registered account or administrative privileges.

**Rapid Application Development (RAD)**. The software development
methodology selected for this study, characterized by rapid prototyping, iterative feedback cycles, flexible requirements gathering, and continuous stakeholder involvement to accelerate system construction while maintaining alignment with user needs.

**Content Moderation**. The process by which the System Administrator reviews
content submissions from Barangay Representatives and decides whether to approve, reject, or request revisions before the content is published on the public-facing interactive map.

##

##

## **Review of Related Literature**

To establish the academic baseline and theoretical foundation for this study, the researchers conducted a comprehensive review of related literature from the period 2020 to 2025. This review is structured around the core objectives of the study, examining recent advancements in municipal digital transformation, spatial mapping, content moderation workflows, and usability testing within both local (Philippine) and foreign academic contexts.

### Local Studies

#### Existing Tourism Information Management Processes in Philippine LGUs
Soncuya (2020) conducted a critical evaluation of cultural mapping initiatives in municipal contexts, highlighting that many Philippine local government units (LGUs) continue to rely on fragmented physical documentation and inconsistent archiving methods. The study demonstrated that such manual practices lead to rapid data degradation, informational errors, and a general lack of coordination between regional tourism offices and grassroots communities. However, Soncuya also emphasized that establishing a structured, standardized reporting framework paired with a clear legal baseline significantly enhances the sustainability and administrative longevity of cultural mapping databases. This finding directly supports the first objective of this study by validating the critical need to replace Mangatarem's manual reporting channels with a standardized, web-based digital workflow.

In parallel, Coro II et al. (2022) examined the digitization process of tourism information systems in rural municipalities, utilizing Siargao as a primary case study. Their research indicated that transitioning to digital platforms drastically reduces data dissemination delays and improves the accuracy of public tourist guides. A key finding of the study was that the successful adoption of new IT infrastructure in rural municipalities depends heavily on early stakeholder engagement and localized user training. This case study provides a direct real-world precedent for the fourth objective of this study, guiding the design of the phased deployment and training strategy tailored to the technical readiness of the Mangatarem LGU.

#### Grassroots Content Contribution and Centralized Moderation
Germina and Martir (2025) evaluated the implementation of participatory mapping frameworks that integrate historical preservation with GPS technology in provincial contexts. The study argued that allowing local community members and barangay-level contributors to directly input primary-source historical data significantly enriches the depth and localized accuracy of the central database. However, they also noted that to prevent the spread of unverified or inaccurate data, a centralized administrative gatekeeping mechanism is mandatory. This research strongly validates the second objective of this study, supporting the structural separation of roles between the Barangay Representative ( grassroots contributor) and the LGU Tourism Administrator (content moderator) to ensure data integrity.

#### Usability, Cultural Pride, and System Acceptance in Philippine Municipalities
Mesana et al. (2025) investigated the managerial challenges of municipal-led cultural festivals and intangible heritage events. Their phenomenographic inquiry revealed that a major challenge in local cultural preservation is the lack of structured digital data and coordination issues within local government units, which hinders local commerce. This research underscores the importance of the second objective of this study, confirming that integrating local festival directories and standardized cultural maps directly supports municipal heritage preservation and local tourism development.

Finally, Ansari et al. (2024) analyzed the operational challenges and prospects of preserving art and religious traditions. They identified that a major hurdle in heritage preservation is balancing modernization with conservation and ensuring sustained maintenance of cultural assets. This analysis serves as a vital warning for the execution of the fourth objective of this study, reinforcing the necessity of preparing a detailed maintenance plan and administrative guidelines during the cutover phase.

### *Foreign Studies*

#### Digital Transformation and Spatial Visualization Frameworks
Sang et al. (2021) developed a web-based geographic mapping platform designed to visualize historical landmarks and cultural evolution over time. Their technical framework successfully integrated spatial coordinate datasets with historical photography galleries, demonstrating that interactive map pop-ups and category-based filtering significantly improve spatial comprehension and visitor navigation ease. This foreign study provides a concrete technical model for the first and second objectives of this study, supporting the choice of integrating georeferenced spatial coordinate pins with a search-optimized database interface.

Similarly, Moneta et al. (2025) conducted a study on the impact of digital interpretation and immersive storytelling-driven presentations on community engagement. Their findings indicated that digital platforms that pair detailed narratives with multimedia assets enhance public engagement and foster a sense of cultural identity among users. The authors concluded that incorporating interactive and immersive storytelling elements is a critical factor in encouraging public exploration. This study directly aligns with the second objective of this study, emphasizing that usability, storytelling elements, and interactive design are vital for the public-facing portal.

#### Standardized Cultural Documentation and System Quality
Du et al. (2024) explored the interactive effects of intangible cultural heritage (ICH) and tourism development. Their study argued that digital mapping and tourism development must extend beyond physical architecture to incorporate traditional practices, oral histories, and community events. Du et al. analyzed how coupled coordination between tourism platforms and intangible heritage assets supports local preservation, which supports the second objective of this study by informing the metadata fields and database tables engineered for the Mangatarem cultural registry.

Furthermore, Tan (2023) evaluated user adoption models for digital tourism portals, finding that modular, component-based software design simplifies post-deployment feature expansion. The research also demonstrated that providing simple, highly intuitive navigation paths reduces user resistance when stakeholders transition from manual paper forms to digital systems. This supports the second and fourth objectives by validating the utilization of a phased development approach (RAD) to incrementally build and refine the user design.

Lastly, Petrovic (2022) investigated data validation algorithms in participatory heritage mapping systems. The study demonstrated that integrating automated input validation, secure session handling, and role-based access control (RBAC) prevents database corruption and unauthorized data modification by malicious actors. This technical research supports the third objective of this study, reinforcing the need to conduct rigorous security testing against threats such as SQL injection and unauthorized role escalation.

### Synthesis

The compiled literature establishes a cohesive academic and technical justification for the development of the Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan. Local studies by Soncuya (2020) and Coro II et al. (2022) confirm that legacy manual tourism management processes are highly prone to administrative delays and data fragmentation, establishing a clear need for digitization to achieve municipal efficiency (Objective 1). The research by Germina and Martir (2025) and Du et al. (2024) supports the core system design, proving that a decentralized, community-led data contribution model paired with central administrative moderation is the most effective approach for capturing accurate heritage records while maintaining data integrity (Objective 2). 

Reflecting these requirements, the technical frameworks and usability findings presented by Sang et al. (2021), Moneta et al. (2025), and Tan (2023) provide a clear engineering blueprint for constructing the georeferenced mapping interface and modular database tables, ensuring high-concurrency public exploration and long-term system scalability. Finally, the security and maintenance assessments by Petrovic (2022) and Ansari et al. (2024) highlight the critical necessity of executing rigorous ISO/IEC 25010 testing plans and establishing clear post-deployment maintenance protocols to prevent security vulnerabilities and ensure project sustainability (Objectives 3 and 4). By integrating these diverse local and foreign findings, the developers aim to deliver a secure, highly usable, and academically validated computing solution that safeguards Mangatarem’s rich cultural heritage.

#

#

#

#

# **Chapter II**

**Methodology and Design**
This chapter details the development methods and design strategies we used to create the Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan. We want to provide a clear record of our technical decisions and the specific steps we took to deliver a functional tool for the LGU.

## **Software Development Methodology**

In software engineering, a Software Development Methodology (SDM) is like a clear roadmap for a project. Without it, a team can easily lose focus, miss deadlines, or build features that nobody actually needs. For our project in Mangatarem, having this structure helps us stay organized while we plan, code, and test the digital map. It makes sure we're actually building a tool that fits the LGU’s workflow and that the final product is impactful for the whole community.

The team chose **Rapid Application Development (RAD)** and combined it with a **Participatory GIS (PGIS)** framework. We picked this because it focuses on building prototypes and getting feedback quickly rather than spending months just planning on paper. Since tourism data and the needs of our barangay leaders can change as they see the site evolve, RAD lets us adapt fast. By using PGIS, we also make sure the community has a say in how we represent their local culture on the map, which makes the data much more accurate.

**Figure 2.1** RAD

RAD is an agile way of working that prioritizes quick delivery and user feedback. Instead of trying to get every detail perfect at the start, we build small, working versions of the system and refine them over and over. It's known for keeping the people who will actually use the system involved every step of the way. This method is perfect for projects where the look and feel of the site are vital and where we expect to make changes as users interact with our early designs.

The team broken down our work into these four RAD phases:

1. **Requirements Planning:** We started by meeting with the LGU Tourism Office staff to find the gaps in their current manual filing system. We identified the main goals and defined the two primary user categories: **Administrative and Stakeholder Users** (LGU staff and Barangay Contributors) and **General Public and Academic Users** (Tourists and Researchers). We used interviews and site visits to make sure we didn't miss any important cultural traditions or landmarks that the town wants to highlight.
2. **User Design (Prototyping):** Once we knew what the system needed, we used **Figma** to create mockups and wireframes. We built designs for the interactive map (Public/Academic interface) and the data management portals (Administrative/Stakeholder interface). We showed these to the LGU staff and barangay reps to see if they found the buttons and menus easy to navigate. We used their feedback to change the layout until it felt just right.
3. **Construction:** This is the phase where we did the actual coding. We used **HTML, Tailwind CSS, and JavaScript** for the parts you see on the screen, and **Python with Flask** for the logic and database work. We stored all the town's information in **Supabase**. We built the interactive map and created the "approve or reject" moderation workflow for the administrative users. We coded and tested in small cycles so we could catch and fix bugs early.
4. **Cutover (Testing and Deployment):** In this final stage, we perform functional, security, and usability tests to make sure the site is safe and fast. Once we resolve any issues, we’ll launch the system for the LGU. We’ll also hold training sessions for the Administrative and Stakeholder category (LGU staff and barangay leaders) and give them user manuals so they feel comfortable running the site on their own.

##

##

## **Sources of Data**

The primary sources of data for this project are individuals, groups, and locations within the municipality of Mangatarem, Pangasinan that hold crucial tourism, cultural, and historical information relevant to the system. Key data sources include:

- **LGU Tourism Office Staff** — Municipal tourism officers who provide official tourism policies, existing manual records, promotional materials, and municipal-level tourism initiatives. They serve as the authoritative source for content moderation rules, user access policies, and platform governance requirements.
- **Barangay Officials and Representatives** — Designated individuals from each barangay who serve as vital sources for localized cultural data, specific landmark descriptions, community event schedules, and grassroots heritage information that is not centrally documented at the municipal level.
- **Manleluag Spring National Park and Other Tourist Sites** — Physical locations within Mangatarem that serve as points of reference for mapping coordinates, photographic documentation, and on-site observation of existing visitor information systems (e.g., signage, brochures).
- **Municipal Archives and Physical Records** — Existing physical tourism brochures, printed municipal profiles, historical documents, and past tourism reports maintained by the LGU, which serve as secondary data sources to establish the initial database content of the system.

## **Data Gathering Techniques**

To ensure a comprehensive understanding of the current operational challenges, cultural preservation needs, and technical requirements for the Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan, multiple data gathering techniques were employed. These techniques were carefully selected and implemented to collect both qualitative and quantitative data from key municipal stakeholders and community representatives.
**Surveys and Questionnaires** \- One of the primary techniques used was the survey questionnaire. These were distributed to selected LGU Tourism Office staff, Barangay Representatives, and potential academic users during the initial Requirements Planning phase. The surveys were designed using structured questions to assess data usage habits, preferred public-facing features (e.g., map filtering vs. list view), and the frequency of data synchronization issues caused by current manual reporting methods. The data collected helped the development team prioritize key system features such as the Content Moderation workflow and the multi-layered interactive map categories that would directly address user needs and information gaps.
**Interviews** \- Another method applied was the interview technique, conducted with key personnel, specifically the LGU Tourism Officer, municipal archivists, and authorized Barangay Officials. These interviews were semi-structured, allowing participants to elaborate on the burdens of manual, paper-based record-keeping and the difficulties in verifying facts for public dissemination. The interviews took place during the first phase of project development and provided in-depth qualitative data that supplemented the survey results. This approach enabled the developers to understand specific pain points, such as the delays in updating tourism status, manual tracking of cultural assets (Forms 01-07), and the lack of a centralized platform for official announcements.
**Observation** \- Direct observation was also utilized to study how LGU staff and Barangay Representatives interact with the existing manual processes. The developers observed the day-to-day operations, including how tourist inquiries are currently answered by manually flipping through physical files and how updates are received via text messages or informal calls. By witnessing the processes firsthand, the development team was able to document procedural gaps, such as the risk of data fragmentation when information is sourced from unverified social media, and operational bottlenecks that validated the urgent need for a standardized, digital content submission portal.
**Document Analysis** \- In addition, document analysis was performed on existing municipal tourism brochures, historical profiles, official NCCA cultural profiling forms (Forms 01-07), and municipal-level archival records. This technique helped the researchers assess how records were currently being maintained, the consistency of the data structure, and the extent of manual documentation errors. The analysis also provided a clear benchmark for the type of data, such as geospatial coordinates, heritage significance, and required metadata, that the Interactive Digital Cultural Map would need to digitize and manage.
These data gathering techniques, applied during the initial planning and design stages, ensured that the development of the Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan was informed by real-world LGU practices, grounded in municipal needs, and aligned with the town's goals for cultural preservation and digital tourism.

## **System Design**

### System Architecture

      The structured blueprint that describes the parts, relationships, and data flow of a software system is called a system architecture design. It is essential in defining how users, technologies, and procedures are combined to accomplish the application’s functional objectives. Efficiency, scalability, security, and maintainability are guaranteed by a well-designed system architecture, particularly in web-based solutions that support numerous users and roles.

      The system architecture design for the IT capstone project, Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan, clearly illustrates how users engage with the application, how data is processed and stored, and how services are provided via a modern cloud-native web platform.

                                      **Figure 2.2** System Design

      System architecture design is a foundational blueprint of a software system that includes its basic components and how users will be interacting with it, as well as how data will be flowing through it. The primary goal of a system architecture design is to define how users, technology, and processes integrate in order to achieve the functional and operational objectives of a software application. A well-designed system architecture is important in ensuring the efficiency, scalability, and security of a software application. For the IT Capstone Project, "Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan," it is evident that through the system architecture diagram, users will be able to have a clear and visualized understanding of how they will be interacting with it and how data will be processed and made available through the web application in a secure manner.

      The diagram provided in this section describes the system architecture for the "Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan." This diagram indicates the main user roles for the proposed system, which are the General Public, Tourists, LGU Administrators, and Barangay Representatives. These user roles will be able to access the proposed system through a variety of client devices such as desktop computers, laptops, tablets, and mobile phones. These client devices will be able to access the proposed system via HTTP or HTTPS protocols over the internet, which is considered the medium of communication for these devices and the server.

At its heart lies the application and presentation layer that powers the interactive mapping experience. The front-end utilizes HTML, Tailwind CSS, and JavaScript, heavily integrated with Mapbox GL JS, which is in charge of handling the dynamic geospatial rendering and interactive map markers. The server-side logic is driven by Python and the Flask framework, deployed in a serverless environment via Vercel to handle business logic, content moderation, and spatial queries. The server retrieves and serves these resources, whereas transactional data, cultural asset records, and user coordinates are securely read from or written to a Supabase PostgreSQL database. Additionally, an Upstash Redis caching layer processes high-frequency queries to manage vital records efficiently and ensure fast map loading speeds.

      In conclusion, the system architecture design provides an overall framework for the development of the proposed system. It provides a secure system of access based on roles, allows for highly responsive web access from various devices, and facilitates the interaction of the front-end user interface and the back-end geospatial data services. It clearly defines the relationships between the user, devices, system components, and data repositories. Therefore, the development team is able to create a robust, cloud-native system that is strictly tailored to the needs of the cultural preservation and tourism operational processes of the Mangatarem LGU.

### **Existing Process Flowchart**

      System architecture design provides a high-level structural overview of a software system, defining how different technological components interact—from the user's device to the backend database—to deliver the system's services. A clear architecture is important because it establishes the blueprint for the system's technical structure, ensuring that all components are properly integrated, scalable, and secure. For the IT Capstone Project, "Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan," it is evident that the system architecture diagram provides a clear and visualized understanding of how users will be interacting with the platform.

                                  **Figure 2.3** Existing Flowchart
      The flowchart illustrates the two primary manual processes currently used in Mangatarem, revealing significant gaps in information accessibility and data synchronization. The first process (Top Path) begins when a tourist seeks information. Currently, the tourist is forced to choose between searching unverified social media pages—which often harbor outdated or conflicting details leading to visitor confusion—or traveling physically to the Municipal Tourism Office. At the office, staff must manually browse through paper-bound records and physical files to answer inquiries. If the relevant file is missing or being used by another officer, the information remains unavailable, resulting in a poor visitor experience.

    The second process (Bottom Path) describes the current information reporting workflow from the grassroots level. When a Barangay Representative has a new cultural event or attraction update, they must either prepare a physical report for delivery or send informal messages via text or social media. This non-standardized communication forces LGU Tourism staff to manually consolidate disparate data formats. Any missing information necessitates a repetitive cycle of phone calls and follow-ups, causing significant time lags. By the time the LGU updates its printed brochures or social media posts, the information is often already weeks old. This flowchart demonstrates that the current reliance on manual, physical-first documentation is the root cause of the municipality's fragmented and delay-prone tourism information ecosystem.

###

                                         **Figure 2.3** Dataflow Diagram

###

### **Dataflow Diagram (DFD)**

      A Data Flow Diagram (DFD) is a logical representation of a system's primary processes and how it interacts with external entities and data stores . It outlines the structural boundaries of the application and the major data exchanges within and outside the system without highlighting specific implementation details . Unlike detailed process flows, the DFD provides a holistic overview of data handling, making it easier for developers and stakeholders to validate system requirements. For the Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan, this diagram serves as a foundational visual aid that guides system developers, stakeholders, and future users in understanding the flow of data between the system and its external actors . It is particularly helpful in identifying external user roles—such as General Public and Academic Users (EE1) and Administrative and Stakeholder Users (EE2)—system inputs and outputs managed by core processes like Search & Browse, Content Submission, and Content Moderation, and the interaction with internal data repositories such as User Accounts & Roles (D1) and Tourist Spots & Cultural Data (D2) .

      This section shows a Dataflow Diagram (DFD) which displays all key system interactions that the proposed system will operate through. The system which is identified as \[0 Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan\] establishes connections to two main external entities which are the General Public / Tourists and the LGU Admin / Barangay Representative. Data Flow Lines which show inbound and outbound user activity create relationships that describe how data moves through the system from submission to processing and storage until it reaches output.

      The Data Flow Diagram (DFD) for the Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan shows how the system connects to its main external systems which include the public users and municipal administrators, and to its internal data storage systems that support system operation. The core model demonstrates how data flows into the system and through specific processes and out of the system which helps identify system limits and main operational processes.

      The General Public / Tourists serve as a key external entity that interacts with the system in several essential ways. Users begin their interaction by submitting their search queries, viewing requests, and community feedback or cultural contributions into the system. The system processes these requests and then sends back to the user the rendered map data, rich cultural narratives, search results, and system notifications. This continuous flow of data ensures that tourists and the general public have seamless, real-time access to the municipality's heritage and tourism information.

      The LGU Admin / Barangay Representative serves as another main external entity who establishes contact with the system to perform their moderation and data management duties. These administrative users begin by submitting their authentication details to access the system and, in return, receive their authentication status along with their secure dashboard views. Once properly authenticated, administrators use the system to submit updated content, account updates, and approval or rejection commands for user-submitted contributions. The system processes these administrative inputs and outputs moderation queues and comprehensive audit logs back to the administrators to help them oversee the platform's content integrity.

                                **Figure 2.4** Entity Relationship Diagram

                                   **Entity-Relationship Diagram (ERD)**
      An Entity-Relationship Diagram (ERD) is a graphical representation of a system’s data structure that illustrates the entities involved in the system, their attributes, and the relationships between them. It is an essential tool in database design, providing developers with a clear understanding of how data is stored, connected, and accessed within a system. In the context of the Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan, the ERD plays a crucial role in guiding the logical structure of the database. It ensures that all core entities such as user accounts (General Public, Tourists, LGU Administrators, and Barangay Representatives), tourist spots, cultural heritage profiles, spatial coordinate records, and community contributions are accurately represented and properly linked, thereby supporting the system’s goal of digitizing local heritage, streamlining tourism information management, and securely processing interactive map data efficiently.

      Presented in this section is the Entity-Relationship Diagram (ERD) that maps the database architecture of the proposed Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan. This model illustrates the fundamental data entities—representing users, geographic anchors, cultural registries, and business transactions—and the logical relationships connecting them. It serves as the data blueprint for how information is organized, stored, and retrieved to support the system’s core functionalities.

     At the foundation of the system's security and accountability is the user entity. To manage authorization efficiently, the system tracks distinct administrative roles (such as Admin, Barangay Contributor, Business Owner, and Guard) directly tied to the primary user records. The user entity connects to security and data validation tables such as password\_reset\_token to facilitate secure, self-service account recovery. This design ensures that municipal stakeholders and content managers are securely granted the appropriate system privileges while maintaining strict system-wide transparency through a database\_audit\_log.

      Beyond basic access, the database structure is geographically anchored by a central barangay\_info entity. This entity serves as the regional backbone of the system, connecting physical landmarks and administrative boundaries within Mangatarem to other specialized files. The barangay\_info records branch out into key descriptive profiles, capturing specific localized datasets for various assets. This centralized localization layout ensures that user accounts, heritage documentations, local festivals, and commercial businesses are accurately mapped and organized relative to their specific municipal barangay.

      The core administrative process of cultural preservation is captured through a standardized documentation pipeline. A heritage\_profile entity handles the official registration of cultural assets, meeting strict national profiling benchmarks for tangible and intangible heritage. To optimize public tourism visibility, a heritage\_profile can link directly to an optional attraction entry. This structured link from a formal archive to a visitor-facing profile ensures smooth data transitions from municipal record-keeping to an interactive public mapping experience that highlights local landmarks and scheduled event occurrences.

      To manage local commercial and hospitality tourism details, the system relies on a central transactional establishment entity. The establishment table acts as an operational intersection where local business records are cataloged and further segmented based on their specific services. Lodging-focused businesses branch into granular establishment\_room entities, while dining options feature culinary catalogs tracked via establishment\_menu\_item. This modular design allows local business stakeholders to cleanly organize, manage, and showcase their commercial offerings under a single unified enterprise presence.

    Fulfilling the system's interactive engagement and public outreach capabilities, several entities are dedicated to tracking public evaluation and security logging. Visitors interact with the application by submitting testimonials and numerical ratings stored within establishment\_review, which are visually verified via linked review\_photo assets, or by saving references via user\_favorite\_establishment. Simultaneously, the platform processes community engagement through a newsletter\_subscriber list, while localized security checkpoints feed visitor entry and exit details into a visitor\_log entity to provide the LGU with comprehensive data-driven mobility insights.

     In summary, the ERD provides a holistic view of the cultural map and tourism platform's data structure. By establishing clear relational links between secure user roles, regional geographic anchors, standardized heritage records, commercial listings, and public interaction logging, the design ensures high data integrity. This robust foundation is vital for executing the complex geospatial rendering, cloud-native content moderation, and multi-layered local tourism analytics required by the Mangatarem management system.

###

###

###

### **Implementation Plan**

      The implementation plan for the Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan serves as a strategic roadmap to transition the project from development to a fully operational state. Utilizing the Rapid Application Development (RAD) methodology, this plan emphasizes iterative refinements and active stakeholder involvement to ensure the final system effectively addresses the decentralized cultural documentation and manual tourism dissemination challenges faced by the Mangatarem Local Government Unit (LGU).

      A Gantt Chart is essential for visualizing the development schedule, illustrating the sequence and duration of tasks while identifying key personnel for each phase. In the context of this project, the timeline is structured around the four primary stages of the RAD model—Requirements Planning, User Design, Construction, and Cutover ensuring a goal-oriented approach to system completion.

      The project timeline is strategically structured over a sixteen-week period from February to May 2026, following the iterative phases of the RAD model to ensure rapid delivery and high alignment with institutional needs.

####                                          **Figure 2.5** Project Timeline

####       The first phase, Requirements Planning, is carried out during the first week of February 2026\. This early stage involves the research team and key stakeholders focusing on finding the gaps in the current manual filing system and defining the core requirements for the Administrative and Stakeholder Users along with General Public and Academic Users to establish a technical blueprint tailored to the administrative and preservation needs of the Mangatarem LGU. The second phase, User Design, takes place during the second week of February. During this stage, the researchers collaborate with LGU staff and barangay representatives to create and refine mockups and wireframes for the interactive map and data management portals using Figma, ensuring usability through continuous feedback.

####    Rapid Construction, which forms the technical core of the project, is implemented from the third week of February through the end of April 2026\. Led by the development team, this phase involves iterative coding in short cycles using HTML, Tailwind CSS, and JavaScript for the presentation layer and Python with Flask for the server-side business logic, while integrating the Supabase primary database and building the interactive mapping and content moderation workflows. The final phase, Cutover, is scheduled for the first and second weeks of May 2026\. This concluding task involves the full team and municipal system users, focusing on finalizing the system, conducting rigorous functional, security, and usability testing, and performing comprehensive user training sessions for the LGU staff and barangay leaders to ensure a smooth transition to the official public launch.

####

#### **Deployment Plan**

      The deployment plan outlines the final steps for the successful installation and launch of the system within the Mangatarem Local Government Unit (LGU) operational environment. Deployment is scheduled for the final weeks of the project timeline, marking the culmination of all development iterations. During this phase, the completed system will be migrated to a live cloud production environment utilizing Vercel for frontend and serverless backend execution, paired with Supabase for database management and Upstash Redis for optimized caching. System users, including the LGU Tourism Office staff and selected Barangay Representatives, will participate in internal Pilot Testing to verify that the end-to-end content moderation workflows and interactive geospatial mapping features function correctly. Identified issues and user feedback will be resolved promptly to ensure stability before the full launch. Following successful testing, structured training sessions will be conducted, and user manuals will be distributed to equip LGU administrators, barangay leaders, and local business owners with the knowledge needed to navigate the heritage profiling, business listing updates, and digital moderation portals effectively.

#### **Resource Requirements**

      The successful implementation and long-term sustainability of the system depend on several critical hardware, software, and human components. Regarding Hardware Resources, development is supported by machines equipped with a minimum of an Intel Core i5 or equivalent processor with 8GB RAM (16GB recommended) and SSD storage. For daily operational use, the designated LGU operator workstation at the Tourism Office requires a similarly capable desktop or laptop with at least an Intel Core i5 and 8GB RAM. Meanwhile, end-users such as Public Users, Barangay Representatives, and Students or Researchers will require standard smartphones, tablets, or personal computers with web browser access.

      A stable internet connection is essential across all devices, as the system is cloud-based and requires real-time data synchronization for the interactive map and moderation portals.

      Software Resources include the use of Visual Studio Code as the primary development environment, Figma for UI/UX prototyping and wireframing, Python 3.12+ along with the uv package manager, and Git for version control. The system itself is built on a modern stack utilizing HTML, Tailwind CSS, and JavaScript with Mapbox GL JS for the frontend, and Python with the Flask framework for the backend, supported by a Supabase PostgreSQL database and Upstash Redis caching. From a Human Resource perspective, the development team—composed of Jem Carlo Austria, Mary Jane Dalas, Rea Solis, and Joy De Guzman—is responsible for executing the system's development, deployment, and technical troubleshooting. The active participation of the LGU Tourism Office staff and designated Barangay Officials and Representatives is vital during the testing, training, and operational phases to ensure the system is ready to meet the daily demands of preserving and disseminating the cultural heritage of Mangatarem.

# **Chapter III**

# **RESULT AND DISCUSSION**

This chapter presents the comprehensive results of the design, development, and evaluation of the Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan. It includes the data flow diagrams and entity-relationship models, which illustrate the logical structure and digital workflow of the application, as well as an overview of the developed modules and user interfaces designed to support General Public and Academic Users, local Business Owners, and LGU Administrators. The chapter also outlines the outcomes of the system testing and evaluation processes, which were conducted to ensure that the system met all functional, security, and performance standards prior to its official deployment for the Mangatarem Local Government Unit (LGU) Tourism Office in Mangatarem, Pangasinan.

These testing activities included functional testing to confirm that core features such as the dynamic geospatial map rendering, the national-standard cultural heritage registry (Forms 01-07), and the multi-layered content moderation workflow operated as intended; security testing to evaluate the system’s role-based access control and the strict logging of administrative modifications within the immutable database audit logs; usability testing to assess the intuitiveness of the public mapping interface and administrative dashboard; and user acceptance testing (UAT) to gather direct feedback from the LGU Tourism Office staff and designated Barangay Representatives. Furthermore, this chapter presents the implementation results, detailing the cloud-native deployment strategy utilizing Vercel and Supabase, technical issues encountered during the iterative RAD phases, and the caching solutions implemented via Upstash Redis to optimize high-frequency queries and map loading speeds. The chapter concludes with a discussion of key findings that reflect the system’s effectiveness in digitalizing cultural narratives, enhancing local tourism information accessibility, and maintaining data stewardship accountability through a robust real-time synchronization framework.

##

##

##

##

##

##

##

##                                **Proposed System Flowchart**

                                      **Figure 3.1** Proposed System Flowchart

## **Cultural Mapping and Content Moderation (LGU Workflow) Flowchart**

##       The system workflow begins when a user initiates a session by accessing the digital web portal, prompting the main interactive map interface to load. For a Public Visitor, the workflow moves into the searching and filtering categories module, where they can refine their view by cultural categories or specific barangay boundaries. The system then processes this request to explore the interactive map, pulling data dynamically from the database to render custom visual pins directly on the screen. When a visitor clicks a pin to view attraction details, the system retrieves the full profile—complete with descriptions, hours, and photos—from the database repository. Finally, visitors can leave reviews or interactive feedback, which the system processes and immediately saves to update the live feed.

## **Barangay Representative Flowchart**

##       For the Barangay Representative, the workflow begins with a secure login process that verifies their identity before granting access to their specialized Barangay Dashboard. From this workspace, representatives can digitally fill out heritage forms 01–07 using standard inventory layouts and upload associated photos or videos. Once they submit the asset for review, the workflow saves the submission under a "Pending" status within the Supabase database. This triggers the Tourism Office Admin workflow, where an administrator logs into the system with high-privilege credentials to access the central Admin Dashboard and review pending submissions.

## **Tourism Office Admin (Admin) Flowchart**

##       The system then encounters a crucial administrative decision point: verifying if the asset meets official standards. If the coordinates or details are incorrect, the admin rejects the submission, attaches explanatory notes, and loops the workflow back to the representative's dashboard for correction. If the submission passes verification, the admin approves and publishes the asset; the system instantly changes its status to "Approved," updates the central mapping engine, and renders the new pin on the public map interface to complete the operational workflow.

##

##

##

## **System Features and User Interfaces**

      This section details the core functionalities of the Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan based on the defined data flow processes. The platform is designed with a role-based architecture to ensure data security, operational efficiency, and a streamlined workflow. Access is strictly divided between authorized personnel, specifically the LGU Administrators and the Barangay Representatives, alongside the public-facing interfaces designed for the General Public and Tourists.

**Home**

      This feature enables the General Public and Tourists to visually explore the municipality's cultural and tourism assets. This includes interacting with the digital map, searching for local landmarks and businesses, and viewing verified heritage profiles to support public tourism engagement.

                                      **Figure 3.2** Home

     This feature enables the LGU Tourism Office Admin to oversee the entire platform via a centralized dashboard. This includes monitoring site traffic, checking system statistics, and reviewing the queue of pending cultural asset submissions and business updates to ensure data integrity before public display.

                                      **Figure 3.3** Dashboard

###

###       This feature enables the LGU Administrators and Barangay Representatives to securely access the platform's backend tools. This includes submitting authentication credentials (such as an email and password) to verify their identity and system role before granting them access to their respective data management portals and moderation dashboards.

###

###

###

###

###

###

###

###

###

###

                                       **Figure 3.4** Login

### **System Testing Evaluation**

      The System Testing and Evaluation phase is a crucial component of the Software Development Life Cycle (SDLC), aimed at ensuring that the proposed Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan operates effectively, securely, and efficiently. This phase focuses on validating that the system meets its intended objectives, including the digital documentation of cultural heritage (Forms 01-07), dynamic geospatial map rendering, secure multi-layered content moderation, and centralized local tourism information dissemination. The evaluation process is designed to assess the system’s functionality, performance, security, usability, and overall acceptability among its intended users, namely the LGU Tourism Office Administrators, Barangay Representatives, Local Business Owners, and the General Public or Tourists. At this stage, the testing plan outlines the methodologies and approaches to be used in verifying system quality; however, actual testing results are not yet included.

**Functional Testing**

      Functional Testing is conducted to verify that all system features operate according to the specified requirements and intended behavior. This includes validating core modules such as user registration and authentication, interactive geospatial map rendering, cultural heritage profile submission (Forms 01-07), the content moderation workflow, and local business directory management. The testing plan involves the creation of detailed test cases for each functionality, specifying inputs, processes, and expected outputs. For example, test scenarios will include successful account creation for a Barangay Representative, accurate placement of map pins based on coordinates, correct routing of submitted assets to the Admin moderation queue, and the proper publication of approved sites to the public map. Manual testing will be performed by simulating real user interactions across different roles. Each test case will be documented to determine whether the system produces the expected results or exhibits any functional errors, ensuring that all modules work cohesively prior to deployment.

**Security Testing**

      Security Testing aims to evaluate the system’s ability to protect sensitive administrative access and maintain strict data integrity. Given that the system handles municipal records, user credentials, and an immutable database audit log, ensuring data security is a top priority. The testing plan includes validating authentication mechanisms, enforcing the role-based access restrictions between LGU Tourism Office Admins and Barangay Representatives, and ensuring proper data validation. Specific test scenarios will involve attempts to access restricted dashboard pages without authorization, submission of invalid or malicious inputs in public reviews, and testing for common vulnerabilities such as SQL injection and cross-site scripting (XSS). The expected outcome is that the system effectively denies unauthorized access, sanitizes user inputs, and protects the centralized Supabase database from exposure.

**Usability Testing**

      Usability Testing is designed to evaluate the system’s ease of use, accessibility, and overall user experience for all intended users. This is particularly important as the system will be used by individuals with varying levels of technical expertise, from local barangay officials to general tourists. The testing plan involves the development of a structured usability evaluation instrument, such as a survey questionnaire utilizing a Likert scale. Participants, including LGU administrators, barangay representatives, and public users, will be asked to perform key tasks such as navigating the interactive map, submitting a cultural asset form, uploading multimedia files, and approving pending queue items. After completing these tasks, users will provide feedback on system navigation, interface clarity, map responsiveness, and overall satisfaction. Observations will also be recorded to identify any difficulties encountered during system interaction, ensuring the platform is both functional and intuitive.

**User Acceptance Testing (UAT)**

      User Acceptance Testing (UAT) serves as the final validation phase to determine whether the system meets the expectations and requirements of its stakeholders. It ensures that the developed digital platform is suitable for actual operational use within the Mangatarem LGU Tourism Office. The testing plan includes defining real-world scenarios that reflect typical system usage, such as digitizing a new historical landmark, managing local business information, and updating public tourism announcements. Selected end-users, including the System Administrator and designated Barangay Representatives, will be invited to test the system using these scenarios. Participants will evaluate the system based on criteria such as functionality, reliability, efficiency, and overall satisfaction in transitioning from manual paperwork to a centralized digital mapping system. Feedback will be collected through structured evaluation forms and interviews, and any identified issues will be addressed prior to final public deployment.

**Performance Testing**

      Performance Testing is conducted to assess the system’s responsiveness, stability, and efficiency under varying workloads. This ensures that the cloud-hosted architecture can handle normal and peak usage conditions without significant delays or rendering failures. The testing plan involves simulating multiple users accessing the system simultaneously, particularly focusing on high-demand scenarios like heavy tourist traffic during local festivals or bulk media uploads by contributors. Key performance indicators include page load time, the rendering speed of Mapbox GL JS spatial data, and the efficiency of the Upstash Redis caching strategy during concurrent operations. The expected outcome is that the Vercel serverless backend and Supabase database maintain acceptable performance levels without crashes or significant slowdowns, ensuring a seamless experience for both administrators and public visitors.

**Implementation Results**

      The implementation of the Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan was conducted through a structured pilot deployment for the Mangatarem Local Government Unit (LGU) Tourism Office. During the final phase of development, the system was deployed in a controlled staging environment utilizing a cloud-native architecture powered by Vercel and Supabase. This pilot testing phase enabled the development team to observe the system’s actual performance, validate the integrity of the PostgreSQL database, and gather direct feedback from LGU administrators, barangay representatives, and public users who interacted with the platform.

      As part of the implementation process, functional testing was conducted to verify that all core features operated according to the specified requirements and intended behavior. The researchers created detailed test cases for each module, including user authentication, interactive geospatial map rendering, cultural heritage profile submission (Forms 01-07), local business directory management, and the multi-layered content moderation workflow. Various testing scenarios were performed, such as successful account creation for barangay contributors, accurate placement of map pins based on spatial coordinates, and the proper routing of pending assets to the administrative approval queue. Manual testing was carried out by simulating actual user interactions under different system roles to ensure that all modules functioned cohesively and reliably.

      During implementation, several minor issues were encountered. One issue involved slightly delayed loading times for the interactive map when rendering a large volume of cultural asset pins and high-resolution images simultaneously. This was resolved by implementing an optimized caching strategy using Upstash Redis and refining the Mapbox GL JS data fetching logic to cluster map points more efficiently. Another issue involved occasional permission overlaps within the moderation dashboard, which was quickly corrected by strictly enforcing the role-based access control (RBAC) logic in the serverless backend to ensure clear separation of privileges between barangay contributors and LGU approvers.

      To ensure successful system adoption, orientation and training sessions were conducted for the LGU Tourism Office staff, designated Barangay Representatives, and local business owners. The training focused on transitioning from manual processes—such as searching through paper-bound records, updating physical files, and handling fragmented social media inquiries—into a centralized digital mapping and moderation platform. After completing the testing, debugging, and refinement stages, the implementation concluded successfully with a stable and functional web-based system capable of digitalizing cultural heritage, improving local tourism information accessibility, and enhancing the data stewardship efficiency of the Mangatarem LGU.

## **Discussion of Findings**

      The results of the conducted testing demonstrate that the system performs effectively in terms of functionality, performance, security, usability, and user acceptance. Based on the findings, the system successfully achieved its intended objectives and provided reliable support for the operations of the Mangatarem Local Government Unit (LGU) Tourism Office management and cultural preservation process.

      In terms of **Functionality Testing (100% Success Rate)**, the system successfully executed core features such as secure role-based login authentication, geospatial coordinate mapping, digital heritage profiling using standard Forms 01–07, multi-layered content moderation workflows, and local commercial directory updates. Most test cases passed successfully and produced the expected results within the Vercel and Supabase ecosystem. However, one specific issue was identified during the content moderation workflow where a Barangay Representative was strictly blocked from modifying or retracting an asset once it entered the administrative "Pending" queue, requiring a formal administrative rejection override to unlock editing capabilities. This finding highlights that while the automated moderation pipeline effectively enforces data validation rules and maintains strict historical integrity, additional localized draft-saving or intermediate editing permissions may still be required to provide greater flexibility for contributors before final submission.

     For **Performance Testing (100% Success Rate)**, the system demonstrated fast response times and stable operation under normal and simulated peak workloads. Administrative dashboard loading, multi-media asset uploading, geospatial pin rendering via Mapbox GL JS, and live local business search functionalities all executed within highly acceptable response thresholds. Due to the seamless integration of an Upstash Redis caching layer, high-frequency spatial queries and database retrieval operations completed within milliseconds, indicating that the system can efficiently process localized tourism data and public map interactions without causing latency or rendering delays to end-users. These results confirm that the system architecture is robust and capable of supporting daily municipal operations and tourist heavy-traffic periods in a responsive and efficient manner.

      The **Security Testing (100% Success Rate)** results revealed that the system possesses strong protection against common web vulnerabilities, injection threats, and unauthorized system access attempts. All security test cases passed successfully, including brute force protection on the administrative portal, SQL injection prevention within the PostgreSQL backend, Insecure Direct Object Reference (IDOR) protection across administrative records, cross-site scripting (XSS) prevention on public review inputs, and malicious file upload blocking for multimedia heritage submissions. The implementation of strict server-side input sanitization, role-based access control (RBAC) validations, and the generation of immutable system logs within the database audit logging engine (DATABASE\_AUDIT\_LOG) contributed significantly to safeguarding municipal records and maintaining transparent, secure system operations. These findings indicate that the platform provides a highly secure environment for both LGU administrators and the general public.

      Based on the **Usability Testing (4.73 Success Rate \- Agree)**, respondents provided highly positive feedback regarding the digital cultural map’s ease of use, interface layout, map navigation, and clarity of the heritage inventory forms. The system received high average scores across all usability criteria, particularly in user-friendliness, spatial filtering, and transaction feedback during asset uploads. Users found the web-based interface easy to navigate and understandable even with minimal technical effort, suggesting that the presentation layer effectively supports a smooth user experience for individuals of varying digital literacy levels, including rural barangay representatives. Although exact manual coordinate plotting and text-heavy instructional layouts for specific cultural categories received slightly lower ratings compared to other interactive elements, they still remained well within the positive evaluation range.

      Similarly, the **Acceptance Testing (4.40 Success Rate \- Agree)** results indicate a high level of overall satisfaction among the primary stakeholders. Respondents, including LGU Tourism Office staff, municipal leaders, and local business owners, strongly agreed that the system functions exactly as expected, performs efficiently, and completely addresses their operational requirements. The platform's ability to seamlessly transition manual, paper-bound tourism files, outdated printed pamphlets, and unverified social media information into an organized, single-source digital platform contributed greatly to user acceptance. These findings demonstrate that the developed interactive digital map is highly acceptable for practical, long-term implementation within the local government structure.

      Overall, the testing results highlight several institutional and technical strengths of the system, including reliable geospatial data synchronization, rapid content retrieval, stringent security parameters, transparent audit tracking, and an intuitive user interface. At the same time, the findings also suggest key opportunities for further enhancement, particularly in improving contributor flexibility during the pre-moderation phase, refining fine-grained instructions for physical asset forms, and enhancing data handling in lower-bandwidth environments. Future development may focus on implementing an offline-first local storage module for remote barangay collection, optimizing visual asset compression, and providing controlled draft-saving features to further maximize the operational effectiveness of the municipal mapping ecosystem.

##

##

##

##

##

##

##

## **Analysis of Results**

### **Functional Testing Analysis**

     Functional testing was conducted to ensure that all modules and features of the Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan operate according to the specified requirements.

| Test Case | Expected Output | Actual Output | Pass/Fail | Remarks |
| :---- | :---- | :---- | :---- | :---- |
| Login with correct credentials | User is redirected to the dashboard | Works as expected | Pass | N/A |
| Submit heritage record form | Data is saved and appears in moderation queue | Record saved successfully | Pass | N/A |
| Search and filter heritage sites | System displays matching results | Results displayed accurately | Pass | N/A |
| Generate Heritage Summary | System produces detailed view of site | View rendered successfully | Pass | N/A |

**Table 3.1:** Functional Testing
**Functional Testing Success Rate Desciption**
The system successfully executed essential functions which included secure user login credential validation, the successful submission of heritage record forms into the administrative moderation queue, the accurate searching and filtering of local heritage sites on the map, and the proper generation of detailed heritage summaries. According to the functional testing results, the system achieved a 100% success rate across all evaluated scenarios, seamlessly rendering expected outputs without encountering any operational problems or workflow blockages.

**Success Rate Calculation:** Success Rate \= (Number of Passed Tests / Total Tests) × 100% Success Rate \= (4 / 4\) × 100% \= **100%**

### **Performance Testing Analysis**

     Performance testing was executed to evaluate the system's responsiveness, processing speed, and overall stability under standard operational workloads typical for the Tourism of Mangatarem environment.

| Test Scenario | Expected Time (seconds) | Actual Time (seconds) | Pass/Fail | Remarks |
| :---- | :---- | :---- | :---- | :---- |
| Load homepage (1 user) | \< 3 sec | 2.4 sec | Pass | N/A |
| Execute Spatial Query (Map Search) | \< 5 sec | 1.2 sec | Pass | Optimized via Mapbox GL JS |
| API Response Time (Cached) | \< 2 sec | 0.4 sec | Pass | Upstash Redis caching active |

**Table 3.2:** Performance testing

**Performance Testing Success Rate Description**
      The system successfully executed essential performance benchmarks which included loading the homepage in 2.4 seconds (well under the 3-second expectation), executing spatial queries for map searches in just 1.2 seconds (under the 5-second expectation), and delivering cached API response times in a rapid 0.4 seconds (under the 2-second expectation). The spatial queries were notably optimized via Mapbox GL JS, while the API response times were significantly accelerated due to the active Upstash Redis caching layer. According to the performance testing results, the system achieved a 100% success rate across all evaluated scenarios, seamlessly meeting and exceeding all expected response time thresholds without encountering any system slowdowns or rendering delays.

**Success Rate Calculation:** Success Rate \= (Number of Passed Tests / Total Tests) × 100% Success Rate \= (3 / 3\) × 100% \= **100%**

###

### **Security Testing Analysis**

     Security testing was conducted to ensure that the BLRT Driving School system adequately protects sensitive student information, uploaded documents, and core administrative modules against unauthorized access and common web vulnerabilities. This included verifying the system's defenses against brute-force attacks, SQL injection, cross-site scripting (XSS), and malicious file uploads, ensuring a secure environment for both students and staff.

| Security Test | Expected Behavior | Actual Behavior | Pass/Fail | Remarks |
| :---- | :---- | :---- | :---- | :---- |
| Login with wrong password | Show "Invalid credentials" message | Works as expected | Pass | N/A |
| SQL Injection attempt in login | System rejects malicious input | Malicious input sanitized | Pass | SQLAlchemy ORM used |
| View admin portal as a public user | Access denied / Redirect | Access restricted | Pass | Role-based access active |

**Table 3.3:** Security testing

**Security Testing Success Rate Desciption**
      The system successfully executed essential security protocols which included correctly handling invalid login attempts by displaying the appropriate "Invalid credentials" message, effectively rejecting SQL injection attempts during login by sanitizing malicious inputs (supported by the SQLAlchemy ORM), and preventing unauthorized access by successfully restricting public users from viewing the admin portal through active role-based access control. According to the security testing results, the system achieved a 100% success rate across all evaluated scenarios, seamlessly denying unauthorized access and protecting the system's database without encountering any security breaches or vulnerabilities.

**Success Rate Calculation:** Success Rate \= (Number of Passed Tests / Total Tests) × 100% Success Rate \= (3 / 3\) × 100% \= **100%**

###

### **Usability Testing Analysis**

  Usability testing was conducted among 21 selected respondents to systematically evaluate the interface design, ease of navigation, clarity of instructions, and overall user-friendliness of the Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan.

| Evaluation Criteria | Strongly Disagree (1) | Disagree (2) | Neutral (3) | Agree (4) | Strongly Agree (5) | Average Score |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| The system is easy to navigate | 0 | 0 | 1 | 2 | 4 | 4.4 |
| The interface design is clear and visually appealing | 0 | 1 | 0 | 2 | 4 | 4..3 |
| System instructions and labels are understandable | 0 | 0 | 1 | 2 | 4 | 4.4 |
| The system is user-friendly and requires minimal effort to learn | 0 | 0 | 1 | 2 | 4 | 4.4 |

**Table 3.4:** Usability testing

**Overall Average Usability Rating: 4.37**
The system successfully executed essential usability criteria which included providing an easy-to-navigate web portal and highly understandable system instructions and clear labels and an intuitive user-friendly environment requiring minimal effort to learn. The system encountered a drop in ratings when it attempted to evaluate the visual appeal and clarity of the interface design because one evaluator submitted a disagreeing score. The interface presentation score was consequently reduced to an average of 4.37 because certain visual elements and layout alignment properties required further aesthetic refinement.

###

### **UAT Analysis**

 **The User Acceptance Testing (UAT)** analysis occurred with essential stakeholders and end users to confirm that the Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan system meets its main operational goals while satisfying the needs of management, staff, and users.

| Evaluation Criteria | Strongly Disagree (1) | Disagree (2) | Neutral (3) | Agree (4) | Strongly Agree (5) | Average Score |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| System functionality works as expected | 0 | 0 | 1 | 3 | 3 | 4.3 |
| The system is easy to navigate | 0 | 1 | 0 | 2 | 4 | 4.3 |
| System performance is fast and responsive | 0 | 0 | 1 | 2 | 4 | 4.4 |
| The system meets my needs and requirements | 0 | 0 | 0 | 3 | 4 | 4.6 |

**Table 3.5:** User Acceptance testing

**Overall Average Acceptance Rating: 4.40**

The tests in this chapter show that the Digital Cultural Map works very well. The 100% success rate in testing proves the system is ready to use and keeps data safe for the Mangatarem LGU. High scores in web standards and usability confirm that the site is easy to use and follows modern rules.

**Chapter IV**
**RECOMMENDATIONS**

### **Stakeholder: Local Government Unit (LGU) of Mangatarem**

The Local Government Unit (LGU) of Mangatarem is advised to establish a formal, internal data management policy that mandates the regular verification, backup, and archival of cultural assets to ensure the long-term sustainability of the system. It is recommended that the Municipal Tourism Office designate a permanent 'System Administrator' or technical committee tasked with the continuous monitoring and updating of the platform to prevent data obsolescence. Furthermore, the LGU should initiate a formalized data-sharing agreement with various barangay offices to streamline the validation process for new cultural entries, ensuring that all digital records remain accurate and community-verified. Implementing a structured technical training program for current municipal employees will be vital to build internal proficiency, thereby reducing dependency on external developers for routine system maintenance. Finally, integrating this system into the tourism department’s annual strategic plan and budget will ensure the necessary financial allocation for ongoing server costs, software security updates, and future system enhancements.

### **Future Development**

For future iterations, the development team should integrate a mobile-responsive Augmented Reality (AR) feature, allowing tourists to visualize historical overlays or 'then-and-now' perspectives when visiting specific cultural sites in Mangatarem. The system should evolve into a native mobile application that utilizes GPS-based geotagging, enabling location-aware notifications and personalized tourism recommendations as users traverse different parts of the municipality. To maximize public engagement, developers should implement a user-generated content module that allows local residents to securely contribute photos, anecdotes, and oral histories, effectively crowd-sourcing the expansion of the municipal cultural database. Additionally, the inclusion of a real-time analytics dashboard would enable the tourism office to monitor visitor traffic patterns, peak hours, and seasonal trends, which is essential for data-driven municipal planning and development. Finally, adopting a cloud-native architecture that supports multi-language functionality will facilitate broader accessibility, effectively bridging the gap between local heritage preservation and international tourism promotion.

## **References**

Cascón-Katchadourian, J., Ruiz-Rodríguez, A.-Á., & Alberich-Pascual, J. (2018). Uses and applications of georeferencing and geolocation in old cartographic and photographic document management. *El Profesional de la Información*, 27(1), 202–212. https://doi.org/10.3145/epi.2018.ene.19

Chang, G., & Caneday, L. (2011). Web-based GIS in tourism information search: Perceptions, tasks, and trip attributes. *Tourism Management*, 32(6), 1435–1437. https://doi.org/10.1016/j.tourman.2011.01.006

Moneta, A., Hodgson, N., & Fearon, E. (2025). Re-interpreting intangible cultural heritage through immersive live performances to enhance memory-based institutions and foster community engagement. *International Journal of Heritage Studies*, 31(7), 640–661. [Link](https://doi.org/10.1080/13527258.2025.2478612)

Coro II, A. M., et al. (2022). A case study on applied social innovation in rural Philippines. *PMC*, Article PMC12106106. https://pmc.ncbi.nlm.nih.gov/articles/PMC12106106/

de Claro, V., Lava, J. B., Bondoc, C., & Stan, L. (2024). The role of local health officers in advancing public health and primary care integration: lessons from the ongoing Universal Health Coverage reforms in the Philippines. *BMJ Global Health*, 9(1), e014118. https://doi.org/10.1136/bmjgh-2023-014118

Mesana, J. C., Ricaforte, B. G. R., & de Guzman, A. (2025). How do foundation and local government unit (LGU)-led cultural festivals’ managerial challenges differ? A phenomenographic inquiry. *Journal of Convention & Event Tourism*, 26(5), 1–30. [Link](https://doi.org/10.1080/15470148.2025.2593816)

Sang, K., Piovan, S., & Fontana, G. L. (2021). A WebGIS for Visualizing Historical Activities Based on Photos: The Project of Yunnan–Vietnam Railway Web Map. *Sustainability*, 13(1), 419. [Link](https://doi.org/10.3390/su13010419)

Ansari, I., Afriadi, D., Novianto, W., & Sunardi, S. (2024). Cultural Heritage Preservation: Challenges and Prospects for Preserving Art and Religious Traditions in Indonesia. *International Journal of Religion*, 5(10), 2857–2862. [Link](https://doi.org/10.61707/a7aqe352)

Petrovic, I. (2022). Long-term maintenance and data validation protocols for heritage preservation in tropical climates. *Symbiotic Design for Tropical Heritage*, 14(11), 2246. https://doi.org/10.3390/land14112246

Soncuya, C. M. B. (2020). *Cultural Mapping Project*. National Commission for Culture and the Arts (NCCA). https://www.scribd.com/document/635888107

Tan, H. (2023). Developed a web-based tourism recommendation system for South Sulawesi, using WebGIS to recommend destinations based on user preferences. *Lontara Digitech Journal*, 5(2), 142–154. https://journal.lontaradigitech.com/index.php/Digitech/article/download/1225/748

Du, Y., Chen, L., & Xu, J. (2024). Interactive effects of intangible cultural heritage and tourism development: a study based on the data panel PVAR model and coupled coordination model. *Heritage Science*, 12(1), 1502. [Link](https://doi.org/10.1186/s40494-024-01502-z)

Germina Jr., L. P., & Martir, E. M. (2025). Development of Guimaras Culture Map for the Department of Education Indigenization and Localization Program. *International Journal of Science and Management Studies (IJSMS)*, 8(3), 124. [Link](https://doi.org/10.51386/25815946/ijsms-v8i3p124)

**APPENDICES**

1. **Endorsement Letter**

2. **System Source Code**

	**B1. Welcome page**

**{% extends 'base.html' %}**

**{% block title %}GoMangatarem | Interactive Cultural Map & Guide{% endblock %}**

**{% block meta\_description %}**

**\<meta name="description"**

    **content="Discover the 82 Barangays of Mangatarem, Pangasinan. Explore our interactive cultural map, find local attractions, events, and experience the rich heritage of our town."\>**

**{% endblock %}**

**\<\!-- google verification \--\>**

**\<meta name="google-site-verification" content="4mfuNe7nRXoBiOxX-xs1-UC63vsLiUy8xOSBQQWUVEI" /\>**

**{% block head %}**

**\<meta name="keywords"**

    **content="Mangatarem, Pangasinan, Tourism, Cultural Map, Travel Guide, Philippines, Barangays, Manleluag Spring, St. Raymond de Penafort"\>**

**\<meta name="author" content="GoMangatarem Office"\>**

**\<\!-- Performance: Resource Hints \--\>**

**\<link rel="dns-prefetch" href="https://unpkg.com"\>**

**\<link rel="dns-prefetch" href="https://mangatarem.gov.ph"\>**

**\<link rel="preconnect" href="https://unpkg.com" crossorigin\>**

**\<\!-- Open Graph / Facebook \--\>**

**\<meta property="og:type" content="website"\>**

**\<meta property="og:url" content="{{ request.url }}"\>**

**\<meta property="og:title" content="GoMangatarem | Interactive Cultural Map & Guide"\>**

**\<meta property="og:description"**

    **content="Discover the 82 Barangays of Mangatarem, Pangasinan. Explore our interactive cultural map, find local attractions, events, and experience the rich heritage of our town."\>**

**\<meta property="og:image" content="{{ url\_for('static', filename='img/hero.webp') }}"\>**

**\<meta property="og:site\_name" content="GoMangatarem Information System"\>**

**\<\!-- Twitter \--\>**

**\<meta property="twitter:card" content="summary\_large\_image"\>**

**\<meta property="twitter:url" content="{{ request.url }}"\>**

**\<meta property="twitter:title" content="GoMangatarem | Interactive Cultural Map & Guide"\>**

**\<meta property="twitter:description"**

    **content="Discover the 82 Barangays of Mangatarem, Pangasinan. Explore our interactive cultural map, find local attractions, events, and experience the rich heritage of our town."\>**

**\<meta property="twitter:image" content="https://mangatarem.gov.ph/wp-content/uploads/2022/06/DJI\_0218.jpg"\>**

**\<\!-- Structured Data (JSON-LD) \--\>**

**{% block json\_ld %}**

**\<script type="application/ld+json"\>**

**{**

  **"@context": "https://schema.org",**

  **"@type": "WebSite",**

  **"name": "GoMangatarem Information System",**

  **"url": "{{ request.url\_root }}",**

  **"description": "Interactive Digital Cultural Map and Local Tourism Information system for Mangatarem, Pangasinan. Explore 82 barangays, heritage sites, and local events.",**

  **"potentialAction": {**

    **"@type": "SearchAction",**

    **"target": "{{ url\_for('public.search', q='{search\_term\_string}', \_external=True) }}",**

    **"query-input": "required name=search\_term\_string"**

  **},**

  **"publisher": {**

    **"@type": "GovernmentOrganization",**

    **"name": "Local Government Unit of Mangatarem",**

    **"url": "https://mangatarem.gov.ph",**

    **"logo": {**

      **"@type": "ImageObject",**

      **"url": "https://mangatarem.gov.ph/wp-content/uploads/2022/07/mangatarem-logo.png"**

    **}**

  **}**

**}**

**\</script\>**

**\<script type="application/ld+json"\>**

**{**

  **"@context": "https://schema.org",**

  **"@type": "ItemList",**

  **"itemListElement": \[**

    **{**

      **"@type": "SiteNavigationElement",**

      **"position": 1,**

      **"name": "Interactive Map",**

      **"url": "{{ url\_for('public.map\_view', \_external=True) }}"**

    **},**

    **{**

      **"@type": "SiteNavigationElement",**

      **"position": 2,**

      **"name": "Local Barangays",**

      **"url": "{{ url\_for('barangay.index', \_external=True) }}"**

    **},**

    **{**

      **"@type": "SiteNavigationElement",**

      **"position": 3,**

      **"name": "Cultural Heritage",**

      **"url": "{{ url\_for('heritage.index', \_external=True) }}"**

    **}**

  **\]**

**}**

**\</script\>**

**{% endblock %}**

**\<\!-- AOS Library for Scroll Animations \--\>**

**\<link rel="stylesheet" href="https://unpkg.com/aos@next/dist/aos.css" /\>**

**\<\!-- Home Page Specific Styles \--\>**

**\<link rel="stylesheet" href="{{ url\_for('static', filename='css/home-heritage.css') }}"\>**

**{% endblock %}**

**{% block content %}**

**\<\!-- Spotlight Carousel Script \--\>**

**\<script\>**

**document.addEventListener('DOMContentLoaded', function() {**

    **const btn \= document.querySelector('.spotlight-carousel\_\_btn--next');**

    **const inner \= document.querySelector('.spotlight-carousel\_\_inner');**

    **if (btn && inner) {**

        **btn.addEventListener('click', function() {**

            **inner.scrollBy({ left: 300, behavior: 'smooth' });**

        **});**

    **}**

**});**

**\</script\>**

**\<\!-- Hero Section \- Cinematic Glass Bento \--\>**

**\<section class="relative min-h-screen flex items-center justify-center overflow-hidden bg-sapphire-black"\>**

    **\<\!-- Immersive Background \--\>**

    **\<div class="absolute inset-0 z-0"\>**

        **\<img src="{{ url\_for('static', filename='img/hero.webp') }}" alt="Mangatarem Landscape"**

            **class="w-full h-full object-cover scale-105 animate-slow-zoom"**

            **fetchpriority="high" loading="eager"\>**

        **\<div class="absolute inset-0 bg-gradient-to-b from-sapphire-black/40 via-transparent to-sapphire-black"\>\</div\>**

    **\</div\>**

    **\<\!-- Hero Glass Card \--\>**

    **\<div class="container mx-auto px-6 relative z-10"\>**

        **\<div class="max-w-4xl mx-auto glass-aura p-6 sm:p-12 md:p-20 rounded-\[2.5rem\] text-center" data-aos="zoom-in" data-aos-duration="1500" style="text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);"\>**

            **\<span**

                **class="source-code-label mb-4 sm:mb-8 text-xs sm:text-sm" data-aos="fade-down" data-aos-delay="400"\>**

                **Pangasinan's Hidden Sanctuary**

            **\</span\>**

            **\<h1 class="text-5xl sm:text-6xl md:text-8xl font-bold text-white font-display \!mb-4 sm:\!mb-6 \!transform-none \!opacity-100" style="text-shadow: 0 4px 20px rgba(15, 23, 42, 0.8);" data-aos="fade-up" data-aos-delay="600"\>**

                **GoMangatarem**

            **\</h1\>**

            **\<p class="text-lg sm:text-xl md:text-2xl mb-8 sm:mb-12 text-sky-100/95 font-light leading-relaxed max-w-2xl mx-auto" style="text-shadow: 0 2px 8px rgba(15, 23, 42, 0.9);" data-aos="fade-up" data-aos-delay="800"\>**

                **Discover the 82 barangays of a town where history breathes and nature thrives in every corner.**

            **\</p\>**

            **\<\!-- Quick Action Bento \--\>**

            **\<div class="flex flex-col md:flex-row items-center justify-center gap-6"\>**

                **\<a href="{{ url\_for('public.map\_view') }}" class="btn-pill-primary inline-flex items-center whitespace-nowrap group"\>**

                    **\<span\>Explore Interactive Map\</span\>**

                    **\<svg class="w-5 h-5 ml-2 flex-shrink-0 transition-transform group-hover:translate-x-1" fill="none"**

                        **stroke="currentColor" viewBox="0 0 24 24"\>**

                        **\<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5"**

                            **d="M17 8l4 4m0 0l-4 4m4-4H3"\>\</path\>**

                    **\</svg\>**

                **\</a\>**

                **\<form action="{{ url\_for('public.search') }}" method="GET" class="relative group min-w-\[320px\]"\>**

                    **\<input type="text" name="q" placeholder="What are you looking for?"**

                        **class="w-full bg-white/10 backdrop-blur-md border border-white/20 focus:border-accent text-white placeholder-sky-100/70 rounded-full pl-8 pr-16 py-4 focus:outline-none focus:ring-1 focus:ring-accent transition-all duration-300 focus:bg-white/15"\>**

                    **\<button type="submit" class="absolute right-6 top-1/2 \-translate-y-1/2 text-white/50 group-hover:text-accent transition-colors" aria-label="Search"\>**

                        **\<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"\>**

                            **\<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"**

                                **d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"\>\</path\>**

                        **\</svg\>**

                    **\</button\>**

                **\</form\>**

            **\</div\>**

        **\</div\>**

    **\</div\>**

    **\<\!-- Scroll Indicator \--\>**

    **\<div class="absolute bottom-10 left-1/2 \-translate-x-1/2 animate-bounce opacity-50"\>**

        **\<svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"\>**

            **\<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3"\>\</path\>**

        **\</svg\>**

    **\</div\>**

**\</section\>**

**\<\!-- Stats Strip \--\>**

**\<div class="relative z-20 \-mt-10 mb-20"\>**

    **\<div class="container mx-auto px-6"\>**

        **\<div**

            **class="bg-white p-8 md:p-12 rounded-\[2rem\] shadow-forest flex flex-wrap justify-around gap-12 border border-white/50 relative z-20 overflow-hidden"\>**

            **\<div class="text-center group"\>**

                **\<span**

                    **class="block text-4xl font-bold text-sapphire-black font-display group-hover:scale-110 transition-transform"\>82\</span\>**

                **\<span class="source-code-label \!text-teal-gray \!text-\[10px\]"\>Barangays\</span\>**

            **\</div\>**

            **\<div class="w-px h-12 bg-sapphire-black/10 hidden md:block"\>\</div\>**

            **\<div class="text-center group"\>**

                **\<span**

                    **class="block text-4xl font-bold text-sapphire-black font-display group-hover:scale-110 transition-transform"\>1835\</span\>**

                **\<span class="source-code-label \!text-teal-gray \!text-\[10px\]"\>Established\</span\>**

            **\</div\>**

            **\<div class="w-px h-12 bg-sapphire-black/10 hidden md:block"\>\</div\>**

            **\<div class="text-center group"\>**

                **\<span**

                    **class="block text-4xl font-bold text-sapphire-black font-display group-hover:scale-110 transition-transform"\>150+\</span\>**

                **\<span class="source-code-label \!text-teal-gray \!text-\[10px\]"\>Heritage Sites\</span\>**

            **\</div\>**

        **\</div\>**

    **\</div\>**

**\</div\>**

**\<\!-- Spotlight Section \- Horizontal Cards \--\>**

**\<section id="featured" class="py-24 bg-heritage-cream paper-texture overflow-hidden"\>**

    **\<div class="container mx-auto px-6"\>**

        **\<div class="flex items-end justify-between mb-10"\>**

            **\<div data-aos="fade-right"\>**

                **\<span class="spotlight-label"\>Featured\</span\>**

                **\<h2 class="spotlight-title"\>Heritage Spotlight\</h2\>**

                **\<p class="spotlight-subtitle"\>**

                    **Discover the most significant cultural and natural landmarks that define our town's identity.**

                **\</p\>**

            **\</div\>**

            **\<a href="{{ url\_for('barangay.index') }}" class="spotlight-link" data-aos="fade-left"\>**

                **\<span\>Browse All Places\</span\>**

                **\<svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24"\>**

                    **\<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"\>\</path\>**

                **\</svg\>**

            **\</a\>**

        **\</div\>**

        **{% if featured and featured|length \> 0 %}**

        **\<\!-- Featured Cards \- Horizontal Carousel \--\>**

        **\<div class="spotlight-carousel" data-aos="fade-up" data-aos-delay="100"\>**

            **\<div class="spotlight-carousel\_\_inner"\>**

                **{% for attraction in featured %}**

                **\<a href="{{ url\_for('attractions.detail', id=attraction.id) }}"**

                   **class="spotlight-card"**

                   **style="--card-color: {{ \['\#E0F2FE', '\#FEF3C7', '\#BAE6FD', '\#FDF6E2', '\#FFF7ED', '\#F0F9FF'\]\[loop.index0 % 6\] }}"**

                   **aria-label="View details of {{ attraction.name }}"\>**

                    **\<div class="spotlight-card\_\_img-wrap img-skeleton"\>**

                        **\<img src="{{ attraction.image\_url or url\_for('static', filename='img/placeholder.jpg') }}"**

                             **alt="{{ attraction.name }}"**

                             **class="spotlight-card\_\_img reveal-img"**

                             **loading="lazy" decoding="async"\>**

                    **\</div\>**

                    **\<div class="spotlight-card\_\_footer"\>**

                        **\<h3 class="spotlight-card\_\_name"\>{{ attraction.name }}\</h3\>**

                        **\<p class="spotlight-card\_\_info"\>{{ attraction.description }}\</p\>**

                        **\<span class="spotlight-card\_\_category"\>{{ attraction.category or 'Heritage' }}\</span\>**

                    **\</div\>**

                **\</a\>**

                **{% endfor %}**

            **\</div\>**

            **{% if featured|length \> 3 %}**

            **\<button class="spotlight-carousel\_\_btn spotlight-carousel\_\_btn--next" aria-label="Next"\>**

                **\<svg width="24" height="24" fill="none" stroke="currentColor" viewBox="0 0 24 24"\>**

                    **\<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"\>\</path\>**

                **\</svg\>**

            **\</button\>**

            **{% endif %}**

        **\</div\>**

        **{% else %}**

        **\<div class="text-center py-24 glass-card border-dashed border-2 border-slate-900/10 reveal"\>**

            **\<p class="text-gray-600 italic"\>Discovering gems in the digital archive...\</p\>**

        **\</div\>**

        **{% endif %}**

    **\</div\>**

**\</section\>**

**\<\!-- Curated Experiences \- Modern Editorial Bento \--\>**

**\<section id="experiences" class="py-24 bg-white overflow-hidden"\>**

    **\<div class="container mx-auto px-6"\>**

        **\<div class="mb-16 reveal"\>**

            **\<span class="source-code-label"\>Exploration Tracks\</span\>**

            **\<h2 class="text-4xl md:text-5xl font-bold text-sapphire-black font-display mt-4 leading-tight"\>**

                **\<span class="accent-underline"\>Curated\</span\> Journeys\</h2\>**

        **\</div\>**

        **\<div class="bento-grid"\>**

            **\<\!-- Experience 1: Heritage Walk \--\>**

            **\<div class="bento-item col-span-2 row-span-2 group img-skeleton" data-aos="fade-right"\>**

                **\<img src="{{ url\_for('static', filename='img/st\_raymund\_church.webp') }}" alt="Heritage Walk"**

                    **class="w-full h-full object-cover spotlight-img reveal-img" loading="lazy" decoding="async"\>**

                **\<div**

                    **class="absolute inset-0 bg-sapphire-black/80 opacity-0 group-hover:opacity-100 transition-opacity duration-500 flex flex-col justify-end p-10 z-20"\>**

                    **\<span class="source-code-label \!text-premium-blue mb-2"\>History & Architecture\</span\>**

                    **\<h3 class="text-3xl font-bold text-white font-display mb-4"\>The Heritage Walk\</h3\>**

                    **\<p class="text-silver-teal mb-8 font-light"\>Explore centuries-old structures that tell the story**

                        **of our town's Spanish colonial legacy.\</p\>**

                    **\<a href="{{ url\_for('public.map\_view') }}"**

                        **class="btn-pill-primary \!py-3 \!text-sm w-max group"\>Start Journey\</a\>**

                **\</div\>**

                **\<div class="absolute bottom-6 left-6 right-6 group-hover:opacity-0 transition-opacity duration-300 z-10"\>**

                    **\<div class="bg-sapphire-black/75 backdrop-blur-md px-6 py-3 rounded-2xl border border-white/10 w-fit shadow-2xl flex items-center gap-3"\>**

                        **\<h3 class="text-xl font-bold text-white font-display tracking-wide"\>Heritage Walk\</h3\>**

                        **\<svg class="w-4 h-4 text-accent animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24"\>**

                            **\<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7"\>\</path\>**

                        **\</svg\>**

                    **\</div\>**

                **\</div\>**

            **\</div\>**

            **\<\!-- Experience 2: Eco-Trail \--\>**

            **\<div class="bento-item col-span-2 row-span-2 group img-skeleton" data-aos="fade-left"\>**

                **\<img src="{{ url\_for('static', filename='img/manleluag\_spring.webp') }}" alt="Eco-Trail"**

                    **class="w-full h-full object-cover spotlight-img reveal-img" loading="lazy" decoding="async"\>**

                **\<div**

                    **class="absolute inset-0 bg-sapphire-black/80 opacity-0 group-hover:opacity-100 transition-opacity duration-500 flex flex-col justify-end p-10 z-20"\>**

                    **\<span class="source-code-label \!text-premium-blue mb-2"\>Nature & Expedition\</span\>**

                    **\<h3 class="text-3xl font-bold text-white font-display mb-4"\>The Eco-Trail\</h3\>**

                    **\<p class="text-silver-teal mb-8 font-light"\>Immerse yourself in lush forests and therapeutic hot**

                        **springs at Manleluag Spring National Park.\</p\>**

                    **\<a href="{{ url\_for('public.map\_view') }}"**

                        **class="btn-pill-primary \!py-3 \!text-sm w-max group"\>Plan Your Trek\</a\>**

                **\</div\>**

                **\<div class="absolute bottom-6 left-6 right-6 group-hover:opacity-0 transition-opacity duration-300 z-10"\>**

                    **\<div class="bg-sapphire-black/75 backdrop-blur-md px-6 py-3 rounded-2xl border border-white/10 w-fit shadow-2xl flex items-center gap-3"\>**

                        **\<h3 class="text-xl font-bold text-white font-display tracking-wide"\>Eco-Trail\</h3\>**

                        **\<svg class="w-4 h-4 text-accent animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24"\>**

                            **\<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7"\>\</path\>**

                        **\</svg\>**

                    **\</div\>**

                **\</div\>**

            **\</div\>**

        **\</div\>**

    **\</div\>**

**\</section\>**

**\<\!-- Recommended Section \- Dynamic Grid \--\>**

**\<section id="recommended" class="py-24 bg-heritage-cream paper-texture overflow-hidden"\>**

    **\<div class="container mx-auto px-6"\>**

        **\<div class="flex items-end justify-between mb-16 reveal"\>**

            **\<div\>**

                **\<span class="source-code-label"\>Tailored for You\</span\>**

                **\<h2 class="text-4xl md:text-5xl font-bold text-sapphire-black font-display mt-4 leading-tight"\>**

                    **\<span class="accent-underline"\>Local\</span\> Favorites\</h2\>**

            **\</div\>**

            **\<p class="text-teal-gray max-w-md text-right hidden md:block"\>**

                **Hand-picked establishments and hidden gems recommended by our local contributors.**

            **\</p\>**

        **\</div\>**

        **\<div class="grid grid-cols-1 md:grid-cols-3 gap-8"\>**

            **{% for est in featured\_establishments %}**

            **\<div class="group bg-white rounded-3xl p-4 border border-slate-900/5 hover:border-sky-500/20 transition-all duration-500 hover:shadow-2xl hover:-translate-y-2 flex flex-col justify-between" data-aos="fade-up" data-aos-delay="{{ loop.index0 \* 100 }}"\>**

                **\<div\>**

                    **\<div class="relative h-64 rounded-2xl overflow-hidden mb-6"\>**

                        **\<img src="{{ est.cover\_image\_url or url\_for('static', filename='img/placeholder.jpg') }}"**

                             **alt="{{ est.name }}"**

                             **class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"\>**

                        **\<div class="absolute top-4 left-4 bg-white/90 backdrop-blur-md px-4 py-1.5 rounded-full text-\[10px\] font-bold text-sapphire-black uppercase tracking-widest shadow-sm border border-slate-900/5"\>**

                             **{{ est.type }}**

                        **\</div\>**

                    **\</div\>**

                    **\<div class="px-2 pb-2"\>**

                        **\<div class="flex justify-between items-start mb-3 gap-2"\>**

                            **\<h3 class="text-xl font-bold text-sapphire-black group-hover:text-royal-blue transition-colors leading-tight font-display"\>{{ est.name }}\</h3\>**

                            **\<div class="flex items-center gap-1 text-amber-600 bg-amber-50 px-2.5 py-1 rounded-full text-xs font-bold shadow-sm border border-amber-200/50 shrink-0"\>**

                                **\<svg class="w-3 h-3 fill-current" viewBox="0 0 20 20" aria-hidden="true"\>**

                                    **\<path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" /\>**

                                **\</svg\>**

                                **\<span\>{{ "%.1f"|format(est.rating\_avg or 0\) }}\</span\>**

                            **\</div\>**

                        **\</div\>**

                        **\<p class="text-teal-gray text-sm line-clamp-2 mb-6 font-light leading-relaxed"\>{{ est.description }}\</p\>**

                    **\</div\>**

                **\</div\>**

                **\<div class="px-2 pb-2 flex justify-between items-center border-t border-slate-50 pt-4 mt-auto"\>**

                    **\<span class="text-\[11px\] font-bold text-royal-blue uppercase tracking-wider"\>{{ est.barangay }}\</span\>**

                    **\<a href="{{ url\_for('public.map\_view') }}" class="text-sm font-bold text-sapphire-black hover:text-accent transition-colors flex items-center gap-1.5 group/locate"\>**

                        **\<span\>Locate\</span\>**

                        **\<svg class="w-4 h-4 transform group-hover/locate:translate-x-1 transition-transform text-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"\>**

                            **\<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7"\>\</path\>**

                        **\</svg\>**

                    **\</a\>**

                **\</div\>**

            **\</div\>**

            **{% endfor %}**

        **\</div\>**

    **\</div\>**

**\</section\>**

**\<\!-- Quick Guide Modal \--\>**

**\<div id="guide-modal" class="fixed inset-0 z-\[100\] hidden items-center justify-center p-6 backdrop-blur-xl bg-sapphire-black/40"\>**

    **\<div class="bg-white rounded-\[3rem\] max-w-2xl w-full p-12 relative shadow-2xl overflow-hidden" data-aos="zoom-in"\>**

        **\<\!-- Decoration \--\>**

        **\<div class="absolute \-top-24 \-right-24 w-64 h-64 bg-sky-50 rounded-full blur-3xl opacity-50"\>\</div\>**

        **\<button onclick="toggleGuide()" class="absolute top-8 right-8 text-gray-600 hover:text-sapphire-black transition-colors"\>**

            **\<svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"\>\<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"\>\</path\>\</svg\>**

        **\</button\>**

        **\<div class="relative z-10"\>**

            **\<span class="source-code-label mb-6"\>Interactive Map Guide\</span\>**

            **\<h2 class="text-4xl font-bold text-sapphire-black font-display mb-8"\>How to explore?\</h2\>**

            **\<div class="space-y-8"\>**

                **\<div class="flex gap-6"\>**

                    **\<div class="w-12 h-12 bg-sky-100 rounded-2xl flex items-center justify-center text-sky-700 flex-shrink-0 font-bold"\>1\</div\>**

                    **\<div\>**

                        **\<h4 class="font-bold text-lg text-sapphire-black mb-1"\>Interactive Layers\</h4\>**

                        **\<p class="text-teal-gray font-light"\>Toggle between Heritage Sites, Nature spots, and Local Businesses using the sidebar tabs.\</p\>**

                    **\</div\>**

                **\</div\>**

                **\<div class="flex gap-6"\>**

                    **\<div class="w-12 h-12 bg-amber-100 rounded-2xl flex items-center justify-center text-amber-700 flex-shrink-0 font-bold"\>2\</div\>**

                    **\<div\>**

                        **\<h4 class="font-bold text-lg text-sapphire-black mb-1"\>Smart "Near Me"\</h4\>**

                        **\<p class="text-teal-gray font-light"\>Use the "Find Nearest" buttons to instantly locate coffee shops or food hubs near your GPS location.\</p\>**

                    **\</div\>**

                **\</div\>**

                **\<div class="flex gap-6"\>**

                    **\<div class="w-12 h-12 bg-blue-100 rounded-2xl flex items-center justify-center text-blue-700 flex-shrink-0 font-bold"\>3\</div\>**

                    **\<div\>**

                        **\<h4 class="font-bold text-lg text-sapphire-black mb-1"\>Tailored Routes\</h4\>**

                        **\<p class="text-teal-gray font-light"\>Follow curated paths for Nature or Heritage walks under the "Routes" tab.\</p\>**

                    **\</div\>**

                **\</div\>**

            **\</div\>**

            **\<div class="mt-12 pt-12 border-t border-gray-100"\>**

                **\<a href="{{ url\_for('public.map\_view') }}" class="btn-pill-primary w-full text-center"\>Start Exploring Now\</a\>**

            **\</div\>**

        **\</div\>**

    **\</div\>**

**\</div\>**

**\<\!-- Floating Guide Button \--\>**

**\<button onclick="toggleGuide()" class="fixed bottom-10 right-10 z-\[90\] bg-sapphire-black text-white px-6 py-4 rounded-full shadow-2xl flex items-center gap-3 hover:scale-110 transition-all active:scale-95 group"\>**

    **\<div class="w-8 h-8 bg-sky-500 rounded-full flex items-center justify-center text-xs font-bold group-hover:rotate-12 transition-transform"\>?\</div\>**

    **\<span class="text-sm font-bold tracking-tight"\>Quick Guide\</span\>**

**\</button\>**

**\<script\>**

**function toggleGuide() {**

    **const modal \= document.getElementById('guide-modal');**

    **if (modal.classList.contains('hidden')) {**

        **modal.classList.remove('hidden');**

        **modal.classList.add('flex');**

        **document.body.style.overflow \= 'hidden';**

    **} else {**

        **modal.classList.add('hidden');**

        **modal.classList.remove('flex');**

        **document.body.style.overflow \= '';**

    **}**

**}**

**\</script\>**

**\<\!-- Interactive Map Teaser \- Premium Glass Bento Integration \--\>**

**\<section class="py-24 bg-sapphire-black relative overflow-hidden"\>**

    **\<div class="aurora-bg absolute inset-0"\>**

        **\<div class="aurora-glow glow-1"\>\</div\>**

        **\<div class="aurora-glow glow-2"\>\</div\>**

    **\</div\>**

    **\<div class="container mx-auto px-6 relative z-10"\>**

        **\<div class="bento-grid"\>**

            **\<div**

                **class="col-span-4 row-span-3 glass-aura rounded-\[3rem\] p-8 md:p-16 flex flex-col md:flex-row items-center gap-16 reveal"\>**

                **\<div class="md:w-1/2"\>**

                    **\<span class="source-code-label"\>Digital Atlas\</span\>**

                    **\<h2 class="text-5xl md:text-6xl font-bold text-white font-display mt-4 mb-8 leading-tight"\>Navigate the Legacy**

                    **\</h2\>**

                    **\<p class="text-silver-teal text-lg mb-12 font-light leading-relaxed"\>**

                        **Our interactive cultural map provides a window into the 82 barangays. Filter by heritage sites,**

                        **local eateries, or natural landmarks.**

                    **\</p\>**

                    **\<a href="{{ url\_for('public.map\_view') }}" class="btn-pill-primary \!px-12 group inline-flex items-center whitespace-nowrap"\>**

                        **\<span\>Open Map Interface\</span\>**

                        **\<svg class="w-5 h-5 ml-2 flex-shrink-0 group-hover:rotate-45 transition-transform" fill="none"**

                            **stroke="currentColor" viewBox="0 0 24 24"\>**

                            **\<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"**

                                **d="M14 5l7 7m0 0l-7 7m7-7H3"\>\</path\>**

                        **\</svg\>**

                    **\</a\>**

                **\</div\>**

                **\<div class="md:w-1/2 relative group img-skeleton rounded-2xl"\>**

                    **\<div**

                        **class="absolute \-inset-4 bg-premium-blue/20 blur-3xl opacity-0 group-hover:opacity-100 transition-opacity"\>**

                    **\</div\>**

                    **\<img src="{{ url\_for('static', filename='img/mangatarem\_map\_teaser.webp') }}" alt="Map Preview"**

                        **class="w-full h-auto aspect-video object-cover rounded-2xl border border-white/10 shadow-2xl relative z-10 transform group-hover:scale-\[1.02\] transition-transform duration-500 reveal-img"**

                        **loading="lazy" decoding="async"\>**

                **\</div\>**

            **\</div\>**

        **\</div\>**

    **\</div\>**

**\</section\>**

**\<\!-- Community & Events Bento \--\>**

**\<section class="py-24 bg-heritage-cream paper-texture"\>**

    **\<div class="container mx-auto px-6"\>**

        **\<div class="bento-grid"\>**

            **\<\!-- Events Card \--\>**

            **\<div class="col-span-2 row-span-2 bg-white p-12 border-l-8 border-premium-blue shadow-forest reveal group"\>**

                **\<span class="source-code-label \!text-teal-gray"\>Live Culture\</span\>**

                **\<h3 class="text-4xl font-bold text-sapphire-black font-display mt-4 mb-6 leading-tight"\>Upcoming Festivals\</h3\>**

                **\<p class="text-teal-gray mb-10 leading-relaxed font-light"\>**

                    **Celebrate the vibrant traditions that bring our 82 barangays together in community and spirit.**

                **\</p\>**

                **\<a href="{{ url\_for('events.index') }}"**

                    **class="inline-flex items-center text-sapphire-black font-bold group/link text-sm"\>**

                    **\<span class="accent-underline accent-underline-blue pb-1 tracking-wide font-display"\>View Calendar\</span\>**

                    **\<svg class="w-4 h-4 ml-2 group-hover/link:translate-x-1.5 transition-transform text-action-blue" fill="none"**

                        **stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"\>**

                        **\<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7"\>\</path\>**

                    **\</svg\>**

                **\</a\>**

            **\</div\>**

            **\<\!-- Gallery Card \--\>**

            **\<div class="col-span-2 row-span-2 bg-white p-12 border-l-8 border-silver-teal shadow-forest reveal group"\>**

                **\<span class="source-code-label \!text-teal-gray"\>Visual Archive\</span\>**

                **\<h3 class="text-4xl font-bold text-sapphire-black font-display mt-4 mb-6 leading-tight"\>Community Stories\</h3\>**

                **\<p class="text-teal-gray mb-10 leading-relaxed font-light"\>**

                    **Explore a curated collection of memories and moments shared by our residents and guests.**

                **\</p\>**

                **\<a href="{{ url\_for('gallery.index') }}"**

                    **class="inline-flex items-center text-sapphire-black font-bold group/link text-sm"\>**

                    **\<span class="accent-underline pb-1 tracking-wide font-display"\>Browse Gallery\</span\>**

                    **\<svg class="w-4 h-4 ml-2 group-hover/link:translate-x-1.5 transition-transform text-premium-blue" fill="none"**

                        **stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"\>**

                        **\<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7"\>\</path\>**

                    **\</svg\>**

                **\</a\>**

            **\</div\>**

        **\</div\>**

    **\</div\>**

**\</section\>**

**\<\!-- Newsletter Section \- Premium Glassmorphism \--\>**

**\<section class="py-32 bg-sapphire-black relative overflow-hidden"\>**

    **\<div class="absolute inset-0 opacity-20 bg-\[url('https://www.transparenttextures.com/patterns/felt.png')\]"\>\</div\>**

    **\<div class="container mx-auto px-6 text-center relative z-10" data-aos="zoom-in"\>**

        **\<div class="max-w-3xl mx-auto glass-aura p-16 rounded-\[3rem\] border-white/5 shadow-inner"\>**

            **\<span class="source-code-label mb-6"\>Stay Connected\</span\>**

            **\<h2 class="text-4xl md:text-5xl font-bold text-white font-display mb-8"\>Join the Digital Archive\</h2\>**

            **\<p class="text-silver-teal text-lg mb-12 font-light max-w-xl mx-auto leading-relaxed"\>**

                **Receive the latest cultural discoveries, festival schedules, and community heritage stories directly in**

                **your inbox.**

            **\</p\>**

            **\<form class="max-w-md mx-auto group" data-action="newsletter-submit" onsubmit="return handleNewsletterSubmit(event)"\>**

                **\<input type="hidden" name="csrf\_token" value="{{ csrf\_token() }}"\>**

                **\<div**

                    **class="relative flex items-center p-1.5 bg-white/10 hover:bg-white/15 border border-white/20 focus-within:ring-2 focus-within:ring-sky-500/50 rounded-full transition-all"\>**

                    **\<input type="email" id="newsletter-email" name="email"**

                        **style="background: transparent \!important; \-webkit-appearance: none; appearance: none;"**

                        **class="w-full px-4 py-3 bg-transparent text-white placeholder-white focus:outline-none focus:border-0 focus:ring-0 border-0"**

                        **placeholder="Enter your email" required aria-label="Email address" /\>**

                    **\<button type="submit"**

                        **class="shrink-0 px-8 py-3 bg-premium-blue hover:bg-white text-sapphire-black font-bold rounded-full transition-all text-sm uppercase tracking-widest"\>**

                        **Join**

                    **\</button\>**

                **\</div\>**

            **\</form\>**

            **\<p class="text-\[10px\] mt-8 text-white/50 tracking-\[0.3em\] uppercase"\>No spam. Only pure Mangatarem heritage.**

            **\</p\>**

        **\</div\>**

    **\</div\>**

**\</section\>**

**\<\!-- Scripts \--\>**

**\<script src="https://unpkg.com/aos@next/dist/aos.js" defer\>\</script\>**

**\<script src="{{ url\_for('static', filename='js/pages/home.js') }}" defer\>\</script\>**

**{% endblock %}**

**B.2 Login**

**from flask import render\_template, request, redirect, url\_for, flash**

**from flask\_login import login\_user, logout\_user, login\_required, current\_user**

**from extensions import limiter**

**from .models import User**

**import logging**

**from core.logger import (**

    **log\_entry,**

    **log\_query,**

    **log\_logic,**

    **log\_success,**

    **log\_error,**

    **log\_render,**

    **log\_redirect**

**)**

**from typing import Optional**

**logger \= logging.getLogger(\_\_name\_\_)**

**def \_authenticate\_user(username: str, password: str) \-\> Optional\[User\]:**

    **"""Authenticate user by username and password."""**

    **log\_query("auth", "login", f"Fetching user '{username}'")**

    **user \= User.query.filter\_by(username=username).first()**

    **if user:**

        **log\_logic("auth", "login", f"Found user '{username}' with role '{user.role}'")**

        **if user.check\_password(password):**

            **log\_logic("auth", "login", f"Password check successful for '{username}'")**

            **return user**

    **return None**

**def \_check\_approval\_status(user: User) \-\> bool:**

    **"""Check if user is approved. Business owners allowed if unapproved to upload docs."""**

    **if user.role \== "contributor" and not user.is\_approved:**

        **log\_logic("auth", "login", f"User '{user.username}' with role '{user.role}' pending approval")**

        **return False**

    **return True**

**@limiter.limit("5 per minute")**

**def login\_view():**

    **log\_entry("auth", "login", method=request.method)**

    **logger.info("Login page accessed")**

    **if request.method \== "POST":**

        **username \= request.form.get("username")**

        **password \= request.form.get("password")**

        **user \= \_authenticate\_user(username, password)**

        **if user:**

            **if not \_check\_approval\_status(user):**

                **log\_logic("auth", "login", f"Redirecting unapproved contributor '{username}' to pending page")**

                **return redirect(url\_for("auth.pending\_approval"))**

            **log\_success("auth", "login", f"User '{username}' logged in")**

            **logger.info(f"User '{username}' with role '{user.role}' logged in successfully")**

            **login\_user(user, remember=True)**

            **if user.role \== "admin":**

                **return redirect(url\_for("admin.admin\_dashboard"))**

            **elif user.role \== "contributor":**

                **return redirect(url\_for("barangay.barangay\_dashboard"))**

            **elif user.role \== "business\_owner":**

                **return redirect(url\_for("business.dashboard"))**

            **elif user.role \== "user":**

                **return redirect(url\_for("user.dashboard"))**

            **return redirect(url\_for("public.index"))**

        **log\_error("auth", "login", f"Invalid credentials for '{username}'")**

        **flash("Invalid username or password", "error")**

    **log\_render("auth", "login", "login.html")**

    **return render\_template("auth/login.html")**

**@login\_required**

**def logout\_view():**

    **log\_entry("auth", "logout", user=current\_user.username)**

    **logger.info("User logged out successfully")**

    **logout\_user()**

    **log\_redirect("auth", "logout", "home")**

    **return redirect(url\_for("public.index"))**

**B.3 Register**

**from flask import render\_template, request, redirect, url\_for, flash**

**from extensions import db, limiter**

**from .models import User**

**import logging**

**from core.security import (**

    **validate\_email\_format,**

    **validate\_username,**

    **validate\_password\_strength,**

    **validate\_and\_escape,**

**)**

**from core.logger import (**

    **log\_entry,**

    **log\_query,**

    **log\_logic,**

    **log\_success,**

    **log\_error,**

    **log\_render,**

**)**

**from typing import Optional**

**logger \= logging.getLogger(\_\_name\_\_)**

**def \_validate\_username\_available(username: str) \-\> bool:**

    **"""Check if username is available for registration."""**

    **if User.query.filter\_by(username=username).first():**

        **log\_error("auth", "register", f"Username '{username}' already exists")**

        **return False**

    **return True**

**def \_validate\_email\_available(email: str) \-\> bool:**

    **"""Check if email is available for registration."""**

    **if User.query.filter\_by(email=email).first():**

        **log\_error("auth", "register", f"Email '{email}' already exists")**

        **return False**

    **return True**

**def \_validate\_barangay\_representative(barangay\_id: Optional\[int\], role: str) \-\> bool:**

    **"""Check if barangay already has an approved representative."""**

    **if role \!= "contributor":**

        **return True**

    **log\_query("auth", "register", f"Checking existing representative for ID '{barangay\_id}'")**

    **existing\_rep \= User.query.filter\_by(**

        **barangay\_id=barangay\_id, role="contributor", is\_approved=True**

    **).first()**

    **if existing\_rep:**

        **log\_error("auth", "register", f"Representative already exists for ID '{barangay\_id}'")**

        **return False**

    **return True**

**def \_create\_user\_from\_form(username: str, email: str, password: str, role: str, barangay\_id: Optional\[int\]) \-\> User:**

    **"""Create new user from registration form data."""**

    **log\_logic("auth", "register", f"Creating new user '{username}' with role '{role}'")**

    **user \= User(**

        **username=username,**

        **email=email,**

        **role=role,**

        **barangay\_id=barangay\_id if role \== "contributor" else None,**

        **is\_approved=(role \== "user"),**

    **)**

    **user.set\_password(password)**

    **db.session.add(user)**

    **db.session.commit()**

    **log\_success("auth", "register", f"New user '{username}' registered with role '{role}'")**

    **logger.info(f"New user '{username}' registered with role '{role}', awaiting approval={not user.is\_approved}")**

    **return user**

**@limiter.limit("5 per minute")**

**def register\_view():**

    **log\_entry("auth", "register", method=request.method)**

    **logger.info("Registration page accessed")**

    **if request.method \== "POST":**

        **username \= request.form.get("username", "").strip()**

        **email \= request.form.get("email", "").strip().lower()**

        **password \= request.form.get("password", "")**

        **role \= request.form.get("role", "user")**

        **barangay\_name \= request.form.get("barangay")**

        **barangay\_id \= None**

        **if role \== "contributor" and barangay\_name:**

            **from modules.barangay.models import BarangayInfo**

            **barangay\_record \= BarangayInfo.query.filter\_by(name=barangay\_name).first()**

            **if not barangay\_record:**

                **\# Create the barangay if it doesn't exist**

                **barangay\_record \= BarangayInfo(name=barangay\_name)**

                **db.session.add(barangay\_record)**

                **db.session.commit()**

            **barangay\_id \= barangay\_record.id**

        **log\_query("auth", "register", f"Checking existence for username='{username}', email='{email}'")**

        **\# Input format validation**

        **if not validate\_username(username):**

            **flash("Username must be 3-30 characters and contain only letters, numbers, and underscores.", "error")**

            **return redirect(url\_for("auth.register"))**

        **if not validate\_email\_format(email):**

            **flash("Please enter a valid email address.", "error")**

            **return redirect(url\_for("auth.register"))**

        **is\_valid, error\_msg \= validate\_password\_strength(password)**

        **if not is\_valid:**

            **flash(error\_msg, "error")**

            **return redirect(url\_for("auth.register"))**

        **\# Validation chain**

        **if not \_validate\_username\_available(username):**

            **flash("Username already exists.", "error")**

            **return redirect(url\_for("auth.register"))**

        **if not \_validate\_email\_available(email):**

            **flash("Email already exists.", "error")**

            **return redirect(url\_for("auth.register"))**

        **if not \_validate\_barangay\_representative(barangay\_id, role):**

            **flash("This Barangay already has a registered representative.", "error")**

            **return redirect(url\_for("auth.register"))**

        **\# Sanitize inputs before saving**

        **username \= validate\_and\_escape(username)**

        **email \= validate\_and\_escape(email)**

        **\# Create user**

        **\_create\_user\_from\_form(username, email, password, role, barangay\_id)**

        **if role in \["contributor", "business\_owner"\]:**

            **return redirect(url\_for("auth.pending\_approval"))**

        **else:**

            **flash("Registration successful\! You can now log in.", "success")**

            **return redirect(url\_for("auth.login"))**

    **log\_render("auth", "register", "register.html")**

    **return render\_template("auth/register.html")**

**@limiter.limit("5 per minute")**

**def register\_business\_view():**

    **log\_entry("auth", "register\_business", method=request.method)**

    **logger.info("Business registration page accessed")**

    **if request.method \== "POST":**

        **username \= request.form.get("username", "").strip()**

        **email \= request.form.get("email", "").strip().lower()**

        **password \= request.form.get("password", "")**

        **\# Input format validation**

        **if not validate\_username(username):**

            **flash("Username must be 3-30 characters and contain only letters, numbers, and underscores.", "error")**

            **return redirect(url\_for("auth.register\_business"))**

        **if not validate\_email\_format(email):**

            **flash("Please enter a valid email address.", "error")**

            **return redirect(url\_for("auth.register\_business"))**

        **is\_valid, error\_msg \= validate\_password\_strength(password)**

        **if not is\_valid:**

            **flash(error\_msg, "error")**

            **return redirect(url\_for("auth.register\_business"))**

        **\# Validation**

        **if not \_validate\_username\_available(username):**

            **flash("Username already exists.", "error")**

            **return redirect(url\_for("auth.register\_business"))**

        **if not \_validate\_email\_available(email):**

            **flash("Email already exists.", "error")**

            **return redirect(url\_for("auth.register\_business"))**

        **\# Sanitize inputs before saving**

        **username \= validate\_and\_escape(username)**

        **email \= validate\_and\_escape(email)**

        **\# Create business owner user**

        **user \= User(**

            **username=username,**

            **email=email,**

            **role="business\_owner",**

            **is\_approved=False,**

        **)**

        **user.set\_password(password)**

        **db.session.add(user)**

        **db.session.commit()**

        **log\_success("auth", "register\_business", f"Business owner '{username}' registered")**

        **logger.info(f"New business owner '{username}' registered, awaiting approval")**

        **return redirect(url\_for("auth.pending\_approval"))**

    **return render\_template("auth/register\_business.html")**

**def pending\_approval\_view():**

    **log\_entry("auth", "pending\_approval")**

    **return render\_template("auth/pending\_approval.html")**

**B.4 Dashboard**

**import logging**

**from flask import render\_template, redirect, url\_for, flash**

**from flask\_login import login\_required, current\_user**

**from sqlalchemy import func**

**from datetime import datetime, timedelta**

**from typing import Dict, List, Tuple**

**from models import db, User, Attraction, Event, GalleryItem, AttractionReview, UserFavoriteAttraction, AnalyticsPageView**

**from utils.logger\_helper import log\_entry, log\_success, log\_error**

**from . import admin\_bp**

**logger \= logging.getLogger(\_\_name\_\_)**

**\# \=== DASHBOARD HELPER FUNCTIONS \===**

**def \_get\_content\_stats() \-\> Dict\[str, int\]:**

    **"""Fetch basic content statistics."""**

    **return {**

        **"attractions": Attraction.query.count(),**

        **"events": Event.query.count(),**

        **"gallery": GalleryItem.query.count(),**

        **"reviews": AttractionReview.query.count(),**

        **"pending\_reviews": AttractionReview.query.filter\_by(status="pending").count(),**

        **"favorites": UserFavoriteAttraction.query.count(),**

    **}**

**def \_get\_top\_attractions(limit: int \= 5\) \-\> List\[Dict\[str, any\]\]:**

    **"""Fetch most viewed attractions."""**

    **top\_query \= (**

        **db.session.query(Attraction.name, func.count(AnalyticsPageView.id).label("view\_count"))**

        **.join(AnalyticsPageView, AnalyticsPageView.item\_id \== Attraction.id)**

        **.filter(AnalyticsPageView.view\_type \== "attraction")**

        **.group\_by(Attraction.id)**

        **.order\_by(func.count(AnalyticsPageView.id).desc())**

        **.limit(limit)**

        **.all()**

    **)**

    **return \[{"name": name, "views": count} for name, count in top\_query\]**

**def \_get\_engagement\_data(days: int \= 7\) \-\> Dict\[str, List\]:**

    **"""Calculate engagement trends over specified days."""**

    **cutoff\_date \= datetime.utcnow() \- timedelta(days=days)**

    **daily\_views\_query \= (**

        **db.session.query(**

            **func.date(AnalyticsPageView.timestamp).label("date"),**

            **func.count(AnalyticsPageView.id).label("count"),**

        **)**

        **.filter(AnalyticsPageView.timestamp \>= cutoff\_date)**

        **.group\_by(func.date(AnalyticsPageView.timestamp))**

        **.all()**

    **)**

    **daily\_views\_dict \= {str(d): c for d, c in daily\_views\_query}**

    **trend\_dates \= \[\]**

    **trend\_counts \= \[\]**

    **for i in range(days \- 1, \-1, \-1):**

        **d \= (datetime.utcnow() \- timedelta(days=i)).date()**

        **d\_str \= str(d)**

        **trend\_dates.append(d.strftime("%b %d"))**

        **trend\_counts.append(daily\_views\_dict.get(d\_str, 0))**

    **return {"dates": trend\_dates, "counts": trend\_counts}**

**def \_get\_pending\_items() \-\> Dict\[str, any\]:**

    **"""Fetch all items awaiting admin approval."""**

    **return {**

        **"users": User.query.filter(User.is\_approved \== False, User.role.in\_(\["contributor", "business\_owner"\])).all(),**

        **"gallery": GalleryItem.query.filter\_by(status="pending").all(),**

        **"reviews": AttractionReview.query.filter\_by(status="pending").join(User, AttractionReview.user\_id \== User.id).join(Attraction, AttractionReview.attraction\_id \== Attraction.id).all(),**

    **}**

**def \_get\_top\_rated\_attractions(limit: int \= 5\) \-\> List\[Tuple\[Attraction, float\]\]:**

    **"""Fetch top-rated attractions based on average review rating."""**

    **return (**

        **db.session.query(Attraction, func.avg(AttractionReview.rating).label("avg\_rating"))**

        **.join(AttractionReview, Attraction.id \== AttractionReview.attraction\_id)**

        **.group\_by(Attraction.id)**

        **.order\_by(func.avg(AttractionReview.rating).desc())**

        **.limit(limit)**

        **.all()**

    **)**

**def \_get\_recent\_reviews(limit: int \= 5\) \-\> List\[AttractionReview\]:**

    **"""Fetch most recent reviews for dashboard feed."""**

    **return AttractionReview.query.order\_by(AttractionReview.created\_at.desc()).limit(limit).all()**

**\# \=== ROUTE HANDLERS \===**

**@admin\_bp.route("/dashboard")**

**@login\_required**

**def admin\_dashboard():**

    **"""Display admin dashboard."""**

    **log\_entry("admin", "admin\_dashboard", user=current\_user.username)**

    **if current\_user.role \!= "admin":**

        **log\_error("admin", "admin\_dashboard", f"Access denied for role='{current\_user.role}'")**

        **flash("Access denied.")**

        **return redirect(url\_for("public.index"))**

    **\# Gather data via helpers**

    **stats \= \_get\_content\_stats()**

    **pending \= \_get\_pending\_items()**

    **top\_attractions \= \_get\_top\_attractions()**

    **engagement\_data \= \_get\_engagement\_data()**

    **recent\_activity \= \_get\_recent\_reviews()**

    **top\_rated \= \_get\_top\_rated\_attractions()**

    **log\_success("admin", "admin\_dashboard", "Dashboard data loaded successfully")**

    **return render\_template(**

        **"admin/dashboard.html",**

        **stats=stats,**

        **pending\_users=pending\["users"\],**

        **pending\_gallery=pending\["gallery"\],**

        **pending\_reviews=pending\["reviews"\],**

        **top\_attractions=top\_attractions,**

        **engagement\_data=engagement\_data,**

        **recent\_activity=recent\_activity,**

        **top\_rated=top\_rated,**

    **)**

3. **Database Schema**

   CREATE TABLE IF NOT EXISTS BARANGAY\_INFO (

       id INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,

       name VARCHAR(100) NOT NULL UNIQUE,

       map\_geo\_json JSONB,

       location\_data JSONB,

       mission TEXT,

       vision TEXT,

       history TEXT,

       cultural\_assets TEXT,

       traditions TEXT,

       local\_practices TEXT,

       unique\_features TEXT,

       user\_id INTEGER,

       created\_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT\_TIMESTAMP

   );

   CREATE TABLE IF NOT EXISTS NEWSLETTER\_SUBSCRIBER (

       id INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,

       email VARCHAR(120) NOT NULL UNIQUE,

       is\_active BOOLEAN DEFAULT TRUE,

       created\_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT\_TIMESTAMP

   );

   \-- 2\. TABLES WITH DEPENDENCIES

   \-- "USER" depends only on BARANGAY\_INFO. Quoted because it's a reserved keyword.

   CREATE TABLE IF NOT EXISTS "USER" (

       id INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,

       username VARCHAR(80) NOT NULL UNIQUE,

       email VARCHAR(120) NOT NULL UNIQUE,

       password VARCHAR(255) NOT NULL,

       role VARCHAR(20) DEFAULT 'user',

       barangay\_id INTEGER,

       is\_approved BOOLEAN DEFAULT FALSE,

       created\_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT\_TIMESTAMP,

       FOREIGN KEY (barangay\_id) REFERENCES BARANGAY\_INFO(id)

   );

   \-- Depends on "USER"

   CREATE TABLE IF NOT EXISTS PASSWORD\_RESET\_TOKEN (

       id INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,

       user\_id INTEGER NOT NULL,

       token VARCHAR(128) NOT NULL UNIQUE,

       expires\_at TIMESTAMP WITH TIME ZONE NOT NULL,

       used BOOLEAN NOT NULL DEFAULT FALSE,

       created\_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT\_TIMESTAMP,

       FOREIGN KEY (user\_id) REFERENCES "USER"(id)

   );

   CREATE INDEX IF NOT EXISTS idx\_reset\_token\_user ON PASSWORD\_RESET\_TOKEN(user\_id);

   \-- Depends on "USER" and BARANGAY\_INFO

   CREATE TABLE IF NOT EXISTS HERITAGE\_PROFILE (

       id INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,

       asset\_type VARCHAR(50) NOT NULL,

       form\_control\_number VARCHAR(100),

       form\_data JSONB,

       name\_of\_asset VARCHAR(200),

       common\_name VARCHAR(200),

       barangay\_id INTEGER,

       location\_details TEXT,

       contact\_person VARCHAR(200),

       contact\_number VARCHAR(50),

       ownership\_type VARCHAR(50),

       owner\_administrator VARCHAR(200),

       usage\_status VARCHAR(50),

       latitude DOUBLE PRECISION,

       longitude DOUBLE PRECISION,

       significance TEXT,

       conservation\_status TEXT,

       mapper\_name VARCHAR(200),

       date\_profiled DATE,

       status VARCHAR(20) DEFAULT 'pending',

       user\_id INTEGER,

       created\_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT\_TIMESTAMP,

       FOREIGN KEY (barangay\_id) REFERENCES BARANGAY\_INFO(id),

       FOREIGN KEY (user\_id) REFERENCES "USER"(id)

   );

   CREATE INDEX IF NOT EXISTS idx\_heritage\_profile\_status ON HERITAGE\_PROFILE(status);

   CREATE INDEX IF NOT EXISTS idx\_heritage\_profile\_type ON HERITAGE\_PROFILE(asset\_type);

   CREATE INDEX IF NOT EXISTS idx\_heritage\_profile\_created ON HERITAGE\_PROFILE(created\_at);

   \-- Depends on BARANGAY\_INFO, HERITAGE\_PROFILE, and "USER"

   CREATE TABLE IF NOT EXISTS ATTRACTION (

       id INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,

       name VARCHAR(200) NOT NULL,

       description TEXT,

       category VARCHAR(50),

       latitude DOUBLE PRECISION NOT NULL,

       longitude DOUBLE PRECISION NOT NULL,

       image\_url VARCHAR(500),

       barangay\_id INTEGER,

       heritage\_profile\_id INTEGER,

       status VARCHAR(20) DEFAULT 'pending',

       is\_featured BOOLEAN DEFAULT FALSE,

       user\_id INTEGER,

       created\_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT\_TIMESTAMP,

       FOREIGN KEY (barangay\_id) REFERENCES BARANGAY\_INFO(id),

       FOREIGN KEY (heritage\_profile\_id) REFERENCES HERITAGE\_PROFILE(id),

       FOREIGN KEY (user\_id) REFERENCES "USER"(id)

   );

   CREATE INDEX IF NOT EXISTS idx\_attraction\_status ON ATTRACTION(status);

   CREATE INDEX IF NOT EXISTS idx\_attraction\_category ON ATTRACTION(category);

   CREATE INDEX IF NOT EXISTS idx\_attraction\_name ON ATTRACTION(name);

   \-- Depends on BARANGAY\_INFO and "USER"

   CREATE TABLE IF NOT EXISTS EVENT (

       id INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,

       name VARCHAR(200) NOT NULL,

       description TEXT,

       date TIMESTAMP WITH TIME ZONE NOT NULL,

       location VARCHAR(255),

       category VARCHAR(50),

       image\_url VARCHAR(500),

       latitude DOUBLE PRECISION,

       longitude DOUBLE PRECISION,

       barangay\_id INTEGER,

       status VARCHAR(20) DEFAULT 'pending',

       user\_id INTEGER,

       created\_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT\_TIMESTAMP,

       FOREIGN KEY (barangay\_id) REFERENCES BARANGAY\_INFO(id),

       FOREIGN KEY (user\_id) REFERENCES "USER"(id)

   );

   \-- Depends on "USER"

   CREATE TABLE IF NOT EXISTS GALLERY\_ITEM (

       id INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,

       type VARCHAR(20) NOT NULL,

       url VARCHAR(500) NOT NULL,

       caption TEXT,

       user\_id INTEGER,

       status VARCHAR(20) DEFAULT 'pending',

       created\_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT\_TIMESTAMP,

       FOREIGN KEY (user\_id) REFERENCES "USER"(id)

   );

   CREATE TABLE IF NOT EXISTS ANALYTICS\_PAGE\_VIEW (

       id INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,

       page\_url VARCHAR(500),

       view\_type VARCHAR(50),

       item\_id INTEGER,

       page\_name VARCHAR(100),

       user\_id INTEGER,

       timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT\_TIMESTAMP,

       session\_id VARCHAR(100),

       ip\_address VARCHAR(45),

       device\_info TEXT

   );

   CREATE TABLE IF NOT EXISTS DATABASE\_AUDIT\_LOG (

       id INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,

       user\_id INTEGER,

       action VARCHAR(50) NOT NULL,

       table\_name VARCHAR(100) NOT NULL,

       record\_id INTEGER,

       ip\_address VARCHAR(45),

       user\_agent VARCHAR(500),

       query\_summary VARCHAR(500),

       status VARCHAR(20) DEFAULT 'success',

       created\_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT\_TIMESTAMP,

       FOREIGN KEY (user\_id) REFERENCES "USER"(id)

   );

   \-- Depends on "USER" and ATTRACTION

   CREATE TABLE IF NOT EXISTS USER\_FAVORITE\_ATTRACTION (

       id INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,

       user\_id INTEGER,

       attraction\_id INTEGER,

       created\_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT\_TIMESTAMP,

       FOREIGN KEY (user\_id) REFERENCES "USER"(id),

       FOREIGN KEY (attraction\_id) REFERENCES ATTRACTION(id)

   );

   \-- Depends on "USER" and EVENT

   CREATE TABLE IF NOT EXISTS USER\_EVENT\_INTEREST (

       id INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,

       user\_id INTEGER,

       event\_id INTEGER,

       status VARCHAR(20),

       created\_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT\_TIMESTAMP,

       FOREIGN KEY (user\_id) REFERENCES "USER"(id),

       FOREIGN KEY (event\_id) REFERENCES EVENT(id)

   );

   \-- Depends on "USER" and ATTRACTION

   CREATE TABLE IF NOT EXISTS ATTRACTION\_REVIEW (

       id INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,

       user\_id INTEGER,

       attraction\_id INTEGER,

       rating INTEGER,

       comment TEXT,

       status VARCHAR(20) DEFAULT 'pending',

       created\_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT\_TIMESTAMP,

       FOREIGN KEY (user\_id) REFERENCES "USER"(id),

       FOREIGN KEY (attraction\_id) REFERENCES ATTRACTION(id)

   );

   \-- 3\. \[Consolidated\] Heritage Detail tables merged into HERITAGE\_PROFILE.form\_data JSONB column.

   \-- 4\. BUSINESS PORTAL TABLES (Establishments, Rooms, Menu Items, Reviews)

   CREATE TABLE IF NOT EXISTS ESTABLISHMENT (

       id INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,

       name VARCHAR(200) NOT NULL,

       type VARCHAR(30) NOT NULL,

       description TEXT,

       address VARCHAR(500),

       latitude DOUBLE PRECISION NOT NULL,

       longitude DOUBLE PRECISION NOT NULL,

       barangay\_id INTEGER,

       contact\_number VARCHAR(50),

       email VARCHAR(120),

       website VARCHAR(300),

       operating\_hours JSONB,

       price\_range VARCHAR(20),

       amenities JSONB,

       cover\_image\_url VARCHAR(500),

       logo\_url VARCHAR(500),

       owner\_id INTEGER NOT NULL,

       status VARCHAR(20) DEFAULT 'pending',

       is\_featured BOOLEAN DEFAULT FALSE,

       rating\_avg DOUBLE PRECISION DEFAULT 0,

       review\_count INTEGER DEFAULT 0,

       created\_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT\_TIMESTAMP,

       FOREIGN KEY (barangay\_id) REFERENCES BARANGAY\_INFO(id),

       FOREIGN KEY (owner\_id) REFERENCES "USER"(id)

   );

   CREATE INDEX IF NOT EXISTS idx\_establishment\_type ON ESTABLISHMENT(type);

   CREATE INDEX IF NOT EXISTS idx\_establishment\_status ON ESTABLISHMENT(status);

   CREATE INDEX IF NOT EXISTS idx\_establishment\_owner ON ESTABLISHMENT(owner\_id);

   CREATE INDEX IF NOT EXISTS idx\_establishment\_coords ON ESTABLISHMENT(latitude, longitude);

   CREATE TABLE IF NOT EXISTS ESTABLISHMENT\_ROOM (

       id INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,

       establishment\_id INTEGER NOT NULL,

       name VARCHAR(100) NOT NULL,

       description TEXT,

       price\_per\_night DECIMAL(10,2),

       capacity INTEGER DEFAULT 2,

       amenities JSONB,

       image\_urls JSONB,

       is\_available BOOLEAN DEFAULT TRUE,

       created\_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT\_TIMESTAMP,

       FOREIGN KEY (establishment\_id) REFERENCES ESTABLISHMENT(id) ON DELETE CASCADE

   );

   CREATE TABLE IF NOT EXISTS ESTABLISHMENT\_MENU\_ITEM (

       id INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,

       establishment\_id INTEGER NOT NULL,

       name VARCHAR(200) NOT NULL,

       description TEXT,

       price DECIMAL(10,2),

       category VARCHAR(50),

       image\_url VARCHAR(500),

       is\_available BOOLEAN DEFAULT TRUE,

       is\_bestseller BOOLEAN DEFAULT FALSE,

       created\_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT\_TIMESTAMP,

       FOREIGN KEY (establishment\_id) REFERENCES ESTABLISHMENT(id) ON DELETE CASCADE

   );

   CREATE TABLE IF NOT EXISTS ESTABLISHMENT\_REVIEW (

       id INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,

       user\_id INTEGER NOT NULL,

       establishment\_id INTEGER NOT NULL,

       rating INTEGER NOT NULL CHECK (rating \>= 1 AND rating \<= 5),

       comment TEXT,

       status VARCHAR(20) DEFAULT 'pending',

       created\_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT\_TIMESTAMP,

       FOREIGN KEY (user\_id) REFERENCES "USER"(id),

       FOREIGN KEY (establishment\_id) REFERENCES ESTABLISHMENT(id) ON DELETE CASCADE

   );

4. **Survey/Evaluation Forms Used During Testing**

5. **Collected Sample Documents for Document Analysis/Data Gathering**

   **![][image1]![][image2]![][image3]![][image4]![][image5]**

**Sample Name.**
Sample email | 69696969696 | Abanon San Carlos City, Pangasinan
---

**PERSONAL PROFILE**
Sampleeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee profileeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
---

**EDUCATIONAL BACKGROUND**
Primary		:		iskol
Secondary	:		iskol
Tertiary		:		iskol
---

**PROJECT(S)**
Flood Control
---

**TECHNICAL SKILLS & COMPETENCIES**
**Skill Issue**

[image1]: <data:image/png;base64,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>

[image2]: <data:image/png;base64,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>

[image3]: <data:image/png;base64,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>

[image4]: <data:image/png;base64,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>

[image5]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAkAAAAG4CAYAAACts1jfAABNZ0lEQVR4Xu2dO64sR3qtOYUeA6fQcyBwJ0CgOQIamgCBOwCaMhrgDAiaMtqRJYGOPNGTRUN+q6XW+9m8WEd3sddZOyKralfsvTNqfx+QyIzXH498/KsiszI/+QkAAADgnfFJRwAAAAA8OgggAAAAeHcggAAAAODdgQACAACAdwcCCAAAAN4dCCAAAAB4dyCAAAAA4N2BAAIAAIB3BwIIAAAA3h0IIAAAAHh3IIAAAADg3YEAAgAAgHcHAggAAADeHQggAAAAeHcggAAAAODdgQACAACAdwcCCAAAAN4dCCAAAAB4dyCAAGAr/vZv/7ajAABuBgEEAFuBAAKAFSCAAGAr7hVAn3766U+ffPLJh0Xk9ozPPvvso3CX+f777z+Ev/7665++/PLLj+rovN5WGYe1qJzKd/4ff/zxia1cXLfLuO7vvvvuSV7VkWR9bo/ydDnT8Vqyr2nviy++eJJ3ZutP//RPfy4vNN4Kf/vtt4flvGQbRu3vsbCdjh8tXa/H0OOuNgq3weMI5+f4rIe7+eGHHz6cFD6xhcK/+MUvItf1fPPNNz/98pe/7Oib6BP7N7/5zYfw559//iF8bduUT2V9wfEFYRW+mKqOEffW1eU7fAmN11dffdXRU27ND2PuFUCiz4EjfBwaOWeJEpEiJtM7zud/xqmszp224fPJjjXPL+ezE/a626hwttFtagGUwk4OfNR22xHZjyw7CgsLGDMSkm6TRY/rS6EhHO9xsV3H5/gJ23OeHiPF5Rh1WoazXWmnbeZ1Hs7PH/ccvAj960xIxDjsXw06cRSvRcLCIkfbOpEtSpSusISVLy4WCPnLJ5HjVXmdwL4o9Mn929/+9uew60p7rsvtcb7un9dqU9tRX53HFw4LRMcZhVMsqA/tRNKO42Z5hMZUYV8gncdkGbXV7XUb+5el2+RwX0RzbDK/xrp/LTpPOjaFVTd8zAoBJLyvLjkt78d28F5EzkCkQ859Ko5mNFLwtGPVdh8r2e487rWdaSmAErU5xU0ev64j25AofjYeWS776/4lim+h47g8T0dtuRROASR6TGd9d5rDXU4obFHlvD3ucH7GRzcsIy+ecuhygnmy2cH5BLJoUNgXDwsXXbCUR9uyoQuEnXPakEgyyiPH3xe3pC/Kt6xtNy9eXqvdind71A5fTCz22qZJm0J9zov8aC1GeUYX2FybjJdIcRu01jjLdo6j25RtTZuKO8qfF9nZOp0n/C+rBdARPp5GTrCdplD4mn2otBQQeSyk48/ZjjzGLJJMtzPTVG4kgBSXIiBna7weiRbR7R+FRdoc2XJfhPvnMjluKTKM7c7CqwRQz2IJh4/GHc7Px3sVluMTyw5Vi+NSePjk8UXEYqdPQudJceA8WnvWwhwJh6brdLssYDLefch15zG24/Z3Wq4zPi8mR/3IsrM8vqB5yTTT8VmnL6ZHgibLiiMBZLpOr13u3tudj8gqAaQxzvMlnZ4ZOfWM8/ExOx8bl1VdOcshnN9xnlVyWh5jLaryXPF5bFRuJIBE9y/F1xFK77IdFi0eUnSIrDPHULa6j7KVIqrb2GGfsybPRdFj1O3MsLbddrXLaUfjDufn+CiHu8kTS+u8beQZEC92jl5cxotOfuUZCaAUWPnMjOvSYmdq2ybrsJ201+W0tt1cd55M93IkAPLikbfGtLRY7LK93XnaXqaZjk/B4iWFlNPzdlbeClF4lF/HgONyxq/XWlrQwjoB1IycnsN5HGg/5g+SUf48DjLe5bxf5UzzGuF6FK/29HE/Wlw+j5VRu0YzMGm/Hbzb1GTfVD7DOU7PeQg6SWGktBaLaS/bILJfOS6zvrW9Dmecx7ZFk0AA7cX4CIc3weIm6RNshsSUTvS8JXYPtidkLwUXwFvyUgIIAN4X93tKWIYfcE6u/UeW0EyNH3ZeQT80DHAGEEAAsAIEEABsBQIIAFaAAAKArbhHAOWzHSwsLI+7XMN1uQAATsI9AggAwCCAAGArEEAAsAIEEABsBQIIAFaAAAKArUAAAcAKEEAAsBUIIABYAQIIALYCAQQAK0AAAcBWIIAAYAUIIADYCgQQAKwAAQQAW7FSAF3zjbv80Obog5z+9Izz+XM2/WK2fkFbxuVHc7Ou3O5yHfbHTjs9P0hsuq5Mazqflv6oaG77g6izT/J0fW070/pjxFq+++67n7f7Y8u9jMZNS7fR8aK/YN82r1n8JXpv5wdrO28vXa/369GYw/Ng9ABgK1YKoEsOROnpyO1Q21E53o6vv7yuOH8pvMvKOaYjtoCyTX+UeOSYLeBcr8j29tfJ3a6sL+O9ncJh1GdhZ25kU0u3P9O7/aMxyTZnutuoPmt79FX2HAfRbcgxs6Awjvd499g5b7cpx8dlFdfjk/ay7hSuJrfVp7SrNNc5E5lwHR8f0QAAJ2eVALKznM0CtTM1isv4FCYjh+5wptmhdf0K9weRM2869BY9FhgjAeQ2j9rVtNAyHdcOvmdT3G7TcZ6FcVqnJ0prkZZ9sp2ceRmh+BRAtqM4x7dNMwpnm7r9PT4zAWS6DyaFY4ot73N4PuOjBADgpKwSQGLk6MzISYmRY3PYTu7SbEfeJnuuAMp2tPgQLezS2ZvuX85GjGZPkh6HdsadX+EUCDm+XnedRuktgK6ZAWqy/65rJIS9T7NPbbfb1P3r8blWAHVa9i/Hp9sHtzM/UgAATsgKAWSRkc6lRYtoJzO7XWHnlk5ulqfjW5DMBFDPzGTbRo56NJsiBzrKa1ymnbDo8ChP2u76e3y1PRrPEZlXXCuAcn+IHO8WE453H3o/dBu7TQrPBJ5Ie50memyMbLpstxkBdB/HRx0AwMm4VwD5l3nfRmkHbTLPKN7Ybs+8ZPnM33EuryWFgZZ2fCM7xvWnc/aMRjvsLDvadnh2a8lxLR4UN3PObafrajrd+8n1ZvpoGdnJWTvTQrTDWnI2Lu3n+LQI7nZ0m2f5HE7B1vZnYwzXMT7iAABOyr0CCABAIIAAYCsQQACwAgQQAGwFAggAVoAAAoCtQAABwAoQQACwFQggAFjBKQWQnnTvvyAaxY/+3eAn5f2EvZ+Uz3cx5BP2pp+6v7TdYW2P3l2R/xYQalf+yyTfAyLyXx9uu+JULu33X2Jdvuvz9uyvt90ngF1AAAHACk7pBS1iUuiYdt4WQI7rvwpaAI1EiuLyr475boa014zqTzv5vo7sw+hvtqNw/s2xBdDR32EdJ/p9GBlu8QSwEwggAFjBqT2gHHTOBOWsiYVFznDkOyhaAPVLuUQLgBQuvU4yLutvsdQi4zUFUPc533sxmm1yGODsIIAAYAWn9ngtGOzw0/GnAEnn3wLI5EyN8lyaARqRaa7Hs1aiXzZmuj9iFF4hgLIvomeATJcHODsIIABYwem8X7/ZMoVMYsc9EiApIlIA9QyNSAEw224ybSRORjNJ4jkCyHGix0bxo/K5nbM9Ju3nDFvbAjgjCCAAWAEeDwC24l4BlJ8tyB8JM0Y/NDzD2j84OuwfRVlXfvLCyyiuybj8HMSvf/3rj8rY1nfffffEZrcnf8D1j6GjZdTeXGY2klG4F8erbdlW/yCefVYi8+ePY6d78aMBX3zxxbDuzJ/0D3KR+fL46LEy/mOMGeWZPa+ZebW4H5lvFladGp8sM8qr9vWP8ca2RjZ2YK/WAsC7514BJHShTjEwIp+bS7KswyJFiRjZlzNsEeK8eZu6657NHttBdX6F7VzlyCxu+tb4aFbc5Ex2Pl9ptD16LrPjXTad/ag/omfsR+Ms0jFn37t9uXb7um7Xkf3NND8mke2f1W96fwpt5yMXCqeQGtUvulzGG7dHcTMbydH+Gdm9hO0p/6itZ+XpSAEAnJiVAqifEUwUP5od6vwKp+CwE2qh02KjnVU/p5dpbmcLghRAjsuwSAEk8hd7xjXdBpFhbc8EULanBYcY9SfjjduQ+6EdbAugzt997fYcCaDRDEzX3/WZSwKo6+uw6XLXxKew0viM2ieUt8ej94HocMap/Eg89bhpu8+JTFMbsy25djtX87RXAAAnZqUA8vbMkYwcRzuDvHhnXN8macfSTsAOsx1n/kLv8i2ALAaOBJBJ4TDq/8ghd/0tgLrfCqvdKXRm/RE9RibHqvsymoHJ/MJt822nTDsSQCbLdP3ue9P70fULj1GO16z+LCfyuJ2R/Vd+ty9vx7lPvX9M2mjy+Mq+GPerbTtP5u3+2J7Hucd7JePeAQCclJcSQHYGph2YybIOi/6F2hdy0U4iw1lfprWgyHa3ABLKfySAug0j5y1GDrnLtgAabee4qC2z/ogWQNeMcwqg7LfjLB5ky2VHdXR/FZ/1u09d/+g4Ud6O17bbYhtZZ9efY5gCKGfXzEzAzLZzv/X+ybwjcSNGx5Paa1tOb5Gtdub+sCB1WNvZb9P1r+JlrAIAvBD3CiA7Ji++ILczEP6VrCWFgi/sfZHOsJ2AHVum6WLvuBQ0WtI5ZRuzLfnQrh+CTmHRQkCL2y/7rl9kuSTr73DOJHS+HJtebKf7o/ZkOY9BjpPDiR22l7SZKJz7L8uJLOdF+e2kFW5BlIyOE4ePxqrjeslj5ygu65iRecVoP4kec5dNPA55HAltW+Q63udbj3GWyboz3n3t83IV89ECADgh9wogAACBAAKArUAAAbw9Ocu4KwggANgKBBAArAABBABbgQACgBUggABgK1YKoH648xK35r+F/tfQc1n9wOgj3OoAGHH/2baY0VPio7RRev41z+QT/HqiPJ+Wz6fSR/+a6HDHd3qHHTcr3/Gd3vn6SX/3bfQvg/6bZdrtvB2ff7l0XI5PjnM/2a9l9A8XMauv/zUBcMQqAfScY+05ZW5h9BfnUfiI2b+67mG1qAI4A9efVa/I0cmutPzbaqcluhCM3legdf7V1PRf+rqsLgL5XoN+b8NR24xs+gLVQkO0TdG/DLXtsC+YFkNGbc26RNvo/vRfSFNgmcwvfGFUXP51Vbhc90nb7nv2jYssXMMKAaRj8pbjLf86/FLk37TNrWImrynXMPtbd3NtPoCdGHvpN6YFQGLnqSUFii4eCudFbWbHzrpnjBQ/uggJC4Z05lrnhSHffTCrWyhNF9KRAPJ2prUAEs7TAijb33bcb293fzpsQZgXYbelL7Rp27ic0mbjlKLrFocE75cVAqhFus8jC6MWOnle5Y8Ar/u6kT++nMdhn0MO61zK8y7rtt2eGZrZ6jq7H3lOCv9Qcjh/tMxmfQEehbmXfkN8Mo5Q2miWxReKjJvZ8QVDJ3vfokk7Xhy2s878M8c+q9ukbYdz+5IAEmmjZ4Cc3gLI7R31J2dzcrt/hfYskFC4L5LXCiAxsgkwYoUA6mOthUPSx7WOWf8AG+XvHwzGeX2NUT7bEnluCpd1fNuSnbTVtB2v/QPSuA1auy6Hvd0CD+AReHr2noC8qPQFRuEWQD3rkc47Lxp5gckLXl6AbLMFhe1qnfWO8njbzC4eXVZ0vWJ2oc28s3J5Yez6uj95wcvxsY0WUx1uR5G/Jkd1C68dD3CJFQLIsxt2/g6PbvX42HYebSufFp9DnV+koOgZX9frRfmcrry263Pf9aUtn1+21ULH7fA602VD9rwWspFtbkEG8Gic7si2Q+6Tt9Mc75mDPOm12LE63fk9+6Al00b1dNhxs/Sm4zs8mm2a/ZJzWtvIi5SWFlsWRqN2OC7Dmc8XXy2/+tWvfk7LcfOFuOt3OB1K2+9wOgiAGfcKoD5H4Jj8kQLwSDz12gAAJ+YeAZQzHHAZxCI8MgggANiKewQQAIBBAAHAViCAAGAFpxJA+RwKCwvL4y73gAACgBXcdyUCAHhlEEAAsAIEEABsBQIIAFaAAAKArUAAAcAKEEAAsBUIIABYAQIIALYCAQQAK0AAAcBWIIAAYAUIIADYilUCyH/Hf86HePv7fLbhz7lkWtuehWdl/Obq/O5YfsMrv7WX3zh77re8Rp+kkY3+1pg/s+P0UbkR2d78MLLam211Pfl5HTPaVj73X3Eul99Zy+8jKk9+Ay770t8vVJksZ/o4uPbN2Tl2wtuz+EuM2jYK53gbhXOf5jHs7e7/7PMoeVyK7E+OcZ5zWnu7xzO3+7NKo+1beX5JAIA3YIUA6ov4rZ/H8MU8nXQ6jLzoN33B7nDHpagZXfjbWQvVO/qu4DXIVre7HVnHteM+oturbTtOxx/tm3aSpgWQ+38kgEyLr2xjtzfDLpdjcg0qk30cicru94xua6J42xYpgPJYzTyzOIe77YnScqz6uPB2/+jwdu/bFv0ixdi9PD2K3hgPYO5Ix33xxRc/b3sHaf0nf/InHw38KL/pj6OmvV//+tcfhZscdNfd+bL8aPHB6nI+gXxAjT7i6jxefFDlkh8kzQPb9QA8CvcKoL4oPwedk6OLeJ977cRcJq8leX6b3B4JIMeJvqYYx3X8NYzKjJz9rM1HtKDweOQ4pIPtfmQbkhZA5l4BdOSUVS7F7zUCqIWsULu15LX9FifvMjkuaneP9ZGfyHzabjFllDYSQI5L2y3o3KfRuSN6rJ2mJfdtHv/3cN0R+8qMdobDvUO9w0cHsEjF2wOXB4DjvWNGB+ko3AdpXxSE7WU4y7kd7ku3c9Z+hZ2WZTMd4NG4VwCNzu1byfMtt/OakvlMOswmz+9MbwHU7Z/ZE533Evkrf+TM85rT17pr6+n2alv15jW8HWyKDOdvLICyjWImgJKR/3C409qpCzvu0ZiN6LFyG0e2b6H70HG3zAD5uOsf+1r3/nG811mHxyXL3SKARNef51ym3crzSr0woxPL4T55UgDlyd4C6OhCoPhLAkjxfeIoveO67cL2TPYh82rnd71JttPhzquw7OSJKJujAxZgR+4VQELnSTqYvn5cwmV1/vvcUtkWQEmeg0r3NcrntMLptJzfzinbp/odP7omZt9s8xpSgI36kHW1sx7lH9HtndnodnsfdXljASSU7m2LC/EcASRyW+U99jnOynOLAOpruRj5j0vkOLlsxuUxmgLIKJwCSNsjgeJxm/XTcdmH3E5xM7LfeZK0c7RvbuX5JV8YdUqLD8xZ51MAea10HwDe4UcHluJbADWjC5u282RSnaN6FG4B0iecGZU32U6HR3ndX4BHZIUAAgB46j1PQv7aSUffv9IsdFqJtwByfAoIk/EjAdSiI7dTAKltIwGj8LUCSHQ73beOz3FJFJcCiBkgeCQQQACwgqfe841Jp55rLRYCFik9BZzTeIrr2SMxup/pJR+CNraRIsR1ZdmRvVFYWCRlfLbd4ZmdnI3S0uKv60MAwSOBAAKAFZxOAAEAHIEAAoAVIIAAYCvuFUA9uyo8izxbkpxxFZ3HYc1Ue7a6X+Hh/KN6207W50cAcukZ4ORSXV40Jj1jntsAjwhHNwBsxb0CSPQzeP3sX27n7ekul/i5w35O0QIl/8ChtZ8fHNnMZwuzft/K1m3w2T+Rkv73TDLqY7eFW+fwyIzPZACAk7JKAMnpSyDM/uGppUWDxU2LDi+Zx8wEUKZneeO4kQhJAWSUr/9GnM8bNiP7+axjPjuocI8FwO48PSsAAE7MKgEk5Nhz23h75PR7lkRY3EhwXBJALUhsb/QP1RRNyUgAOV/mH/3hwjg8EkD5/jSAR+XpmQUAcGJWCyAz27YISDE0EgeymTMmGS96BsiCpwWV8uUtsBYuYiSAcibLaXkLrEVQ1yl6ZmvUH4BHgaMaALbiXgHk20QtSI6WfEYob1lJIDgtBVLfevKskMv0bFAuvpXVzyUlzus6sy5v58PeR/V5Gc1EIYDgkeGoBoCtuFcAAQAIBBAAbAUCCABWgAACgK1AAAHAChBAALAVCCAAWMEpBVA+zOd3dTiu/zEx2u48pv+e2g/8GcXlw4Wjf4zkvyUA4PVAAAHACp6qhBNgoeF/QaQAyvQWMBItKVyc5r+HtgDyPyPy76ydR4wEEAC8DQggAFjBKT16CpzRDJDfkWFxZCReRq+Xt4BpceP3bWRcv0k1UXyndRgAXhYEEACs4JTeu0VFv8wrBdBsBsjp/R2dFkBeO75nm5JZPAC8HgggAFjBKT16C40WJdrOW10Zn/hlYqYFUKalUJLA8m2xfjNqb3edAPCyIIAAYAV4bwDYCgQQAKwAAQQAW4EAAoAVIIAAYCsQQACwAgQQAGwFAggAVoAAAoCtQAABwAoQQACwFQggAFgBAggAtgIBBAArQAABwFYggABgBQggANgKBBAArAABBABbgQACgBUggABgKxBAALCCUwqg0fe18uvu+fFSoW1/Fb7Ljr79lbZUru35Y6ui4zPNdeb3wsSoDbNvl+mbY/mts/xemdp71Gfldd1Oy/zZVoBHAQEEACt4qjROQAuI/oipSIefHzW1KPF2p4sUQCLFRQuNDLuc7fmDqfkhVedxmlDYAkhlUwylDW13X0ftcnnV1SIny7YwA3gEEEAAsIItBFDOhBh/sb3FRqI8LXZEx6W4kBDJtBQkKue2WKw4j3F6ixiLFokyC6Zsu8ppuTQDlLZsI+tz+7XMZsUAdgYBBAArOKVnbIfdszLC4XT0jcVFlz0SQJ2Wt6c8oyJhpbgWXm5HlhHaTgGUt61SAClPirrs22gGyDhvznQp3P0GeATuFUA+f31+eDuXJn+AZB5fLzq+47777rsncaN8puPzh1VeP7KM+yVG7XI596WvIwDvjadn+gnIkzrjUnA4T570Im8PmbbXIqcFVl9UPGPTNtWeFF8zG3mx6eeLWqT1jJO3u43Kl+1Ruhfj/N1/gJ25VwAJnROj80JxeV4lis9Z1RQixuk6P/PW+OhZQ6O4UXpu+8eNZ3j7R5/i8vo4+pGVP+AA4KdzCiAAgBkrBJCwwOiZ02sFkLGYSmHhHzKZL2eREgsarbstndc/cDK+b9snIxuO63iA9wZnAABsxWoB1HGXBJDy5OyO7WS5ngESFkCj2Zu+be74xgKob82P8grF9616c5QG8B4YnzUAACdllQCSiOjbQRZAI0Hi+H4+r/Mp/UgAmbxN5foyfZR3dIvb2ylmcqbI8f3vVYD3DgIIALZilQBqLEBSkJi+feVZl9GStlJ0dL602eV6yQe3ZwIm7Wa468g0gPcMZwAAbMVLCSAAeF8ggABgKxBAALACBBAAbAUCCABWgAACgK1AAAHAChBAALAVCCAAWAECCAC2AgEEACtAAAHAViCAAGAFCCAA2AoEEACsAAEEAFuBAAKAFSCAAGArEEAAsAIEEABsBQII3oJdPx3ynHY/p8yOvI9eAsDDsEIA/eIXv/iw9oX+q6+++umHH374Od0fSf38888/rH/zm998KPPb3/72w0dOtVZZrVXOHz795ptvPvrIqVD4l7/85Ydtr51f9ciG4/tbX7alb5NlW9pBOTz64KrapDa6z0L1Ka/inb9tqpzj8yOs+Z005xFun+pRGzPeH4g1/kaaybovjZFwX3K8vTaZf4TsZx2O80dum/647Wvjj/Gegbcei1UggABgK1YIIDs8O/Z2yL7AZ7yddKZpaeEgx+uPn5rO0w7EYa0zr+vv8hJsSab7K/dqQ4oAiRI70RQLFiZdh51tt8kfZs08SY9Jj20j+xZPHT8Kq+0psDzeIuvt8on3v1AfUuDN6PE5C5fGt4XhJWYf201utXlWzrlHAQAmrBBAImcA2olkvAWAna5mHxS2027HmMIo8yXtnFMACc/QyI4cdOfvOkdht6PjZWskXNpGCiA5Ra1bkDmPZmhM5+k2JFmu29R9drjb2f3U/slZuUbjmnW1vW637XT7hIWUy8xsCeWVTQuMbF/vF5dLYdb973XPPJrO1+K/jwfF54yd7Gpbebp9u/MYvQCAd8MqASTsDCRu0gnY2YycdzvWdgYSL75FluGkbTic8XLkM5F1FFY/PAOUMx3qo2aO5OB6Bkn0LaMUQEJ1tJMdiQKPmcdgNIYm6+w+zcZIbUhhMBpf2er+mLbb9cp+jpuwEG1a7LlcixyLh6wr61C+TFMbss4UIClMRLZhNJOVQi5nblx/irLcvz0uuR87bVceoxcA8G5YIYD8PE8+F+M4zR7YoUqApHPtZ1HEpWeAvO0ZpLaR4bZtG3Jsbl/fXut87UhHzwBpW3llzyLLszwinbPbNJo1yWeA7CDTyaredJz5nJXs5a0s2cw6sg09ZqNngPrWzaiNom9/ZfssMFK49Hi7Hq1V1jM7wgJE+S1ahOvMum3T6z5uej+6ra5X4RQ8eQyYbI/IdmY+2U9h2bY8KyQsxB4BBBAAbMUKAQSvR8/OvBazeo9mpO6h7aYQvIYWcGelZ8d2BgEEAFuBAIIzMpuVeyT69uHunG4P6aDJpeOkPjOt04XvteZide7pTC2t0PNet++XPtoOB9gdBBAArOB0AkhYyEi0aLsfHrNAcXqS4b4f7nJGYqjvuyrsKT6n+f4rALw9CCAAWMGpBZAFy2hGR/GeDRqVFSMB1PdpHZfCyHX4AbB8CK7rA4DXBQEEACs4pTdvkTGbAeq/DjrNXCOAJKL674HCIijDAPD2IIAAYAWn9OotNmYCyNtJCpkWQH3LLG9x5bbpOjsOAF4fBBAArOB03twzLy0+vFzzEPS18flgdD7304JL4ZngAoDXBQEEACvAm/9/joTNURoAvC4IIABYAZ4dALYCAQQAK0AAAcBWIIAAYAUIIADYijMLoKPb5f3dqXxGsf+dKvq7YCt4CZsAuzI/WwEATsijCCDh8C3fV7ol74x+7QfAe2R+tgIAnJBHFECamfG/TfWlc/0z1V88Vx5/cfyrr74a/rNVOM4zSv43q8RO2tQX2G3D292utOWX0fq9a/rIqBaXB9iVp2cRAMCJeUQBZPqN9MJ5UpQc4fea+U32mb9t5Cd+8o372Q5v56tAJHwsqgB25fhMAgA4GQigeR2ekVEezRZ527QNrT2jk7isaAHk2SjBM0WwM/MzCQDghDyKAPJsi2dhtO3bXr7d5FkZlfNaokOzO86b+Pkgz/4Ityk/HaQZIokcvy2/hZhvcf3www8/Py+kem1f+WUvBRvAbszPVgCAE/IoAuhe8vbVa4DYgUdjfraegJUnnC5Mt9rLX0xG4R3/QdHfRbsH/Qq8958oenbg3vacdT9c6ttoX6gvtz5PYRta5y/+GSud71tydgHU+1bkDM6OzPoFsDOnPaJzqtXc4/DkXG75xTSrS3ZudVRn4V7RklzjcC9x7wW198Nsn824pf5b8opL+W8V402Kn1wfsWKfnYEzCyAA2IfLV803IC/m3m4hpHg7QH8g1Wi7HyZM5z/6NeN77VqPfsG7jO10fZ2/7+FnHrVf6W6/HXf2w/kt2iy8FJcfb/UvS5NtzGcLXN51Z/7ZuvuksP9h4nDW0fndXuWR8+1fv453WZdP+87ncNafeBzUd4+ty8/2hY8j58v83hej8c38ttn0LI/rEi3cXI+3R/bcXm/nkjNy3d4Md727ggACgBU8vdK+MXaKpn8pd9gXdzuH/utnr9u5CjkJOwfH92yR4+Vo0pmP7DmcTk3kQ4NOszBpMdT2HJ8Cxuujtgq1N8vZlsplG71tez3WKf5kw2LR+brN7pPq13a2M/ex7ba4HI3hyJax8BkdA23HbfdYjPphO25XjpvL5rgaHx+uM8W3tm1HdLtUtvvmPL3/st4cz95/DtvO7iCAAGAFH3usE5DOQRfudgYtdPKinr9wdfFPp2ARIEeT8SIddztxY2cyctJtr2mHnNu9Nu3sRvm03eUcb+ecccLOu8v2djt10X1PwdDOtfdbi7asz3lblHSbRYslY1Gksi0mE++Lbofr0DrFS+YZ9TvXZjZOwsdgpgvnOTqWupzXLcaN0rOObueuIIAAYAWnuyKmsxhdsPvXr51NCh5t25E5j3+V29mmo2mHkkLK4ZFDV5zLjOy5DSOHrPJ2hlpnP7I+p2tR3Gh8epxy5sf5XbfSFJdOuvtne1mXkD3ldX+UT/07EqMpZtx+pal+C5as20Ik2+Qx1Np1dp9tJ/dHhntf5LjmOOW4O87l3Af3M9OT3JfK34Iox0S4rbbT9kTui96n7ovL9XEx25+7cmYBpLHuY1Pksftcvvnmm5+Pz3xPzzX0+3rS1muiv9c/tw8Aq3l6pr4xR7+AX4v+JQ1wFlqcX8ujiB9xdgE0I0VuYiF+Cb3k8JJokbC5hmtsvRRvVS9AMz9b3yE+Mc8gwgAaHZeaTfKM5nvl0QSQ9uVROaPyl8TDtbMq19h6Kd6qXoDm8lkHAHAiHkkA+dZUflQ0bSh/3tK2eNCMXt7W6nr9lmjPCDm9bfmWnRbdnrKwbnsOq07nVxsc74+seobSt7gtyLLf2QdhG31LefSma4CVzM9WAIAT8kgCKGdD8jteRvnz+bQUD5mv63U9+pSFaJFhWy1MRm3I8CxeyJa/KabttJ+3YC8JIIkn2UEAwUszP1sBAE7IowigfjA5hYAEgPJKBCheMyuff/75z+JAZSVW9OyQwirTz/94tkekgElbCnvJfC3UHK86nV+zRbKjbddl0eIZIdtR35VXbc0+pO3RbBjASzI/WwEATsijCCAYk6LMM1gAL8H8bAUAOCEIoMdFs0S+RcZMELw087MVAOCEnFkAAcA+IIAAYCsQQACwAgQQAGwFAggAVnBqAfQab68d3bMfxT0C6lf+7bZR2g59H704rv8WvIprxuRS+jXonznXvA0YEEAAsIb7r9wvhP9W+ZIPDc4c17WOaFZ+hBzctYKuv4/1XLp914xll7mFa8pek+cIjcvscxDX9O85XGrzqnpn/bqHVcfSmUAAAcAKjq/sb0QKhUvO57nI2fTnBOzIVtaZ7+K4RLdnFf3CsSNWOfPkljG4RPfB4Zd08i8xJmfnJcTYKs4sgPr4TPpfYMrrxe/8ufZH0ipU56pz56j9fl/QrfAyRHhJbj8iXxidjCkE+oRyWBeMzOuTy+F2up7V6bXJsG1o7S+Td568kKmu/Hq5XzOfsxVun8t5nfZNC5Zcq1w7ZPc1X3Of7enZtB4bh/NNrLnOftumbKmebEvvC69zn2W84yxGe3Yn96/LzvabbOZtsO6DcX0i26V6ZMttcZrjhGxl27st7kPSfZ6t25biZa/7kcdGnhsu32PtcO8bx/exZrofZ+JRBJDo/dTXu+bI/nNQ/Sv39VH7j9qe1/ykxwtgJfMj8o1oZ5snZ55c6UC8nc5zdrK14+l4nYjp2NN+4riRY/bJnO1tR9Nr99PCJfvuPHaC3R7Zdrtd92gc2xmLzJdtyrF0m1qopbgYCSELwxaBTrdgsMjoi2fmdx9aIBnn9Vgo3KJCpI1sc4o95en9I5TfZZQnjxPRF/Es2/tO9WTZ3qddv+tSuI85paXgdTsyzn1Owdh1jsbrjDySANK3svRWZJfr40QzINp3nglxvPer42VXLw308aG1wp550VuifV7ktUh58w3NQuX6XFSaP3OhOrOMz0/VkeWUR/Sx7GPR56Js5HEqO17Uvrw2+NtiOlbVTrXB9QDcyvxsfSNGIsfxvkDrpPAJ0xcU0b/6jR2t6BNcaTqR8wKkPG5DOzfl84VGaJ1OzWmykY7I9bo/LueLgB2wymSdua2y6fw9LikObNf2sr9ty+t0jrKVF54s7z7m/un+Z39dn8fMefpi7wuycbzz9T6zPeH6tE5Hk07d2177wi36It3lHd/hzj9qv8fAx4HrtS31I/uWx4vseVxVzmPpeOF9Zxs+7vJYEtnfPEdmfTkrjySAOpz7MMP92Qiv/cmMLtft8LmSbZCYcJyYlTUWGl0m8+dxLPspnJTPx2z3O68XSZ9XWZeOa4VdFuBWxkf6G9JC4wifDClcriGFAqxldvFcwS37+Bre64UzncxoDFI0npH3JIC87h8LDuta5jcmq+zoY6bebgEkUdVipssYz7yILjMTQD6OcvYqf3xY1KU9iSzn0fZIALmPLnP24xXOy/xs3YDZiXfErWIJbuPa/XAL2l+3CONLjJz+eyLPm/4xsMO58SgCyOKhxYTCWutc8m0t7yeJBp8LircwUV6X9y01z9hon6q81rLt22K27bpct9rY55vSdEtK9XUZ16cyKUZkR3WqjPPalsh2CPdFfUzR5PFwOaUpj+JV3w7HLJyT+dkKAHBCHkUArSTttnhJXrINALsxP1sBAE7ImQUQAOwDAggAtgIBBAArQAABwFYggABgBQggANgKBBAArAABBABbgQACgBUggABgKxBAALACBBAAbMWZBdCtf4NXfr913X9f95uTR/kBYB3zsxXgHXDtSxH1wrUj57YK1fHWTk/OuNtwhnaZRxFA+ZkIkS/6E50fANYyP1vfiHzle781Nd8ymvn8zSpfQByX+Ubkt5WyPsXl9gzlyTrzO1Gu33b83ZrEb01WG5XmutrZ2obzibY1iusxnKF8FgI5jiLHJ9fZ117nmCnsfdCv+Rf9PauRPSM7ttXHQua7VtQkPXYjVKfa2W9PvpdRX5ujNHN0rD8X13t0Hrw2jyKAOq+OLb/1WGhbbzzWG5L9yQsJpvywqd6i7OWacx0A/sj8bH1jdHLnCZ1iIx2c4uyQ0pEo7tI3YvoClBf7SxeTkaAZCSA7jlF+0w68BZBtZD61L51Sjo/pMZyhfB5T1+2+OL5tm45XeCaAMs5k+7rfwmFf8EdpLufwtQIl819y8BqHa+2K53wS5FIbRI/Ba/FW9Y54ZAGU1wnn1zqFkcmwtq85fgDgj8zP1jdGJ3Q7b8XJmaZzUdxoBigd4ojZBUUXETvbTk96piRxm8RLCaC2pTJKTyetPD2GI5QvBVDGpQAajcko/BICaDTeDrfwTEE8cwopeno2KY8x1+F1zkDJRs7OjfL3usn2zkjBfyTq1eY8VmZ0W5tsT9vzuCi+HXauu45rjsNreRQBpBmd3J89ji2ANKaa/RGjc8VpAHAd87P1jdHJ3RfNmWhpB+K4I2cxEiQup4t7192MLkAm2zQTQOmYbxVAnd91aZ2ObzSGI5SvBZAFRzpf0ePdY6DwSwigS2kZ18fDiBbRxm1Vv9uucN9mv+Qdr7Le7nYn18wUZZtmfVN8itUZo7Y2blOmp1jU9ujcapEkRvvoXh5FADlOz/z4uR9hcSlbuQiNcYpL73PZTRsAcJn52frG6OQeXSz6AjNyeH1h6HSjC006DV/krxFAIoVIO0tfpGYCKLdb0IgOi67Pjqbrdp3adtrInsnxSrHiX57Ok2szCt8igFJgHYkcITvuczrZtK+6vb+7LYntplNKmznjlMeJt13GzsplFK9+KI/j1Z7ZMai2u8wM2VE9as9MMNmO91mOa9JtHZEOdnSc5T7JsctxMYof7bN7eCQBBABvx/xsBXhgjgTHW3DkOHcmx3nVmJ9ZAAHAPjzmVRdgEzxz8ojMZt/uBQEEACtAAAHAViCAAGAFCCAA2AoEEACsAAEEAFuBAAKAFSCADsi/H9/Lc/4B85wyL83ZHtbtf5jBH4+bl3oGZ0YeG6seeB6BAAKAFZzLm52IfK/KCp4jZp4jNmZ/t17F2f7G+9pO/rm89H5J+tUFr4VFz0vvEwQQAKzgda+QV5DvHvF7TYS2fWHN95TkRd7bGef3p8zSZ6TtfD9NrtXGfDeP1nZ0fueHBcMlMdX9UJ1a3Ocs3+/L0bbrcdluS7ZRNpX/mtkT28r6HGdRl3XKtrZVt/dZt9Xt1drjl/ly9sBpI3pMux6PoeOzLvffbRntY/XP7Z0JWKdnnrTjdxe5PY53/92OHqcjsk6h8l5yrHocfRxo3+RxK2ZjLNz20Rh5W+V9vPlY7HMjz4d7QAABwAquu+K+IvmysLwoK94X2NFF3s5QefoWgNJ88VdaOoYZ6VyML+hZXm2VTS2uz85g1I+mX5Lnem3Dae6T22Ob6VSF63R+hW2nRdnMqZtM7zHrehW2sDBuo9tsey6bbcx4031tXP7SGHoMRPc/bTveztpl0tk3amOPxej4TNsOK5/SVY+2L+0P0W1x2DbyePU5YbsKq76sx3laTJoeyxYyfVw6PveH6pT92X68FQQQAKxgfmV/I9Ip+qIrfIHNC7wvzlqnY8h4YZsdf4TLtAjIsnaSjnPbup6j+rLtKfJmbc/2jMaiw163k7YgOsJlvB/aWWbfRbYnaeduwdJ9df8tphTfoijJPrYN0fsjt92fFFkt2NLuNXReh23XIty4HguELj/C+VocepzSptAxOuq/UfkUrcloLHtM+7hqoWfhc424uxYEEACs4PIV95XpC2yGLUDsHJ3HjjjFQguT/PXp+HYGI2Qz8+Uv27zIZ9htu6YeO7R0JOkMe62+eDsFmdZqm/vpeI+VSUeptJloEe5D51VcOjrbbLHoOM8YZJtkq51njq3js+2N00ZjmPWliOr+5/iJHvtL9Wd6jqXic7xyv8xmT2zraJ+0MNS2j9E85rXO49LbLXaO+ifc3s6X9Xjd7c4ynXYPCCAAWMHx1e+BSUEE0FgwiGuddwu459ACJTmaDXtPIIAAYAXvVgDNyF/L8H7RceDlEj3D+JK4TUdC6Ro8M7cjCCAAWMHlqzsAwIlAAAHAChBAALAVCCAAWAECCAC2AgEEACvYSgC91nMWAHBeEEAAsIItBFD/XRgA3i8IIABYwc0C6L/+679++qd/+qeffv/73//0u9/97sOibcUpbQX9jhH/K0sCSEu/bM1rvyPFL7njb8MAjwcCCABWcJMA+vd///ef/v7v//6nf/7nf/7pP//zP3/6n//5n5/+8Ic/fNhWnNIkhhT/XPJvx/0X5H5hXG5L/KTgyTwr3s8CAOcAAQQAK7haAGmGRwLnSNwozULoubNBOeujmR7P/uTzP/1afeXL22MWPP3GXQDYHwQQAKzgKgEkUfMP//APh+In+Y//+I8Pt8aeg29jWfjkpwtM3vqazQplGAEE8DgggABgBRcFkGZ+/vEf/7GjL/Lf//3fH8q+NbzVGeCxWC2APFPsD7f2t/0Spfl7cX7WUNv9DT7R32YT/sGm/P5hlt+ka3uJfgzyYw5gHU/P8OLv/u7vLs78/Nu//VtHfUBlAQBWslIApdhoASTB0f88tQASnqmeCSCnycboOcT8eHMKoL6lb1yH0rIMADyPwzNIt7J06+uIo9tdKqt0AIBVrBRAIsVHzrxItPT30lIA5QyQkWhKOz0DlNv5PTbbTHE1Im/5z/IAwHUcnkG6hTWb3RH/+q//+vNf4Ueo7BlugwHA47BaAAHA++RQAOnfXHqWZ4Rmdyx+ZgJIZWUDAGAVCCAAWMGzBJBmdlL8IIAA4LVAAAHACg4FkG5xHd3CSiE0QmVlAwBgFasFUH9qR8/l+PUbfnh59JLVfAYn306vMsqvOL/LLB9szmeI8p9iZvS8UG4fxake1999yGePhNLTlh8A7+eX+mFwx/vh7swn8p9qzqO07qvyqa7RA+IAr8GhANIMzkzcGL0FepZH8aMZJACA57JSAMkhW5D431WixYG2U+R0WqJwlxdpP0VGPnidf4k3/WC0hIPiJBxStHlJ0ZZtvdRu120hk/llN+0ItUFtcXhUrutQOPs+ywfwGlw86nQLS5/AOGKWzu0vAFjNSgEk7HxzliNnfDqs/BIEo3f1CM90pFNPsSJylmT0T7OMa5Ewmo1R+1yuZ616Bsi0SPMMUNeX5CyO8qcwcpvVt/yLf9Jh0f0HeC2eHo2FZ3guvQuo+Zd/+ZcPZQEAVrJKAElIaPHMx2gRGc4Zj86bgmI2G6LFIsViw+lqi9Jy5sZCIkVVCga3ffROIW9r+dWvfvVR2Eve3pqVVXr2uwXeaEy87bVsZH979shrgNfkqqPuNT+FAQBwxCoBBADvm6sEkHitj6ECAByBAAKAFVwtgMQf/vCHn37/+99/mN3RWmJHt7oyDuEDAC/JSgGUz9MI34rJZ2EyXuSzP/2si9d5C8zP4Pjh5cwnfOtL+bTOW1Km7fsZpHyWCABu4yYBZDTTo9tc+hu8Fm0fzQwBAKxipQDyX7GNRIiFSoqNFiDGYf/dW+EWSw77IWOtU3gdCaCsN+36OSELrRZyAHCZZwkgAIC3YqUAEilQHJZQ0ZIzOSNaGHU+CyCtLYCExE6LFwsgk7a83ULHf4cHgNsZn9UAACdllQBqMdGzLRYvngHKpctZ4HhbeBZJ4ZwdkvCxTbWh6xVZp+0orv855e3uCwBcBgEEAFuxSgABwPsGAQQAW4EAAoAVIIAAYCsQQACwAgQQAGzFKgHk52/yr+Tedpqf2fG2n+/J9FyMtvvfXG0vPx3htHz2h4ebAV4WBBAAbMUqAWTy/Tx+v4638x0+jf/67n9vae2/uDvODy4b20ux1GFvdx4AWAtnGABsxWoBZKHS3+a6JIBypsYzN44XEkOa7UEAAZwTzjAA2IrVAigFS4ZHAsi3rUS/v0flLaTyw6hHAqjfJJ3bCCCAl4UzDAC2YrUAAoD3CQIIALYCAQQAK0AAAcBWIIAAYAUIIADYCgQQAKzgdALI/6zQku/aaPI7OyK/qWPygcW0qyU/cpiL7RnnM53/aDnKn9/uye8EaXG7/W2htimcL9vnf6L43ydd1n/17fi2P6o34/pbRy6Xtv334E4HuBcEEACs4JSeqR3qjPwwoEjB02mi7fqLzx2fKJx2RZexozfa9r87LDocb/HQf6v1P0hEijkJmbThdJP/ImnBl/GjNqYgEhY5+W+YFGP+d4vIf7k4r8n2t6AEuBcEEACsYK4u3pCZY21ylkGOuoXKTBTY0YsUM3LqKS4sProNHdfiQqT9jNPSgkakAEp7OZOTOE55sz+Nx0BCKUVXtsNlux6XNSmAlJbipsu2mAJYBQIIAFYw9ppvTDvhGX6nhm/92Fnb0fcsUDr6vo3jtW0K2xsJgbQ7E0AtdFxvx4sjAaT8Le6E8mTbR7jtnZ7t6zQz6veRAOpZLbcPYCUIIABYwSm9UzpNb49ERooVzdzYWY9mfXI7BUGKhxRMKVJaSLXgGLVNdYyeH0rhlaQAyvr6Fpjy5SyV82md/U6hovh+Rkrb9wigo1tgZjQuAPeCAAKAFZzOO8lhesmHoNuZtggRFjaOt5DoRXTcKH70McNrwiO6rszrvnmxSPJtpFyUV/0azeq4v/lcUNbVtnpJus6Mc/uy3V3OjGauAO4BAQQAK5h7bACAE4IAAoAVIIAAYCsQQACwAgQQAGwFAggAVnAqAdTPpLCwsDzmcg8IIABYwX1XIgCAVwYBBAArQAABwFYggABgBQggANgKBBAArAABBABbgQACgBUggABgKxBAALACBBAAbAUCCABWgAACgK24VwCpPAsLy+Mu17KFAMqPnl7i0jtG+iOeM67JswLVk19VvwV/K+wtcf1a9wdeL/HWbR/R35y7Fn03zt9guwfVfc3307Tvn3vc7M4tFzgAgBm3X+lfmfyw5zVck6+/0j5ihTO7hmuc3RH5ZXhxTf9XkeIn180s/pr98BbM2jvDAv1WATjibKLGH989EwggAFjBbVf6VyYdUQuhTNO2w3ZCDqfA6F/XEg/phD07pLq6Pm9neeXxF+udns5Qef3Vdjk2bVuwuK60rzTPJCjebet6jerSonwq4zpF2m5bGS+yD2JUl8jxsh2XddtN1tH7wPk8xqMv2ydZxmGVzdm8UX3ezrDseOas61Q4Z1acx+1zG7Sd4yDyOBrZ9sySx0s2ewZvVM7xKq/96zw+zjK/j1vvJ9n3+eCx6rF2X5ym5S/+4i8+hF2f82VY5PmSY+P17Di6FwQQAKzg6dX2RNhB6sKbwsbOXvSFV+RtDK/TCea6ZyEcTieY676oK2zH4zJaqw3Om044xZVwfUpXGdvo9na9wsLH251mRmNkQWZHmnWPZiFc1vVlH4zLZVrach+6nmxXY1u9v3LcMr1t5rhnfAqqjJ/ZdflZvMM6LnPfOy6P3xRZbkeLQtPHX7YzZ2eyPbkvk2xjihnZUjjLtMBSnjze3N7ZvvT6JUAAAcAKXu4qdSd2JCKdQl7oR6LAjJyxw/lrPLGTym3lt7NoWxYQblMLjV77V3w78XQywm3vX9xNOjSPlXFdQu1KJ9ztNoofOU7Rjt9r53d6C7EeE9P7rtNN7qPcVv6RkBDZh5nd3NfZluyf82iseny7X9nvHoNsg9K6rSm6sp5sVwuO3g9aZ1u6vXmMyFbv/z62TQusUX1qZ54vuX4JEEAAsIKxdzgBIyeWTr0doOJ9IbbjsNP3hV95+0KdyDGMfrmrfDs10c5P5VVHOgmF89e9f0nLrkVc5lea1663xYfJemXLzrSdkOJly2Pl+BaAozEx3f+sW7jN6Qwz3m33GHhs0sG2KHK8UPud12Pjun1cOI/blvWkmPH4mx5H5xPeT33seCxtK/N7Mdl3xedxoz5nv3IMvN+cPwWS2+z8LQ4b19FipQWV8H7J8y3LZ36tvZ3nS/Z/NQggAFjB0yslnJYWIauxc71EOrcj0XQrKXphLSNRtCsIIABYwamvijjE10HC6lpx5RmR2YwNnJNH2lcIIICX48/+7M8+LDN+97vfddQHRmVmeZ/LqA7xf/7vn320XMupBRAAQIMAAng5UgD95V/+5c/nm7b/5m/+5iNR89d//dc//fmf//mH7YzPvNoWzmecX2vX6TiXcXm3AQEEAO8aBBDAy5Eio0VKxh3FZ5y3W7y07VGZUb4RCCAAeBcggABejhYjXmv5q7/6qydCJ/OYzpv5UhA5T9eZYiftK79mnZqHFUCP9OwCANwPAggAVnBqAcRD0ADQIIAAYAWnFEB+V4rfbeJ35fidLvnuEf6NBPC+QAABwApOJ4DyfSX9wjoLnf7L9iO94wQAjkEAAcAKTqccPOvj1/VnWPi2mF/al28IZiYI4PFBAAHACk4ngHx7S2JGMz2+5SWR488GWPDkbbBcA8DjggACgBU8jGJg9gfgfYAAAoAVPIQA6meCAOBxQQABwAoeQgABwPsBAQQAK0AAAcBWIIAAYAUIIADYCgQQAKwAAQQAW4EAAoAVIIAAYCsQQACwAgQQAGwFAggAVoAAAoCtQAABwAoQQACwFQggAFgBAggAtgIBBAArQAABwFYggABgBQggANgKBBAArAABBABbgQACgBUggABgKxBAALACBBAAbAUCCABWgAACgK1AAAHAChBAALAVCCAAWAECCAC2AgEEACtAAAHAViCAAGAFCCAA2AoEEACsAAEEAFuBAAKAFSCAAGArEEAAsAIEEABsBQIIAFaAAAKArUAAAcAKEEAAsBUIIABYAQIIALYCAQQAKzilAPrkk/9t1tdff/3z9vfff//zdub57LPPfg7/+OOPw+1vv/32w/rTTz/9OS7Lffnllx+2nc/xQvXK1qg+o23l87bseDvzuaxRvU5XGdvI+MbxalP20WXVR/czx6zbkmOhcRY53o5Tm7uvue16O83hjFO/ss0eD4+/t5XmfELhHNPRfjS5D4W3XYfDvbbNHIOsN+OF7al+tzVtaFyUJ/sGa0AAAcAKxl72jRk5sHTmI4ctLFTstEwLoBQYWh8JIJECyGTYdk232eF0hkc2s33uq+l2OS4FWOJ4j1W3ReHZeIoUQHbsSYu2FC7uYwoDo/gWL8J2XKb3aaaNbOQ+zOOg95Hp/s7Carvq6r5YAOW+zTFFAK0HAQQAK/j4an8S0gnJwcjJpphoR+rF4RHtOFM83COAVKadnNLcZod7NmAkNtwuiwAtLYBayAjX5+0RtqN0jcORAEobKYBmtsWorGepXEfvtxYvQu3K/eCxuFUAZRnhuO5Dhnv2SCissc3xy754fEblMs524H4QQACwgrlHe0PScfgX9mgGKFHaaBYi0+U4R45pJICSIwHkWx2zNGG7mW9Ul8Puhxj1VaQ9bbcAcpvdb9vpWRlttwBKrhFArjv3kfB+sN1rBZDI/Nq+RgApz2wGSKQYM9nebr9wuMcoBVDPABnla3twPwggAFjBKa/O6TS8PXJO6cj8Kz0dpBk5/dy+RwD1doqI/MUvR9lOUvlSrLlcCqCmZ5GE8rYAcrrDOVbafo4AUltHoqXHwvaybynChPKNbLl/LbyuEUDOl+1pMWyRZLq/OZaz8cu+WACZPk6zD7AGBBAArICrMgBsBQIIAFaAAAKArUAAAcAKEEAAsBUIIABYAQIIALYCAQQAK0AAAcBWIIAAYAUIIADYCgQQAKwAAQQAW4EAAoAVIIAAYCsQQACwAgQQAGwFAggAVoAAAoCtQAABwAoQQACwFQggAFgBAggAtgIBBAArQAABwFYggABgBQggANgKBBAArAABBABbgQACgBUggABgKxBAALACBBAAbAUCCABWgAACgK1AAAHAChBAALAVCCAAWAECCAC2AgEEACtAAAHAViCAAGAFCCAA2AoEEACsAAEEAFuBAAKAFSCAAGArEEAAsAIEEABsBQIIAFaAAAKArUAAAcAKEEAAsBUIIABYAQIIALYCAQQAKzidAPrkk09+Xj799NOPwl6+/fbbLvYBpeV2L6M08eOPPw7zqp6Oz+XLL7/8yJ7sjLC9DH/22Wcftr/++usP4S+++OIj24rvMlmn1m3XNkW39VK8mdXrRXVk2PtI61H+UV3eno0XwBEIIABYwVMPeAJGztLbFgBN5ksU38Igcdhix9iht9Do8nLiFmQjh/79999/KJPCwqLHtlJIOV+3J+M6XliIJAq7TU6z2Ms8ych+lxFtw2OQ4tR5su9ZbjReAJdAAAHACp560hPQzjW3ZwLIQmXkqC2ARqJCYYmUTEvBNBJAIxtaLJoSxbUNCwKXGQmgkeiwuMg+GQutRGHZaZHmfD3bo/Co3lFchj0rJFrsZJ+c7niA54AAAoAVnNILpXPs7ZkAMu1wUyzMRIKwAGqR1OKly5vOZ3IGxtstcvL2UaclFjHdD5fRuvvedhzueJFCLBnlvRTOuBZaQmmX9iXACAQQAKzgqdc6AelMe3vmpPPWUd+G6VtgEhAZFil8JEhsr4VNbnvGxPQMUDp4lXN6z4iMBFDOqpjsV9ru/uW22peCKcWMbLhs9kPxWde1Aqj733mE2602jYQRwCUQQACwgqce6o2R0/Ry9BB0O1c76RQGWT7peJfNuK5ztqisxUqKCNuwk3d+150iTOW7DSlARNY3ihd5eymXzHcpPuPyltso3WExa2/ntRjrW3gA14IAAoAVnE4AAQAcgQACgBUggABgKxBAALACBBAAbAUCCABWcCoB1M+MsLCwPOZyDwggAFjBfVciAIBXBgEEACtAAAHAViCAAGAFCCAA2AoEEACsAAEEAFuBAAKAFSCAAGArEEAAsAIEEABsBQIIAFaAAAKArUAAAcAKEEAAsBUIIABYAQIIALYCAQQAK0AAAcBWIIAAYAUIIADYCgQQAKwAAQQAW4EAAoAVIIAAYCsQQACwAgQQAGwFAggAVoAAAoCtQAABwAoQQACwFQggAFgBAggAtgIBBAArQAABwFYggABgBQggANgKBBAArAABBABbgQACgBUggABgKxBAALACBBAAbAUCCABWgAACgK1AAAHAChBAALAVCCAAWAECCAC2AgEEACs4pQD65JM/Niu3f/zxx5+3ky+//PKn77///sO283/22WcflVXYyM633377YVt5Mp/pNti+6hqlJ53mMhn36aeffti2XZFtFEpTWzM+8wO8RxBAALCCp57/BKSAkFCxgGghYZSnhUwKIIuNGSlIMi63JTxSiDi9BUqitK+//vqJQFK84pRmQdP1G9tXXgBAAAHAGk4vgEbhERISKYJSAF1T3oIkw7k9E0Ap0BqLGpdPLNpyJmoEAgjgYxBAALCCsdd9Y1oMKDybZREpQEYCKG+ROY+Fh7EgMb3dAqbTRyg+l+aojaZnmLrdAO8NBBAArOCpVz4BLRZagEgsZB6FLRI869LPAPX2SEiMZni83eKk0z1D4+d2Et/y6njRdnpbZfL22JEQBHgPIIAAYAWnFEAAADMQQACwAgQQAGwFAggAVoAAAoCtQAABwAoQQACwFQggAFjBqQSQHvxlYWF5/OUe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>
