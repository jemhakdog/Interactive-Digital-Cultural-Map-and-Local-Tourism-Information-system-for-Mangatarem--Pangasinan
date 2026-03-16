# Explanation: User Login and Authentication Flows

This document details the multi-layered authentication system designed to accommodate different user types and security scenarios.

### 1. Standard Login
The primary entry for Admins, Contributors, and Registered Users. The system validates credentials and performs a **Role-Based Check** to route users to their appropriate dashboards (Admin Panel, Barangay Dashboard, or User Home).

### 2. Google OAuth Integration
Provides a "One-Tap" login experience for general visitors. 
- **Security Check**: Accounts with administrative or contributor roles are restricted from Using Google Login to ensure they utilize the more secure standard credentials.
- **Auto-Provisioning**: For new visitors, the system automatically creates a profile upon first Google login.

### 3. Account Recovery (Password Reset)
A secure token-based workflow triggered by the "Forgot Password" link. It utilizes time-sensitive email verification to allow users to regain access without administrator intervention.

### 4. Session Security (Logout)
Ensures user safety by terminating server-side sessions and clearing local authentication tokens, redirecting the user back to the public landing page.
