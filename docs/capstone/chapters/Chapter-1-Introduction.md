# Chapter 1: Introduction

## Background of the Study

Local government units (LGUs) in the Philippines are mandated under the Local Government Code of 1991 to promote tourism and preserve local cultural heritage. However, many municipal offices face operational difficulties due to their reliance on paper-based records and manual archiving. The Municipal Tourism Office of Mangatarem, Pangasinan, currently handles tourism data and cultural profiling through physical folders and manual logbooks. This setup limits the public's access to historical information and delays the administrative updates of local attractions. Academic studies show that establishing a centralized web platform for municipal data improves public engagement and coordinates tourism information more effectively than physical-first archives (Chang & Caneday, 2011). Transitioning to a digital database and spatial mapping system is therefore a practical step to resolve these administrative delays and secure local heritage records.

Mangatarem is a first-class municipality with historical sites and natural attractions, including the Manleluag Spring National Park. Despite its tourism potential, the LGU struggles to distribute accurate cultural and tourism information. The tourism office acts as the main depository for data from the municipality's 82 barangays, but the lack of a unified system leads to fragmented records. When researchers or visitors request data, staff must search through physical filing cabinets, which is time-consuming and risks data loss. These administrative bottlenecks highlight the need for a structured digital platform that coordinates cultural mapping and tourism management at the municipal level (de Claro et al., 2024).

To address these inefficiencies, this study develops the 'Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan.' The system replaces the current manual record-keeping with a web-based mapping application. By digitizing cultural records and centralizing tourism information, the platform aims to streamline the LGU's approval workflow, prevent data duplication, and provide real-time updates. The integration of geographical maps and digital profiles allows tourists, residents, and academic researchers to access verified historical records online, supporting long-term cultural preservation in a secure digital repository (Cascón-Katchadourian et al., 2018).

### Encountered Problems

The Municipal Tourism Office of Mangatarem currently experiences operational bottlenecks in collecting and verifying data from individual barangays. Barangay representatives report updates on local attractions or events through informal channels, such as text messages, personal phone calls, or physical paper documents. This lack of standardization requires tourism office staff to manually compile and format incoming reports, causing delays in publishing updates. Additionally, because there is no synchronized database, conflicting information about local landmarks and schedules is sometimes posted on unofficial social media accounts, which misleads visitors and reduces the LGU's credibility (Chang & Caneday, 2011).

The manual archiving system also creates access problems for researchers and students. Academic users looking for cultural profiles or barangay history must travel to the tourism office to inspect physical folders. These physical documents are subject to wear and tear and can be easily misplaced. Furthermore, the slow coordination between the municipal office and local stakeholders prevents the LGU from promoting seasonal events or local businesses in a timely manner. These issues demonstrate the necessity of a web-based, multi-role system that standardizes data entry, enforces administrative review, and provides secure public access to cultural mapping data (Cascón-Katchadourian et al., 2018).

## Purpose and Description

The primary purpose of this Capstone Project is to design, develop, and implement a web-based Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan. This computing solution seeks to centralize, digitize, and standardize the management of the municipality's tourism assets and cultural heritage records, replacing legacy, manual processes with a secure, highly interactive digital platform. By providing a unified administrative moderation pipeline and an engaging, map-driven public interface, the system aims to improve administrative efficiency, eliminate data redundancy, and promote local heritage to a global audience.

Upon deployment, the Interactive Digital Cultural Map and Local Tourism Information System will provide significant benefits and operational value to the following specific stakeholders and beneficiaries:

**Local Government Unit (LGU) and Tourism Office staff** – The system provides a robust, centralized administrative dashboard that simplifies data moderation, allowing tourism officers to verify, approve, or reject content submissions from grassroots contributors. This automated workflow reduces the administrative workload, ensures data integrity, and enables the LGU to maintain an authoritative, synchronized repository of municipal cultural assets.

**Barangay Representatives and Contributors** – Designated barangay officials gain a secure, dedicated portal to directly upload localized historical profiles, high-resolution media, and event announcements. This decentralized contribution structure empowers local representatives to showcase their respective jurisdictions' heritage while standardizing the data formatting before submission to the central admin.

**General Public, Tourists, and Visitors** – Public users benefit from an interactive, mobile-responsive geographical map equipped with spatial filtering, detailed landmark pop-ups, dynamic routing, and heritage categorization. This interface enhances the visitor experience, facilitates travel planning, and increases the discoverability of local landmarks and business establishments.

**Students and Academic Researchers** – Academic users are provided with structured access to the Digital Cultural Atlas, allowing them to search, filter, and extract detailed historical records, cultural profiles, and community traditions from any location, eliminating the necessity for physical travel to municipal archives.

**Local Residents of Mangatarem** – The community benefits from the digital preservation of their intangible heritage, traditional practices, and historical festivals. This secure repository fosters municipal pride and ensures that Mangatarem's rich cultural identity is preserved for future generations.

The administrative rationale behind the project is to resolve the inconsistencies, communication delays, and accessibility bottlenecks inherent in the current manual workflow. By replacing fragmented communication with a standardized digital pipeline, the project assumes that the system will establish a definitive "source of truth" for municipal tourism and cultural data, thereby maximizing stakeholder satisfaction and enhancing operational transparency.

## Objectives of the Study

The main objective of this study is to design and develop an Interactive Digital Cultural Map and Local Tourism Information System for the Local Government Unit (LGU) of Mangatarem, Pangasinan. The system is engineered to replace legacy, manual processes with a centralized, web-based platform that optimizes information management and promotional workflows.

Furthermore, the developers aim to achieve the following specific objectives:

1. To analyze the existing processes of collecting, verifying, and disseminating tourism and cultural information in Mangatarem, Pangasinan, in order to identify administrative inefficiencies, workflow bottlenecks, and data integration challenges.
2. To identify and design the key system modules, workflows, and access control parameters for the designated user categories:
   * **Administrative and Stakeholder Users**: Incorporating System Administrators (Tourism Office Staff) and Barangay Representatives (Contributors) to facilitate secure data entry, content submission, and moderation workflows.
   * **General Public and Academic Users**: Incorporating Tourists, Visitors, and Academic Researchers to facilitate spatial mapping, digital heritage exploration, and research-oriented data extraction.
3. To test and evaluate the system's functionality, performance, security, usability, and acceptability in accordance with the ISO/IEC 25010 Software Quality Standards to ensure compliance with technical specifications and user expectations.
4. To prepare a comprehensive, phased implementation plan for the deployment of the system, including server migration, database initialization, and stakeholder training.

## Conceptual Framework

This study utilizes the Input-Process-Output (IPO) model to delineate the systematic framework and developmental lifecycle of the proposed computing solution. The IPO model serves as a structured technical roadmap, defining the foundational resources required (Input), the software engineering methodology executed to construct the platform (Process), and the resulting operational system delivered to the municipality (Output), with a continuous feedback loop to ensure long-term maintenance and alignment.

The **Input** phase encompasses the technical, physical, and domain-specific requirements necessary to initiate development. This includes *Knowledge Requirements*, which demand technical proficiency in full-stack web development (specifically HTML, CSS, JavaScript, Python, Flask, and PostgreSQL) and a thorough understanding of municipal tourism workflows, spatial mapping, and user role privileges. *Hardware Requirements* specify the physical development and hosting infrastructure, requiring workstations equipped with at least an Intel Core i5/AMD Ryzen 5 processor, 8GB to 16GB of RAM, and high-speed SSD storage to support compilation and database execution. *Software Requirements* include the necessary developmental tools, specifically Visual Studio Code, Git, Figma for UI/UX design, Supabase for cloud-native PostgreSQL data management, and Vercel for hosting.

The **Process** phase outlines the execution of the Rapid Application Development (RAD) methodology, which systematically progresses through four iterative, stakeholder-driven stages:
1. *Requirements Planning*: Collaborating with LGU officers to establish system boundaries, define user categories, and analyze legacy processes.
2. *User Design*: Creating interactive Figma prototypes and conducting stakeholder reviews to refine user interfaces.
3. *Construction*: Implementing frontend rendering (Tailwind CSS, Mapbox GL JS) and server-side logic (Flask, SQLAlchemy) in rapid development cycles.
4. *Cutover*: Executing comprehensive testing, database migration, and administrator training prior to final server deployment.

The **Output** phase represents the completed, fully functional computing solution: the Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan. The system integrates the inputs and processes into a secure, multi-role platform that resolves operational inefficiencies and preserves municipal cultural heritage.


The conceptual framework illustrated above delineates the systematic flow of the project. The Inputs specify the technical and physical resources, along with the domain knowledge required by the developers to undertake the project. These resources feed into the Process, which employs the Rapid Application Development (RAD) methodology to iteratively design, prototype, and build the platform through structured phases. This structured process ensures that the final Output — the Interactive Digital Cultural Map and Local Tourism Information System — is developed efficiently and aligns with the functional and operational requirements of the Mangatarem LGU and its stakeholders. The feedback loop ensures that any issues identified during testing or post-deployment can be communicated back to the development team to refine the system inputs and processes, resulting in continuous improvement.

## Scope and Limitations

### Scope

The scope of this project is strictly defined by the design, development, and deployment of a web-based Interactive Digital Cultural Map and Local Tourism Information System tailored for the LGU of Mangatarem, Pangasinan. The technology stack consists of HTML5, CSS3 (utilizing the Tailwind CSS framework), and vanilla JavaScript for the responsive client-side interface, with Mapbox GL JS integrated for spatial mapping and vector tile rendering. The backend application logic is engineered in Python using the Flask micro-framework, and the relational database is built on PostgreSQL, hosted and managed via Supabase Cloud. Figma serves as the primary UI/UX design tool during the prototyping phase. 

The software's key functionalities are divided between two main access tiers. The Public and Academic tier provides public users, tourists, and students with an interactive municipal map to search, locate, and filter tourist attractions, natural heritage sites, local events, and business establishments by category. It also includes the Digital Cultural Atlas, providing structured access to verified historical profiles and barangay-level cultural records to support academic research. The Administrative and Stakeholder tier provides authorized Barangay Representatives with a secure contribution portal to submit, edit, and upload media assets for their respective jurisdictions. It also equips LGU Tourism Admins with a centralized dashboard to moderate incoming submissions through a formal approve-or-reject workflow, manage user accounts, oversee role-based access control, and publish municipal-wide tourism notices and announcements.

### Limitations

This section outlines the boundaries of the system’s functionality to establish realistic expectations and clearly define areas excluded from the initial development scope. Primarily, the system is a web-based application, meaning its operational availability is highly dependent on an active internet or mobile data connection; offline map caching or offline data browsing features are entirely excluded from this scope. The system operates as an independent municipal platform and does not feature online booking, ticketing, reservation management, or payment gateways for local accommodations, restaurants, tour guides, or events. All financial transactions and external bookings must be conducted directly with the respective third-party establishments.

Furthermore, the system’s advanced scheduling, analytical, or automated features are restricted to specific administrative parameters. The content contribution and moderation workflows are strictly restricted to authenticated LGU staff and registered Barangay Representatives; the general public has no write permissions to alter map pins or database records directly. Additionally, the system does not integrate with national government networks, such as the Department of Tourism (DOT) or the National Commission for Culture and the Arts (NCCA) databases. Finally, the geographic scope of the system is strictly limited to the administrative boundaries of Mangatarem, Pangasinan, and does not capture spatial or cultural data from neighboring municipalities or provinces.

## Definition of Terms

For the purpose of clarity and conceptual consistency, the key terms utilized in this study are operationally defined as follows:

**Administrative and Stakeholder Users** – The user category consisting of the LGU Tourism Office staff (System Administrators) and authorized Barangay Representatives (Contributors) who hold internal access to the system. This category is responsible for submitting, reviewing, and approving cultural heritage data, managing the platform's operational integrity, and overseeing the municipality's digital tourism presence.

**General Public and Academic Users** – The user category consisting of tourists, visitors, students, and researchers who access the system to navigate the interactive map, search for points of interest, and view published cultural and tourism information. These users consume the data for leisure, travel planning, or academic data gathering without requiring administrative privileges.

**Interactive Digital Cultural Map** – The core spatial visualization module of the system that provides an interactive, georeferenced visual map of tourist spots, historical landmarks, natural attractions, and cultural heritage sites within the municipality of Mangatarem, Pangasinan. Users can interact with the map by clicking pins, filtering categories, and viewing detailed multimedia information for each location.

**Local Government Unit (LGU)** – Refers to the municipal government of Mangatarem, Pangasinan, serving as the main beneficiary, authoritative body, and decision-maker over the tourism information system and its content governance policies.

**Rapid Application Development (RAD)** – The software development methodology selected for this study, characterized by rapid prototyping, iterative feedback cycles, flexible requirements gathering, and continuous stakeholder involvement to accelerate system construction while maintaining alignment with user needs.

**Content Moderation Workflow** – The formal administrative pipeline by which the System Administrator reviews pending submissions (historical data, landmark profiles, media files) from Barangay Representatives and decides whether to approve, reject, or request revisions before publishing them to the public interface.

**Digital Cultural Atlas** – The search-optimized historical database module designed to support academic users and researchers by providing structured, easily accessible historical records, barangay profiles, and cultural narratives matching national documentation standards.

## Review of Related Literature

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

### Foreign Studies

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