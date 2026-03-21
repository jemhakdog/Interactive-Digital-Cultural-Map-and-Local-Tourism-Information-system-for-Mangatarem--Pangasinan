-- Initial schema for Mangatarem Cultural Mapping System (SQLite)
-- Alignment: models.py and heritage_models detail classes (2025-03-21)

PRAGMA foreign_keys = ON;

-- Barangay Information
CREATE TABLE IF NOT EXISTS BARANGAY_INFO (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL,
    map_geo_json JSON,
    location_data JSON,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- User Table
CREATE TABLE IF NOT EXISTS "USER" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    barangay_id INTEGER,
    is_approved BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (barangay_id) REFERENCES BARANGAY_INFO(id)
);

-- Password Reset Tokens
CREATE TABLE IF NOT EXISTS PASSWORD_RESET_TOKEN (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    token VARCHAR(128) UNIQUE NOT NULL,
    expires_at DATETIME NOT NULL,
    used BOOLEAN DEFAULT 0 NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES "USER"(id)
);

-- Core Heritage Profile (Base for all forms)
CREATE TABLE IF NOT EXISTS HERITAGE_PROFILE (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_type VARCHAR(50) NOT NULL,
    form_control_number VARCHAR(100) UNIQUE,
    name_of_asset VARCHAR(200),
    common_name VARCHAR(200),
    barangay_id INTEGER,
    location_details TEXT,
    contact_person VARCHAR(200),
    contact_number VARCHAR(50),
    ownership_type VARCHAR(50),
    owner_administrator VARCHAR(200),
    usage_status VARCHAR(50),
    latitude FLOAT,
    longitude FLOAT,
    significance TEXT,
    conservation_status TEXT,
    mapper_name VARCHAR(200),
    date_profiled DATE,
    status VARCHAR(20) DEFAULT 'pending',
    user_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (barangay_id) REFERENCES BARANGAY_INFO(id),
    FOREIGN KEY (user_id) REFERENCES "USER"(id)
);

-- Tourism Attractions
CREATE TABLE IF NOT EXISTS ATTRACTION (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(50) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    image_url VARCHAR(500),
    barangay_id INTEGER,
    heritage_profile_id INTEGER,
    status VARCHAR(20) DEFAULT 'pending',
    user_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (barangay_id) REFERENCES BARANGAY_INFO(id),
    FOREIGN KEY (heritage_profile_id) REFERENCES HERITAGE_PROFILE(id),
    FOREIGN KEY (user_id) REFERENCES "USER"(id)
);

-- Events
CREATE TABLE IF NOT EXISTS EVENT (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    date DATETIME NOT NULL,
    location VARCHAR(255) NOT NULL,
    barangay_id INTEGER,
    image_url VARCHAR(500),
    category VARCHAR(50) DEFAULT 'Civic',
    status VARCHAR(20) DEFAULT 'pending',
    user_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (barangay_id) REFERENCES BARANGAY_INFO(id),
    FOREIGN KEY (user_id) REFERENCES "USER"(id)
);

-- Gallery items
CREATE TABLE IF NOT EXISTS GALLERY_ITEM (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type VARCHAR(20) NOT NULL,
    url VARCHAR(500) NOT NULL,
    caption TEXT,
    user_id INTEGER,
    status VARCHAR(20) DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES "USER"(id)
);

-- Analytics
CREATE TABLE IF NOT EXISTS ANALYTICS_PAGE_VIEW (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    page_url VARCHAR(500) NOT NULL,
    user_id INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    session_id VARCHAR(100),
    ip_address VARCHAR(45),
    device_info TEXT
);

-- User Interactions
CREATE TABLE IF NOT EXISTS USER_FAVORITE_ATTRACTION (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    attraction_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES "USER"(id),
    FOREIGN KEY (attraction_id) REFERENCES ATTRACTION(id)
);

CREATE TABLE IF NOT EXISTS USER_EVENT_INTEREST (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    event_id INTEGER NOT NULL,
    status VARCHAR(20) DEFAULT 'interested',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES "USER"(id),
    FOREIGN KEY (event_id) REFERENCES EVENT(id)
);

CREATE TABLE IF NOT EXISTS ATTRACTION_REVIEW (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    attraction_id INTEGER NOT NULL,
    rating INTEGER NOT NULL,
    comment TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES "USER"(id),
    FOREIGN KEY (attraction_id) REFERENCES ATTRACTION(id)
);

-- Newsletter
CREATE TABLE IF NOT EXISTS NEWSLETTER_SUBSCRIBER (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(120) UNIQUE NOT NULL,
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- === Heritage Form Detail Tables ===

-- Form 01A: Natural Heritage
CREATE TABLE IF NOT EXISTS NATURAL_HERITAGE (
    heritage_profile_id INTEGER PRIMARY KEY,
    scientific_name VARCHAR(200),
    common_name VARCHAR(200),
    conservation_status VARCHAR(100),
    description TEXT,
    FOREIGN KEY (heritage_profile_id) REFERENCES HERITAGE_PROFILE(id)
);

-- Form 02A: Built Heritage Detail
CREATE TABLE IF NOT EXISTS BUILT_HERITAGE_DETAIL (
    heritage_profile_id INTEGER PRIMARY KEY,
    kind_of_structure VARCHAR(100),
    historical_significance TEXT,
    architectural_description TEXT,
    estimated_date_of_construction VARCHAR(100),
    FOREIGN KEY (heritage_profile_id) REFERENCES HERITAGE_PROFILE(id)
);

-- Form 03A: Tangible Movable (Archaeological) Heritage
CREATE TABLE IF NOT EXISTS MOVABLE_HERITAGE_DETAIL (
    heritage_profile_id INTEGER PRIMARY KEY,
    type_of_object VARCHAR(100),
    material TEXT,
    dimensions VARCHAR(100),
    current_location TEXT,
    state_of_conservation TEXT,
    FOREIGN KEY (heritage_profile_id) REFERENCES HERITAGE_PROFILE(id)
);

-- Form 04A: Intangible Cultural Heritage
CREATE TABLE IF NOT EXISTS INTANGIBLE_HERITAGE_DETAIL (
    heritage_profile_id INTEGER PRIMARY KEY,
    category VARCHAR(100),
    description TEXT,
    practitioners TEXT,
    transmission_mode TEXT,
    FOREIGN KEY (heritage_profile_id) REFERENCES HERITAGE_PROFILE(id)
);

-- Form 05: Significant Personalities
CREATE TABLE IF NOT EXISTS PERSONALITY_DETAIL (
    heritage_profile_id INTEGER PRIMARY KEY,
    full_name VARCHAR(200),
    dates_of_birth_death VARCHAR(100),
    place_of_birth VARCHAR(200),
    major_achievements TEXT,
    FOREIGN KEY (heritage_profile_id) REFERENCES HERITAGE_PROFILE(id)
);

-- Form 06: Cultural Institutions
CREATE TABLE IF NOT EXISTS INSTITUTION_DETAIL (
    heritage_profile_id INTEGER PRIMARY KEY,
    type_of_institution VARCHAR(100),
    year_established INTEGER,
    head_of_institution VARCHAR(200),
    activities_services TEXT,
    FOREIGN KEY (heritage_profile_id) REFERENCES HERITAGE_PROFILE(id)
);

-- Form 07: LGU Programs and Projects for Culture
CREATE TABLE IF NOT EXISTS LGU_PROGRAM_DETAIL (
    heritage_profile_id INTEGER PRIMARY KEY,
    program_name VARCHAR(200),
    starting_year INTEGER,
    description TEXT,
    culture_projects JSON,
    FOREIGN KEY (heritage_profile_id) REFERENCES HERITAGE_PROFILE(id)
);

-- Indices for performance
CREATE INDEX IF NOT EXISTS idx_attraction_category ON ATTRACTION(category);
CREATE INDEX IF NOT EXISTS idx_heritage_profile_status ON HERITAGE_PROFILE(status);
CREATE INDEX IF NOT EXISTS idx_heritage_profile_asset_type ON HERITAGE_PROFILE(asset_type);
CREATE INDEX IF NOT EXISTS idx_event_date ON EVENT(date);
CREATE INDEX IF NOT EXISTS idx_newsletter_email ON NEWSLETTER_SUBSCRIBER(email);
