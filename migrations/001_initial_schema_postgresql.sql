-- ============================================================
-- Migration: 001_initial_schema_postgresql
-- Database: PostgreSQL (Supabase compatible)
-- Generated: 2026-02-18
-- Description: Consolidated initial schema for Mangatarem Cultural Heritage & Tourism
-- ============================================================

-- ============================================================
-- CORE TABLES
-- ============================================================

-- User accounts with roles (admin, contributor, user)
CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(256),
    role VARCHAR(20) DEFAULT 'user',
    barangay VARCHAR(100),
    is_approved BOOLEAN DEFAULT FALSE
);

-- Base model for all cultural heritage documentation
CREATE TABLE IF NOT EXISTS heritage_profile (
    id SERIAL PRIMARY KEY,
    asset_type VARCHAR(50) NOT NULL,
    form_control_number VARCHAR(50) UNIQUE,
    mapper_name VARCHAR(200),
    date_profiled DATE,
    status VARCHAR(20) DEFAULT 'pending',
    user_id INTEGER REFERENCES "user"(id) ON DELETE SET NULL,
    reviewed_by INTEGER REFERENCES "user"(id) ON DELETE SET NULL,
    reviewed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    key_informants JSONB,
    reference_sources TEXT,
    significance TEXT,
    constraints_threats TEXT,
    conservation_measures TEXT,
    common_photo_url VARCHAR(500)
);

-- Tourism attractions and spots
CREATE TABLE IF NOT EXISTS attraction (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(50) NOT NULL,
    barangay VARCHAR(100),
    lat DOUBLE PRECISION NOT NULL,
    lng DOUBLE PRECISION NOT NULL,
    image_url VARCHAR(200),
    form_control_number VARCHAR(50),
    heritage_profile_id INTEGER REFERENCES heritage_profile(id) ON DELETE SET NULL,
    status VARCHAR(20) DEFAULT 'pending',
    user_id INTEGER REFERENCES "user"(id) ON DELETE SET NULL,
    reviewed_by INTEGER REFERENCES "user"(id) ON DELETE SET NULL,
    reviewed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Local events and festivals
CREATE TABLE IF NOT EXISTS event (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    date TIMESTAMP NOT NULL,
    location VARCHAR(100) NOT NULL,
    barangay VARCHAR(100),
    image_url VARCHAR(200),
    user_id INTEGER REFERENCES "user"(id) ON DELETE SET NULL,
    status VARCHAR(20) DEFAULT 'pending',
    category VARCHAR(50) NOT NULL DEFAULT 'Civic',
    reviewed_by INTEGER REFERENCES "user"(id) ON DELETE SET NULL,
    reviewed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Photo and video gallery items
CREATE TABLE IF NOT EXISTS gallery_item (
    id SERIAL PRIMARY KEY,
    type VARCHAR(20) NOT NULL,
    url VARCHAR(200) NOT NULL,
    caption VARCHAR(200),
    user_id INTEGER REFERENCES "user"(id) ON DELETE SET NULL,
    status VARCHAR(20) DEFAULT 'pending',
    reviewed_by INTEGER REFERENCES "user"(id) ON DELETE SET NULL,
    reviewed_at TIMESTAMP,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Barangay-level cultural information
CREATE TABLE IF NOT EXISTS barangay_info (
    id SERIAL PRIMARY KEY,
    barangay_name VARCHAR(100) UNIQUE NOT NULL,
    history TEXT,
    cultural_assets TEXT,
    traditions TEXT,
    local_practices TEXT,
    unique_features TEXT,
    user_id INTEGER REFERENCES "user"(id) ON DELETE SET NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- ANALYTICS & USER ENGAGEMENT TABLES
-- ============================================================

-- Page view tracking for analytics
CREATE TABLE IF NOT EXISTS analytics_page_view (
    id SERIAL PRIMARY KEY,
    view_type VARCHAR(50) NOT NULL,
    item_id INTEGER,
    page_name VARCHAR(100),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE SET NULL
);

-- User favorite attractions
CREATE TABLE IF NOT EXISTS user_favorite_attraction (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    attraction_id INTEGER NOT NULL REFERENCES attraction(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, attraction_id)
);

-- User interest in events
CREATE TABLE IF NOT EXISTS user_event_interest (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    event_id INTEGER NOT NULL REFERENCES event(id) ON DELETE CASCADE,
    status VARCHAR(20) DEFAULT 'interested',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, event_id)
);

-- User reviews and ratings for attractions
CREATE TABLE IF NOT EXISTS attraction_review (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    attraction_id INTEGER NOT NULL REFERENCES attraction(id) ON DELETE CASCADE,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    reviewed_by INTEGER REFERENCES "user"(id) ON DELETE SET NULL,
    reviewed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- HERITAGE DETAIL TABLES (Tourism Forms)
-- ============================================================

-- Form 01A: Natural Heritage Details (Natural Resources and Land Formations)
CREATE TABLE IF NOT EXISTS natural_heritage_details (
    profile_id INTEGER PRIMARY KEY REFERENCES heritage_profile(id) ON DELETE CASCADE,
    subcategory VARCHAR(50),
    area_hectares FLOAT,
    ownership VARCHAR(200),
    protection_status VARCHAR(100)
);

-- Form 02A: Built Heritage Details (Tangible Immovable Heritage)
CREATE TABLE IF NOT EXISTS built_heritage_details (
    profile_id INTEGER PRIMARY KEY REFERENCES heritage_profile(id) ON DELETE CASCADE,
    building_type VARCHAR(50),
    year_constructed INTEGER,
    ownership_type VARCHAR(20),
    declaration_legislation TEXT,
    physical_description TEXT,
    history_structure TEXT,
    occupation_status VARCHAR(20),
    is_altered BOOLEAN,
    is_original_site BOOLEAN,
    integrity_remarks TEXT,
    movable_heritage_list JSONB
);

-- Form 03A: Movable Heritage Details (Archaeological Heritage)
CREATE TABLE IF NOT EXISTS movable_heritage_details (
    profile_id INTEGER PRIMARY KEY REFERENCES heritage_profile(id) ON DELETE CASCADE,
    object_type VARCHAR(50),
    place_found VARCHAR(200),
    date_found DATE,
    estimated_age VARCHAR(100),
    acquisition_type VARCHAR(50),
    materials VARCHAR(200),
    dimensions VARCHAR(100),
    comparative_criteria TEXT
);

-- Form 04A: Intangible Heritage Details (Oral Traditions and Expressions)
CREATE TABLE IF NOT EXISTS intangible_heritage_details (
    profile_id INTEGER PRIMARY KEY REFERENCES heritage_profile(id) ON DELETE CASCADE,
    heritage_type VARCHAR(50),
    geographical_range TEXT,
    related_domains JSONB,
    culture_bearers TEXT,
    culture_bearer_photos JSONB,
    transmission_mode TEXT,
    objects_used JSONB,
    flora_fauna_used JSONB,
    safeguarding_measures JSONB,
    supporting_docs JSONB
);

-- Form 05: Personality Profile Details (Significant Personalities)
CREATE TABLE IF NOT EXISTS personality_details (
    profile_id INTEGER PRIMARY KEY REFERENCES heritage_profile(id) ON DELETE CASCADE,
    date_of_birth DATE,
    date_of_death DATE,
    birth_place VARCHAR(200),
    present_address VARCHAR(300),
    age INTEGER,
    prominence_field VARCHAR(100),
    biography TEXT,
    works_achievements JSONB
);

-- Form 06: Cultural Institution Details (Libraries, Museums, Schools)
CREATE TABLE IF NOT EXISTS institution_details (
    profile_id INTEGER PRIMARY KEY REFERENCES heritage_profile(id) ON DELETE CASCADE,
    municipality VARCHAR(100),
    province VARCHAR(100),
    institution_type VARCHAR(100),
    mandate_description TEXT,
    milestones TEXT,
    condition_status TEXT,
    supporting_docs JSONB
);

-- Form 07: LGU Culture Program Details (Municipal Programs and Policies)
CREATE TABLE IF NOT EXISTS lgu_program_details (
    profile_id INTEGER PRIMARY KEY REFERENCES heritage_profile(id) ON DELETE CASCADE,
    vision_statement TEXT,
    mission_statement TEXT,
    goal_statements TEXT,
    adoption_date DATE,
    brief_history TEXT,
    logo_url VARCHAR(500),
    logo_legislation_date DATE,
    logo_explanation TEXT,
    chief_executives JSONB,
    resolutions JSONB,
    ordinances JSONB,
    ela_action_items JSONB,
    major_policies JSONB,
    program_strategies TEXT,
    annual_investments JSONB,
    culture_projects JSONB,
    arts_council JSONB,
    alternative_livelihoods JSONB,
    community_enterprises JSONB,
    peoples_stories TEXT
);

-- ============================================================
-- INDEXES FOR PERFORMANCE
-- ============================================================

-- User indexes
CREATE INDEX IF NOT EXISTS idx_user_username ON "user"(username);
CREATE INDEX IF NOT EXISTS idx_user_email ON "user"(email);
CREATE INDEX IF NOT EXISTS idx_user_role ON "user"(role);

-- Attraction indexes
CREATE INDEX IF NOT EXISTS idx_attraction_name ON attraction(name);
CREATE INDEX IF NOT EXISTS idx_attraction_category ON attraction(category);
CREATE INDEX IF NOT EXISTS idx_attraction_barangay ON attraction(barangay);
CREATE INDEX IF NOT EXISTS idx_attraction_status ON attraction(status);
CREATE INDEX IF NOT EXISTS idx_attraction_user_id ON attraction(user_id);
CREATE INDEX IF NOT EXISTS idx_attraction_created_at ON attraction(created_at);
CREATE INDEX IF NOT EXISTS idx_attraction_heritage_profile_id ON attraction(heritage_profile_id);

-- Event indexes
CREATE INDEX IF NOT EXISTS idx_event_date ON event(date);
CREATE INDEX IF NOT EXISTS idx_event_status ON event(status);
CREATE INDEX IF NOT EXISTS idx_event_category ON event(category);

-- Heritage profile indexes
CREATE INDEX IF NOT EXISTS idx_heritage_profile_status ON heritage_profile(status);
CREATE INDEX IF NOT EXISTS idx_heritage_profile_asset_type ON heritage_profile(asset_type);
CREATE INDEX IF NOT EXISTS idx_heritage_profile_created_at ON heritage_profile(created_at);

-- Page view indexes
CREATE INDEX IF NOT EXISTS idx_analytics_page_view_timestamp ON analytics_page_view(timestamp);
CREATE INDEX IF NOT EXISTS idx_analytics_page_view_type ON analytics_page_view(view_type);

-- Review indexes
CREATE INDEX IF NOT EXISTS idx_attraction_review_attraction_id ON attraction_review(attraction_id);
CREATE INDEX IF NOT EXISTS idx_attraction_review_status ON attraction_review(status);
CREATE INDEX IF NOT EXISTS idx_attraction_review_user_id ON attraction_review(user_id);

-- Gallery item indexes
CREATE INDEX IF NOT EXISTS idx_gallery_item_status ON gallery_item(status);
CREATE INDEX IF NOT EXISTS idx_gallery_item_type ON gallery_item(type);

-- Favorite indexes
CREATE INDEX IF NOT EXISTS idx_user_favorite_attraction_user_id ON user_favorite_attraction(user_id);
CREATE INDEX IF NOT EXISTS idx_user_favorite_attraction_attraction_id ON user_favorite_attraction(attraction_id);

-- Event interest indexes
CREATE INDEX IF NOT EXISTS idx_user_event_interest_user_id ON user_event_interest(user_id);
CREATE INDEX IF NOT EXISTS idx_user_event_interest_event_id ON user_event_interest(event_id);

-- Barangay info index
CREATE INDEX IF NOT EXISTS idx_barangay_info_name ON barangay_info(barangay_name);

-- Heritage detail table indexes (profile_id is primary key, but add for FK lookups)
-- Note: These are already primary keys, so indexes exist automatically
-- But we add explicit indexes for FK lookups from heritage_profile
CREATE INDEX IF NOT EXISTS idx_natural_heritage_profile_id ON natural_heritage_details(profile_id);
CREATE INDEX IF NOT EXISTS idx_built_heritage_profile_id ON built_heritage_details(profile_id);
CREATE INDEX IF NOT EXISTS idx_movable_heritage_profile_id ON movable_heritage_details(profile_id);
CREATE INDEX IF NOT EXISTS idx_intangible_heritage_profile_id ON intangible_heritage_details(profile_id);
CREATE INDEX IF NOT EXISTS idx_personality_profile_id ON personality_details(profile_id);
CREATE INDEX IF NOT EXISTS idx_institution_profile_id ON institution_details(profile_id);
CREATE INDEX IF NOT EXISTS idx_lgu_program_profile_id ON lgu_program_details(profile_id);

-- ============================================================
-- ROW LEVEL SECURITY (RLS) - For Supabase
-- ============================================================

-- Enable RLS on all tables
ALTER TABLE heritage_profile ENABLE ROW LEVEL SECURITY;
ALTER TABLE attraction ENABLE ROW LEVEL SECURITY;
ALTER TABLE event ENABLE ROW LEVEL SECURITY;
ALTER TABLE gallery_item ENABLE ROW LEVEL SECURITY;
ALTER TABLE barangay_info ENABLE ROW LEVEL SECURITY;
ALTER TABLE analytics_page_view ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_favorite_attraction ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_event_interest ENABLE ROW LEVEL SECURITY;
ALTER TABLE attraction_review ENABLE ROW LEVEL SECURITY;
ALTER TABLE natural_heritage_details ENABLE ROW LEVEL SECURITY;
ALTER TABLE built_heritage_details ENABLE ROW LEVEL SECURITY;
ALTER TABLE movable_heritage_details ENABLE ROW LEVEL SECURITY;
ALTER TABLE intangible_heritage_details ENABLE ROW LEVEL SECURITY;
ALTER TABLE personality_details ENABLE ROW LEVEL SECURITY;
ALTER TABLE institution_details ENABLE ROW LEVEL SECURITY;
ALTER TABLE lgu_program_details ENABLE ROW LEVEL SECURITY;

-- Drop existing policies if they exist (for re-running migrations)
DROP POLICY IF EXISTS "Public Read Approved Profiles" ON heritage_profile;
DROP POLICY IF EXISTS "Public Read Approved Attractions" ON attraction;
DROP POLICY IF EXISTS "Public Read Approved Events" ON event;
DROP POLICY IF EXISTS "Public Read Approved Gallery" ON gallery_item;
DROP POLICY IF EXISTS "Public Read Barangay Info" ON barangay_info;
DROP POLICY IF EXISTS "Public Read Approved Reviews" ON attraction_review;
DROP POLICY IF EXISTS "Users can view own favorites" ON user_favorite_attraction;
DROP POLICY IF EXISTS "Users can view own event interests" ON user_event_interest;

-- Public read policies for approved content
CREATE POLICY "Public Read Approved Profiles" ON heritage_profile
    FOR SELECT USING (status = 'approved');

CREATE POLICY "Public Read Approved Attractions" ON attraction
    FOR SELECT USING (status = 'approved');

CREATE POLICY "Public Read Approved Events" ON event
    FOR SELECT USING (status = 'approved');

CREATE POLICY "Public Read Approved Gallery" ON gallery_item
    FOR SELECT USING (status = 'approved');

CREATE POLICY "Public Read Barangay Info" ON barangay_info
    FOR SELECT USING (true); -- Barangay info is always public

CREATE POLICY "Public Read Approved Reviews" ON attraction_review
    FOR SELECT USING (status = 'approved');

-- Users can view their own favorites and event interests
CREATE POLICY "Users can view own favorites" ON user_favorite_attraction
    FOR SELECT USING (auth.uid()::text = user_id::text OR true); -- Allow public read for now

CREATE POLICY "Users can view own event interests" ON user_event_interest
    FOR SELECT USING (auth.uid()::text = user_id::text OR true); -- Allow public read for now

-- Detail tables: inherit approval status from heritage_profile
DROP POLICY IF EXISTS "Public Read Approved Natural Details" ON natural_heritage_details;
DROP POLICY IF EXISTS "Public Read Approved Built Details" ON built_heritage_details;
DROP POLICY IF EXISTS "Public Read Approved Movable Details" ON movable_heritage_details;
DROP POLICY IF EXISTS "Public Read Approved Intangible Details" ON intangible_heritage_details;
DROP POLICY IF EXISTS "Public Read Approved Personality Details" ON personality_details;
DROP POLICY IF EXISTS "Public Read Approved Institution Details" ON institution_details;
DROP POLICY IF EXISTS "Public Read Approved LGU Program Details" ON lgu_program_details;

CREATE POLICY "Public Read Approved Natural Details" ON natural_heritage_details
    FOR SELECT USING (EXISTS (
        SELECT 1 FROM heritage_profile WHERE id = natural_heritage_details.profile_id AND status = 'approved'
    ));

CREATE POLICY "Public Read Approved Built Details" ON built_heritage_details
    FOR SELECT USING (EXISTS (
        SELECT 1 FROM heritage_profile WHERE id = built_heritage_details.profile_id AND status = 'approved'
    ));

CREATE POLICY "Public Read Approved Movable Details" ON movable_heritage_details
    FOR SELECT USING (EXISTS (
        SELECT 1 FROM heritage_profile WHERE id = movable_heritage_details.profile_id AND status = 'approved'
    ));

CREATE POLICY "Public Read Approved Intangible Details" ON intangible_heritage_details
    FOR SELECT USING (EXISTS (
        SELECT 1 FROM heritage_profile WHERE id = intangible_heritage_details.profile_id AND status = 'approved'
    ));

CREATE POLICY "Public Read Approved Personality Details" ON personality_details
    FOR SELECT USING (EXISTS (
        SELECT 1 FROM heritage_profile WHERE id = personality_details.profile_id AND status = 'approved'
    ));

CREATE POLICY "Public Read Approved Institution Details" ON institution_details
    FOR SELECT USING (EXISTS (
        SELECT 1 FROM heritage_profile WHERE id = institution_details.profile_id AND status = 'approved'
    ));

CREATE POLICY "Public Read Approved LGU Program Details" ON lgu_program_details
    FOR SELECT USING (EXISTS (
        SELECT 1 FROM heritage_profile WHERE id = lgu_program_details.profile_id AND status = 'approved'
    ));

-- ============================================================
-- END OF MIGRATION 001
-- ============================================================
