**Binalatongan Community College Employee Information System**

*(Note: Change the header above to "Interactive Digital Cultural Map and Local Tourism Information System" if it shouldn't say "Employee Information System")*

**A Capstone Project Presented to the Faculty of the**   
**Information Technology Department**  
**Binalatongan Community College**  
**San Carlos City, Pangasinan**

**In Partial Fulfillment of the Requirements**  
**for the Degree of Bachelor of Science**  
**in Information Technology**

**Submitted by:**

**Jem Carlo Austria**  
**Maryjane Dalas**  
**Rea Solis**  
**Joy De Guzman**

**May 2024 / 2025** *(Adjust Year accordingly)*  

---

**APPROVAL SHEET**

This capstone project entitled **INTERACTIVE DIGITAL CULTURAL MAP AND LOCAL TOURISM INFORMATION SYSTEM FOR MANGATAREM, PANGASINAN** prepared and submitted by **JEM CARLO AUSTRIA, MARYJANE DALAS, REA SOLIS,** and **JOY DE GUZMAN** in partial fulfillment of the requirements for the degree **BACHELOR OF SCIENCE IN INFORMATION TECHNOLOGY,** has been examined and is recommended for acceptance and approval.  
                                                                            ____________________________  
						**[INSERT ADVISER NAME]**  
Adviser

               PANEL OF EXAMINERS

____________________________  
    **[INSERT CHAIRPERSON NAME]**  
	    Chairperson

___________________________		     ____________________________	  
      **[INSERT MEMBER 1 NAME]**	  	              **[INSERT MEMBER 2 NAME]**  
               Member                                                                 Member

	**ACCEPTED** and **APPROVED** in partial fulfillment of the requirements for the degree **BACHELOR OF SCIENCE IN INFORMATION TECHNOLOGY** on **[INSERT DATE]** with a grade of _______.

  ____________________________		             ____________________________  
   **[INSERT DEAN NAME]**	 	          **[INSERT PRESIDENT NAME]**	     
    Dean, Information Technology Department   		        College President		  
 

---

**Abstract** 

**Jem Carlo Austria, Maryjane Dalas, Rea Solis, Joy De Guzman, “Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan,”** Bachelor of Science in Information Technology, College of Information Technology, Binalatongan Community College, San Carlos City, Pangasinan, Philippines, [Insert Month Year].

Adviser: 	**[Insert Adviser Name]**   
 		
The tourism landscape in Mangatarem, Pangasinan is undergoing a digital transformation. Currently, information regarding its cultural and tourist spots is fragmented, relying heavily on traditional word-of-mouth and scattered social media posts. This capstone project, entitled "Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan," addresses these challenges by developing a centralized, interactive, and community-driven web platform. The system integrates an interactive mapping interface (using Mapbox GL JS) with a comprehensive cultural information portal, providing tourists, students, and stakeholders with seamless navigation and engaging cultural profiles. Built using the Rapid Application Development (RAD) methodology, the platform utilizes Python (Flask) for the backend, Tailwind CSS for the frontend, and a dual local-production database architecture (SQLite/Supabase). Key features include CBIS community stewardship for decentralized data management by barangay representatives across 82 barangays, a cultural heritage registry aligned with national standards, an events and festival directory, and an analytics dashboard for the LGU Tourism Office. The implementation of this system aims to bridge the information gap, foster cultural appreciation, and stimulate local economic growth by effectively promoting the municipality's rich heritage and tourism assets.


---

**Acknowledgement**

*(Insert personal acknowledgments here. Be sure to acknowledge your partner: Rachelle T. Cabornay, Senior Tourism Operations Officer, Municipal Economic Enterprise Office (M.E.O.), as well as your adviser, panelists, institution, and families.)*

---

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
|  | Purpose and Description ………………………………………..  | # |
|  | Objectives of the Study ……………………………………...…..   | # |
|  | Conceptual Framework (IPO) ……………………………..….. | # |
|  | Scope and Limitations …………………………………………… | # |
|  | Definition of Terms …………….……………………………..…..  | # |
|  | Review of Related Literature.……………………………..…… | # |
|  |  |  |
| **2** | **METHODOLOGY AND DESIGN** .…………………………. | # |
|  | Software Development Methodology (RAD) ……………………… | # |
|  | Sources of Data …………………………………………………… | # |
|  | Data Gathering Techniques…………………………………….. | # |
|  | System Design ..…………………………………………….......... | # |
|  |           System Architecture ……………………………………. | # |
|  |           Dataflow Diagram ………………………………………. | # |
|  |           Entity-Relationship Diagram ………………………… | # |
|  |           Implementation Diagram …………………………….. | # |
|  |  |  |
| **3** | **RESULTS AND DISCUSSION** |  |
|  | System Process Flowchart.………………………. | # |
|  | System Features and User Interfaces ………………………. | # |
|  | System Testing and Evaluation …………………....…………. | # |
|  | Implementation Results .…………………………………......... | # |
|  | Analysis of Results ………...………………………………......... | # |
|  | Discussion of Findings ………………..……………………….... | # |
|  |  |  |
| **4** | **RECOMMENDATIONS**.…………………………………………. | # |
|   |  |  |
| **Appendices** ………………………….……………………….…………………….. |  | # |
| **A** | Endorsement Letter ………………………………………………… | # |
| **B** | System Source Codes ………………………..…….…………….. | # |
| **C** | Database Schema (Actual Database Structure) ….……… | # |
| **D** | Survey/Evaluation Forms Used During Testing ………….. | # |
| **E** | Collected Sample Documents for Document Analysis/Data Gathering…..………………………………………. | # |
|  |  |  |
| **Curriculum Vitae** …………………………………………………………………. |  | # |

---

**List of Tables**

| Table | 		Title | Page |
| :---: | :---- | :---: |
| 1.1 | Users of the System and Roles | # |
| 4.1 | Hardware Requirements | # |
| 4.2 | Software and Service Requirements | # |
*(Add any other tables used in your manuscript)*

---

**List of Figures**

| Figure | 		Title | Page |
| :---: | :---- | :---: |
| 2.1 | Entity Relationship Diagram (ERD) | # |
| 2.2 | Data Flow Diagram (DFD) | # |
| 2.3 | Login and Security Flows | # |
| 2.4 | Registration & Validation Logic | # |
| 2.5 | Map Exploration Flow | # |
| 2.6 | System Architecture Design | # |

*(Note: Adjust the figure numbers to align with the chapter they are actually placed in, typically Chapter 2 for Design).*
