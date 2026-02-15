# Deployment Guide

**Interactive Digital Cultural Map and Local Tourism Information System for Mangatarem, Pangasinan**

This guide covers deploying the application to Vercel with Supabase as the production database.

---

## Overview

The application is optimized for deployment on Vercel's serverless platform with the following architecture:

- **Platform**: Vercel (Serverless Functions)
- **Database**: Supabase (PostgreSQL) with connection pooling
- **CDN**: Vercel Edge Network
- **Region**: Automatic edge deployment

---

## Prerequisites

Before deploying, ensure you have:

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Supabase Project**: Create a project at [supabase.com](https://supabase.com)
3. **GitHub Repository**: Code pushed to GitHub (recommended for CI/CD)
4. **Environment Variables**: Collected from Supabase and other services

---

## Environment Variables

### Required Variables

Configure these environment variables in your Vercel project settings:

| Variable | Description | Example | Source |
|----------|-------------|---------|--------|
| `SECRET_KEY` | Flask secret key for session encryption | `your-strong-secret-key-here` | Generate using `python -c "import secrets; print(secrets.token_hex(32))"` |
| `DATABASE_URL` | Supabase PostgreSQL connection string (pooler) | `postgresql://user:pass@host:6543/postgres` | Supabase Dashboard → Settings → Database → Connection pooling |
| `SUPABASE_URL` | Supabase project URL | `https://xxxxx.supabase.co` | Supabase Dashboard → Settings → API |
| `SUPABASE_KEY` | Supabase anon/public key | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` | Supabase Dashboard → Settings → API |
| `FLASK_ENV` | Environment name | `production` | Set to `production` for Vercel |

### Optional Variables

| Variable | Description | Default | Notes |
|----------|-------------|---------|-------|
| `MAPBOX_TOKEN` | Mapbox access token for map features | `""` | Required if using Mapbox maps |
| `PREFERRED_URL_SCHEME` | URL scheme (http/https) | `https` | Use `https` for production |

---

## Supabase Database Configuration

### Step 1: Create Supabase Project

1. Go to [supabase.com](https://supabase.com) and create a new project
2. Choose a region close to your target users (e.g., Singapore for Philippines)
3. Set a strong database password
4. Wait for project provisioning (2-3 minutes)

### Step 2: Apply Database Schema

1. Navigate to **SQL Editor** in Supabase Dashboard
2. Open the [supabase_schema.sql](file:///d:/porjects/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan/supabase_schema.sql) file from your project
3. Copy the entire SQL content
4. Paste into Supabase SQL Editor and click **Run**
5. Verify all tables are created in **Table Editor**

Expected tables:
- `user`
- `attraction`
- `event`
- `gallery_item`
- `barangay_info`
- `page_view`
- `favorite`
- `event_interest`
- `review`

### Step 3: Get Connection Strings

1. Go to **Settings** → **Database**
2. Copy **Connection pooling** string (port 6543) for `DATABASE_URL`
   - **Use Transaction mode** for better compatibility
   - Format: `postgresql://postgres.[project-ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres`
3. Copy **Connection string** (port 5432) as backup

### Step 4: Get API Keys

1. Go to **Settings** → **API**
2. Copy **Project URL** for `SUPABASE_URL`
3. Copy **anon public** key for `SUPABASE_KEY`

---

## Vercel Deployment

### Method 1: GitHub Integration (Recommended)

1. **Connect Repository**:
   ```bash
   # Push code to GitHub
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Import to Vercel**:
   - Go to [vercel.com/new](https://vercel.com/new)
   - Click **Import Git Repository**
   - Select your GitHub repository
   - Click **Import**

3. **Configure Project**:
   - **Framework Preset**: Other
   - **Build Command**: Leave empty (using serverless functions)
   - **Output Directory**: Leave empty
   - **Install Command**: `pip install -r requirements.txt`

4. **Add Environment Variables**:
   - Click **Environment Variables**
   - Add all required variables from the table above
   - Ensure `FLASK_ENV=production`

5. **Deploy**:
   - Click **Deploy**
   - Wait for build to complete (3-5 minutes)
   - Vercel will provide a deployment URL

### Method 2: Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy to production
vercel --prod

# Follow prompts to configure environment variables
```

---

## Vercel Configuration

The application includes Vercel-specific optimizations in [app.py](file:///d:/porjects/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan/app.py):

### ProxyFix Middleware

Handles Vercel's reverse proxy headers correctly:

```python
if "VERCEL" in os.environ:
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
```

### Smart Cache Headers

Automatic edge caching based on path type:

| Path Type | Cache-Control | Description |
|-----------|---------------|-------------|
| Admin/Auth routes | `private, no-store` | Never cached |
| HTML pages | `public, max-age=60, s-maxage=300, stale-while-revalidate=600` | Edge cached for 5 min, stale for 10 min |
| Static assets (JS/CSS/images) | `public, max-age=31536000, immutable` | Cached for 1 year |
| API responses | `public, max-age=30, s-maxage=120, stale-while-revalidate=300` | Edge cached for 2 min |

### Lazy Supabase Client

Supabase client is initialized only when needed to reduce cold start time:

```python
def _init_supabase_support(app: Flask) -> None:
    """Adds lazy-loaded Supabase client to the app instance."""
    # Implementation uses descriptor pattern for on-demand initialization
```

---

## Post-Deployment Checklist

### 1. Database Verification

```bash
# Test database connection
curl https://your-app.vercel.app/api/attractions
```

Expected response: JSON with attractions array and pagination

### 2. Environment Variables Check

Verify all environment variables are set:
- Vercel Dashboard → Project → Settings → Environment Variables

### 3. Custom Domain (Optional)

1. Go to **Settings** → **Domains**
2. Add your custom domain
3. Update DNS records as instructed
4. Wait for SSL certificate provisioning

### 4. Error Monitoring

Check Vercel logs for errors:
- Vercel Dashboard → Deployments → [Latest Deployment] → Build Logs
- Vercel Dashboard → Deployments → [Latest Deployment] → Function Logs

### 5. Performance Testing

Test load times from different regions:
- Use [WebPageTest.org](https://www.webpagetest.org)
- Target: First Contentful Paint < 1.5s
- Leverage Vercel's Edge Network

---

## Database Migrations (Production)

### Applying Schema Changes

**⚠️ Warning**: Flask-Migrate is **disabled** on Vercel. Use direct SQL execution.

1. **Prepare SQL Migration**:
   - Test migration locally with SQLite
   - Generate equivalent PostgreSQL SQL
   - Review schema changes carefully

2. **Apply to Supabase**:
   - Navigate to Supabase SQL Editor
   - Execute migration SQL
   - Verify changes in Table Editor

3. **Update `supabase_schema.sql`**:
   - Keep schema file in sync with production
   - Update file in repository
   - Commit changes

### Best Practices

- **Test locally first**: Use SQLite to test migrations
- **Backup before changes**: Export Supabase data
- **Apply during low traffic**: Minimize user impact
- **Verify after migration**: Test all affected endpoints

**Example migration workflow**:

```sql
-- Add new column to attraction table
ALTER TABLE attraction ADD COLUMN opening_hours TEXT;

-- Update existing rows with default value
UPDATE attraction SET opening_hours = 'Not specified' WHERE opening_hours IS NULL;
```

---

## Rollback Strategy

### Vercel Deployment Rollback

1. Go to Vercel Dashboard → Deployments
2. Find the last working deployment
3. Click **⋮** (three dots) → **Promote to Production**
4. Confirm rollback

### Database Rollback

1. **Restore from Backup**:
   - Supabase Dashboard → Database → Backups
   - Select backup point
   - Click **Restore**

2. **Manual Reversion**:
   ```sql
   -- Example: Remove added column
   ALTER TABLE attraction DROP COLUMN opening_hours;
   ```

---

## Secrets Management

### Secure Practices

1. **Never commit secrets**:
   - `.env` is in `.gitignore`
   - Use Vercel environment variables

2. **Rotate secrets regularly**:
   - Update `SECRET_KEY` quarterly
   - Rotate database passwords annually

3. **Use separate keys per environment**:
   - Different `SECRET_KEY` for dev/staging/prod
   - Separate Supabase projects for staging

### Generating Secure Secrets

```bash
# Generate SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"

# Generate random password
python -c "import secrets; print(secrets.token_urlsafe(24))"
```

---

## Monitoring and Debugging

### Vercel Function Logs

Access real-time logs:
```bash
vercel logs [deployment-url]
```

### Performance Monitoring

- **Vercel Analytics**: Enable in project settings
- **Custom Logging**: Review logs in Vercel Dashboard
- **Supabase Logs**: Database query performance in Supabase Dashboard

### Common Issues

#### Cold Start Delays

**Symptom**: First request after idle takes 3-5 seconds

**Solution**: 
- Already optimized with lazy Supabase loading
- Consider Vercel Pro for faster cold starts

#### Database Connection Errors

**Symptom**: `Connection refused` or timeout errors

**Solution**:
- Verify `DATABASE_URL` uses connection pooler (port 6543)
- Check Supabase project is not paused
- Verify `pool_pre_ping=True` in config

#### 502 Bad Gateway

**Symptom**: Function timeout after 10 seconds

**Solution**:
- Optimize database queries
- Add indexes to frequently queried columns
- Review slow query logs in Supabase

---

## Scaling Considerations

### Database Scaling

- **Connection Pooling**: Already configured via Supabase pooler
- **Read Replicas**: Available in Supabase Pro
- **Vertical Scaling**: Upgrade Supabase compute resources

### Application Scaling

- **Vercel Edge Network**: Automatic global distribution
- **Serverless Auto-scaling**: Handles traffic spikes automatically
- **Static Asset Caching**: Configured for optimal CDN usage

---

## Local Development vs Production

| Aspect | Local | Production |
|--------|-------|------------|
| Database | SQLite (`instance/app.db`) | Supabase PostgreSQL |
| Migrations | Flask-Migrate | Direct SQL in Supabase |
| Cache Headers | Disabled | Smart caching enabled |
| ProxyFix | Not applied | Applied for Vercel |
| Static Files | Flask dev server | Vercel CDN |
| Database Seeding | Automatic | Manual via Supabase |

---

## Troubleshooting Guide

### Issue: Static Files Not Loading

**Check**: Verify `static/` folder is committed to Git

**Solution**: Ensure `.gitignore` doesn't exclude necessary static files

### Issue: Database Schema Mismatch

**Check**: Compare `models.py` with Supabase tables

**Solution**: Apply missing migrations via Supabase SQL Editor

### Issue: Session Not Persisting

**Check**: Verify `SECRET_KEY` is set in Vercel environment variables

**Solution**: Set `SECRET_KEY` and redeploy

---

## Additional Resources

- **Vercel Documentation**: [vercel.com/docs](https://vercel.com/docs)
- **Supabase Documentation**: [supabase.com/docs](https://supabase.com/docs)
- **Flask Documentation**: [flask.palletsprojects.com](https://flask.palletsprojects.com)
- **Project Architecture**: [architecture.md](file:///d:/porjects/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan/docs/architecture.md)
- **Database Migrations**: [database_migration.md](file:///d:/porjects/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan/docs/database_migration.md)

---

**Last Updated**: 2026-02-12
