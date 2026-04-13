# Deployment Guide (Vercel + Supabase)

This guide provides the steps to deploy and maintain the **Interactive Digital Cultural Map** in a production environment.

## 1. Prerequisites

- **Supabase Account**: For the PostgreSQL database.
- **Vercel Account**: For serverless hosting.
- **Python 3.12+**: For local builds and testing.

---

## 2. Supabase Configuration

### Database Setup
1. Create a new project in Supabase.
2. Go to **Settings > Database**.
3. Locate the **Connection String** for PostgreSQL.
4. **Important**: Use the **Transaction Pooler** (Port 6543) for Vercel functions to prevent connection exhaustion.

### Initial Schema Migration
1. Copy the contents of your local migration SQL or a full schema dump.
2. Go to **SQL Editor** in Supabase and run the script.
3. Verify that all 19+ tables (including Heritage Registry) exist in the **Table Editor**.

---

## 3. Vercel Configuration

### Environment Variables
Configure the following variables in the **Vercel Project Settings > Environment Variables**:

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Long random string for session security. Generate with: `openssl rand -hex 32` |
| `DATABASE_URL` | Supabase pooler URI (`postgresql://postgres:[PASSWORD]@...:6543/postgres`). |
| `SUPABASE_URL` | Your Supabase project URL. |
| `SUPABASE_KEY` | Your Supabase Service Role or Anon key. |
| `FLASK_ENV` | Set to `production`. |
| `MAIL_SERVER` | SMTP server for notifications. |
| `MAIL_USERNAME` | SMTP account email. |
| `MAIL_PASSWORD` | SMTP account password. |

**Security Note**: Never commit `SECRET_KEY` or passwords to version control. Use Vercel's encrypted environment variables.

### Build Settings
- **Framework Preset**: Other (Static / Dynamic)
- **Output Directory**: `static`
- **Install Command**: `pip install -r requirements.txt`

---

## 4. Post-Deployment Verification

### Security Verification

Before going live, complete the [Deployment Security Checklist](DEPLOYMENT_SECURITY_CHECKLIST.md):

1. **Security Headers**: Verify CSP, HSTS, X-Frame-Options, etc.
   ```bash
   curl -I https://your-domain.com
   ```

2. **Cookie Security**: Check HttpOnly, Secure, and SameSite flags in browser DevTools

3. **Rate Limiting**: Test authentication endpoints return 429 after limit exceeded

4. **XSS Protection**: Submit test payloads to verify sanitization

### Functional Verification

1. **Cold Start**: Visit the home page. The first load should take <1.5s due to lazy-loaded database drivers.
2. **API Check**: Visit `/api/attractions`. Verify you receive a JSON response.
3. **Map Check**: Ensure the Leaflet interactive map loads and displays markers without error.
4. **Auth Check**: Test the login and registration flows.

## 5. Maintenance and Logging

- **Vercel Logs**: Monitor real-time logs at **Vercel > Activity > Logs**.
- **Supabase Logs**: View database query errors at **Supabase > Settings > Database > Logs**.
- **Rate Limits**: If users report 429 errors, adjust the `FLASK_LIMITER` settings in `app.py`.
