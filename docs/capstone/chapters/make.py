from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

def create_document():
    doc = Document()

    # Set default font for the document
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    font.color.rgb = RGBColor(0, 0, 0) # Black

    # Configure Heading styles to be Black and Times New Roman
    for i in range(1, 4):
        heading_style = doc.styles[f'Heading {i}']
        heading_style.font.name = 'Times New Roman'
        heading_style.font.color.rgb = RGBColor(0, 0, 0) # Force Black
        heading_style.font.bold = True
        if i == 1:
            heading_style.font.size = Pt(16) # Chapter Title
        elif i == 2:
            heading_style.font.size = Pt(14) # Section Title
        else:
            heading_style.font.size = Pt(12) # Subsection Title

    # Helper to add styled paragraphs
    def add_para(text, style='Normal', bold=False, alignment=WD_PARAGRAPH_ALIGNMENT.JUSTIFY):
        p = doc.add_paragraph(text, style=style)
        p.alignment = alignment
        if bold:
            for run in p.runs:
                run.bold = True
        return p

    # --- CHAPTER 1 CONTENT ---
    doc.add_heading('Chapter 1: Introduction', level=1)

    doc.add_heading('Background of the Study', level=2)
    add_para('The integration of computing solutions in local governance and tourism has become increasingly vital in modernizing public services and promoting cultural heritage. System software and web applications serve as powerful tools to centralize information, streamline processes, and enhance the overall experience for both administrators and end-users. By digitizing cultural data and tourism information, municipalities can ensure wider accessibility, preserve historical records, and promote local attractions more effectively to a broader audience. Embracing such IT infrastructure plans allows organizations to overcome traditional, manual challenges and transition towards a more efficient, interconnected, and dynamic approach to managing local resources.')
    
    add_para('This study will be conducted for the Local Government Unit (LGU) of Mangatarem, Pangasinan, the main beneficiary and decision-maker for tourism promotion and cultural data management in the municipality. The LGU of Mangatarem plays a central role in driving economic growth through tourism while preserving the rich cultural identity and heritage of the community. As the primary governing body, the LGU is responsible for curating and disseminating accurate information about local landmarks, events, and traditions, ensuring that both residents and visitors have access to reliable resources that reflect the town\'s historical significance.')
    
    add_para('Currently, the LGU of Mangatarem encounters significant difficulties in managing and promoting tourism information. The existing process is fragmented and largely manual, which results in irregularly updated online content. The lack of standardized tourism materials leads to inconsistent data across different platforms, causing confusion for tourists. Furthermore, slow coordination with stakeholders relying on traditional communication methods delays the sharing of accurate information. This traditional approach also presents limited accessibility for students and researchers who seek reliable cultural and historical information. These challenges establish the need for a centralized platform that can unify and streamline tourism data management.')
    
    add_para('To address these challenges, the "Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan" will be developed. This computing solution is introduced as an improved approach to enhancing the organization\'s existing system by replacing fragmented manual processes with a centralized, interactive web-based platform. By digitizing cultural mapping and tourism information, the proposed system aims to provide standardized, easily accessible, and consistently updated data, thereby improving the efficiency of the LGU\'s tourism promotion and enriching the experience of tourists, residents, and researchers alike.')

    doc.add_heading('Purpose and Description', level=2)
    add_para('This Capstone Project was conducted in order to centralize and digitize the tourism and cultural information of Mangatarem, Pangasinan, providing an accessible and interactive platform that streamlines information management and promotes local heritage.')
    
    add_para('Once the proposed Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan is implemented to the Local Government Unit (LGU) of Mangatarem, it will hold particular significance for the following beneficiaries:')
    
    # List items
    p = doc.add_paragraph(style='List Number')
    p.add_run('Local Government Unit (LGU) of Mangatarem').bold = True
    p.add_run(' – The main beneficiary and decision-maker will benefit from a robust platform for tourism promotion and cultural data management, enabling them to verify and publish accurate information efficiently.')
    
    p = doc.add_paragraph(style='List Number')
    p.add_run('System Administrators (Tourism Office Staff / IT Staff)').bold = True
    p.add_run(' – They will benefit from an administrative dashboard that simplifies the management of user accounts, access permissions, and the approval/rejection of content submissions from contributors.')
    
    p = doc.add_paragraph(style='List Number')
    p.add_run('Barangay Representatives (Contributors)').bold = True
    p.add_run(' – They will benefit from a dedicated portal to submit and update local content, photos, and videos, empowering them to showcase the attractions and events within their respective jurisdictions.')
    
    p = doc.add_paragraph(style='List Number')
    p.add_run('Public Users (Tourists / Visitors)').bold = True
    p.add_run(' – They will benefit from an interactive map that helps them easily locate attractions, search and filter points of interest, and view suggested routes and cultural information for a better travel experience.')
    
    p = doc.add_paragraph(style='List Number')
    p.add_run('Students and Researchers').bold = True
    p.add_run(' – They will benefit from reliable access to historical data, cultural profiles, and community practices, facilitating their academic research and data gathering easily.')
    
    p = doc.add_paragraph(style='List Number')
    p.add_run('Residents of Mangatarem').bold = True
    p.add_run(' – They will gain cultural pride and benefit from the preservation of their heritage through a secure, digital platform that documents their traditions.')
    
    add_para('The rationale of the project is to resolve the inconsistencies, slow communication, and limited accessibility prevalent in the current manual tourism management processes. By standardizing information and leveraging digital mapping technology, the project creates a unified resource for all stakeholders. It is assumed that the proposed computing solution will effectively address the existing problems by providing real-time, accurate updates, fostering better coordination among barangay representatives and the LGU, and offering an engaging, user-friendly interface for public exploration.')

    doc.add_heading('Objectives of the Study', level=2)
    add_para('The main objective of the study is to design and develop an Interactive Digital Cultural Map and Local Tourism Information System for the Local Government Unit (LGU) of Mangatarem, Pangasinan.')
    
    add_para('Furthermore, the developers aim to achieve the following specific objectives:')
    
    p = doc.add_paragraph(style='List Number')
    p.add_run('To analyze the existing process of managing and disseminating tourism and cultural information in the municipality to identify inefficiencies, challenges, and opportunities for improvement in information centralization.')
    
    p = doc.add_paragraph(style='List Number')
    p.add_run('To identify the features of the system for the following users:')
    doc.add_paragraph('System Administrator (Tourism/IT Staff)', style='List Bullet')
    doc.add_paragraph('Barangay Representative (Contributor)', style='List Bullet')
    doc.add_paragraph('Public User (Tourists / Visitors)', style='List Bullet')
    doc.add_paragraph('Students and Researchers', style='List Bullet')
    
    p = doc.add_paragraph(style='List Number')
    p.add_run('To test and evaluate the system’s functionality, performance, security, usability, and acceptability to ensure it meets user requirements and standards.')
    
    p = doc.add_paragraph(style='List Number')
    p.add_run('To prepare an implementation plan for the deployment of the system.')

    doc.add_heading('Conceptual Framework', level=2)
    add_para('The Input-Process-Output (IPO) model is utilized to provide a clear and structured representation of the system’s development lifecycle. The Input phase defines the foundational prerequisites, encompassing the knowledge, hardware, and software requirements necessary to build the system. The Process phase outlines the systematic Software Development Methodology chosen to transform these inputs into a functional product, detailing the specific stages of development. The Output phase represents the final deliverable, which is the operational computing solution that addresses the needs identified during the analysis. Feedback mechanisms continuously refine the inputs and processes to ensure the output meets the desired standards.')
    
    add_para('Input includes knowledge requirements (technical skills in web system development using HTML, CSS, JavaScript, PHP, MySQL, and an understanding of tourism mapping and user roles such as admins, contributors, and tourists), hardware requirements (components needed for both development and deployment, such as an Intel Core i5/AMD Ryzen 5, 8GB-16GB RAM, SSD storage, and standard peripherals), and software requirements (software tools such as Visual Studio Code, MySQL, XAMPP/LAMP server, and UI design tools like Figma).')
    
    add_para('Process refers to the Rapid Application Development (RAD) Methodology to be used, involving Requirements Planning, User Design, Construction, and Cutover.')
    
    add_para('Output is the expected computing solution: the Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan.')

    # Conceptual Framework Diagram (Text representation)
    add_para('[Conceptual Framework Diagram - See original Mermaid code for visual representation]', style='Normal', alignment=WD_PARAGRAPH_ALIGNMENT.CENTER)
    # Optional: Add the mermaid code as a note or skip it? I'll skip the raw code in the DOCX for cleanliness, or add it as a code block. Let's add it as plain text for reference if needed, but usually diagrams are images. I will omit the raw code to keep the doc clean.

    add_para('The conceptual framework illustrated above delineates the systematic flow of the project. The Inputs specify the technical and physical resources, along with the domain knowledge required by the developers. These resources feed into the Process, which employs the Rapid Application Development (RAD) methodology to iteratively design, prototype, and build the platform. This structured process guarantees that the final Output—the Interactive Digital Cultural Map—is developed efficiently and aligns with the requirements of the Mangatarem LGU and its stakeholders. The feedback loop ensures that any issues identified post-deployment can be addressed to refine and maintain the system.')

    doc.add_heading('Scope and Limitations', level=2)
    
    doc.add_heading('Scope', level=3)
    add_para('The project focuses on the development of a web-based Interactive Digital Cultural Map and Local Tourism Information System for the LGU of Mangatarem. The system will be built utilizing web technologies including HTML, CSS, JavaScript, PHP, and MySQL as the primary database management system, with Figma utilized for interface design. The key functionalities provided by the software include a public interactive map for tourists to locate attractions, filter points of interest, and view cultural information. It features a decentralized content contribution portal allowing authorized Barangay Representatives to upload photos, update local history, and add events. Furthermore, the system includes a centralized Admin Dashboard for LGU/Tourism staff to moderate content submissions (approve/reject), manage user accounts, and oversee platform operations. Students and researchers are provided structured access to historical data and cultural profiles to support academic data gathering.')

    doc.add_heading('Limitations', level=3)
    add_para('While the system aims to comprehensive tourism management, it will not include an online booking or payment gateway for local accommodations or tour guides. The system is highly dependent on internet connectivity; thus, full offline capabilities for the interactive map are restricted. Performance and scalability are designed to accommodate the current reasonable volume of tourist traffic and barangay contributions, but extreme surges beyond typical municipal capacity may require future server upgrades. Access to the content contribution and moderation modules is strictly restricted to authorized LGU personnel and registered Barangay Representatives, meaning the general public cannot directly alter map data without LGU approval.')

    doc.add_heading('Definition of terms', level=2)
    
    terms = [
        ("Admin/System Administrator:", "Refers to the LGU Tourism Office Staff or IT personnel responsible for reviewing content, managing users, and overseeing the technical maintenance of the system."),
        ("Barangay Representative:", "An authorized contributor who submits, updates, and uploads local tourism and cultural information to the system on behalf of their specific jurisdiction."),
        ("Contributor:", "A user role (typically a Barangay Representative) with permissions to propose new content such as photos, history, and events to the platform."),
        ("Interactive Digital Cultural Map:", "The core feature of the system that provides a visual, geographical representation of tourist spots, landmarks, and cultural heritage sites within Mangatarem."),
        ("Local Government Unit (LGU):", "In this study, it refers to the municipal government of Mangatarem, Pangasinan, serving as the main beneficiary and authoritative body over the tourism system."),
        ("Public User:", "Refers to tourists, visitors, or general users who navigate the interactive map and view the published cultural information without the need for administrative access."),
        ("Rapid Application Development (RAD):", "The selected software development methodology characterized by rapid prototyping, iterative feedback, and flexible requirements gathering to speed up system construction.")
    ]
    
    for term, definition in terms:
        p = doc.add_paragraph()
        p.add_run(term).bold = True
        p.add_run(f" {definition}")

    doc.add_heading('Review of Related Literature', level=2)
    
    add_para('(Note for implementation: This section requires sourcing 5 local and 5 foreign literature from 2020-2025 aligned with the objectives. Temporary placeholders are provided here to adhere to the formatting structure until formal literature review research is conducted and injected).', bold=True)

    doc.add_heading('Existing Tourism and Cultural Information Management Processes', level=3)
    add_para('Smith (2022) highlights the inefficiencies in traditional municipal tourism management, stating that reliance on fragmented physical records and isolated social media announcements significantly limits the reach and accuracy of cultural promotion. A critical evaluation of Smith\'s work underscores the necessity for municipalities to shift from manual archiving to centralized digital repositories to ensure consistent data availability.')
    add_para('Dela Cruz et al. (2021) observed similar challenges in local Philippine contexts, where LGUs struggle with inconsistent tourism data across various barangays due to the lack of a unified reporting system. The study suggests that empowering local grassroots (barangays) with direct contribution access to a centralized pool can drastically reduce data dissemination delays.')

    doc.add_heading('Key Features of Web-Based Tourism Systems', level=3)
    add_para('Johnson and White (2023) examined the impact of interactive mapping on tourist engagement, finding that digital maps equipped with filtering capabilities and rich multimedia pop-ups increase visitor retention and exploration confidence by 40%. The research emphasizes that an intuitive UI is a critical feature for public-facing tourism platforms to effectively guide tourists.')
    add_para('Reyes (2024) evaluated the role of decentralized content management in e-governance systems. The study determined that creating specific user roles, such as local contributors and central moderators, improves content accuracy and accountability. This points directly to the necessity of the proposed Admin and Barangay Representative roles to ensure the integrity of the published cultural data.')

    doc.add_heading('Usability and Acceptability of Information Systems', level=3)
    add_para('Anderson (2021) provides a comprehensive review of usability testing methodologies for public sector web applications. The author emphasizes that utilizing standardized Likert-scale surveys to measure navigation ease and interface clarity is essential for systems targeting diverse demographics, such as both tech-savvy students and general tourists.')
    add_para('Bautista (2022) explores user acceptance testing (UAT) frameworks in Philippine LGUs adopting new IT infrastructure. The findings suggest that early and iterative involvement of stakeholders (e.g., tourism officers) during the prototyping phase drastically improves the final acceptance score of the system, supporting the use of the RAD methodology for this project.')

    doc.add_heading('System Implementation and Deployment Strategies', level=3)
    add_para('Chen (2023) discusses deployment strategies for cloud-based municipal systems, identifying that a phased rollout paired with comprehensive user training for administrative staff significantly reduces early-stage operational friction. The review points out that a clear implementation timeline and resource allocation plan are crucial for minimizing downtime during the cutover phase.')
    add_para('Gomez et al. (2025) analyzed recent case studies of digital tourism map deployments in rural areas. They highlight that ensuring reliable web hosting and defining clear data governance policies prior to the launch are critical steps. This supports the objective of preparing a detailed and robust implementation plan tailored specifically to the technological readiness of the target LGU.')

    # --- CHAPTER 2 CONTENT ---
    doc.add_page_break()
    doc.add_heading('Chapter 2: Methodology and Design', level=1)

    add_para('This chapter discusses the methodology and design processes employed in developing the Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem. It details the chosen software development methodology, the sources of data, the data gathering techniques applied, and presents the structural design of the system through architectural diagrams and flowcharts, culminating in a planned implementation strategy.')

    doc.add_heading('Software Development Methodology', level=2)
    add_para('The implementation of a robust Software Development Methodology (SDM) is crucial in software engineering as it provides a structured framework for planning, creating, testing, and deploying an information system. For the development of the Interactive Digital Cultural Map and Local Tourism Information System, a well-defined SDM ensures that the specific requirements of the Mangatarem LGU and its stakeholders are met systematically, minimizing risks and ensuring the timely delivery of a functional product.')
    
    add_para('The methodology chosen for this study is Rapid Application Development (RAD). This approach was selected because it emphasizes rapid prototyping and iterative delivery over strict planning. Given the dynamic nature of tourism information and the need to accommodate the evolving input from various Barangay Representatives and the LGU, RAD allows the developers to quickly adapt to feedback without disrupting the overall project timeline.')
    
    add_para('Rapid Application Development is an agile-based methodology characterized by its flexible, user-centric approach. Its key principles involve continuous stakeholder engagement, where users actively participate in reviewing prototypes. This methodology is typically utilized in projects where user interface constraints are critical, and requirements might shift as the stakeholders visualize the developing software. The primary advantage of RAD is its capability to significantly reduce development time while maintaining high user satisfaction through iterative refinement.')

    add_para('[RAD Methodology Image Placeholder]', style='Normal', alignment=WD_PARAGRAPH_ALIGNMENT.CENTER)
    add_para('(Note: Placeholder generic image for illustration. Replace with the specific RAD image from the defense/design assets.)', alignment=WD_PARAGRAPH_ALIGNMENT.CENTER)

    add_para('The phases of the RAD methodology utilized by the developers are broken down as follows:')
    
    phases = [
        ("Requirements Planning:", "In this initial phase, the developers collaborated with the LGU staff and potential users to identify the core problems of the fragmented manual system. Key objectives, such as centralizing data and establishing user roles (Admin, Barangay Representative, Public User), were defined."),
        ("User Design (Prototyping):", "Developers created interactive prototypes and wireframes of the Interactive Map, Admin Dashboard, and Contributor Portals using Figma. These designs were presented to stakeholders for iterative feedback, ensuring the UI/UX aligned with tourist and administrative expectations."),
        ("Construction:", "Following the approval of prototypes, the actual coding commenced. Utilizing HTML, CSS, JavaScript for the frontend and PHP/MySQL for the backend, developers built the functional modules in iterative cycles, continuously testing features against the refined requirements."),
        ("Cutover (Testing, Deployment, & Maintenance):", "The final phase involves comprehensive functional, usability, and security testing. Once the system meets the quality standards, it will be deployed to the LGU's live environment, followed by user training for the Tourism Officers and Barangay Representatives, and ongoing technical maintenance.")
    ]
    
    for i, (title, desc) in enumerate(phases, 1):
        p = doc.add_paragraph(style='List Number')
        p.add_run(title).bold = True
        p.add_run(f" {desc}")

    doc.add_heading('Sources of Data', level=2)
    add_para('The primary sources of data for this project are individuals, groups, and locations within the municipality of Mangatarem that hold crucial tourism and cultural information. Key sources include the LGU Tourism Office Staff, who provide the official policies, existing manual records, and municipal-level tourism initiatives. Barangay Officials and Representatives serve as vital sources for localized cultural data, specific landmarks, and grassroots community events. Additionally, existing municipal archives, physical maps, and local historical documents act as secondary data sources to establish the initial database of the system.')

    doc.add_heading('Data Gathering Techniques', level=2)
    add_para('To ensure comprehensive and accurate requirement analysis, the following data gathering techniques were applied:')
    
    techniques = [
        ("Interviews:", "Semi-structured interviews were conducted with the Tourism Office Staff and select Barangay Representatives. This technique was chosen to understand HOW the current manual sharing of tourism data operates and WHY delays occur. It was applied during the Requirements Planning phase to gather qualitative insights directly from the administrators."),
        ("Observation:", "The developers observed the daily workflow of the Tourism Office when handling inquiries and content updates. This was done to identify the specific bottlenecks in their traditional communication methods and to determine the necessary features for the Admin Dashboard."),
        ("Document Analysis:", "The team analyzed existing physical tourism brochures, fragmented social media posts, and municipal records. This technique was used to assess the current inconsistency of data formats, which justified the need for a standardized digital database.")
    ]
    
    for title, desc in techniques:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(title).bold = True
        p.add_run(f" {desc}")

    doc.add_heading('System Design', level=2)

    doc.add_heading('System Architecture', level=3)
    add_para('The System Architecture diagram illustrates the high-level structural overview of the Interactive Digital Cultural Map system. It defines how the different technological components interact to deliver the service from the users to the backend database.')
    add_para('[Insert System Architecture Diagram here]', alignment=WD_PARAGRAPH_ALIGNMENT.CENTER)
    add_para('The architecture follows a standard client-server model. Users (Admin, Barangay Representatives, Public Users, and Students) interact with the system via web browsers on their devices (Client side). The interface, built with HTML/CSS/JS, sends HTTP requests to the Web Server (handled by Apache/PHP). The application logic processes these requests—such as verifying admin credentials or fetching map coordinates—from the Backend Database (MySQL). Once data is retrieved or stored, the server sends the appropriate response back to the client interface. This architecture ensures a secure separation between the user interface and the sensitive central repository.')

    doc.add_heading('Existing Process Flowchart', level=3)
    add_para('The flowchart below illustrates the manual/current process of managing and accessing tourism information before the introduction of the digital system.')
    add_para('[Insert Existing Process Flowchart here]', alignment=WD_PARAGRAPH_ALIGNMENT.CENTER)
    add_para('The flowchart begins with an individual seeking tourism information or a barangay attempting to update an event. Tourists typically rely on fragmented social media searches or must physically visit the Tourism Office. For data updates, barangay officials submit physical files or use informal chat channels to notify the LGU. The Tourism Office then manually collates this information, a process that is highly prone to delays and inconsistencies. Ultimately, this results in irregular public updates and a high risk of confusion, visibly demonstrating the inefficiencies of the current workflow.')

    doc.add_heading('Dataflow Diagram (DFD)', level=3)
    add_para('A Dataflow Diagram (DFD) is utilized to map out the flow of information for any process or system. It highlights where data originates, how it is processed within the system, and where it is stored or outputted.')
    add_para('[Insert Data Flow Diagram Level 0/1 here. Ensure compliance with external entity (rectangle), process (rounded square), data store, and flow lines formatting]', alignment=WD_PARAGRAPH_ALIGNMENT.CENTER)
    add_para('The DFD details the interactions between the main external entities and the system. Public Users/Tourists send search queries (requests) to the system and receive map data, cultural profiles, and location details in return. Barangay Representatives (Contributors) input new content (photos, history, events) into the system\'s processing module, which temporarily stores it for review. The System Administrator interacts with the moderation process, receiving pending submissions and sending approval/rejection statuses. Approved data is then formatted and committed to the main Central Database (Data Store), making it available to the public interface.')

    doc.add_heading('Entity-Relationship Diagram (ERD)', level=3)
    add_para('The Entity-Relationship Diagram (ERD) visually represents the logical structure of the system\'s database by defining the entities, their attributes, and the relationships connecting them.')
    add_para('[Insert Entity-Relationship Diagram here. Ensure primary keys are underlined and cardinality is indicated]', alignment=WD_PARAGRAPH_ALIGNMENT.CENTER)
    add_para('The ERD illustrates the core data tables required for the system. The USERS entity stores credentials and role types (Admin, Contributor), dictating access levels. The BARANGAY_PROFILE entity holds localized data and has a one-to-many relationship with the TOURIST_SPOT and CULTURAL_EVENT entities, as one barangay can have multiple spots and events. TOURIST_SPOT contains attributes such as Spot_ID (Primary Key), Name, Description, Latitude, Longitude, and Media_URL. The SUBMISSION_LOG entity links to both the USERS (who submitted it) and the TOURIST_SPOT/CULTURAL_EVENT to track the status (Pending, Approved, Rejected) executed by the Administrator.')

    doc.add_heading('Implementation Plan', level=2)
    add_para('The successful deployment of the Interactive Digital Cultural Map requires a structured implementation plan encompassing a timeline, deployment strategy, and resource allocation.')

    doc.add_heading('Project Timeline (Gantt Chart overview):', level=3)
    timeline = [
        "Weeks 1-2: Requirements Planning and initial data gathering.",
        "Weeks 3-4: User Design and Figma prototyping.",
        "Weeks 5-10: Construction phase (Frontend and Backend development).",
        "Weeks 11-12: System Testing (Functional, Usability, Security) and bug fixing.",
        "Week 13: Cutover, user training, and final deployment."
    ]
    for item in timeline:
        doc.add_paragraph(item, style='List Bullet')
    add_para('(Note: visually represent this using a Gantt Chart in the final document version).')

    doc.add_heading('Deployment Plan:', level=3)
    add_para('The deployment will follow a phased approach. Initially, a pilot test will be conducted internally with the Tourism Office and a select few Barangay Representatives to validate the content moderation flow. Following pilot adjustments, the system will be migrated to a live production web hosting server. Finally, a formal launch will be coordinated with the LGU, alongside the distribution of customized training manuals for administrators and contributors.')

    doc.add_heading('Resource Requirements:', level=3)
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Hardware:').bold = True
    p.add_run(' A minimum of an Intel Core i5 machine with 8GB RAM for the administrative operator at the LGU; standard smartphones/PCs for Public Users and Contributors.')
    
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Software:').bold = True
    p.add_run(' A reliable cloud-hosting service with SSL certification (HTTPS) for deployment; MySQL database server; standard updated web browsers (Chrome, Edge, Safari).')
    
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Human Resources:').bold = True
    p.add_run(' At least one trained IT/Tourism staff member to act as the permanent System Administrator; designated Barangay Representatives committed to content contribution.')

    # --- CHAPTER 3 CONTENT ---
    doc.add_page_break()
    doc.add_heading('Chapter 3: Results and Discussion', level=1)

    add_para('(Note: As per the BCC BSIT Capstone Project Guide Revised 2025, Capstone 1 focuses exclusively on Chapters 1, 2, and the system design/features of Chapter 3. The actual implementation results, deployment findings, and final evaluation scores will be completed during Capstone 2. This chapter currently outlines the expected system features per user role and the planned testing and evaluation methodologies.)', bold=True)

    doc.add_heading('System Features and Modules', level=2)
    add_para('The Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan is designed to address the challenges of fragmented manual tourism processes. The system is divided into specific modules tailored to the needs and access privileges of its key stakeholders.')

    # Module 1
    doc.add_heading('1. System Administrator (Tourism Office Staff / IT Staff)', level=3)
    add_para('The System Administrator represents the highest level of access and is the core regulatory body of the platform, ensuring all published data is accurate and appropriate.')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Content Moderation Module:').bold = True
    p.add_run(' A centralized dashboard where the Admin receives, reviews, and either approves or rejects cultural and tourism data submissions from Barangay Representatives.')
    
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('User Assessment and Management:').bold = True
    p.add_run(' Ability to manage user accounts, assign or revoke access permissions for Contributors, and monitor audit logs of system activity.')
    
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Platform Operations:').bold = True
    p.add_run(' Tools to oversee general platform maintenance, configure map settings, and update global LGU announcements or emergency tourism notices.')

    # Module 2
    doc.add_heading('2. Barangay Representative (Contributor)', level=3)
    add_para('The Barangay Representative acts as the localized data source, bridging the gap between grassroots cultural events and the municipal database.')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Content Submission Portal:').bold = True
    p.add_run(' A dedicated interface allowing representatives to draft and submit proposals detailing local history, new attractions, and upcoming community events within their specific jurisdiction.')
    
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Media Upload Capabilities:').bold = True
    p.add_run(' Features enabling the secure upload of localized photos and videos to visually enhance the cultural profile of their barangay.')
    
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Update and Edit Tracking:').bold = True
    p.add_run(' Ability to request updates to previously approved information to ensure the interactive map remains current with real-world changes.')

    # Module 3
    doc.add_heading('3. Public User (Tourists / Visitors)', level=3)
    add_para('This module focuses heavily on UI/UX to ensure tourists have an engaging, accessible, and informative experience without requiring an account.')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Interactive Digital Cultural Map:').bold = True
    p.add_run(' A dynamic, visually engaging geographic map that allows users to navigate the municipality and locate specific attractions (e.g., Manleluag Spring).')
    
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Search and Filter Functions:').bold = True
    p.add_run(' Tools to easily query specific points of interest based on categories (e.g., historical sites, nature, dining) or general keywords.')
    
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Pop-up Details and Routing:').bold = True
    p.add_run(' Clicking on a map pin reveals rich multimedia pop-up details, cultural background information, and suggested routes/directions to the landmark.')

    # Module 4
    doc.add_heading('4. Students and Researchers (Academic Users)', level=3)
    add_para('Designed to support the academic community, this module provides structured access to the municipality\'s heritage records.')
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Historical Data Archives:').bold = True
    p.add_run(' Access to detailed barangay profiles, historical data, and cultural traditions specifically formatted for academic research and data gathering.')
    
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Heritage Study Tools:').bold = True
    p.add_run(' Capabilities to read comprehensive articles regarding local practices and community history, ensuring reliable educational resources are readily available.')

    doc.add_heading('Evaluation Results', level=2)
    add_para('(Note: This section will remain a placeholder detailing the Evaluation Plan for Capstone 1. The actual statistical results and interpretation will be conducted in Capstone 2).', bold=True)

    doc.add_heading('Testing Plan', level=3)
    add_para('The evaluation of the system is a critical component to ensure the computing solution resolves the identified problems effectively. The testing plan is designed to validate the system against the objectives set in Chapter 1. The evaluation will utilize the ISO/IEC 25010 Software Quality Standards as the primary framework.')
    
    add_para('The following quality characteristics will be tested:')
    
    tests = [
        ("Functional Suitability:", "To evaluate if the interactive map correctly filters locations, if the submission portal accurately transmits data to the Admin, and if the moderation module effectively publishes approved content. User Acceptance Testing (UAT) will be conducted involving actual Tourism Office staff and Barangay officials to verify these workflows."),
        ("Performance Efficiency:", "To assess the loading speed of the interactive map and multimedia pop-ups under typical traffic loads. Stress testing will simulate multiple concurrent public users accessing the map simultaneously."),
        ("Usability:", "To measure the user-friendliness of both the public map interface and the backend Admin Dashboard. The System Usability Scale (SUS) will be administered to a sample group of tourists and local administrators to gather quantitative feedback."),
        ("Security:", "To ensure the Contributor Portal and Admin Dashboard are protected against unauthorized access, and that content cannot be published without proper LGU approval.")
    ]
    
    for i, (title, desc) in enumerate(tests, 1):
        p = doc.add_paragraph(style='List Number')
        p.add_run(title).bold = True
        p.add_run(f" {desc}")

    doc.add_heading('Evaluation Instrument', level=3)
    add_para('The primary evaluation instrument will be a modified Likert-scale questionnaire based on the ISO/IEC 25010 criteria. The questionnaire will target the specific user groups (Admin, Contributors, Tourists, and Students).')
    
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Part 1:').bold = True
    p.add_run(' Demographic profile of the respondents (e.g., Role, Age, Technical Proficiency).')
    
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Part 2:').bold = True
    p.add_run(' Assessment of Functional Suitability, Performance Efficiency, Usability, and Security, structured as statements where respondents indicate their level of agreement (e.g., "5 - Strongly Agree" to "1 - Strongly Disagree").')
    
    p = doc.add_paragraph(style='List Bullet')
    p.add_run('Part 3:').bold = True
    p.add_run(' Open-ended section for qualitative suggestions and feedback regarding the interactive map\'s features and the content contribution process.')

    add_para('(The findings, statistical treatment of data, and interpretation of these evaluation results will proudly constitute the core of Chapter 3 during the final Capstone 2 defense).')

    return doc

# Generate and save
doc = create_document()
output_path = "Chapter_1_to_3_Consolidated.docx"
doc.save(output_path)

output_path