# Database Manager Migration Plan

Migrate `app.py` to use the centralized `utils/db_manager.py` module for database configuration, enabling multi-provider support (SQLite, MySQL, PostgreSQL/Supabase) via environment variables.

---

## Proposed Changes

### Core Application

#### [MODIFY] [app.py](file:///d:/porjects/Interactive-Digital-Cultural-Map-and-Local-Tourism-Information-system-for-Mangatarem--Pangasinan/app.py)

**1. Add Imports (line ~12)**
```python
from utils.db_manager import get_database_uri, get_db_config
from flask_migrate import Migrate
```

**2. Replace Database Configuration (lines 52-74)**

Current hardcoded SQLite logic:
```python
# Handle SQLite database path for Vercel
if IS_VERCEL:
    db_path = "/tmp/mangatarem.db"
    # ... copy logic
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
else:
    instance_path = os.path.join(BASE_DIR, "instance")
    # ...
    app.config["SQLALCHEMY_DATABASE_URI"] = ...
```

Replace with:
```python
# Database Configuration via db_manager
app.config["SQLALCHEMY_DATABASE_URI"] = get_database_uri()
get_db_config(app)  # Applies engine options & TRACK_MODIFICATIONS
```

**3. Initialize Flask-Migrate (after line 101)**
```python
# Initialize database
db.init_app(app)
migrate = Migrate(app, db)  # NEW: Enable migration commands
```

**4. Remove Redundant Line (line 48)**
```diff
-app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
```
> Already set by `get_db_config()`

---

## Environment Variables

| Variable | Provider | Example |
|----------|----------|---------|
| `DB_PROVIDER` | All | `sqlite`, `mysql`, `supabase`, `xampp` |
| `DATABASE_URL` | Supabase/Postgres | `postgresql://user:pass@host:5432/db` |
| `DB_USER` | MySQL | `root` |
| `DB_PASS` | MySQL | `password` |
| `DB_HOST` | MySQL | `localhost` |
| `DB_PORT` | MySQL | `3306` |
| `DB_NAME` | MySQL | `mangatarem` |

---

## Verification Plan

### Automated Tests
```powershell
# 1. Test default SQLite (no env vars)
uv run python app.py

# 2. Test MySQL provider
$env:DB_PROVIDER="mysql"; $env:DB_USER="root"; $env:DB_NAME="test"
uv run python -c "from utils.db_manager import get_database_uri; print(get_database_uri())"

# 3. Test Flask-Migrate commands
uv run flask db init      # First time only
uv run flask db migrate -m "Initial"
uv run flask db upgrade
```

### Manual Verification
- Confirm app starts without errors
- Verify database connection logs show correct provider
- Check Flask-Migrate `migrations/` folder is created
