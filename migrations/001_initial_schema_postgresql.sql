-- Initial schema for Mangatarem Cultural Mapping System (PostgreSQL)
-- Alignment: models.py and heritage_models detail classes (2025-03-21)

-- Barangay Information
CREATE TABLE IF NOT EXISTS "BARANGAY_INFO" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    map_geo_json TEXT,
    location_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- User Table
CREATE TABLE IF NOT EXISTS "USER" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    barangay_id INTEGER REFERENCES "BARANGAY_INFO"(id),
    is_superuser BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Attraction Table
CREATE TABLE IF NOT EXISTS "ATTRACTION" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    category VARCHAR(50),
    latitude FLOAT,
    longitude FLOAT,
    barangay_id INTEGER REFERENCES "BARANGAY_INFO"(id),
    image_url VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Event Table
CREATE TABLE IF NOT EXISTS "EVENT" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    date DATE,
    barangay_id INTEGER REFERENCES "BARANGAY_INFO"(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Heritage Profile Table (Base)
CREATE TABLE IF NOT EXISTS "HERITAGE_PROFILE" (
    id SERIAL PRIMARY KEY,
    form_control_number VARCHAR(100),
    name_of_asset VARCHAR(200) NOT NULL,
    common_name VARCHAR(200),
    asset_type VARCHAR(100),
    barangay_id INTEGER REFERENCES "BARANGAY_INFO"(id),
    location_details TEXT,
    contact_person VARCHAR(200),
    contact_number VARCHAR(50),
    ownership_type VARCHAR(50),
    owner_administrator VARCHAR(200),
    usage_status VARCHAR(50),
    latitude FLOAT,
    longitude FLOAT,
    conservation_status TEXT,
    status VARCHAR(20) DEFAULT 'draft',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Newsletter Subscriber
CREATE TABLE IF NOT EXISTS "NEWSLETTER_SUBSCRIBER" (
    id SERIAL PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- === Heritage Form Detail Tables ===

-- Form 01A: Natural Heritage
CREATE TABLE IF NOT EXISTS "NATURAL_HERITAGE_DETAIL" (
    heritage_profile_id INTEGER PRIMARY KEY REFERENCES "HERITAGE_PROFILE"(id),
    type_of_natural_heritage VARCHAR(100),
    area_size VARCHAR(100),
    primary_features TEXT,
    biodiversity_significance TEXT
);

-- Form 02A: Built Heritage Detail
CREATE TABLE IF NOT EXISTS "BUILT_HERITAGE_DETAIL" (
    heritage_profile_id INTEGER PRIMARY KEY REFERENCES "HERITAGE_PROFILE"(id),
    kind_of_structure VARCHAR(100),
    historical_significance TEXT,
    architectural_description TEXT,
    estimated_date_of_construction VARCHAR(100)
);

-- Form 03A: Tangible Movable (Archaeological) Heritage
CREATE TABLE IF NOT EXISTS "MOVABLE_HERITAGE_DETAIL" (
    heritage_profile_id INTEGER PRIMARY KEY REFERENCES "HERITAGE_PROFILE"(id),
    type_of_object VARCHAR(100),
    material TEXT,
    dimensions VARCHAR(100),
    current_location TEXT,
    state_of_conservation TEXT
);

-- Form 04A: Intangible Cultural Heritage
CREATE TABLE IF NOT EXISTS "INTANGIBLE_HERITAGE_DETAIL" (
    heritage_profile_id INTEGER PRIMARY KEY REFERENCES "HERITAGE_PROFILE"(id),
    category VARCHAR(100),
    description TEXT,
    practitioners TEXT,
    transmission_mode TEXT
);

-- Form 05: Significant Personalities
CREATE TABLE IF NOT EXISTS "PERSONALITY_DETAIL" (
    heritage_profile_id INTEGER PRIMARY KEY REFERENCES "HERITAGE_PROFILE"(id),
    full_name VARCHAR(200),
    dates_of_birth_death VARCHAR(100),
    place_of_birth VARCHAR(200),
    major_achievements TEXT
);

-- Form 06: Cultural Institutions
CREATE TABLE IF NOT EXISTS "INSTITUTION_DETAIL" (
    heritage_profile_id INTEGER PRIMARY KEY REFERENCES "HERITAGE_PROFILE"(id),
    type_of_institution VARCHAR(100),
    year_established INTEGER,
    head_of_institution VARCHAR(200),
    activities_services TEXT
);

-- Form 07: LGU Programs and Projects for Culture
CREATE TABLE IF NOT EXISTS "LGU_PROGRAM_DETAIL" (
    heritage_profile_id INTEGER PRIMARY KEY REFERENCES "HERITAGE_PROFILE"(id),
    program_name VARCHAR(200),
    starting_year INTEGER,
    description TEXT,
    culture_projects JSONB
);

-- Table: PASS_RESET TOKEN
CREATE TABLE IF NOT EXISTS "PASSWORD_RESET_TOKEN" (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "USER"(id),
    token VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- No indices here to avoid DuplicateTable errors if they already exist on old tables.
-- They can be added later or via models.
