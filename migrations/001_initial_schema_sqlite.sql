-- ============================================================
-- Migration: 001_initial_schema_sqlite
-- Database: SQLite
-- Generated: 2026-02-18
-- Description: Consolidated initial schema for Mangatarem Cultural Heritage & Tourism
-- ============================================================

-- Enable foreign key support (SQLite specific)
PRAGMA foreign_keys = ON;

-- ============================================================
-- CORE TABLES
-- ============================================================

-- User accounts with roles (admin, contributor, user)
CREATE TABLE IF NOT EXISTS "user" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128),
    role VARCHAR(20) DEFAULT 'user',
    barangay VARCHAR(100),
    is_approved BOOLEAN DEFAULT FALSE
);

-- Base model for all cultural heritage documentation
CREATE TABLE IF NOT EXISTS heritage_profile (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_type VARCHAR(50) NOT NULL,
    form_control_number VARCHAR(50) UNIQUE,
    mapper_name VARCHAR(200),
    date_profiled DATE,
    status VARCHAR(20) DEFAULT 'pending',
    user_id INTEGER,
    reviewed_by INTEGER,
    reviewed_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    key_informants JSON,
    reference_sources TEXT,
    significance TEXT,
    constraints_threats TEXT,
    conservation_measures TEXT,
    common_photo_url VARCHAR(500),
    FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE SET NULL,
    FOREIGN KEY (reviewed_by) REFERENCES "user"(id) ON DELETE SET NULL
);

-- Tourism attractions and spots
CREATE TABLE IF NOT EXISTS attraction (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(50) NOT NULL,
    barangay VARCHAR(100),
    lat FLOAT NOT NULL,
    lng FLOAT NOT NULL,
    image_url VARCHAR(200),
    form_control_number VARCHAR(50),
    heritage_profile_id INTEGER,
    status VARCHAR(20) DEFAULT 'pending',
    user_id INTEGER,
    reviewed_by INTEGER,
    reviewed_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (heritage_profile_id) REFERENCES heritage_profile(id) ON DELETE SET NULL,
    FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE SET NULL,
    FOREIGN KEY (reviewed_by) REFERENCES "user"(id) ON DELETE SET NULL
);

-- Local events and festivals
CREATE TABLE IF NOT EXISTS event (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    date DATETIME NOT NULL,
    location VARCHAR(100) NOT NULL,
    barangay VARCHAR(100),
    image_url VARCHAR(200),
    user_id INTEGER,
    status VARCHAR(20) DEFAULT 'pending',
    category VARCHAR(50) NOT NULL DEFAULT 'Civic',
    reviewed_by INTEGER,
    reviewed_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE SET NULL,
    FOREIGN KEY (reviewed_by) REFERENCES "user"(id) ON DELETE SET NULL
);

-- Photo and video gallery items
CREATE TABLE IF NOT EXISTS gallery_item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type VARCHAR(20) NOT NULL,
    url VARCHAR(200) NOT NULL,
    caption VARCHAR(200),
    user_id INTEGER,
    status VARCHAR(20) DEFAULT 'pending',
    reviewed_by INTEGER,
    reviewed_at DATETIME,
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE SET NULL,
    FOREIGN KEY (reviewed_by) REFERENCES "user"(id) ON DELETE SET NULL
);

-- Barangay-level cultural information
CREATE TABLE IF NOT EXISTS barangay_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    barangay_name VARCHAR(100) UNIQUE NOT NULL,
    history TEXT,
    cultural_assets TEXT,
    traditions TEXT,
    local_practices TEXT,
    unique_features TEXT,
    user_id INTEGER,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE SET NULL
);

-- ============================================================
-- ANALYTICS & USER ENGAGEMENT TABLES
-- ============================================================

-- Page view tracking for analytics
CREATE TABLE IF NOT EXISTS page_view (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    view_type VARCHAR(50) NOT NULL,
    item_id INTEGER,
    page_name VARCHAR(100),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE SET NULL
);

-- User favorite attractions
CREATE TABLE IF NOT EXISTS favorite (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    attraction_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE CASCADE,
    FOREIGN KEY (attraction_id) REFERENCES attraction(id) ON DELETE CASCADE,
    UNIQUE(user_id, attraction_id)
);

-- User interest in events
CREATE TABLE IF NOT EXISTS event_interest (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    event_id INTEGER NOT NULL,
    status VARCHAR(20) DEFAULT 'interested',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES event(id) ON DELETE CASCADE,
    UNIQUE(user_id, event_id)
);

-- User reviews and ratings for attractions
CREATE TABLE IF NOT EXISTS review (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    attraction_id INTEGER NOT NULL,
    rating INTEGER NOT NULL,
    comment TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    reviewed_by INTEGER,
    reviewed_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE CASCADE,
    FOREIGN KEY (attraction_id) REFERENCES attraction(id) ON DELETE CASCADE,
    FOREIGN KEY (reviewed_by) REFERENCES "user"(id) ON DELETE SET NULL
);

-- ============================================================
-- HERITAGE DETAIL TABLES (Tourism Forms)
-- ============================================================

-- Form 01A: Natural Heritage Details (Natural Resources and Land Formations)
CREATE TABLE IF NOT EXISTS natural_heritage_details (
    profile_id INTEGER PRIMARY KEY,
    subcategory VARCHAR(50),
    area_hectares FLOAT,
    ownership VARCHAR(200),
    protection_status VARCHAR(100),
    FOREIGN KEY (profile_id) REFERENCES heritage_profile(id) ON DELETE CASCADE
);

-- Form 02A: Built Heritage Details (Tangible Immovable Heritage)
CREATE TABLE IF NOT EXISTS built_heritage_details (
    profile_id INTEGER PRIMARY KEY,
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
    movable_heritage_list JSON,
    FOREIGN KEY (profile_id) REFERENCES heritage_profile(id) ON DELETE CASCADE
);

-- Form 03A: Movable Heritage Details (Archaeological Heritage)
CREATE TABLE IF NOT EXISTS movable_heritage_details (
    profile_id INTEGER PRIMARY KEY,
    object_type VARCHAR(50),
    place_found VARCHAR(200),
    date_found DATE,
    estimated_age VARCHAR(100),
    acquisition_type VARCHAR(50),
    materials VARCHAR(200),
    dimensions VARCHAR(100),
    comparative_criteria TEXT,
    FOREIGN KEY (profile_id) REFERENCES heritage_profile(id) ON DELETE CASCADE
);

-- Form 04A: Intangible Heritage Details (Oral Traditions and Expressions)
CREATE TABLE IF NOT EXISTS intangible_heritage_details (
    profile_id INTEGER PRIMARY KEY,
    heritage_type VARCHAR(50),
    geographical_range TEXT,
    related_domains JSON,
    culture_bearers TEXT,
    culture_bearer_photos JSON,
    transmission_mode TEXT,
    objects_used JSON,
    flora_fauna_used JSON,
    safeguarding_measures JSON,
    supporting_docs JSON,
    FOREIGN KEY (profile_id) REFERENCES heritage_profile(id) ON DELETE CASCADE
);

-- Form 05: Personality Profile Details (Significant Personalities)
CREATE TABLE IF NOT EXISTS personality_details (
    profile_id INTEGER PRIMARY KEY,
    date_of_birth DATE,
    date_of_death DATE,
    birth_place VARCHAR(200),
    present_address VARCHAR(300),
    age INTEGER,
    prominence_field VARCHAR(100),
    biography TEXT,
    works_achievements JSON,
    FOREIGN KEY (profile_id) REFERENCES heritage_profile(id) ON DELETE CASCADE
);

-- Form 06: Cultural Institution Details (Libraries, Museums, Schools)
CREATE TABLE IF NOT EXISTS institution_details (
    profile_id INTEGER PRIMARY KEY,
    municipality VARCHAR(100),
    province VARCHAR(100),
    institution_type VARCHAR(100),
    mandate_description TEXT,
    milestones TEXT,
    condition_status TEXT,
    supporting_docs JSON,
    FOREIGN KEY (profile_id) REFERENCES heritage_profile(id) ON DELETE CASCADE
);

-- Form 07: LGU Culture Program Details (Municipal Programs and Policies)
CREATE TABLE IF NOT EXISTS lgu_program_details (
    profile_id INTEGER PRIMARY KEY,
    vision_statement TEXT,
    mission_statement TEXT,
    goal_statements TEXT,
    adoption_date DATE,
    brief_history TEXT,
    logo_url VARCHAR(500),
    logo_legislation_date DATE,
    logo_explanation TEXT,
    chief_executives JSON,
    resolutions JSON,
    ordinances JSON,
    ela_action_items JSON,
    major_policies JSON,
    program_strategies TEXT,
    annual_investments JSON,
    culture_projects JSON,
    arts_council JSON,
    alternative_livelihoods JSON,
    community_enterprises JSON,
    peoples_stories TEXT,
    FOREIGN KEY (profile_id) REFERENCES heritage_profile(id) ON DELETE CASCADE
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

-- Event indexes
CREATE INDEX IF NOT EXISTS idx_event_date ON event(date);
CREATE INDEX IF NOT EXISTS idx_event_status ON event(status);
CREATE INDEX IF NOT EXISTS idx_event_category ON event(category);

-- Heritage profile indexes
CREATE INDEX IF NOT EXISTS idx_heritage_profile_status ON heritage_profile(status);
CREATE INDEX IF NOT EXISTS idx_heritage_profile_asset_type ON heritage_profile(asset_type);
CREATE INDEX IF NOT EXISTS idx_heritage_profile_created_at ON heritage_profile(created_at);

-- Page view indexes
CREATE INDEX IF NOT EXISTS idx_page_view_timestamp ON page_view(timestamp);
CREATE INDEX IF NOT EXISTS idx_page_view_type ON page_view(view_type);

-- Review indexes
CREATE INDEX IF NOT EXISTS idx_review_attraction_id ON review(attraction_id);
CREATE INDEX IF NOT EXISTS idx_review_status ON review(status);

-- Gallery item indexes
CREATE INDEX IF NOT EXISTS idx_gallery_item_status ON gallery_item(status);
CREATE INDEX IF NOT EXISTS idx_gallery_item_type ON gallery_item(type);

-- Heritage detail table indexes
CREATE INDEX IF NOT EXISTS idx_natural_heritage_profile_id ON natural_heritage_details(profile_id);
CREATE INDEX IF NOT EXISTS idx_built_heritage_profile_id ON built_heritage_details(profile_id);
CREATE INDEX IF NOT EXISTS idx_movable_heritage_profile_id ON movable_heritage_details(profile_id);
CREATE INDEX IF NOT EXISTS idx_intangible_heritage_profile_id ON intangible_heritage_details(profile_id);
CREATE INDEX IF NOT EXISTS idx_personality_profile_id ON personality_details(profile_id);
CREATE INDEX IF NOT EXISTS idx_institution_profile_id ON institution_details(profile_id);
CREATE INDEX IF NOT EXISTS idx_lgu_program_profile_id ON lgu_program_details(profile_id);

-- ============================================================
-- END OF MIGRATION 001
-- ============================================================
