# Defense Presentation Slide Outline
## Technical Diagrams Section - Slide-by-Slide Guide

---

## 📊 EXISTING POWERPOINT INTEGRATION

Your current presentation: `docs/ppt/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-System.pptx`

This guide shows where to insert the technical diagrams section.

---

## 🎯 RECOMMENDED SLIDE SEQUENCE

### Slide 1: Title Slide (Already exists)
**Content:** Project title, team members, adviser
**Speaker:** Brief introduction

---

### Slide 2: Problem Statement (Already exists or add)
**Content:** 
- Current manual process inefficiencies
- Paper-based data collection challenges
- Need for digital transformation

**Speaker:** "The Tourism Office of Mangatarem currently uses a manual, paper-based system for collecting heritage and tourism data. This creates several problems..."

**Time:** 1 minute

---

### Slide 3: Project Objectives (Already exists)
**Content:** 
- Digitize heritage data collection
- Streamline approval workflow
- Provide public access via interactive map

**Speaker:** "Our system addresses these challenges through three main objectives..."

**Time:** 1 minute

---

## 🔷 TECHNICAL DIAGRAMS SECTION (NEW)

### Slide 4: Flowchart of Existing Processes
**Visual:** `docs/diagrams/flowchart_p1.png` (or combined flowchart)

**Bullet Points:**
- Manual field surveys with 7 forms (01A-07)
- Manual encoding into Word/Excel
- Barangay submission → Admin review → Database
- **Bottlenecks:** Paper-based, error-prone, slow retrieval

**Speaker Notes:**
"Let me walk you through the current process flow. As you can see here, the process begins with manual field surveys where tourism officers fill out 7 different paper forms. These forms must then be manually encoded into digital formats, creating opportunities for errors. The key bottlenecks we identified are: [point to each on diagram]. These inefficiencies established the foundation for our proposed system."

**Time:** 4-5 minutes
**Team Member:** Member 1

---

### Slide 5: Entity-Relationship Diagram (Overview)
**Visual:** `docs/diagrams/erd.drawio` (full ERD or zoomed sections)

**Bullet Points:**
- 9 core entities
- Normalized to 3NF
- Role-based access control
- Approval workflow support

**Speaker Notes:**
"Our Entity-Relationship Diagram defines the data structure for the entire system. We have 9 core entities, all normalized to Third Normal Form to eliminate redundancy. Key entities include: USER for authentication with role-based access, ATTRACTION for tourism spots with GPS coordinates, and BARANGAYINFO for local cultural context. Notice how all relationships use foreign keys with referential integrity, and each entity includes status fields to support our approval workflow."

**Time:** 2 minutes (overview)
**Team Member:** Member 2

---

### Slide 6: ERD - Key Entities Detail
**Visual:** Zoomed sections of ERD (USER, ATTRACTION, BARANGAYINFO)

**Bullet Points:**
- **USER**: id (PK), username (UK), email (UK), role, is_approved
- **ATTRACTION**: id (PK), name, lat/lng, category, status, created_by (FK)
- **BARANGAYINFO**: id (PK), barangay_name, history, traditions, cultural_assets

**Speaker Notes:**
"Let me highlight three critical entities. The USER entity manages authentication with unique constraints on username and email. The ATTRACTION entity is our core content table, storing GPS coordinates for map display and foreign key references to both the submitter and barangay location. BARANGAYINFO preserves the cultural context for each barangay, including history, traditions, and cultural assets - this is what makes our system more than just a map."

**Time:** 2 minutes
**Team Member:** Member 2

---

### Slide 7: ERD - Relationships & Integrity
**Visual:** ERD with relationships highlighted

**Bullet Points:**
- USER → ATTRACTION (1:N)
- ATTRACTION → REVIEW (1:N)
- BARANGAYINFO → ATTRACTION (1:N)
- Cascade rules for data integrity

**Speaker Notes:**
"The relationships between entities enforce business rules. One user can submit multiple attractions, but each attraction has one submitter. One barangay contains many attractions. Reviews are tied to both users and attractions, enabling quality feedback. We've implemented cascade rules to maintain referential integrity - if a user is deleted, their favorites are removed but their attractions remain (with null submitter) to preserve content."

**Time:** 2 minutes
**Team Member:** Member 2

---

### Slide 8: Data Flow Diagram (Level 1)
**Visual:** `docs/diagrams/dfd-level-1-clean.png`

**Bullet Points:**
- 4 External Entities (ADMIN, TOURIST, Google OAuth, Mapbox API)
- 8 Main Processes
- 6 Data Stores
- Clear system boundaries

**Speaker Notes:**
"Our Level 1 Data Flow Diagram shows how data moves through the system. On the left, we have external entities: ADMIN and TOURIST users, plus third-party services like Google OAuth and Mapbox API. The 8 numbered processes represent major system functions. The open rectangles are data stores where information persists. Notice how all flows pass through the central system boundary - this ensures security and validation."

**Time:** 2 minutes (overview)
**Team Member:** Member 3

---

### Slide 9: DFD - Core Processes
**Visual:** DFD with processes 1.0, 2.0, 5.0 highlighted

**Bullet Points:**
- **1.0 User Authentication**: OAuth + session management
- **2.0 Content Management**: Create/update attractions & events
- **5.0 Admin Approval**: Moderation workflow

**Speaker Notes:**
"Let me trace a typical data flow. Process 1.0 handles authentication - users must log in before accessing admin features. Process 2.0 manages content creation - admins and barangay reps submit attractions and events. Process 5.0 is the approval gateway - only approved content becomes publicly visible. This three-step flow ensures security, content quality, and proper access control."

**Time:** 2 minutes
**Team Member:** Member 3

---

### Slide 10: DFD - Public-Facing Processes
**Visual:** DFD with processes 3.0, 4.0, 8.0 highlighted

**Bullet Points:**
- **3.0 Interactive Map Display**: Mapbox integration
- **4.0 Content Discovery**: Search & filter
- **8.0 Review & Feedback**: User ratings

**Speaker Notes:**
"For public users, Process 3.0 renders the interactive map using Mapbox API for base tiles and our database for attraction markers. Process 4.0 enables search and filtering by category, location, or keywords. Process 8.0 collects user reviews and ratings, which go through moderation before publication. This flow provides rich user experience while maintaining content quality."

**Time:** 2 minutes
**Team Member:** Member 3

---

### Slide 11: Software Development Methodology
**Visual:** Agile/Scrum cycle diagram

**Bullet Points:**
- Agile methodology (Scrum framework)
- 10 sprints × 2 weeks = 20 weeks total
- Continuous stakeholder feedback
- Iterative development

**Speaker Notes:**
"We adopted Agile methodology with 2-week sprints. This allowed us to incorporate continuous feedback from the LGU, which was crucial because they were discovering their own needs as they saw the system's capabilities. Sprint 0 focused on requirements gathering, Sprints 1-2 on design, Sprints 3-8 on development, Sprint 9 on testing, and Sprint 10 on deployment and training."

**Time:** 2 minutes (overview)
**Team Member:** Member 4

---

### Slide 12: Sprint Breakdown
**Visual:** Timeline showing sprint phases

**Bullet Points:**
- **Sprint 0**: Requirements & interviews (2 weeks)
- **Sprint 1-2**: System design, ERD, DFD (4 weeks)
- **Sprint 3-4**: Foundation - auth, database (4 weeks)
- **Sprint 5-6**: Content management (4 weeks)
- **Sprint 7-8**: Public features, map (4 weeks)
- **Sprint 9-10**: Testing & deployment (4 weeks)

**Speaker Notes:**
"Each sprint delivered working software. By Sprint 4, we had authentication and database working. Sprint 6 added the content management and approval workflow. Sprint 8 completed public features including the interactive map. This incremental approach meant the LGU could start testing core features halfway through development, not just at the end."

**Time:** 2 minutes
**Team Member:** Member 4

---

### Slide 13: Agile Benefits Realized
**Visual:** Before/After comparison or benefits list

**Bullet Points:**
- Early value delivery (features by Sprint 4)
- Adaptability to change (added approval workflow)
- Risk reduction (caught issues early)
- Stakeholder engagement (bi-weekly demos)

**Speaker Notes:**
"Agile delivered four key benefits. First, early value - the LGU had working features by week 8. Second, adaptability - when they requested rejection comments in the approval workflow, we added it in the next sprint. Third, risk reduction - we caught database design issues in Sprint 2, not at deployment. Fourth, engagement - bi-weekly demos kept the Tourism Office invested in the project."

**Time:** 1 minute
**Team Member:** Member 4

---

## 🔷 RETURN TO MAIN PRESENTATION

### Slide 14: System Features (Continue with existing slides)
**Content:** Your existing features slides
**Speaker:** Transition: "Now that you understand our technical foundation, let me show you the actual system features..."

---

### Slide 15-N: Continue with your existing presentation

---

## 📝 SLIDE DESIGN TIPS

### For Flowchart Slide:
- Use **red/orange** highlights for bottlenecks
- Add **callout boxes** for key pain points
- Include **⚠ emoji** for problem areas

### For ERD Slides:
- Use **color coding**: 
  - Blue for user-related entities
  - Green for content entities
  - Yellow for analytics entities
- **Zoom in** on complex sections
- Use **animation** to reveal relationships one at a time

### For DFD Slides:
- Use **arrows animation** to show data flow direction
- **Highlight** one process at a time
- Use **consistent colors** for external entities vs processes vs data stores

### For Methodology Slides:
- Use **timeline visualization** for sprint breakdown
- Include **photos** from sprint reviews/LGU meetings (if available)
- Add **metrics** (velocity, burndown) if you tracked them

---

## 🎤 TRANSITION SCRIPTS BETWEEN SLIDES

**Slide 4 → 5:**
"Now that we've seen the problems in the current process, let me show you how we structured the data to solve these issues."

**Slide 7 → 8:**
"With the data structure defined, let's now see how that data flows through the system."

**Slide 10 → 11:**
"These processes didn't build themselves. Let me explain our development approach that brought this all together."

**Slide 13 → 14:**
"This methodology delivered the features you're about to see. Let me now demonstrate the actual system."

---

## ⏱️ TIMING BREAKDOWN

| Section | Time | Percentage |
|---------|------|------------|
| Problem & Objectives | 2 min | 10% |
| Flowchart | 5 min | 25% |
| ERD (3 slides) | 6 min | 30% |
| DFD (3 slides) | 6 min | 30% |
| Methodology (3 slides) | 5 min | 25% |
| **Total** | **20 min** | **100%** |

**Note:** Adjust based on your total defense time allocation. For a 30-minute defense, spend 20 minutes on technical diagrams. For 45 minutes, spend 25-30 minutes.

---

## 🎯 ANIMATION SEQUENCE (PowerPoint)

### Slide 5 (Flowchart):
1. Click 1: Show start point
2. Click 2: Animate flow to "Manual Collection"
3. Click 3: Highlight bottleneck callouts
4. Click 4: Show full flow to completion

### Slide 6 (ERD Overview):
1. Click 1: Show all entities faded
2. Click 2: Highlight USER entity (full color)
3. Click 3: Highlight ATTRACTION entity
4. Click 4: Highlight BARANGAYINFO
5. Click 5: Show all entities

### Slide 8 (DFD):
1. Click 1: Show external entities
2. Click 2: Show processes one by one
3. Click 3: Show data stores
4. Click 4: Animate data flow arrows

### Slide 12 (Sprint Timeline):
1. Click 1: Show Sprint 0-2
2. Click 2: Show Sprint 3-6
3. Click 3: Show Sprint 7-10
4. Click 4: Show benefits callouts

---

## 🖨️ PRINTED BACKUP MATERIALS

Prepare these for panelists:

1. **Flowchart handout** (1 page, color if possible)
2. **ERD full diagram** (1 page, may be large)
3. **DFD Level 1** (1 page)
4. **Sprint timeline** (1 page)

**Print specs:**
- Size: A4 or Letter
- Quality: High resolution (300 DPI)
- Quantity: 5 copies (3 panelists + 2 backups)
- Binding: Stapled or in clear folder

---

## 💻 TECHNICAL SETUP CHECKLIST

**Day Before:**
- [ ] Test projector/display compatibility (HDMI, VGA, USB-C)
- [ ] Verify all diagrams display clearly on big screen
- [ ] Check animation timing (not too fast/slow)
- [ ] Test laser pointer or digital highlighting tool
- [ ] Backup presentation on USB + cloud + email
- [ ] Save PDF version as backup
- [ ] Verify video/audio if embedded

**Day Of:**
- [ ] Arrive 30 minutes early for setup
- [ ] Test microphone volume
- [ ] Verify slide advance remote works
- [ ] Have printed handouts ready
- [ ] Designate someone to manage slides if needed

---

## 🎨 COLOR SCHEME RECOMMENDATIONS

Match your existing presentation theme:

**Primary Colors:**
- Dark Blue: #1E3A8A (headers, titles)
- Light Blue: #3B82F6 (accents, highlights)
- Green: #10B981 (success, approved status)
- Red/Orange: #F59E0B (warnings, bottlenecks)
- Gray: #6B7280 (secondary text)

**Background:**
- White or very light gray (#F9FAFB)
- Avoid busy patterns or gradients

**Text:**
- Dark gray (#1F2937) for body text
- Black (#000000) for titles
- Minimum font size: 18pt for body, 24pt+ for titles

---

## 📊 DIAGRAM EXPORT SETTINGS

For best quality in PowerPoint:

**From Draw.io:**
1. File → Export As → PNG
2. Resolution: 300 DPI
3. Background: Transparent or White
4. Zoom: 100%
5. Check "Embed fonts" if using custom fonts

**From diagrams.net:**
1. File → Export → PNG
2. Quality: 100%
3. Scale: 2x (for high DPI displays)
4. Check "Transparent background" if overlaying

**File sizes:**
- Aim for < 2MB per image
- PowerPoint will compress, so start with high quality
- Keep original high-res versions for printing

---

## ✅ FINAL SLIDE REVIEW CHECKLIST

**Content:**
- [ ] All diagrams clearly visible
- [ ] Text is readable from back of room
- [ ] No typos in entity names or process labels
- [ ] Consistent terminology across slides
- [ ] All foreign keys marked with (FK)
- [ ] All primary keys underlined or marked (PK)

**Design:**
- [ ] Consistent font family throughout
- [ ] Consistent color scheme
- [ ] Adequate white space (not cluttered)
- [ ] Alignment consistent (left-align text)
- [ ] No orphaned text or cut-off diagrams

**Functionality:**
- [ ] All animations work correctly
- [ ] Slide transitions smooth
- [ ] Hyperlinks work (if any)
- [ ] Embedded videos play (if any)
- [ ] Speaker notes visible in presenter view

---

## 🎤 PRESENTATION MODE SETTINGS

**PowerPoint:**
- Use "Presenter View" to see notes
- Set slide timing if auto-advance needed
- Disable screensaver during presentation
- Turn off notifications (Focus Assist on Windows)

**Google Slides:**
- Enable "Presenter Tools"
- Download offline copy as backup
- Test internet connection if streaming

**PDF Backup:**
- Export as PDF in case PowerPoint fails
- Keep formatting locked
- Smaller file size for easy sharing

---

**You're now ready to deliver a professional, well-structured technical diagrams presentation. Good luck! 🎓**
