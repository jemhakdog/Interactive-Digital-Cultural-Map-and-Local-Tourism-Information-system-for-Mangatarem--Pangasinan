import os
import sys
from datetime import datetime

# Adjust Python path to allow importing modules from the root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from extensions import db
from sqlalchemy import text, inspect

def migrate():
    app = create_app()
    with app.app_context():
        print("Starting database table consolidation...")
        inspector = inspect(db.engine)
        existing_tables = inspector.get_table_names()
        
        # 1. Fetch old data safely if tables exist
        old_attraction_reviews = []
        old_establishment_reviews = []
        old_photos = []
        old_fav_attractions = []
        old_fav_establishments = []
        old_event_interests = []
        
        # Helper to safely query tables
        def get_records(connection, table_name):
            if table_name in existing_tables:
                try:
                    result = connection.execute(text(f"SELECT * FROM {table_name}")).fetchall()
                    # Convert to list of dicts to keep dynamic access
                    cols = inspector.get_columns(table_name)
                    col_names = [col['name'] for col in cols]
                    records = [dict(zip(col_names, row)) for row in result]
                    print(f"Fetched {len(records)} records from {table_name}")
                    return records
                except Exception as e:
                    print(f"Warning: Failed to fetch from {table_name}: {e}")
            return []

        # We connect once to fetch all existing data
        with db.engine.connect() as fetch_conn:
            old_attraction_reviews = get_records(fetch_conn, "ATTRACTION_REVIEW")
            old_establishment_reviews = get_records(fetch_conn, "ESTABLISHMENT_REVIEW")
            old_photos = get_records(fetch_conn, "REVIEW_PHOTO")
            old_fav_attractions = get_records(fetch_conn, "USER_FAVORITE_ATTRACTION")
            old_fav_establishments = get_records(fetch_conn, "USER_FAVORITE_ESTABLISHMENT")
            old_event_interests = get_records(fetch_conn, "USER_EVENT_INTEREST")

        # 2. Create the new tables
        print("Creating consolidated tables (REVIEW, USER_FAVORITE)...")
        db.create_all()
        
        # 3. Connect to perform insertion in a transaction
        with db.engine.begin() as connection:
            # Disable foreign keys temporarily for SQLite
            is_sqlite = db.engine.url.drivername == 'sqlite' or 'sqlite' in str(db.engine.url)
            if is_sqlite:
                connection.execute(text("PRAGMA foreign_keys = OFF;"))
                print("Disabled SQLite foreign keys for migration.")

            # Consolidate Reviews and map IDs
            attraction_review_map = {}
            establishment_review_map = {}

            # A. Insert Attraction Reviews (parent_id = NULL initially to avoid FK constraint errors)
            print("Migrating Attraction Reviews...")
            for r in old_attraction_reviews:
                created_at = r.get('created_at') or datetime.utcnow()
                updated_at = r.get('updated_at') or datetime.utcnow()
                if isinstance(created_at, str):
                    created_at = datetime.fromisoformat(created_at)
                if isinstance(updated_at, str):
                    updated_at = datetime.fromisoformat(updated_at)
                
                query = text("""
                    INSERT INTO REVIEW (user_id, attraction_id, establishment_id, rating, comment, status, parent_id, created_at, updated_at)
                    VALUES (:user_id, :attraction_id, NULL, :rating, :comment, :status, NULL, :created_at, :updated_at)
                """)
                res = connection.execute(query, {
                    'user_id': r['user_id'],
                    'attraction_id': r['attraction_id'],
                    'rating': r['rating'],
                    'comment': r['comment'],
                    'status': r['status'],
                    'created_at': created_at,
                    'updated_at': updated_at
                })
                attraction_review_map[r['id']] = res.lastrowid

            # B. Insert Establishment Reviews (parent_id = NULL initially)
            print("Migrating Establishment Reviews...")
            for r in old_establishment_reviews:
                created_at = r.get('created_at') or datetime.utcnow()
                updated_at = r.get('updated_at') or datetime.utcnow()
                if isinstance(created_at, str):
                    created_at = datetime.fromisoformat(created_at)
                if isinstance(updated_at, str):
                    updated_at = datetime.fromisoformat(updated_at)
                
                query = text("""
                    INSERT INTO REVIEW (user_id, attraction_id, establishment_id, rating, comment, status, parent_id, created_at, updated_at)
                    VALUES (:user_id, NULL, :establishment_id, :rating, :comment, :status, NULL, :created_at, :updated_at)
                """)
                res = connection.execute(query, {
                    'user_id': r['user_id'],
                    'establishment_id': r['establishment_id'],
                    'rating': r['rating'],
                    'comment': r['comment'],
                    'status': r['status'],
                    'created_at': created_at,
                    'updated_at': updated_at
                })
                establishment_review_map[r['id']] = res.lastrowid

            # C. Update nested replies' parent_ids using mapped IDs
            print("Updating Nested Comment Reply Parents...")
            for r in old_attraction_reviews:
                old_parent = r.get('parent_id')
                if old_parent and old_parent in attraction_review_map:
                    new_id = attraction_review_map[r['id']]
                    new_parent = attraction_review_map[old_parent]
                    connection.execute(text("UPDATE REVIEW SET parent_id = :parent_id WHERE id = :id"), {
                        'parent_id': new_parent,
                        'id': new_id
                    })

            for r in old_establishment_reviews:
                old_parent = r.get('parent_id')
                if old_parent and old_parent in establishment_review_map:
                    new_id = establishment_review_map[r['id']]
                    new_parent = establishment_review_map[old_parent]
                    connection.execute(text("UPDATE REVIEW SET parent_id = :parent_id WHERE id = :id"), {
                        'parent_id': new_parent,
                        'id': new_id
                    })

            # D. Migrate Photos linked to new Review IDs
            print("Migrating Review Photos...")
            connection.execute(text("DELETE FROM REVIEW_PHOTO"))
            for p in old_photos:
                old_review_id = p['review_id']
                if old_review_id in attraction_review_map:
                    new_review_id = attraction_review_map[old_review_id]
                    created_at = p.get('created_at') or datetime.utcnow()
                    if isinstance(created_at, str):
                        created_at = datetime.fromisoformat(created_at)
                    connection.execute(text("""
                        INSERT INTO REVIEW_PHOTO (review_id, url, created_at)
                        VALUES (:review_id, :url, :created_at)
                    """), {
                        'review_id': new_review_id,
                        'url': p['url'],
                        'created_at': created_at
                    })

            # E. Migrate Favorites (Attraction)
            print("Migrating Attraction Favorites...")
            for f in old_fav_attractions:
                created_at = f.get('created_at') or datetime.utcnow()
                if isinstance(created_at, str):
                    created_at = datetime.fromisoformat(created_at)
                connection.execute(text("""
                    INSERT INTO USER_FAVORITE (user_id, attraction_id, establishment_id, event_id, status, created_at)
                    VALUES (:user_id, :attraction_id, NULL, NULL, 'favorite', :created_at)
                """), {
                    'user_id': f['user_id'],
                    'attraction_id': f['attraction_id'],
                    'created_at': created_at
                })

            # F. Migrate Favorites (Establishment)
            print("Migrating Establishment Favorites...")
            for f in old_fav_establishments:
                created_at = f.get('created_at') or datetime.utcnow()
                if isinstance(created_at, str):
                    created_at = datetime.fromisoformat(created_at)
                connection.execute(text("""
                    INSERT INTO USER_FAVORITE (user_id, attraction_id, establishment_id, event_id, status, created_at)
                    VALUES (:user_id, NULL, :establishment_id, NULL, 'favorite', :created_at)
                """), {
                    'user_id': f['user_id'],
                    'establishment_id': f['establishment_id'],
                    'created_at': created_at
                })

            # G. Migrate Event Interests
            print("Migrating Event Interests...")
            for i in old_event_interests:
                created_at = i.get('created_at') or datetime.utcnow()
                if isinstance(created_at, str):
                    created_at = datetime.fromisoformat(created_at)
                connection.execute(text("""
                    INSERT INTO USER_FAVORITE (user_id, attraction_id, establishment_id, event_id, status, created_at)
                    VALUES (:user_id, NULL, NULL, :event_id, :status, :created_at)
                """), {
                    'user_id': i['user_id'],
                    'event_id': i['event_id'],
                    'status': i['status'],
                    'created_at': created_at
                })

            # H. Drop old tables safely
            print("Dropping legacy tables...")
            legacy_tables = [
                "ATTRACTION_REVIEW",
                "ESTABLISHMENT_REVIEW",
                "USER_FAVORITE_ATTRACTION",
                "USER_FAVORITE_ESTABLISHMENT",
                "USER_EVENT_INTEREST"
            ]
            for t in legacy_tables:
                if t in existing_tables:
                    connection.execute(text(f"DROP TABLE {t}"))
                    print(f"Dropped table: {t}")

            if is_sqlite:
                connection.execute(text("PRAGMA foreign_keys = ON;"))
                print("Re-enabled SQLite foreign keys.")

if __name__ == "__main__":
    migrate()
    print("Database table consolidation completed successfully!")
