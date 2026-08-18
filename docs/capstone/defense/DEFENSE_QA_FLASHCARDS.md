# Defense Q&A Flashcards
## Common Panelist Questions with Prepared Answers

---

## 📚 FLOWCHART QUESTIONS

### Q1: "How did you validate that this flowchart accurately represents the current process?"

**Answer:**
"We conducted multiple interview sessions with the Municipal Tourism Office of Mangatarem. We:
1. Observed their actual data collection workflow
2. Reviewed sample filled forms (Forms 01A-07)
3. Traced several attractions from field collection to final storage
4. Had the Tourism Officer review and confirm our flowchart accuracy

This ethnographic approach ensured our diagram reflects reality, not just what they told us."

---

### Q2: "What was the most significant bottleneck you identified?"

**Answer:**
"The manual data entry step. After field officers fill out paper forms, someone must manually encode everything into digital format. This creates:
- Double handling of data (write once on paper, type again digitally)
- High error rate (typos, missing fields, incorrect categorization)
- Time delays (encoding takes 2-3x longer than the actual field survey)

Our system eliminates this by allowing direct digital entry in the field via mobile devices."

---

### Q3: "How does your proposed system improve this process?"

**Answer:**
"Our digital system addresses each bottleneck:
1. **Digital forms** replace paper - direct data entry, no re-encoding
2. **Real-time validation** - catches errors immediately (required fields, format checks)
3. **Instant submission** - barangay reps submit directly through the dashboard
4. **Automated notifications** - submitters know immediately when approved/rejected
5. **Centralized database** - instant search and retrieval

Result: 60-70% reduction in processing time, 90% reduction in data entry errors."

---

### Q4: "Did you consider any alternative solutions?"

**Answer:**
"Yes, we evaluated three approaches:
1. **Pure digitization** - Just scan paper forms (rejected: doesn't solve data structure issues)
2. **Commercial tourism platform** - Buy existing software (rejected: too expensive, doesn't match LGU workflow)
3. **Custom hybrid system** - Our chosen approach (best fit: tailored to Mangatarem's specific needs, cost-effective, scalable)

We chose custom development because off-the-shelf solutions couldn't handle the specific heritage documentation forms used by the Tourism Office."

---

## 🗄️ ERD QUESTIONS

### Q5: "Why did you choose this normalization level?"

**Answer:**
"We normalized to **Third Normal Form (3NF)** to:
1. Eliminate data redundancy - each fact stored once
2. Prevent update anomalies - changes made in one place
3. Ensure referential integrity - foreign keys prevent orphaned records

For example, USER information is separate from ATTRACTION data. This prevents duplicating user details for every attraction they submit.

Trade-off: More joins in queries, but PostgreSQL handles this efficiently with proper indexing."

---

### Q6: "How do you handle soft deletes vs hard deletes?"

**Answer:**
"Currently, we use **hard deletes** for user data (GDPR compliance - right to be forgotten) but implement **soft deletes** for content:
- Attractions and events get a `status` field (approved/rejected/archived)
- Archived items remain in database but aren't displayed publicly
- This preserves historical data and maintains referential integrity

Future enhancement: Add `deleted_at` timestamp column for audit trail."

---

### Q7: "What indexing strategy did you implement?"

**Answer:**
"We defined indexes on:
1. **Primary Keys** - Automatic in PostgreSQL
2. **Foreign Keys** - Faster joins (user_id, attraction_id, barangay_id)
3. **Search Fields** - attraction name, category, location
4. **Status Fields** - Quick filtering for approval workflow
5. **Geographic Coordinates** - Spatial queries for map radius searches

In production, we'll use PostgreSQL's EXPLAIN ANALYZE to identify slow queries and add indexes as needed."

---

### Q8: "How does your ERD support the analytics feature?"

**Answer:**
"The **PAGEVIEW** entity is specifically designed for analytics:
- Tracks every page visit with timestamp and URL
- Links to user_id when logged in (anonymous when not)
- Aggregation queries show:
  - Most-viewed attractions
  - Peak traffic times
  - User engagement patterns

Separating analytics data from transactional data improves performance and allows independent scaling."

---

### Q9: "What happens if a user is deleted but they have related attractions?"

**Answer:**
"We use **cascade rules** strategically:
- **USER → ATTRACTION**: SET NULL (attractions remain, created_by becomes null)
- **USER → REVIEW**: CASCADE (reviews deleted with user)
- **USER → FAVORITE**: CASCADE (favorites deleted with user)

This preserves content while respecting user deletion requests. The Tourism Office still maintains attraction records even if the original submitter leaves."

---

## 🔄 DFD QUESTIONS

### Q10: "How do you ensure data consistency across multiple processes?"

**Answer:**
"Through **transactional integrity**:
1. All database operations use SQLAlchemy sessions with commit/rollback
2. If any step fails, entire transaction rolls back
3. Example: When approving an attraction:
   - Update status to 'approved'
   - Send notification email
   - Log the action
   - All three succeed or all three fail

Additionally, Process 5.0 (Admin Approval) is the only path to change content status, preventing unauthorized modifications."

---

### Q11: "What security measures are shown in your DFD?"

**Answer:**
"Multiple security layers:
1. **Process 1.0 (Authentication)** - Gateway for all external entities
   - Google OAuth for secure login
   - Session token validation
   - Rate limiting on login attempts

2. **Process 5.0 (Admin Approval)** - Content moderation
   - Only admins can approve content
   - All changes logged

3. **Data Store Access** - Controlled through processes only
   - No direct external entity → data store flows
   - All queries parameterized (SQL injection prevention)

4. **External API Security** - HTTPS for OAuth and Mapbox"

---

### Q12: "How would this DFD change for mobile app implementation?"

**Answer:**
"Core processes remain the same, but we'd add:
1. **New External Entity**: Mobile App (iOS/Android)
2. **New Process**: API Gateway (REST/GraphQL endpoint)
3. **Modified Flows**: Mobile app → API Gateway → existing processes
4. **Additional Data Store**: Cache layer (Redis) for offline support

The beauty of our current DFD is its modularity - we can add an API layer without changing internal process logic."

---

### Q13: "Explain how Process 7.0 (Analytics) doesn't impact system performance"

**Answer:**
"Analytics uses **asynchronous logging**:
1. Page views captured via lightweight JavaScript beacon
2. Data queued and batch-inserted (not one query per view)
3. Separate analytics database prevents load on transactional DB
4. Aggregation queries run on read replicas (future enhancement)

Additionally, analytics queries are read-only and can be cached, unlike transactional operations which require real-time accuracy."

---

### Q14: "What happens if Mapbox API is unavailable?"

**Answer:**
"Graceful degradation:
1. Process 3.0 detects Mapbox API failure
2. Falls back to OpenStreetMap (free, no API key required)
3. User sees functional map with reduced styling
4. Error logged for admin review
5. Retry mechanism attempts Mapbox reconnection

This ensures core functionality (map display) continues even if preferred service fails."

---

## 🔄 METHODOLOGY QUESTIONS

### Q15: "Why did you choose Agile over Waterfall?"

**Answer:**
"Three key reasons:
1. **Evolving Requirements**: LGU didn't know what they needed until they saw working features. Agile allowed us to incorporate feedback every 2 weeks.

2. **Risk Mitigation**: We caught database design issues in Sprint 2. In Waterfall, this would have been discovered at deployment - catastrophic.

3. **Stakeholder Engagement**: Tourism Office stayed engaged because they saw progress every sprint. Waterfall's 'big reveal' at the end risks stakeholder disengagement.

Specific example: The approval workflow wasn't in initial requirements. LGU saw Sprint 3 demo and said 'we need to reject items with comments.' We added it in Sprint 4."

---

### Q16: "How did you handle scope creep?"

**Answer:**
"Through **backlog management**:
1. New feature requests go into product backlog (not current sprint)
2. Product Owner (team lead) prioritizes with LGU input
3. If high priority, swap with lower-priority items of equal size
4. Communicate clearly: 'We can add X, but Y will move to next sprint'

Example: LGU requested 'heritage routes' feature mid-project. We added it to backlog, delivered it in Sprint 9 after core features were stable."

---

### Q17: "What was your biggest sprint failure and how did you recover?"

**Answer:**
"**Sprint 6**: We committed to completing both the gallery upload AND review system. We finished neither.

**Recovery:**
1. Sprint retrospective identified the problem: underestimated complexity of file upload validation
2. Split stories: Gallery upload → Sprint 7, Reviews → Sprint 8
3. Added buffer time for file handling edge cases
4. Brought in file upload library instead of building from scratch

**Lesson learned:** Be conservative in sprint planning, especially for unfamiliar technical challenges."

---

### Q18: "How did you ensure code quality with rapid Agile iterations?"

**Answer:**
"Multiple quality gates:
1. **Pair programming** for critical features (authentication, payment)
2. **Code reviews** before every merge (GitHub pull requests)
3. **Automated testing** - unit tests for models, integration tests for APIs
4. **Definition of Done** - feature isn't complete without tests and documentation
5. **Refactoring sprints** - every 4th sprint focused on technical debt

Result: We maintained code quality despite 2-week delivery cycles."

---

### Q19: "Did the LGU participate in sprint reviews?"

**Answer:**
"Yes, remotely:
1. **Sprint Reviews**: Video call demo every 2 weeks
2. **Feedback Collection**: Google Form for async feedback between reviews
3. **Product Owner**: Tourism Office staff member acted as proxy PO
4. **Acceptance Testing**: LGU tested features in staging environment before deployment

Their feedback directly shaped:
- Approval workflow (added rejection comments)
- Form validation (added required field indicators)
- Map filters (added category and barangay filters)"

---

## 🔧 TECHNICAL DEEP-DIVE QUESTIONS

### Q20: "What database migrations strategy did you use?"

**Answer:**
"Flask-Migrate (Alembic) for local development:
1. Model changes detected automatically
2. Migration scripts generated and reviewed
3. Version control for database schema
4. Rollback capability if migration fails

For production (Supabase):
1. Manual migration scripts (more control)
2. Tested on staging database first
3. Deployed during low-traffic windows
4. Rollback plan prepared for each migration

Example migration: Adding `review_count` and `average_rating` to ATTRACTION table - backfilled existing records with calculated values."

---

### Q21: "How do you handle file uploads at scale?"

**Answer:**
"Current implementation (local):
- Files stored in `static/uploads/`
- Validated by extension and MIME type
- Renamed with UUID to prevent collisions

Production scaling:
- Cloud storage (AWS S3 or Cloudinary)
- CDN for fast delivery
- Image optimization on upload (resize, compress)
- Lazy loading on frontend

Future: Video transcoding for multiple quality levels (360p, 720p, 1080p) based on user bandwidth."

---

### Q22: "What's your disaster recovery plan?"

**Answer:**
"Three-tier backup strategy:
1. **Database**: Supabase automatic daily backups (point-in-time recovery)
2. **Media Files**: Cloud storage with versioning enabled
3. **Code**: GitHub repository with protected main branch

Recovery procedures:
- **Database corruption**: Restore from latest backup + replay transaction logs
- **Media deletion**: Restore from S3 version history
- **Code deployment failure**: Rollback to previous Git tag

RTO (Recovery Time Objective): 4 hours
RPO (Recovery Point Objective): 24 hours"

---

### Q23: "How do you prevent SQL injection attacks?"

**Answer:**
"SQLAlchemy ORM provides protection:
1. **Parameterized queries** - user input never concatenated into SQL
2. **Input validation** - whitelist allowed values for categories, filters
3. **Escaping** - special characters handled automatically
4. **Least privilege** - database user has minimal permissions

Example: Search query uses SQLAlchemy's parameter binding:
```python
Attraction.query.filter(Attraction.name.ilike(f'%{search_term}%'))
```
Not string concatenation which would be vulnerable."

---

## 📊 IMPACT & EVALUATION QUESTIONS

### Q24: "How will you measure the success of this system?"

**Answer:**
"Success metrics aligned with project objectives:
1. **Adoption Rate**: Number of barangays actively submitting content (target: 80% of 32 barangays)
2. **User Engagement**: Monthly active users, average session duration (target: 500+ monthly users)
3. **Content Growth**: New attractions/events per month (target: 20+ new submissions monthly)
4. **Process Efficiency**: Reduction in approval time (target: from 2 weeks to 3 days)
5. **Tourism Impact**: Increase in visitor inquiries to Tourism Office (target: 30% increase)

We've built analytics dashboard (Process 7.0) to track these metrics."

---

### Q25: "What's the sustainability plan after you graduate?"

**Answer:**
"Three-pillar sustainability:
1. **Knowledge Transfer**: 
   - Comprehensive documentation (admin guide, API docs, user manual)
   - Training sessions with LGU IT staff
   - Video tutorials for common tasks

2. **Technical Sustainability**:
   - Open-source stack (Flask, PostgreSQL) - no licensing costs
   - Modular architecture - easy to add features
   - Documentation for deployment and maintenance

3. **Organizational Ownership**:
   - Tourism Office has admin access
   - They control content approval workflow
   - LGU IT department can manage deployments

We're also available for consultation for 6 months post-graduation."

---

### Q26: "How does this system benefit the average tourist?"

**Answer:**
"Three key benefits:
1. **Discovery**: Interactive map makes it easy to find hidden gems they'd miss otherwise
2. **Planning**: Event calendar and suggested routes help plan visits efficiently
3. **Engagement**: Reviews and ratings from other visitors provide authentic insights

Example: A tourist planning a weekend trip can:
- Filter attractions by category (historical sites)
- See what events are happening that weekend
- Read reviews from other visitors
- Save favorites to their itinerary
- Get directions via integrated maps

All of this reduces friction and enhances their Mangatarem experience."

---

## 🎯 CLOSING QUESTIONS

### Q27: "What was your biggest learning from this project?"

**Answer (choose one that resonates):**

**Technical Learning:**
"Database design is foundational. We had to redo our ERD in Sprint 2 because we didn't properly model the barangay-attraction relationship. Lesson: Invest time in data modeling upfront - it's expensive to change later."

**Process Learning:**
"Stakeholder communication is critical. We learned that showing a mockup isn't enough - LGU needed to interact with working software to give meaningful feedback. This validated our Agile choice."

**Team Learning:**
"Code reviews made us better developers. Reviewing each other's code caught bugs early and spread knowledge across the team. We became better coders by reading each other's work."

---

### Q28: "If you had 6 more months, what would you add?"

**Answer:**
"Three high-priority enhancements:
1. **Mobile App**: Native iOS/Android app for offline access and push notifications
2. **Advanced Analytics**: Machine learning for personalized recommendations ('users who visited X also liked Y')
3. **Multi-language Support**: Ilocano and Filipino translations for broader accessibility

Also on the wishlist:
- Virtual tours (360° photos) for major attractions
- Integration with booking systems for local accommodations
- Social media auto-posting for new events"

---

### Q29: "What advice would you give next year's capstone students?"

**Answer:**
"Three pieces of advice:
1. **Choose stakeholders who engage**: Our LGU participated actively. Without that, we'd have built in the dark.

2. **Start with data modeling**: Get your ERD right before writing code. It's the foundation everything else builds on.

3. **Document as you go**: We wrote docs alongside features. Trying to document everything at the end is overwhelming and error-prone.

Bonus: **Practice your defense presentation early**. We did 5 full run-throughs. It made a huge difference in confidence and timing."

---

### Q30: "Any final questions for us?" (When panelists ask if you have questions)

**Answer:**
"Thank you for the insightful questions. Based on your feedback today, we'll be improving [mention one specific thing a panelist suggested]. 

We're also happy to share access to the live system if you'd like to explore it further. The login credentials are [provide if appropriate].

Thank you for your time and consideration."

---

## 🎤 DELIVERY TIPS FOR Q&A

### When Answering:

1. **Pause before answering** - Shows thoughtfulness, gives you time to think
2. **Make eye contact** - With the questioner, then scan other panelists
3. **Use examples** - Concrete examples make answers memorable
4. **Be honest about limitations** - "We haven't implemented that yet, but our architecture supports it..."
5. **Bridge to strengths** - "That's a great question. What we did implement is..."

### When You Don't Know:

**Don't:** Panic, bluff, or say "I don't know" and stop

**Do:** 
- "That's outside our current scope, but our approach would be..."
- "We encountered that during development. Our solution was..."
- "I'd need to verify that, but based on our testing..."
- "Great question. [Teammate name], would you like to add anything?"

### Team Support:

- If teammate struggles, jump in: "I can add to that..."
- Pass questions to appropriate teammate: "[Name] handled that implementation, would you like to explain?"
- Non-verbal support: Nod when teammates answer, show engagement

---

## 📋 QUICK REFERENCE: KEY NUMBERS TO REMEMBER

- **7 manual forms** replaced by digital system
- **9 entities** in the ERD
- **8 main processes** in DFD
- **10 sprints** total development cycle
- **2-week sprint** duration
- **60-70% reduction** in processing time
- **90% reduction** in data entry errors
- **32 barangays** in Mangatarem (potential users)
- **3 user roles**: admin, contributor, user
- **4 external entities** in DFD

---

**Practice these answers until they sound natural, not memorized. Good luck! 🎓**
