# Administrative Guide

This guide is for **Admin** (LGU) and **Contributor** (Barangay Representative) roles. It explains how to manage content on the Mangatarem Cultural Map platform.

> [!NOTE]
> For detailed **Contributor**-specific guidance, see the [Contributor Guide](file:///d:/porjects/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan/docs/contributor_guide.md).

---

## Role Overview

### Admin Role
- **Full access** to the system, including user approval, data management across all barangays, and system configuration
- **Content moderation** for all submissions (attractions, events, gallery items, reviews)
- **User management** including approving/rejecting contributor accounts
- **System-wide analytics** and reporting

### Contributor Role
- **Barangay-specific** content submission and management
- Can submit attractions, events, and gallery items for their assigned barangay
- Content requires admin approval before publication
- Limited analytics for own submissions

---

## Content Approval Workflow

### Overview

The platform implements a **three-stage approval system** for all user-generated content:

```
Submission → Pending Review → Admin Review → Approved/Rejected → Published/Returned
```

### Content Types Requiring Approval

| Content Type | Submitter | Approval Required | Review Fields |
|--------------|-----------|------------------|---------------|
| **Attractions** | Contributors | Yes | Name, description, category, location, image |
| **Events** | Contributors | Yes | Title, description, date, location, category |
| **Gallery Items** | Contributors | Yes | Image/video, caption, quality check |
| **Reviews** | Public Users | Yes | Rating, comment, appropriateness |
| **Contributor Accounts** | New Users | Yes | Barangay assignment, credentials verification |

---

## Approval Process (Step-by-Step)

### 1. Reviewing Pending Attractions

**Access**: Admin Dashboard → **Content Management** → **Pending Attractions**

**Review Criteria**:
- **Accuracy**: Location coordinates match the description
- **Quality**: Clear, high-resolution image (> 1280x720)
- **Completeness**: All required fields filled (name, description, category, location)
- **Appropriateness**: Content aligns with tourism/cultural goals
- **Barangay**: Attraction is within the contributor's assigned barangay

**Actions**:

✅ **Approve**:
1. Verify all information is accurate
2. Click **"Approve"** button
3. System automatically:
   - Sets `status = 'approved'`
   - Records `reviewed_by` (your user ID)
   - Sets `reviewed_at` to current timestamp
   - Sends email notification to contributor
   - Makes content publicly visible

❌ **Reject**:
1. Select reason for rejection
2. Provide feedback to contributor
3. Click **"Reject"** button
4. System retains submission data for resubmission

### 2. Reviewing Pending Events

**Access**: Admin Dashboard → **Content Management** → **Pending Events**

**Review Criteria**:
- **Date Validity**: Event date is in the future
- **Completeness**: All details provided (date, time, location)
- **Category**: Appropriate classification (Religious, Civic, Entertainment)
- **Image Quality**: Clear event poster or representative image

**Actions**: Same as attractions (Approve/Reject)

### 3. Reviewing Gallery Items

**Access**: Admin Dashboard → **Content Management** → **Pending Gallery**

**Review Criteria**:
- **Quality**: High resolution, well-composed
- **Relevance**: Culturally or tourism-related
- **Appropriateness**: Respectful, no offensive content
- **Consent**: People in photos have given consent (verified by contributor)

**Actions**: Same as attractions (Approve/Reject)

### 4. Reviewing User Reviews

**Access**: Admin Dashboard → **User Reviews** → **Pending**

**Review Criteria**:
- **Authenticity**: Legitimate review, not spam
- **Language**: Appropriate, no offensive content
- **Relevance**: Related to the attraction

**Actions**: Approve, Reject, or Flag for further review

### 5. Approving Contributor Accounts

**Access**: Admin Dashboard → **User Management** → **Pending Contributors**

**Verification Steps**:
1. **Identity**: Verify user's barangay affiliation
2. **Contact**: Email or phone confirmation
3. **Role**: Ensure they selected "Contributor" during registration
4. **Barangay Assignment**: Confirm assigned barangay is correct

**Approval Process**:
1. Review submitted information
2. Verify with barangay captain or LGU tourism office
3. Click **"Approve User"**
4. System sets `is_approved = True`
5. Contributor receives email with login instructions

---

## Role-Based Permissions

### Who Can Approve What?

| Action | Admin | Contributor | Public User |
|--------|-------|-------------|-------------|
| Approve Attractions | ✅ (All barangays) | ❌ | ❌ |
| Approve Events | ✅ (All barangays) | ❌ | ❌ |
| Approve Gallery Items | ✅ | ❌ | ❌ |
| Approve Reviews | ✅ | ❌ | ❌ |
| Approve Users | ✅ | ❌ | ❌ |
| Submit Attractions | ✅ | ✅ (Own barangay only) | ❌ |
| Submit Events | ✅ | ✅ (Own barangay only) | ❌ |
| Submit Gallery Items | ✅ | ✅ | ❌ |
| Write Reviews | ✅ | ✅ | ✅ (Registered users) |

### Review History Tracking

All approval actions are logged with:
- `reviewed_by`: Admin user ID who approved/rejected
- `reviewed_at`: Timestamp of the decision
- `status`: Current state (`pending`, `approved`, `rejected`)

**Viewing Review History**:
1. Navigate to content item
2. Click **"View Details"**
3. Review history shows:
   - Original submitter
   - Submission date
   - Reviewer name
   - Review date
   - Current status

---

## Managing Attractions

### Adding New Attractions (Admin)

1. **Access Dashboard**: Admin Dashboard → **Attractions** → **Add New**
2. **Provide Details**:
   - Name, precise location (map or manual entry), detailed description
   - Assign category (e.g., Nature, Historical)
   - Upload high-quality images
3. **Admin submitted content**: Auto-approved (bypasses review)

### Editing Approved Content

Only admins can edit approved content:
1. Find attraction in **All Attractions** list
2. Click **"Edit"**
3. Make changes
4. Click **"Save"** (no re-approval needed)

---

## Managing Events and Festivals

### Adding Events

**Access**: Admin Dashboard → **Events** → **Add New**

**Best Practices**:
- Submit events at least 2 weeks in advance
- Include complete schedule information
- Provide contact information for inquiries

### Archiving Past Events

Events automatically move to "Past Events" after their date. To archive manually:
1. Navigate to **Past Events**
2. Select event
3. Click **"Archive"** to hide from public view

---

## Gallery Management

### Curating Media

**Access**: Admin Dashboard → **Gallery** → **All Items**

**Actions**:
- **Feature**: Highlight exceptional photos on homepage
- **Remove**: Delete inappropriate or low-quality items
- **Organize**: Tag items to specific attractions or events

---

## User Management (Admins Only)

### Approving Contributors

**Process**:
1. **Review Request**: Admin Dashboard → **Users** → **Pending**
2. **Verify**:
   - Confirm barangay affiliation
   - Check credentials
   - Contact user if needed
3. **Approve**: Click **"Approve"**, user receives email
4. **Assign Barangay**: Ensure correct barangay is assigned

### Role Assignment

Change user roles:
1. Navigate to **User Management**
2. Find user
3. Click **"Edit Role"**
4. Select: Admin, Contributor, or User
5. **Save**

### Revoking Access

To revoke contributor access:
1. Find user in **User Management**
2. Click **"Edit"**
3. Set `is_approved = False` or change role to "User"
4. User loses content submission privileges

---

## Analytics and Reporting

### Dashboard Overview

**Access**: Admin Dashboard → **Analytics**

**Metrics Available**:
- **Page Views**: Total site traffic
- **Popular Attractions**: Most viewed attractions
- **Barangay Engagement**: Which barangays have most content
- **User Activity**: Submission trends over time
- **Pending Queue**: Number of items awaiting review

### Generating Reports

1. Select date range
2. Choose report type:
   - Content submissions by barangay
   - User engagement statistics
   - Review turnaround time
3. Click **"Generate Report"**
4. Export as CSV or PDF

---

## Best Practices for Admins

### 1. Timely Reviews
- **Target**: Review submissions within 24-48 hours
- **Priority**: Events with upcoming dates
- **Batching**: Review similar content types together for efficiency

### 2. Consistent Standards
- Use the same criteria for all submissions
- Document rejection reasons clearly
- Provide actionable feedback to contributors

### 3. Communication
- Respond to contributor inquiries promptly
- Announce policy changes via platform notifications
- Hold periodic training sessions for contributors

### 4. Quality Control
- Periodically audit approved content
- Remove outdated or inaccurate information
- Update attractions with new photos or details

### 5. Backup and Maintenance
- Regular database backups (automated via Supabase)
- Monitor system performance
- Report technical issues to development team

---

## Troubleshooting

### Issue: Cannot Approve Content

**Possible Causes**:
- Not logged in as admin
- Session expired

**Solution**:
- Log out and log back in
- Verify you have admin role

### Issue: Approval Not Reflecting Immediately

**Cause**: Browser cache

**Solution**: Hard refresh (Ctrl + F5) or clear browser cache

---

## Additional Resources

- **[Contributor Guide](file:///d:/porjects/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan/docs/contributor_guide.md)** - For barangay representatives
- **[User Manual](file:///d:/porjects/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan/docs/user_manual.md)** - For public visitors
- **[Architecture Guide](file:///d:/porjects/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan/docs/architecture.md)** - Technical documentation
- **[Database Migration Guide](file:///d:/porjects/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan/docs/database_migration.md)** - Schema management

---

**Last Updated**: 2026-02-12
