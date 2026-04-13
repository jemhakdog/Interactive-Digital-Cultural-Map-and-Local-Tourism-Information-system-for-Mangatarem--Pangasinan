# Database Security Implementation Guide

## Overview

This document outlines the database security measures implemented to prevent SQL injection and enforce the principle of least privilege.

## 1. Principle of Least Privilege

### Database User Roles

For production deployments, create separate database users with different permission levels:

#### 1.1 Read-Only User (Public Queries)
```sql
CREATE USER app_readonly WITH PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE mangatarem_tourism TO app_readonly;
GRANT USAGE ON SCHEMA public TO app_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO app_readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO app_readonly;
```

**Used for:**
- Public attraction listings
- Event listings
- Map data retrieval
- Public establishment information

#### 1.2 Read-Write User (Authenticated Users)
```sql
CREATE USER app_readwrite WITH PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE mangatarem_tourism TO app_readwrite;
GRANT USAGE ON SCHEMA public TO app_readwrite;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO app_readwrite;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE ON TABLES TO app_readwrite;
-- Explicitly DENY DELETE to prevent accidental data loss
DENY DELETE ON ALL TABLES IN SCHEMA public TO app_readwrite;
```

**Used for:**
- User profile updates
- Creating reviews
- Adding favorites
- Updating user preferences

#### 1.3 Admin User (Administrative Operations)
```sql
CREATE USER app_admin WITH PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE mangatarem_tourism TO app_admin;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO app_admin;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO app_admin;
GRANT DELETE ON ALL TABLES IN SCHEMA public TO app_admin;
```

**Used for:**
- Content moderation (approve/reject)
- User management
- Deleting inappropriate content
- Database maintenance operations

### 1.4 Configuration in Application

Update `.env` file with separate connection strings:

```env
# Production database configuration
DB_PROVIDER=supabase
SUPABASE_HOST=db.xxxxx.supabase.co
SUPABASE_PORT=5432
SUPABASE_DATABASE=postgres

# Separate credentials for each role
DATABASE_READ_ONLY_URI=postgresql://app_readonly:password@host:5432/dbname
DATABASE_READ_WRITE_URI=postgresql://app_readwrite:password@host:5432/dbname
DATABASE_ADMIN_URI=postgresql://app_admin:password@host:5432/dbname
```

## 2. SQL Injection Prevention Measures

### 2.1 Parameterized Queries (Primary Defense)

All database queries use SQLAlchemy ORM which automatically parameterizes queries:

```python
# ✅ CORRECT: Using ORM (automatically parameterized)
user = User.query.filter_by(username=username).first()
attractions = Attraction.query.filter_by(status='approved').all()

# ✅ CORRECT: Using text() with parameters
from sqlalchemy import text
result = db.session.execute(
    text("SELECT * FROM attractions WHERE category = :category"),
    {"category": category}
)

# ❌ WRONG: Using f-strings or string concatenation
result = db.session.execute(
    text(f"SELECT * FROM attractions WHERE category = '{category}'")  # VULNERABLE!
)
```

### 2.2 Input Validation Layer

All user inputs are validated before database operations using `utils/security.py`:

```python
from utils.security import validate_string_input, detect_sql_injection_attempt

# Validate string input
is_valid, error_msg = validate_string_input(
    user_input,
    min_length=1,
    max_length=200,
    block_sql_injection=True
)

if not is_valid:
    return jsonify({'error': error_msg}), 400
```

### 2.3 SQL Injection Detection

The `detect_sql_injection_attempt()` function checks for common attack patterns:

- SQL keywords: SELECT, INSERT, UPDATE, DELETE, DROP, UNION, etc.
- SQL comments: `--`, `/*`, `*/`
- Tautology attacks: `OR 1=1`, `AND 1=1`
- Stacked queries: `; DROP TABLE`
- System tables: `INFORMATION_SCHEMA`, `xp_cmdshell`

## 3. Database Audit Logging

### 3.1 Audit Log Model

The `DatabaseAuditLog` model tracks all database operations:

```python
# Log a database operation
DatabaseAuditLog.log_operation(
    user_id=current_user.id,
    action='INSERT',
    table_name='ATTRACTION',
    record_id=attraction.id,
    ip_address=request.remote_addr,
    user_agent=request.user_agent.string,
    query_summary='Created new attraction',
    status='success'
)
```

### 3.2 What Gets Logged

- **User actions**: All CREATE, UPDATE, DELETE operations
- **Failed attempts**: Blocked SQL injection attempts
- **Admin operations**: All administrative database changes
- **Authentication events**: Login attempts (success/failure)

### 3.3 What Does NOT Get Logged

- SELECT queries (too verbose)
- Full SQL queries (security risk)
- Password hashes or sensitive data
- Session tokens

## 4. Error Message Sanitization

### 4.1 Production Environment

In production, database errors are sanitized to prevent information leakage:

```python
# Server-side logging (detailed)
logger.error(f"Database error: {str(e)}", exc_info=True)

# User-facing message (generic)
return render_template("errors/500.html", 
                      error_message="An unexpected error occurred")
```

### 4.2 Development Environment

In development, full error details are shown for debugging:

```python
if app.config.get("FLASK_ENV") == "production":
    # Generic error message
    return "An error occurred", 500
else:
    # Detailed error for debugging
    raise e
```

## 5. Connection Security

### 5.1 SSL/TLS Encryption

All database connections use SSL in production:

```python
# config.py - ProductionConfig
SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_pre_ping": True,
    "pool_recycle": 300,
    "connect_args": {
        "sslmode": "require"
    }
}
```

### 5.2 Connection Pooling

Connection limits prevent resource exhaustion:

```python
SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_size": 10,           # Max connections in pool
    "max_overflow": 20,        # Max temporary connections
    "pool_timeout": 30,        # Wait time for connection
    "pool_recycle": 1800       # Recycle connections after 30 min
}
```

## 6. Migration Security

### 6.1 Running Migrations

Always use parameterized migrations:

```bash
# Create migration
flask db migrate -m "Description of changes"

# Review migration file BEFORE applying
# Check for any raw SQL that should be parameterized

# Apply migration
flask db upgrade
```

### 6.2 Migration Best Practices

- Never hardcode credentials in migration files
- Use `op.execute()` with parameters, not f-strings
- Test migrations in staging before production
- Always have a rollback plan

## 7. Monitoring and Alerts

### 7.1 What to Monitor

- Failed login attempts (>5 per minute = alert)
- SQL injection attempts (any = alert)
- Unusual query patterns (sudden spikes = investigate)
- Connection pool exhaustion (frequent = scale up)
- Slow queries (>1 second = optimize)

### 7.2 Querying Audit Logs

```python
# Get recent failed operations
failed_ops = DatabaseAuditLog.query.filter_by(
    status='failed'
).order_by(
    DatabaseAuditLog.created_at.desc()
).limit(50).all()

# Get operations by user
user_ops = DatabaseAuditLog.query.filter_by(
    user_id=user_id
).order_by(
    DatabaseAuditLog.created_at.desc()
).all()

# Detect suspicious activity (multiple failures)
from sqlalchemy import func
suspicious = db.session.query(
    DatabaseAuditLog.ip_address,
    func.count('*').label('failure_count')
).filter_by(
    status='blocked'
).group_by(
    DatabaseAuditLog.ip_address
).having(
    func.count('*') > 10
).all()
```

## 8. Validation Decorators

### 8.1 Usage in Routes

Use the validation decorators from `utils/validators.py`:

```python
from utils.validators import validate_form_data, validate_json_input

@validate_form_data({
    'name': {'type': 'string', 'required': True, 'max_length': 200},
    'rating': {'type': 'int', 'min': 1, 'max': 5},
    'email': {'type': 'email', 'required': True}
})
def create_review():
    # request.validated_data contains sanitized values
    name = request.validated_data['name']
    rating = request.validated_data['rating']
```

### 8.2 Available Validators

- `validate_form_data`: Validate form submissions
- `validate_json_input`: Validate JSON API requests
- `validate_query_params`: Whitelist and validate query parameters
- `validate_coordinates_fields`: Validate geographic coordinates

## 9. Security Checklist

Before deploying to production:

- [ ] Create separate database users (readonly, readwrite, admin)
- [ ] Test application with readonly user for public pages
- [ ] Test application with readwrite user for authenticated users
- [ ] Verify audit logging is working
- [ ] Verify error messages are sanitized in production
- [ ] Enable SSL for database connections
- [ ] Set connection pool limits
- [ ] Configure monitoring and alerts
- [ ] Review all routes using validation decorators
- [ ] Test SQL injection prevention with automated tests

## 10. Incident Response

### 10.1 If SQL Injection is Detected

1. **Immediate Actions:**
   - Block the offending IP address
   - Review audit logs for scope of breach
   - Rotate database credentials
   - Enable enhanced logging

2. **Investigation:**
   - Identify vulnerable endpoint
   - Determine what data was accessed
   - Check if data was exfiltrated
   - Document timeline of events

3. **Remediation:**
   - Fix the vulnerability
   - Add automated test for the attack vector
   - Review similar endpoints
   - Update security documentation

## 11. References

- [OWASP SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [SQLAlchemy Security](https://docs.sqlalchemy.org/en/20/core/security.html)
- [PostgreSQL Security Best Practices](https://www.postgresql.org/docs/current/security.html)
