# Team Briefing: Technical Diagrams Defense
## Quick Reference for Team Members

---

## 🎯 YOUR ASSIGNMENT

**Read your section below and practice with the full guide in `DEFENSE_DIAGRAMS_EXPLANATION_GUIDE.md`**

---

## 👤 MEMBER 1: Flowchart of Existing Processes

**Time Allocation:** 4-5 minutes  
**Files to Display:** `docs/diagrams/flowchart_p1.png` through `flowchart_p4.png`

### Key Points to Hit:

✅ **Start:** "This shows how Mangatarem Tourism Office currently collects heritage data"

✅ **Process Flow:**
1. Manual field surveys with 7 paper forms (Forms 01A-07)
2. Manual encoding into Word/Excel
3. Barangay dashboard submission
4. Admin review (approve/reject decision point)
5. Database storage
6. Public access via interactive map

✅ **Bottlenecks to Highlight:**
- Paper forms = prone to damage/loss
- Manual entry = human errors
- No centralized search = slow retrieval
- Physical submission = approval delays

✅ **Closing:** "These inefficiencies justified building our digital system"

### Common Questions:
- **Q:** "How did you map this process?"  
  **A:** "Multiple interviews with Tourism Office + analysis of their actual forms"

---

## 👤 MEMBER 2: Entity-Relationship Diagram (ERD)

**Time Allocation:** 5-6 minutes  
**Files to Display:** `docs/diagrams/erd.drawio` or `erd_v1.drawio`

### Key Entities to Explain:

✅ **USER** - Authentication & roles (admin/contributor/user)
✅ **ATTRACTION** - Core tourism spots with lat/lng coordinates
✅ **EVENT** - Festivals and community activities
✅ **BARANGAYINFO** - Barangay historical/cultural data
✅ **GALLERYITEM** - Photos/videos with moderation
✅ **REVIEW** - User ratings and feedback
✅ **FAVORITE** - User saved attractions
✅ **PAGEVIEW** - Analytics tracking

### Relationships to Emphasize:

✅ USER → ATTRACTION (1:N) - One user submits many attractions
✅ ATTRACTION → REVIEW (1:N) - One attraction gets many reviews
✅ BARANGAYINFO → ATTRACTION (1:N) - One barangay has many attractions
✅ USER → FAVORITE (1:N) - Enables M:N between user and attractions

### Key Design Features:
- Primary Keys underlined
- Foreign Keys marked with (FK#)
- All entities in singular form (USER, not USERS)
- Status fields for approval workflow

### Common Questions:
- **Q:** "How does this support scalability?"  
  **A:** "Normalized design, indexed FKs, PostgreSQL with connection pooling"

---

## 👤 MEMBER 3: Data Flow Diagram (DFD)

**Time Allocation:** 5-6 minutes  
**Files to Display:** `docs/diagrams/dfd-level-1-clean.png`

### Components to Identify First:

✅ **External Entities** (Rectangles): ADMIN, TOURIST, Google OAuth, Mapbox API
✅ **Processes** (Rounded Squares): 1.0 through 8.0
✅ **Data Stores** (Open Rectangles): User_db, Content_db, Analytics_db
✅ **Data Flows** (Arrows): Show data movement direction
✅ **Main System** (Large Box): Entire system boundary

### Process Explanations:

✅ **1.0 User Authentication** - Login, OAuth, session management
✅ **2.0 Content Management** - Create/update attractions and events
✅ **3.0 Interactive Map Display** - Render map with Mapbox API
✅ **4.0 Content Discovery** - Search and filter functionality
✅ **5.0 Admin Approval** - Content moderation workflow
✅ **6.0 Favorite Management** - User bookmarks
✅ **7.0 Analytics & Reporting** - Track page views and engagement
✅ **8.0 Review & Feedback** - User ratings with moderation

### Data Stores:
- User_db, Content_db, Barangay_db, Analytics_db, UserPreferences_db, Feedback_db

### Common Questions:
- **Q:** "How does DFD show security?"  
  **A:** "Process 1.0 is security gateway - all flows must pass authentication first"

---

## 👤 MEMBER 4: Software Development Methodology

**Time Allocation:** 4-5 minutes  
**Display:** Agile/Scrum diagram

### Why Agile?

✅ Evolving requirements from LGU
✅ Needed continuous stakeholder feedback
✅ Risk mitigation through iterations
✅ Flexibility for changes
✅ Continuous improvement

### Sprint Breakdown:

✅ **Sprint 0** (2 weeks): Requirements gathering, interviews, user stories
✅ **Sprint 1-2** (4 weeks): System design, ERD, DFD, UI mockups
✅ **Sprint 3-4** (4 weeks): Foundation - auth, database, admin skeleton
✅ **Sprint 5-6** (4 weeks): Content management, approval workflow
✅ **Sprint 7-8** (4 weeks): Public features, map, gallery, reviews
✅ **Sprint 9** (2 weeks): Testing & QA
✅ **Sprint 10** (2 weeks): Deployment + LGU training

### Sprint Cycle:
Planning → Daily Standups → Development → Review → Retrospective

### Benefits Realized:
✅ Early value delivery (core features by Sprint 4)
✅ LGU engagement every 2 weeks
✅ Adaptability to change
✅ Early bug detection
✅ Better team alignment

### Common Questions:
- **Q:** "Why not Waterfall?"  
  **A:** "LGU was discovering needs as they saw capabilities. Waterfall would have locked us into incomplete requirements."

---

## 🎤 TRANSITION SCRIPTS

**Member 1 → Member 2:**  
"Now that we've seen the problems in the current process, let me pass it to [Name] who will explain how we structured the data to solve these issues."

**Member 2 → Member 3:**  
"With the data structure defined, [Name] will now show how that data flows through our system."

**Member 3 → Member 4:**  
"Now that you've seen how data moves through the system, [Name] will explain our development approach that brought this all together."

**Member 4 → Q&A:**  
"This completes our technical diagrams presentation. We're now ready for your questions."

---

## ⏰ TIMING CUES

Practice with these checkpoints:

- **Member 1:** Should be at "Bottlenecks" at minute 3
- **Member 2:** Should be at "Relationships" at minute 4
- **Member 3:** Should be at "Process 5.0" at minute 3
- **Member 4:** Should be at "Sprint Breakdown" at minute 2

**If running long:** Skip one example, don't rush through everything

---

## 💡 PRESENTATION HACKS

1. **Use a pointer** (physical or digital) to highlight what you're discussing
2. **Pause between sections** - let panelists absorb the information
3. **Make eye contact** - don't just read from notes
4. **If you get a question mid-presentation:** Answer, then say "Continuing from where I left off..."
5. **Nervous habit check:** Don't click pens, tap feet, or say "um" repeatedly
6. **Voice projection:** Speak louder than you think you need to
7. **Body language:** Stand straight, hands visible, don't cross arms

---

## 🚨 EMERGENCY BACKUP

**If technology fails:**
- Printed copies are in the folder
- Member 2 has USB backup
- Files also on Google Drive

**If you forget your lines:**
- Look at the diagram and describe what you see
- It's okay to pause and collect thoughts
- Team members can help jump in

**If panelist seems confused:**
- Slow down
- Use simpler language
- Offer to clarify after your section

---

## 📞 DAY-OF CONTACTS

**Team Leader:** [Fill in]  
**Presentation Coordinator:** [Fill in]  
**Technical Support:** [Fill in]

**Meeting Time:** [Fill in]  
**Defense Time:** [Fill in]  
**Location:** [Fill in]

---

## ✅ FINAL CHECKLIST (Day Before)

- [ ] All diagrams printed and laminated (or on tablet)
- [ ] Presentation file on USB + cloud + email
- [ ] Each member has printed this briefing
- [ ] Full team run-through completed
- [ ] Timing verified for each section
- [ ] Q&A practice session done
- [ ] Outfits prepared (formal/business attire)
- [ ] Sleep 8 hours before defense day

---

**Remember: You've worked hard on this. You know the system. Trust your preparation. Good luck! 🎓**
