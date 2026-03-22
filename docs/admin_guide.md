# Administrative Guide

This guide is for the LGU Tourism Office and system administrators responsible for maintaining the platform.

## Admin Dashboard

Access the dashboard at `/admin/dashboard`. The admin dashboard provides a high-level overview of system metrics, pending reviews, and recent activities.

### 1. Dashboard Overview
- **Pending Actions**: Count of attractions, events, and reviews awaiting approval.
- **Engagement Stats**: Total page views and user signups.
- **Registry Summary**: Breakdown of the 7 heritage form types.

---

## Content Moderation Workflow

Administrators are responsible for reviewing and approving all content submitted by Barangay Contributors.

### 1. Reviewing Attractions
1. Navigate to **Admin > Attractions**.
2. Click **Review** on any "Pending" attraction.
3. Verify the **Latitude** and **Longitude** accuracy.
4. Ensure photos in the **Gallery** follow community guidelines.
5. Click **Approve** to publish or **Reject** with feedback.

### 2. Reviewing events
1. Navigate to **Admin > Events**.
2. Verify the **Event Dates** and **Location**.
3. High-priority events can be marked for the **Home Page Calendar**.

---

## Cultural Heritage Registry (Forms 01-07)

The Heritage Registry is the core of the system's archival functionality. Administrators must review complex details for each profile.

### 1. Heritage Review Process
1. Navigate to **Admin > Heritage Registry**.
2. Filter by **Form Type** (e.g., "Form 01A - Natural Heritage").
3. Ensure that the **Primary Features** and **Significance** fields are correctly filled.
4. If a profile is linked to an existing attraction, verify the mapping consistency.

---

## User and Role Management

### 1. Promoting Users
Administrators can promote regular users to **Barangay Contributors**.
1. Go to **Admin > Users**.
2. Search for the user.
3. Edit the user and change the **Role** to `contributor`.
4. Assign the user to a specific **Barangay**.

### 2. Security Actions
- **Password Resets**: Admins can trigger reset emails for users.
- **Account Blocking**: Suspicious accounts can be deactivated.

---

## Newsletter Management

- **Subscribers**: View the list of active newsletter subscribers.
- **Analytics**: Track campaign reach and open status (if integrated).
