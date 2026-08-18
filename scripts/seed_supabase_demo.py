#!/usr/bin/env python3
"""
Seed Supabase demo DB with ~N random rows per table (auto-generated, FK-aware).

1. Backs up the schema (CREATE TABLE DDL) to backups/supabase_schema_<date>.sql
2. Inserts N random rows per table via direct PostgreSQL connection,
   resolving FKs from already-seeded parent tables.

Usage: uv run python scripts/seed_supabase_demo.py [N]
"""
import sys, random, string, uuid, json, datetime, psycopg2, pathlib

PROJECT = pathlib.Path("/mnt/win-sda3/porjects/capstone_system")
N = int(sys.argv[1]) if len(sys.argv) > 1 else 500
SKIP = {"_migrations", "alembic_version"}  # infra tables, leave alone
# no fixed seed: reruns must generate fresh values or UNIQUE constraints
# swallow every row (ON CONFLICT DO NOTHING would skip them all)

# ---- word bank for auto-generated names (Mangatarem heritage/tourism flavored)
WORDS = ["mangatarem", "heritage", "temple", "river", "church", "plaza", "market",
         "festival", "bamboo", "rice", "fiesta", "shrine", "museum", "lighthouse",
         "bridge", "cave", "mountain", "falls", "garden", "trail", "bayan",
         "simbahan", "ilog", "bundok", "bukid", "bahay", "kultura", "kasaysayan",
         "palengke", "pista", "halaman", "sining", "musika", "sayaw", "pagkain",
         "lakbay", "turismo", "tanawin", "pamanang", "pook", "bantayog", "tulay",
         "kweba", "talon", "baybayin", "kabundukan", "habagat", "amihan"]
SUFFIX = string.ascii_lowercase + "0123456789"

def q(ident):
    return f'"{ident}"'

def words(n=2, cap=False):
    w = " ".join(random.choice(WORDS) for _ in range(n))
    return w.title() if cap else w

_uniq_counter = 0

def unique_word():
    """Word + monotonic counter so UNIQUE columns never collide within a run."""
    global _uniq_counter
    _uniq_counter += 1
    return f"{words(1, cap=True)}{_uniq_counter:05d}"

def text():
    return words(random.randint(4, 12)) + " " + words(3)

def email(i):
    return f"user{random.randint(1000,9999)}.{i}@gmail.com"

def rand_value(col, data_type, char_max, pool, i):
    """Generate a random value for a column based on its type."""
    if col in pool:  # FK -> existing parent PK
        return random.choice(pool[col])
    if data_type == "character varying":
        if "email" in col:
            return f"user{uuid.uuid4().hex[:8]}@gmail.com"  # unique per row
        if "url" in col or "document" in col or "photo" in col:
            return f"https://example.com/uploads/{words(1).replace(' ','-')}-{random.randint(100,999)}.jpg"
        if "token" in col:
            return uuid.uuid4().hex[: (char_max or 32)]
        if "password" in col:
            return f"pbkdf2:sha256$demo${uuid.uuid4().hex}"
        if col in ("username", "name", "name_of_asset", "title", "subject"):
            return unique_word()[: char_max or 255]  # UNIQUE columns must not collide
        return words(2, cap=True)[: char_max or 255]
    if data_type == "text":
        return text()
    if data_type in ("integer", "bigint", "smallint"):
        if "latitude" in col:
            return round(random.uniform(15.7, 16.0), 6)
        if "longitude" in col:
            return round(random.uniform(120.2, 120.5), 6)
        if "rating" in col:
            return random.randint(1, 5)
        if "party" in col or "capacity" in col:
            return random.randint(1, 20)
        if "year" in col:
            return random.randint(1800, 2026)
        return random.randint(1, 10_000)
    if data_type == "double precision":
        if "latitude" in col:
            return round(random.uniform(15.7, 16.0), 6)
        if "longitude" in col:
            return round(random.uniform(120.2, 120.5), 6)
        return round(random.uniform(0, 1000), 2)
    if data_type == "numeric":
        return round(random.uniform(10, 5000), 2)
    if data_type == "boolean":
        return random.choice([True, False])
    if data_type == "date":
        return datetime.date(2024, 1, 1) + datetime.timedelta(days=random.randint(0, 800))
    if "timestamp" in data_type:
        return datetime.datetime(2025, 1, 1) + datetime.timedelta(days=random.randint(0, 500),
                                                                  hours=random.randint(0, 23))
    if data_type == "uuid":
        return str(uuid.uuid4())
    if data_type in ("json", "jsonb"):
        return json.dumps({"note": words(3), "v": random.randint(1, 99)})
    return None

def load_env(path):
    env = {}
    for line in path.read_text().splitlines():
        line = line.rstrip("\r").strip()
        if line and "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            env[k] = v
    return env

env = load_env(PROJECT / ".env")
conn = psycopg2.connect(host=env["host"], port=env["port"], dbname=env["dbname"],
                        user=env["user"], password=env["password"], sslmode="require")
cur = conn.cursor()

# ---- metadata
cur.execute("""
    SELECT c.table_name, c.column_name, c.data_type,
           c.character_maximum_length, c.column_default, c.is_identity,
           c.is_nullable, c.is_generated
    FROM information_schema.columns c
    WHERE c.table_schema='public'
    ORDER BY c.table_name, c.ordinal_position
""")
cols = {}
for t, c, dt, m, dflt, ident, nul, gen in cur.fetchall():
    cols.setdefault(t, []).append(dict(name=c, type=dt, max=m, default=dflt,
                                       identity=ident, nullable=nul == "YES",
                                       generated=gen))

cur.execute("""
    SELECT tc.table_name, kcu.column_name, ccu.table_name
    FROM information_schema.table_constraints tc
    JOIN information_schema.key_column_usage kcu
      ON tc.constraint_name=kcu.constraint_name AND tc.table_name=kcu.table_name
    JOIN information_schema.constraint_column_usage ccu
      ON tc.constraint_name=ccu.constraint_name
    WHERE tc.constraint_type='FOREIGN KEY' AND tc.table_schema='public'
""")
fk = {}
for t, c, ref in cur.fetchall():
    fk.setdefault(t, set()).add((c, ref))

cur.execute("""
    SELECT tc.table_name, kcu.column_name
    FROM information_schema.table_constraints tc
    JOIN information_schema.key_column_usage kcu
      ON tc.constraint_name=kcu.constraint_name AND tc.table_name=kcu.table_name
    WHERE tc.constraint_type='PRIMARY KEY' AND tc.table_schema='public'
""")
pks = {}
for t, c in cur.fetchall():
    pks.setdefault(t, []).append(c)

# ---- topological order (parents before children)
def order(tables, fk):
    visited, out = set(), []
    def dfs(t):
        if t in visited:
            return
        visited.add(t)
        for _, ref in fk.get(t, ()):
            if ref in tables:
                dfs(ref)
        out.append(t)
    for t in sorted(tables):
        dfs(t)
    return out

# ---- 1) schema backup (DDL)
backup_dir = PROJECT / "backups"
backup_dir.mkdir(exist_ok=True)
date = datetime.date.today().isoformat()
with open(backup_dir / f"supabase_schema_{date}.sql", "w") as f:
    for t in sorted(cols):
        if t in SKIP:
            continue
        lines = [f"CREATE TABLE IF NOT EXISTS public.{q(t)} ("]
        defs = []
        for c in cols[t]:
            d = f"    {q(c['name'])} {c['type']}"
            if c["max"] and c["type"] == "character varying":
                d += f"({c['max']})"
            if c["identity"] == "YES":
                d += " GENERATED ALWAYS AS IDENTITY"
            elif not c["default"] and c["nullable"]:
                d += " NULL"
            elif not c["default"]:
                d += " NOT NULL"
            elif c["default"]:
                d += f" DEFAULT {c['default']}"
            defs.append(d)
        pk = ", ".join(q(p) for p in pks.get(t, []))
        if pk:
            defs.append(f"    PRIMARY KEY ({pk})")
        for c, ref in sorted(fk.get(t, set())):
            defs.append(f"    FOREIGN KEY ({q(c)}) REFERENCES public.{q(ref)}")
        lines.append(",\n".join(defs))
        lines.append(");\n")
        f.write("\n".join(lines))
print(f"[backup] wrote {backup_dir}/supabase_schema_{date}.sql")

# ---- 2) seed
id_pools = {}  # table -> list of PK values
total = 0

def flush(t, pk_col, rows):
    """Insert a batch in one multi-VALUES statement, return inserted PKs."""
    if not rows:
        return []
    keys = [k for k in rows[0]]
    cols = ", ".join(q(k) for k in keys)
    placeholders = ", ".join(["(" + ", ".join(["%s"] * len(keys)) + ")"] * len(rows))
    sql = (f"INSERT INTO public.{q(t)} ({cols}) VALUES {placeholders} "
           f"ON CONFLICT DO NOTHING RETURNING {q(pk_col)}")
    params = [v for r in rows for v in r.values()]
    try:
        cur.execute(sql, params)
        return [x[0] for x in cur.fetchall()]
    except Exception as e:
        conn.rollback()
        print(f"  [warn] {t} batch failed: {str(e)[:200]}")
        # fallback: insert one-by-one, skip bad rows
        ids = []
        for r in rows:
            try:
                cur.execute(f"INSERT INTO public.{q(t)} ({cols}) VALUES "
                            f"({', '.join(['%s'] * len(keys))}) "
                            f"ON CONFLICT DO NOTHING RETURNING {q(pk_col)}", r)
                ids.extend(x[0] for x in cur.fetchall())
            except Exception:
                conn.rollback()
        return ids

for t in order(cols.keys(), fk):
    if t in SKIP:
        continue
    pk_cols = pks.get(t, [])
    if not pk_cols:
        print(f"[skip] {t}: no PK")
        continue
    pk_col = pk_cols[0]
    fk_here = dict(fk.get(t, ()))
    batch = []
    ids = []
    for i in range(N):
        row = {}
        for c in cols[t]:
            # let DB fill identity / defaulted / generated columns
            if c["identity"] == "YES" or c["generated"] != "NEVER" or c["default"]:
                continue
            if c["name"] == pk_col:
                continue
            pool = {col: id_pools[ref]
                    for col, ref in fk_here.items() if ref in id_pools}
            if c["name"] in fk_here:
                if pool.get(c["name"]):
                    val = random.choice(pool[c["name"]])
                elif c["nullable"]:
                    val = None  # nullable FK (e.g. self-referencing) -> NULL
                else:
                    # parent table has no rows: cannot satisfy NOT NULL FK,
                    # skip this row entirely instead of corrupting the type
                    row = None
                    break
            else:
                val = rand_value(c["name"], c["type"], c["max"], pool, i)
            if val is None and not c["nullable"]:
                val = words(1)  # last-resort for exotic NOT NULL types
            row[c["name"]] = val
        if row is None:
            continue  # couldn't build a valid row (missing FK parent)
        batch.append(row)
        if len(batch) >= 100:
            ids.extend(flush(t, pk_col, batch))
            batch = []
    ids.extend(flush(t, pk_col, batch))
    id_pools[t] = ids
    total += len(ids)
    conn.commit()  # commit per table so progress persists on failure
    print(f"[seed] {t}: +{len(ids)} rows", flush=True)

conn.commit()
print(f"\nDONE: {total} rows inserted total")
conn.close()
