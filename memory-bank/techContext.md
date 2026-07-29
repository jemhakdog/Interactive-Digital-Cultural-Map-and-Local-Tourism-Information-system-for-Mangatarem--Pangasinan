# Tech Context

## Stack

- Language: Python (>=3.11)
- Framework: Flask
- Dependencies: Flask-SQLAlchemy, Flask-Login, Flask-Migrate, Flask-WTF, Supabase, Upstash Redis, TailwindCSS
- Package manager: uv

## Commands

### Install
```bash
uv sync # or standard pip install -r requirements.txt
```

### Run
```bash
python app.py
```

### Test
```bash
pytest # or .venv\Scripts\pytest within virtual environment
```

### Lint
```bash
uv run ruff check .
```

### Build
- CSS/Tailwind: `npm run build:css` or equivalent compiler setup.

## Environment variables

See `.env.example`.

## Tooling notes

- FAST_INIT stack detection found `pyproject.toml` and `requirements.txt`.
- Added Mapbox GL JS for frontend maps.
- Redis caching requires `UPSTASH_REDIS_REST_URL` and `UPSTASH_REDIS_REST_TOKEN`.
- OSRM used for TSP (Traveling Salesman Problem) routing.
- PostGIS extension required in Supabase database for MVT generation.
- Security relies on `bleach` for HTML sanitization, and Flask-WTF for CSRF.
- Admin attraction form action must use `url_for('admin.add_attraction')` not `url_for('admin.admin_attractions')`.
- Event form date field is `<input type='date'>` — fill with `YYYY-MM-DD` format.
- PWA install prompt z-index set to 100 (was 9999) to avoid covering form buttons.
- `errors/500.html` template required for Flask error handler to render properly.
- Duplicate `core/` modules (security, email, validators, etc.) removed — use `utils/` as canonical source.