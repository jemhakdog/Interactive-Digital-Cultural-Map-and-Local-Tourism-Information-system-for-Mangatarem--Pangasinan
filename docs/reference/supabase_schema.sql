-- ================================================
-- Mangatarem Cultural Map Database Schema
-- For Supabase/PostgreSQL
-- ================================================

-- 1. USER TABLE
CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(256),
    role VARCHAR(20) DEFAULT 'user',
    barangay VARCHAR(100),
    is_approved BOOLEAN DEFAULT FALSE
);

CREATE INDEX idx_user_email ON "user" (email);

CREATE INDEX idx_user_role ON "user" (role);

-- 2. ATTRACTION TABLE
CREATE TABLE IF NOT EXISTS attraction (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(50) NOT NULL,
    barangay VARCHAR(100),
    lat DOUBLE PRECISION NOT NULL,
    lng DOUBLE PRECISION NOT NULL,
    image_url VARCHAR(200),
    status VARCHAR(20) DEFAULT 'pending',
    user_id INTEGER REFERENCES "user" (id) ON DELETE SET NULL,
    reviewed_by INTEGER REFERENCES "user" (id) ON DELETE SET NULL,
    reviewed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_attraction_name ON attraction (name);

CREATE INDEX idx_attraction_category ON attraction (category);

CREATE INDEX idx_attraction_barangay ON attraction (barangay);

CREATE INDEX idx_attraction_status ON attraction (status);

CREATE INDEX idx_attraction_user_id ON attraction (user_id);

CREATE INDEX idx_attraction_created_at ON attraction (created_at);

-- 3. EVENT TABLE
CREATE TABLE IF NOT EXISTS event (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    date TIMESTAMP NOT NULL,
    location VARCHAR(100) NOT NULL,
    barangay VARCHAR(100),
    image_url VARCHAR(200),
    user_id INTEGER REFERENCES "user" (id) ON DELETE SET NULL,
    status VARCHAR(20) DEFAULT 'pending',
    category VARCHAR(50) NOT NULL DEFAULT 'Civic',
    reviewed_by INTEGER REFERENCES "user" (id) ON DELETE SET NULL,
    reviewed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_event_date ON event(date);

CREATE INDEX idx_event_status ON event(status);

CREATE INDEX idx_event_category ON event(category);

-- 4. GALLERY_ITEM TABLE
CREATE TABLE IF NOT EXISTS gallery_item (
    id SERIAL PRIMARY KEY,
    type VARCHAR(20) NOT NULL,
    url VARCHAR(200) NOT NULL,
    caption VARCHAR(200),
    user_id INTEGER REFERENCES "user" (id) ON DELETE SET NULL,
    status VARCHAR(20) DEFAULT 'pending',
    reviewed_by INTEGER REFERENCES "user" (id) ON DELETE SET NULL,
    reviewed_at TIMESTAMP,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_gallery_item_status ON gallery_item (status);

-- 5. BARANGAY_INFO TABLE
CREATE TABLE IF NOT EXISTS barangay_info (
    id SERIAL PRIMARY KEY,
    barangay_name VARCHAR(100) UNIQUE NOT NULL,
    history TEXT,
    cultural_assets TEXT,
    traditions TEXT,
    local_practices TEXT,
    unique_features TEXT,
    user_id INTEGER REFERENCES "user" (id) ON DELETE SET NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_barangay_info_name ON barangay_info (barangay_name);

-- 6. PAGE_VIEW TABLE (Analytics)
CREATE TABLE IF NOT EXISTS page_view (
    id SERIAL PRIMARY KEY,
    view_type VARCHAR(50) NOT NULL,
    item_id INTEGER,
    page_name VARCHAR(100),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER
);

CREATE INDEX idx_page_view_type ON page_view (view_type);

CREATE INDEX idx_page_view_timestamp ON page_view (timestamp);

-- 7. FAVORITE TABLE
CREATE TABLE IF NOT EXISTS favorite (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES "user" (id) ON DELETE CASCADE,
    attraction_id INTEGER NOT NULL REFERENCES attraction (id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, attraction_id)
);

CREATE INDEX idx_favorite_user_id ON favorite (user_id);

CREATE INDEX idx_favorite_attraction_id ON favorite (attraction_id);

-- 8. EVENT_INTEREST TABLE
CREATE TABLE IF NOT EXISTS event_interest (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES "user" (id) ON DELETE CASCADE,
    event_id INTEGER NOT NULL REFERENCES event (id) ON DELETE CASCADE,
    status VARCHAR(20) DEFAULT 'interested',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, event_id)
);

CREATE INDEX idx_event_interest_user_id ON event_interest (user_id);

CREATE INDEX idx_event_interest_event_id ON event_interest (event_id);

-- 9. REVIEW TABLE
CREATE TABLE IF NOT EXISTS review (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES "user" (id) ON DELETE CASCADE,
    attraction_id INTEGER NOT NULL REFERENCES attraction (id) ON DELETE CASCADE,
    rating INTEGER NOT NULL CHECK (
        rating >= 1
        AND rating <= 5
    ),
    comment TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    reviewed_by INTEGER REFERENCES "user" (id) ON DELETE SET NULL,
    reviewed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_review_user_id ON review (user_id);

CREATE INDEX idx_review_attraction_id ON review (attraction_id);

CREATE INDEX idx_review_status ON review (status);

-- ================================================
-- OPTIONAL: Create an admin user (update password!)
-- ================================================
-- INSERT INTO "user" (username, email, password_hash, role, is_approved)
-- VALUES ('admin', 'admin@example.com', 'YOUR_HASHED_PASSWORD', 'admin', TRUE);