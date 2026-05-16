# System Credentials and Test Accounts

This document lists the default credentials for testing and development in the **Interactive Digital Cultural Map and Local Tourism Information System**.

> [!IMPORTANT]
> Change these passwords immediately when deploying to a production environment. 

## 🔐 Core Test Accounts

| Role | Username | Password | Access Level |
| :--- | :--- | :--- | :--- |
| **System Admin** | `admin` | `admin123` | Full control over users, heritage approvals, and site settings. |
| **Dining Owner** | `dining_owner` | `dining123` | Can manage Restaurant/Cafe menus and reviews. |
| **Hospitality Owner** | `hospitality_owner` | `hospitality123` | Can manage Inn/Hotel rooms and bookings. |
| **Test Owner** | `test_owner` | `owner123` | Generic Business Owner account for testing visitor logging. |
| **Tourist (Reviewer)** | `tourist` | `tourist123` | Standard user account — can browse the map and **write reviews**. |

---

## 👥 Proposed Test Accounts
*(If these do not exist in your local database, you can create them via the registration page)*

### 🏛️ Contributor / Cultural Office
*Used for managing cultural heritage profiles and attractions.*
- **Username:** `steward`
- **Password:** `steward123` (Suggested)
- **Role:** `contributor`
- **Description:** Can create and edit heritage profiles, but requires Admin approval for publication.

### 🎒 Tourist / Standard User ✅ Active
*Used for viewing the map and **writing reviews**.*
- **Username:** `tourist`
- **Password:** `tourist123`
- **Role:** `user`  
- **Status:** ✅ Account exists in local DB (`is_approved = True`)
- **Description:** Standard public access. Use this account to test the review and comment system.

---

## 🧪 Testing Reviews

1. Log in as `tourist` / `tourist123` at `http://localhost:5002/auth/login`
2. Visit any attraction: `http://localhost:5002/attractions/1`
3. Scroll down → **Community Reviews** section → **Write a Review** form
4. Select stars → add a comment → click **Submit Review**
5. Log in as `admin` / `admin123` → go to `http://localhost:5002/admin/reviews`
6. Click **Approve** → the review goes live on the attraction page

---

## 🚀 How to Access
1. Start the server: `python app.py`
2. Navigate to `http://localhost:5002/auth/login`
3. Enter the credentials from the table above.

## 🛡️ Role Definitions
- **`admin`**: System-wide authority.
- **`business_owner`**: Restricted to managing specific business entities (`ESTABLISHMENT`).
- **`contributor`**: Specialized content creators for cultural heritage.
- **`user`**: Public users with personal profiles and bookmarking capabilities.

---

## ⚙️ Environment Configuration (`.env`)

The application requires following variables in your `.env` file to function correctly:

| Variable | Description |
| :--- | :--- |
| `DB_PROVIDER` | Set to `sqlite` for local or `supabase` for production. |
| `SUPABASE_URL` | Your Supabase project URL. |
| `SUPABASE_KEY` | Your Supabase API key. |
| `mapbox_token` | Required for the interactive map display. |
| `SMTP_EMAIL` | Email used for password resets and notifications. |
| `SMTP_PASSWORD` | App password for the SMTP email account. |

---

## 📧 Email (SMTP) Credentials
*Current configuration is using a Gmail App Password for notifications.*
- **Service:** Gmail
- **Email:** `zani31349@gmail.com`
- **Purpose:** Password recovery and cultural heritage approval notifications.
