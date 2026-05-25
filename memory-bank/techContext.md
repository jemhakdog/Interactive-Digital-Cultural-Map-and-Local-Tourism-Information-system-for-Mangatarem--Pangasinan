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
TBD
```

### Test
```bash
TBD
```

### Lint
```bash
uv run ruff check .
```

### Build
```bash
TBD
```

## Environment variables

See `.env.example`.

## Tooling notes

- FAST_INIT stack detection found `pyproject.toml` and `requirements.txt`.
- Added Mapbox GL JS for frontend maps.
- Redis caching requires `UPSTASH_REDIS_REST_URL` and `UPSTASH_REDIS_REST_TOKEN`.
- OSRM used for TSP (Traveling Salesman Problem) routing.
- PostGIS extension required in Supabase database for MVT generation.
- Security relies on `bleach` for HTML sanitization, and Flask-WTF for CSRF.