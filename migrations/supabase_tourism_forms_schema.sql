-- =====================================================
-- Tourism Forms Schema Migration for Supabase
-- =====================================================
-- Created: 2026-02-16
-- Description: Adds 5 new heritage tables and enhances Attraction table
-- 
-- Tables Created:
--   1. natural_heritage (Form 01A)
--   2. intangible_heritage (Form 04A)
--   3. personality_profile (Form 05)
--   4. cultural_institution (Form 06)
--   5. lgu_culture_program (Form 07)
--
-- Run this in Supabase SQL Editor
-- =====================================================

-- =====================================================
-- STEP 1: Enhance Attraction Table (Forms 02A & 03A)
-- =====================================================

ALTER TABLE attraction 
ADD COLUMN IF NOT EXISTS heritage_type VARCHAR(50),
ADD COLUMN IF NOT EXISTS building_type VARCHAR(50),
ADD COLUMN IF NOT EXISTS year_constructed INTEGER,
ADD COLUMN IF NOT EXISTS ownership_type VARCHAR(20),
ADD COLUMN IF NOT EXISTS declaration_legislation TEXT,
ADD COLUMN IF NOT EXISTS physical_description TEXT,
ADD COLUMN IF NOT EXISTS history_structure TEXT,
ADD COLUMN IF NOT EXISTS occupation_status VARCHAR(20),
ADD COLUMN IF NOT EXISTS stories_associated TEXT,
ADD COLUMN IF NOT EXISTS condition VARCHAR(20),
ADD COLUMN IF NOT EXISTS condition_remarks TEXT,
ADD COLUMN IF NOT EXISTS is_altered BOOLEAN,
ADD COLUMN IF NOT EXISTS is_original_site BOOLEAN,
ADD COLUMN IF NOT EXISTS integrity_remarks TEXT,
ADD COLUMN IF NOT EXISTS conservation_measures TEXT,
ADD COLUMN IF NOT EXISTS movable_heritage_list JSONB,
ADD COLUMN IF NOT EXISTS object_type VARCHAR(50),
ADD COLUMN IF NOT EXISTS place_found VARCHAR(200),
ADD COLUMN IF NOT EXISTS date_found DATE,
ADD COLUMN IF NOT EXISTS estimated_age VARCHAR(100),
ADD COLUMN IF NOT EXISTS acquisition_type VARCHAR(50),
ADD COLUMN IF NOT EXISTS materials VARCHAR(200),
ADD COLUMN IF NOT EXISTS dimensions VARCHAR(100),
ADD COLUMN IF NOT EXISTS comparative_criteria TEXT,
ADD COLUMN IF NOT EXISTS significance_types JSONB,
ADD COLUMN IF NOT EXISTS constraints_threats TEXT,
ADD COLUMN IF NOT EXISTS key_informants JSONB,
ADD COLUMN IF NOT EXISTS references TEXT,
ADD COLUMN IF NOT EXISTS mapper_name VARCHAR(200),
ADD COLUMN IF NOT EXISTS date_profiled DATE;

COMMENT ON COLUMN attraction.heritage_type IS 'Type: building, archaeological, natural, or standard';
COMMENT ON COLUMN attraction.condition IS 'Values: excellent, good, fair, deteriorated, ruins';

-- =====================================================
-- STEP 2: Create natural_heritage Table (Form 01A)
-- =====================================================

CREATE TABLE IF NOT EXISTS natural_heritage (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    subcategory VARCHAR(50) NOT NULL,
    location VARCHAR(200) NOT NULL,
    area_hectares FLOAT,
    ownership VARCHAR(200),
    lat FLOAT,
    lng FLOAT,
    description TEXT,
    stories TEXT,
    significance TEXT,
    protection_status VARCHAR(100),
    constraints_threats TEXT,
    conservation_measures TEXT,
    key_informants JSONB,
    references TEXT,
    mapper_name VARCHAR(200),
    date_profiled DATE,
    photo_url VARCHAR(500),
    status VARCHAR(20) DEFAULT 'pending' NOT NULL,
    user_id INTEGER REFERENCES "user"(id),
    reviewed_by INTEGER REFERENCES "user"(id),
    reviewed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP DEFAULT NOW() NOT NULL
);

CREATE INDEX IF NOT EXISTS ix_natural_heritage_name ON natural_heritage(name);
CREATE INDEX IF NOT EXISTS ix_natural_heritage_status ON natural_heritage(status);
CREATE INDEX IF NOT EXISTS ix_natural_heritage_user_id ON natural_heritage(user_id);
CREATE INDEX IF NOT EXISTS ix_natural_heritage_created_at ON natural_heritage(created_at);

COMMENT ON TABLE natural_heritage IS 'Form 01A - Natural Resources and Land Formations';

-- =====================================================
-- STEP 3: Create intangible_heritage Table (Form 04A)
-- =====================================================

CREATE TABLE IF NOT EXISTS intangible_heritage (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    type VARCHAR(50) NOT NULL,
    photo_url VARCHAR(500),
    geographical_range TEXT,
    related_domains JSONB,
    description TEXT,
    culture_bearers TEXT,
    culture_bearer_photos JSONB,
    transmission_mode TEXT,
    objects_used JSONB,
    flora_fauna_used JSONB,
    stories_associated TEXT,
    significance TEXT,
    practice_status VARCHAR(100),
    constraints_threats TEXT,
    safeguarding_measures JSONB,
    safeguarding_description TEXT,
    supporting_docs JSONB,
    key_informants JSONB,
    references TEXT,
    mapper_name VARCHAR(200),
    date_profiled DATE,
    status VARCHAR(20) DEFAULT 'pending' NOT NULL,
    user_id INTEGER REFERENCES "user"(id),
    reviewed_by INTEGER REFERENCES "user"(id),
    reviewed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP DEFAULT NOW() NOT NULL
);

CREATE INDEX IF NOT EXISTS ix_intangible_heritage_name ON intangible_heritage(name);
CREATE INDEX IF NOT EXISTS ix_intangible_heritage_status ON intangible_heritage(status);
CREATE INDEX IF NOT EXISTS ix_intangible_heritage_user_id ON intangible_heritage(user_id);
CREATE INDEX IF NOT EXISTS ix_intangible_heritage_created_at ON intangible_heritage(created_at);

COMMENT ON TABLE intangible_heritage IS 'Form 04A - Intangible Heritage (Oral Traditions, Performing Arts)';

-- =====================================================
-- STEP 4: Create personality_profile Table (Form 05)
-- =====================================================

CREATE TABLE IF NOT EXISTS personality_profile (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    date_of_birth DATE,
    date_of_death DATE,
    birth_place VARCHAR(200),
    present_address VARCHAR(300),
    age INTEGER,
    prominence_field VARCHAR(100) NOT NULL,
    photo_url VARCHAR(500),
    biography TEXT,
    significance TEXT,
    works_achievements JSONB,
    key_informants JSONB,
    references TEXT,
    mapper_name VARCHAR(200),
    date_profiled DATE,
    status VARCHAR(20) DEFAULT 'pending' NOT NULL,
    user_id INTEGER REFERENCES "user"(id),
    reviewed_by INTEGER REFERENCES "user"(id),
    reviewed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP DEFAULT NOW() NOT NULL
);

CREATE INDEX IF NOT EXISTS ix_personality_profile_name ON personality_profile(name);
CREATE INDEX IF NOT EXISTS ix_personality_profile_status ON personality_profile(status);
CREATE INDEX IF NOT EXISTS ix_personality_profile_user_id ON personality_profile(user_id);
CREATE INDEX IF NOT EXISTS ix_personality_profile_created_at ON personality_profile(created_at);

COMMENT ON TABLE personality_profile IS 'Form 05 - Significant Personalities';

-- =====================================================
-- STEP 5: Create cultural_institution Table (Form 06)
-- =====================================================

CREATE TABLE IF NOT EXISTS cultural_institution (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    municipality VARCHAR(100) NOT NULL,
    province VARCHAR(100) NOT NULL,
    location_address VARCHAR(300),
    lat FLOAT,
    lng FLOAT,
    facade_photo_url VARCHAR(500),
    logo_url VARCHAR(500),
    logo_description TEXT,
    institution_type VARCHAR(100) NOT NULL,
    mandate_description TEXT,
    milestones TEXT,
    stories TEXT,
    significance TEXT,
    condition_status TEXT,
    constraints_threats TEXT,
    safeguarding_measures TEXT,
    supporting_docs JSONB,
    key_informants JSONB,
    references TEXT,
    mapper_name VARCHAR(200),
    date_profiled DATE,
    status VARCHAR(20) DEFAULT 'pending' NOT NULL,
    user_id INTEGER REFERENCES "user"(id),
    reviewed_by INTEGER REFERENCES "user"(id),
    reviewed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP DEFAULT NOW() NOT NULL
);

CREATE INDEX IF NOT EXISTS ix_cultural_institution_name ON cultural_institution(name);
CREATE INDEX IF NOT EXISTS ix_cultural_institution_status ON cultural_institution(status);
CREATE INDEX IF NOT EXISTS ix_cultural_institution_user_id ON cultural_institution(user_id);
CREATE INDEX IF NOT EXISTS ix_cultural_institution_created_at ON cultural_institution(created_at);

COMMENT ON TABLE cultural_institution IS 'Form 06 - Cultural Institutions (Libraries, Museums, etc.)';

-- =====================================================
-- STEP 6: Create lgu_culture_program Table (Form 07)
-- =====================================================

CREATE TABLE IF NOT EXISTS lgu_culture_program (
    id SERIAL PRIMARY KEY,
    municipality VARCHAR(100) NOT NULL UNIQUE,
    province VARCHAR(100) NOT NULL,
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
    peoples_stories TEXT,
    key_informants JSONB,
    references TEXT,
    mapper_name VARCHAR(200),
    date_profiled DATE,
    status VARCHAR(20) DEFAULT 'pending' NOT NULL,
    user_id INTEGER REFERENCES "user"(id),
    reviewed_by INTEGER REFERENCES "user"(id),
    reviewed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP DEFAULT NOW() NOT NULL
);

CREATE INDEX IF NOT EXISTS ix_lgu_culture_program_municipality ON lgu_culture_program(municipality);
CREATE INDEX IF NOT EXISTS ix_lgu_culture_program_status ON lgu_culture_program(status);
CREATE INDEX IF NOT EXISTS ix_lgu_culture_program_user_id ON lgu_culture_program(user_id);
CREATE INDEX IF NOT EXISTS ix_lgu_culture_program_created_at ON lgu_culture_program(created_at);

COMMENT ON TABLE lgu_culture_program IS 'Form 07 - LGU Programs and Projects for Culture';
COMMENT ON COLUMN lgu_culture_program.municipality IS 'Unique - one record per municipality';

-- =====================================================
-- STEP 7: Enable Row Level Security (RLS)
-- =====================================================

-- Enable RLS for all new tables
ALTER TABLE natural_heritage ENABLE ROW LEVEL SECURITY;
ALTER TABLE intangible_heritage ENABLE ROW LEVEL SECURITY;
ALTER TABLE personality_profile ENABLE ROW LEVEL SECURITY;
ALTER TABLE cultural_institution ENABLE ROW LEVEL SECURITY;
ALTER TABLE lgu_culture_program ENABLE ROW LEVEL SECURITY;

-- Create policies (adjust based on your auth setup)
-- Example: Allow all authenticated users to read approved entries

CREATE POLICY "Allow read access to approved natural heritage" 
ON natural_heritage FOR SELECT 
USING (status = 'approved');

CREATE POLICY "Allow read access to approved intangible heritage" 
ON intangible_heritage FOR SELECT 
USING (status = 'approved');

CREATE POLICY "Allow read access to approved personalities" 
ON personality_profile FOR SELECT 
USING (status = 'approved');

CREATE POLICY "Allow read access to approved institutions" 
ON cultural_institution FOR SELECT 
USING (status = 'approved');

CREATE POLICY "Allow read access to approved programs" 
ON lgu_culture_program FOR SELECT 
USING (status = 'approved');

-- =====================================================
-- VERIFICATION QUERIES
-- =====================================================

-- Run these to verify the migration succeeded:

-- Check all tables exist
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
  AND table_name IN (
    'natural_heritage', 
    'intangible_heritage', 
    'personality_profile', 
    'cultural_institution', 
    'lgu_culture_program'
  )
ORDER BY table_name;

-- Check Attraction table heritage columns
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'attraction' 
  AND column_name LIKE '%heritage%' 
  OR column_name LIKE '%building%'
  OR column_name LIKE '%object%'
ORDER BY column_name;

-- =====================================================
-- ROLLBACK SCRIPT (If needed)
-- =====================================================

/*
-- CAUTION: This will DELETE all heritage data!

DROP TABLE IF EXISTS natural_heritage CASCADE;
DROP TABLE IF EXISTS intangible_heritage CASCADE;
DROP TABLE IF EXISTS personality_profile CASCADE;
DROP TABLE IF EXISTS cultural_institution CASCADE;
DROP TABLE IF EXISTS lgu_culture_program CASCADE;

ALTER TABLE attraction 
DROP COLUMN IF EXISTS heritage_type,
DROP COLUMN IF EXISTS building_type,
DROP COLUMN IF EXISTS year_constructed,
DROP COLUMN IF EXISTS ownership_type,
DROP COLUMN IF EXISTS declaration_legislation,
DROP COLUMN IF EXISTS physical_description,
DROP COLUMN IF EXISTS history_structure,
DROP COLUMN IF EXISTS occupation_status,
DROP COLUMN IF EXISTS stories_associated,
DROP COLUMN IF EXISTS condition,
DROP COLUMN IF EXISTS condition_remarks,
DROP COLUMN IF EXISTS is_altered,
DROP COLUMN IF EXISTS is_original_site,
DROP COLUMN IF EXISTS integrity_remarks,
DROP COLUMN IF EXISTS conservation_measures,
DROP COLUMN IF EXISTS movable_heritage_list,
DROP COLUMN IF EXISTS object_type,
DROP COLUMN IF EXISTS place_found,
DROP COLUMN IF EXISTS date_found,
DROP COLUMN IF EXISTS estimated_age,
DROP COLUMN IF EXISTS acquisition_type,
DROP COLUMN IF EXISTS materials,
DROP COLUMN IF EXISTS dimensions,
DROP COLUMN IF EXISTS comparative_criteria,
DROP COLUMN IF EXISTS significance_types,
DROP COLUMN IF EXISTS constraints_threats,
DROP COLUMN IF EXISTS key_informants,
DROP COLUMN IF EXISTS references,
DROP COLUMN IF EXISTS mapper_name,
DROP COLUMN IF EXISTS date_profiled;
*/
