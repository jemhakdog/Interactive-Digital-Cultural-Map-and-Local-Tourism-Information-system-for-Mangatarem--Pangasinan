# SQL Files Analysis

This document analyzes all files containing SQL queries, table definitions, and SQL-related codes in the Interactive Digital Cultural Map project.

## 1. models.py
Contains SQLAlchemy model definitions for all database tables.

### Table Definitions:
- **User**: Stores user accounts with authentication details.
  - Columns: id (primary key), username, email, password_hash, role, barangay, is_approved
- **Attraction**: Stores tourist attractions.
  - Columns: id, name, description, category, barangay, lat, lng, image_url, status, user_id (FK to User), created_at
- **Event**: Stores cultural events.
  - Columns: id, title, description, date, location, barangay, image_url, user_id, status, category, created_at
- **GalleryItem**: Stores photo/video uploads.
  - Columns: id, type, url, caption, user_id, status, uploaded_at
- **BarangayInfo**: Stores barangay profile information.
  - Columns: id, barangay_name, history, cultural_assets, traditions, local_practices, unique_features, user_id, updated_at
- **PageView**: Tracks page views for analytics.
  - Columns: id, view_type, item_id, page_name, timestamp, user_id

## 2. flask_app.py
Handles database initialization and seeding.

### SQL-Related Code:
- Database configuration: `SQLALCHEMY_DATABASE_URI = 'sqlite:///mangatarem.db'`
- `db.init_app(app)` - Initializes SQLAlchemy
- `db.create_all()` - Creates all tables
- Seeding: Adds default attractions from JSON, creates admin and contributor users
  - `db.session.add(attraction)`
  - `db.session.commit()`

## 3. seed_events.py
Seeds the database with sample events.

### SQL-Related Code:
- Checks if events exist: `Event.query.count() > 0`
- Adds events: `db.session.add(event)`
- Commits: `db.session.commit()`

## 4. routes/auth.py
Handles user authentication and registration.

### SQL-Related Code:
- User registration: `db.session.add(user)` and `db.session.commit()`

## 5. routes/admin.py
Admin dashboard with CRUD operations and analytics.

### SQL-Related Code:
- Analytics queries:
  - Top attractions: `db.session.query(Attraction.name, func.count(PageView.id)).join(PageView).group_by(Attraction.id).order_by(func.count(PageView.id).desc()).limit(5)`
  - Daily views: `db.session.query(func.date(PageView.timestamp).label('date'), func.count(PageView.id)).group_by(func.date(PageView.timestamp)).order_by(func.date(PageView.timestamp).desc()).limit(7)`
- User approval: `user.is_approved = True; db.session.commit()`
- Delete operations: `db.session.delete(user); db.session.commit()`
- Attraction approval: `attraction.status = 'approved'; db.session.commit()`
- Attraction deletion: `db.session.delete(attraction); db.session.commit()`
- Event approval/deletion: Similar to attractions
- Gallery approval/deletion: Similar

## 6. routes/barangay.py
Barangay contributor CRUD operations.

### SQL-Related Code:
- Add attraction: `db.session.add(attraction); db.session.commit()`
- Update attraction: `db.session.commit()`
- Delete attraction: `db.session.delete(attraction); db.session.commit()`
- Similar for events and gallery items
- Barangay profile: Add/update BarangayInfo

## 7. routes/public.py
Public-facing routes with read queries.

### SQL-Related Code:
- Record page views: `db.session.add(view); db.session.commit()`
- Fetch barangays for map: `db.session.query(Attraction.barangay).filter(Attraction.status == 'approved').distinct()`
- Gallery barangays: `db.session.query(User.barangay).join(GalleryItem).filter(GalleryItem.status == 'approved').distinct()`
- Search filters: `db.session.query(Attraction.category).distinct()`, `db.session.query(Attraction.barangay).filter(Attraction.barangay != None).distinct()`
- Barangay names: `db.session.query(User.barangay).filter(User.role == 'contributor').distinct()`

## Summary
The project uses SQLAlchemy ORM for all database interactions. No raw SQL queries are present. The database is SQLite for development. Tables include users, attractions, events, gallery items, barangay info, and page views. Operations cover full CRUD plus analytics queries.
This document analyzes all files containing SQL queries, table definitions, and SQL-related codes in the Interactive Digital Cultural Map project.

## 1. models.py
Contains SQLAlchemy model definitions for all database tables.

### Table Definitions:
- **User**: Stores user accounts with authentication details.
  - Columns: id (primary key), username, email, password_hash, role, barangay, is_approved
- **Attraction**: Stores tourist attractions.
  - Columns: id, name, description, category, barangay, lat, lng, image_url, status, user_id (FK to User), created_at
- **Event**: Stores cultural events.
  - Columns: id, title, description, date, location, barangay, image_url, user_id, status, category, created_at
- **GalleryItem**: Stores photo/video uploads.
  - Columns: id, type, url, caption, user_id, status, uploaded_at
- **BarangayInfo**: Stores barangay profile information.
  - Columns: id, barangay_name, history, cultural_assets, traditions, local_practices, unique_features, user_id, updated_at
- **PageView**: Tracks page views for analytics.
  - Columns: id, view_type, item_id, page_name, timestamp, user_id

## 2. flask_app.py
Handles database initialization and seeding.

### SQL-Related Code:
- Database configuration: `SQLALCHEMY_DATABASE_URI = 'sqlite:///mangatarem.db'`
- `db.init_app(app)` - Initializes SQLAlchemy
- `db.create_all()` - Creates all tables
- Seeding: Adds default attractions from JSON, creates admin and contributor users
  - `db.session.add(attraction)`
  - `db.session.commit()`

## 3. seed_events.py
Seeds the database with sample events.

### SQL-Related Code:
- Checks if events exist: `Event.query.count() > 0`
- Adds events: `db.session.add(event)`
- Commits: `db.session.commit()`

## 4. routes/auth.py
Handles user authentication and registration.

### SQL-Related Code:
- User registration: `db.session.add(user)` and `db.session.commit()`

## 5. routes/admin.py
Admin dashboard with CRUD operations and analytics.

### SQL-Related Code:
- Analytics queries:
  - Top attractions: `db.session.query(Attraction.name, func.count(PageView.id)).join(PageView).group_by(Attraction.id).order_by(func.count(PageView.id).desc()).limit(5)`
  - Daily views: `db.session.query(func.date(PageView.timestamp).label('date'), func.count(PageView.id)).group_by(func.date(PageView.timestamp)).order_by(func.date(PageView.timestamp).desc()).limit(7)`
- User approval: `user.is_approved = True; db.session.commit()`
- Delete operations: `db.session.delete(user); db.session.commit()`
- Attraction approval: `attraction.status = 'approved'; db.session.commit()`
- Attraction deletion: `db.session.delete(attraction); db.session.commit()`
- Event approval/deletion: Similar to attractions
- Gallery approval/deletion: Similar

## 6. routes/barangay.py
Barangay contributor CRUD operations.

### SQL-Related Code:
- Add attraction: `db.session.add(attraction); db.session.commit()`
- Update attraction: `db.session.commit()`
- Delete attraction: `db.session.delete(attraction); db.session.commit()`
- Similar for events and gallery items
- Barangay profile: Add/update BarangayInfo

## 7. routes/public.py
Public-facing routes with read queries.

### SQL-Related Code:
- Record page views: `db.session.add(view); db.session.commit()`
- Fetch barangays for map: `db.session.query(Attraction.barangay).filter(Attraction.status == 'approved').distinct()`
- Gallery barangays: `db.session.query(User.barangay).join(GalleryItem).filter(GalleryItem.status == 'approved').distinct()`
- Search filters: `db.session.query(Attraction.category).distinct()`, `db.session.query(Attraction.barangay).filter(Attraction.barangay != None).distinct()`
- Barangay names: `db.session.query(User.barangay).filter(User.role == 'contributor').distinct()`

## Summary
The project uses SQLAlchemy ORM for all database interactions. No raw SQL queries are present. The database is SQLite for development. Tables include users, attractions, events, gallery items, barangay info, and page views. Operations cover full CRUD plus analytics queries.
