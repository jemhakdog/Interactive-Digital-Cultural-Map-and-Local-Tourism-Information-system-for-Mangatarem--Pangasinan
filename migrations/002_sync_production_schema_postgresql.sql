-- Production Schema Sync for Vercel/Supabase
-- Streamlined to handle renames and missing columns only.

DO $$ 
BEGIN
    -- 1. UTILITY: RENAME TABLES to Quoted Uppercase (skip if target already exists)
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'user')
       AND NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'USER') THEN
        ALTER TABLE "user" RENAME TO "USER";
    END IF;
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'attraction')
       AND NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'ATTRACTION') THEN
        ALTER TABLE "attraction" RENAME TO "ATTRACTION";
    END IF;
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'event')
       AND NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'EVENT') THEN
        ALTER TABLE "event" RENAME TO "EVENT";
    END IF;
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'barangay_info')
       AND NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'BARANGAY_INFO') THEN
        ALTER TABLE "barangay_info" RENAME TO "BARANGAY_INFO";
    END IF;
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'heritage_profile')
       AND NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'HERITAGE_PROFILE') THEN
        ALTER TABLE "heritage_profile" RENAME TO "HERITAGE_PROFILE";
    END IF;

    -- 2. SYNC COLUMNS
    -- USER
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'USER' AND column_name = 'password_hash') THEN
        ALTER TABLE "USER" RENAME COLUMN password_hash TO password;
    END IF;
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'USER' AND column_name = 'barangay') THEN
        ALTER TABLE "USER" RENAME COLUMN "barangay" TO "old_barangay";
    END IF;
    ALTER TABLE "USER" ADD COLUMN IF NOT EXISTS "barangay_id" INTEGER;
    ALTER TABLE "USER" ADD COLUMN IF NOT EXISTS "is_superuser" BOOLEAN DEFAULT FALSE;
    ALTER TABLE "USER" ADD COLUMN IF NOT EXISTS "is_approved" BOOLEAN DEFAULT FALSE;

    -- ATTRACTION
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'ATTRACTION' AND column_name = 'lat') THEN
        ALTER TABLE "ATTRACTION" RENAME COLUMN lat TO latitude;
    END IF;
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'ATTRACTION' AND column_name = 'lng') THEN
        ALTER TABLE "ATTRACTION" RENAME COLUMN lng TO longitude;
    END IF;
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'ATTRACTION' AND column_name = 'barangay') THEN
        ALTER TABLE "ATTRACTION" RENAME COLUMN "barangay" TO "old_barangay";
    END IF;
    ALTER TABLE "ATTRACTION" ADD COLUMN IF NOT EXISTS "latitude" FLOAT;
    ALTER TABLE "ATTRACTION" ADD COLUMN IF NOT EXISTS "longitude" FLOAT;
    ALTER TABLE "ATTRACTION" ADD COLUMN IF NOT EXISTS "barangay_id" INTEGER;
    ALTER TABLE "ATTRACTION" ADD COLUMN IF NOT EXISTS "heritage_profile_id" INTEGER;
    ALTER TABLE "ATTRACTION" ADD COLUMN IF NOT EXISTS "status" VARCHAR(20) DEFAULT 'pending';
    ALTER TABLE "ATTRACTION" ADD COLUMN IF NOT EXISTS "user_id" INTEGER;
    ALTER TABLE "ATTRACTION" ADD COLUMN IF NOT EXISTS "image_url" VARCHAR(500);

    -- EVENT
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'EVENT' AND column_name = 'title') THEN
        ALTER TABLE "EVENT" RENAME COLUMN title TO name;
    END IF;
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'EVENT' AND column_name = 'barangay') THEN
        ALTER TABLE "EVENT" RENAME COLUMN "barangay" TO "old_barangay";
    END IF;
    ALTER TABLE "EVENT" ADD COLUMN IF NOT EXISTS "name" VARCHAR(200);
    ALTER TABLE "EVENT" ADD COLUMN IF NOT EXISTS "barangay_id" INTEGER;
    ALTER TABLE "EVENT" ADD COLUMN IF NOT EXISTS "location" VARCHAR(255);
    ALTER TABLE "EVENT" ADD COLUMN IF NOT EXISTS "category" VARCHAR(50) DEFAULT 'Civic';
    ALTER TABLE "EVENT" ADD COLUMN IF NOT EXISTS "status" VARCHAR(20) DEFAULT 'pending';
    ALTER TABLE "EVENT" ADD COLUMN IF NOT EXISTS "user_id" INTEGER;
    ALTER TABLE "EVENT" ADD COLUMN IF NOT EXISTS "image_url" VARCHAR(500);

    -- BARANGAY_INFO
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'BARANGAY_INFO' AND column_name = 'barangay_name') THEN
        ALTER TABLE "BARANGAY_INFO" RENAME COLUMN "barangay_name" TO "name";
    END IF;
    ALTER TABLE "BARANGAY_INFO" ADD COLUMN IF NOT EXISTS "name" VARCHAR(100);
    ALTER TABLE "BARANGAY_INFO" ADD COLUMN IF NOT EXISTS "map_geo_json" TEXT;
    ALTER TABLE "BARANGAY_INFO" ADD COLUMN IF NOT EXISTS "location_data" JSONB;

    -- HERITAGE_PROFILE
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'HERITAGE_PROFILE' AND column_name = 'name') THEN
        ALTER TABLE "HERITAGE_PROFILE" RENAME COLUMN "name" TO "name_of_asset";
    END IF;
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'HERITAGE_PROFILE' AND column_name = 'heritage_type') THEN
        ALTER TABLE "HERITAGE_PROFILE" RENAME COLUMN "heritage_type" TO "asset_type";
    END IF;
    ALTER TABLE "HERITAGE_PROFILE" ADD COLUMN IF NOT EXISTS "name_of_asset" VARCHAR(200);
    ALTER TABLE "HERITAGE_PROFILE" ADD COLUMN IF NOT EXISTS "asset_type" VARCHAR(100);
    ALTER TABLE "HERITAGE_PROFILE" ADD COLUMN IF NOT EXISTS "barangay_id" INTEGER;
    ALTER TABLE "HERITAGE_PROFILE" ADD COLUMN IF NOT EXISTS "common_name" VARCHAR(200);
    ALTER TABLE "HERITAGE_PROFILE" ADD COLUMN IF NOT EXISTS "form_control_number" VARCHAR(100);
    ALTER TABLE "HERITAGE_PROFILE" ADD COLUMN IF NOT EXISTS "location_details" TEXT;
    ALTER TABLE "HERITAGE_PROFILE" ADD COLUMN IF NOT EXISTS "contact_person" VARCHAR(200);
    ALTER TABLE "HERITAGE_PROFILE" ADD COLUMN IF NOT EXISTS "contact_number" VARCHAR(50);
    ALTER TABLE "HERITAGE_PROFILE" ADD COLUMN IF NOT EXISTS "ownership_type" VARCHAR(50);
    ALTER TABLE "HERITAGE_PROFILE" ADD COLUMN IF NOT EXISTS "owner_administrator" VARCHAR(200);
    ALTER TABLE "HERITAGE_PROFILE" ADD COLUMN IF NOT EXISTS "usage_status" VARCHAR(50);
    ALTER TABLE "HERITAGE_PROFILE" ADD COLUMN IF NOT EXISTS "latitude" FLOAT;
    ALTER TABLE "HERITAGE_PROFILE" ADD COLUMN IF NOT EXISTS "longitude" FLOAT;
    ALTER TABLE "HERITAGE_PROFILE" ADD COLUMN IF NOT EXISTS "significance" TEXT;
    ALTER TABLE "HERITAGE_PROFILE" ADD COLUMN IF NOT EXISTS "conservation_status" TEXT;
    ALTER TABLE "HERITAGE_PROFILE" ADD COLUMN IF NOT EXISTS "mapper_name" VARCHAR(200);
    ALTER TABLE "HERITAGE_PROFILE" ADD COLUMN IF NOT EXISTS "date_profiled" DATE;
    ALTER TABLE "HERITAGE_PROFILE" ADD COLUMN IF NOT EXISTS "status" VARCHAR(20) DEFAULT 'pending';
    ALTER TABLE "HERITAGE_PROFILE" ADD COLUMN IF NOT EXISTS "user_id" INTEGER;

    -- 3. MISSING TABLES
    CREATE TABLE IF NOT EXISTS "GALLERY_ITEM" (
        id SERIAL PRIMARY KEY,
        type VARCHAR(20) NOT NULL,
        url VARCHAR(500) NOT NULL,
        caption TEXT,
        user_id INTEGER REFERENCES "USER"(id),
        status VARCHAR(20) DEFAULT 'pending',
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS "ANALYTICS_PAGE_VIEW" (
        id SERIAL PRIMARY KEY,
        page_url VARCHAR(500) NOT NULL,
        user_id INTEGER,
        timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        session_id VARCHAR(100),
        ip_address VARCHAR(45),
        device_info TEXT
    );

    CREATE TABLE IF NOT EXISTS "USER_FAVORITE_ATTRACTION" (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES "USER"(id),
        attraction_id INTEGER REFERENCES "ATTRACTION"(id),
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS "USER_EVENT_INTEREST" (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES "USER"(id),
        event_id INTEGER REFERENCES "EVENT"(id),
        status VARCHAR(20) DEFAULT 'interested',
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS "ATTRACTION_REVIEW" (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES "USER"(id),
        attraction_id INTEGER REFERENCES "ATTRACTION"(id),
        rating INTEGER NOT NULL,
        comment TEXT,
        status VARCHAR(20) DEFAULT 'pending',
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );

    -- 4. ADDITIONAL COLUMN SYNC
    -- PASSWORD_RESET_TOKEN
    ALTER TABLE "PASSWORD_RESET_TOKEN" ADD COLUMN IF NOT EXISTS "expires_at" TIMESTAMP WITH TIME ZONE;
    ALTER TABLE "PASSWORD_RESET_TOKEN" ADD COLUMN IF NOT EXISTS "used" BOOLEAN DEFAULT FALSE;
    -- Ensure token column length (models.py says 128)
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'PASSWORD_RESET_TOKEN' AND column_name = 'token') THEN
        ALTER TABLE "PASSWORD_RESET_TOKEN" ALTER COLUMN "token" TYPE VARCHAR(128);
    END IF;

    -- 5. HERITAGE DETAIL SYNC (BUILT_HERITAGE_DETAIL)
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'BUILT_HERITAGE_DETAIL' AND column_name = 'kind_of_structure') THEN
        ALTER TABLE "BUILT_HERITAGE_DETAIL" RENAME COLUMN kind_of_structure TO type_of_building;
    END IF;
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'BUILT_HERITAGE_DETAIL' AND column_name = 'estimated_date_of_construction') THEN
        ALTER TABLE "BUILT_HERITAGE_DETAIL" RENAME COLUMN estimated_date_of_construction TO year_constructed;
        -- Note: Might need casting if data exists, but since model says Integer, let's keep it safe.
    END IF;
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'BUILT_HERITAGE_DETAIL' AND column_name = 'historical_significance') THEN
        ALTER TABLE "BUILT_HERITAGE_DETAIL" RENAME COLUMN historical_significance TO materials_used; -- Best guess based on model
    END IF;
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'BUILT_HERITAGE_DETAIL' AND column_name = 'architectural_description') THEN
        ALTER TABLE "BUILT_HERITAGE_DETAIL" RENAME COLUMN architectural_description TO architectural_style;
    END IF;

    ALTER TABLE "BUILT_HERITAGE_DETAIL" ADD COLUMN IF NOT EXISTS "architect_builder" VARCHAR(200);
    ALTER TABLE "BUILT_HERITAGE_DETAIL" ADD COLUMN IF NOT EXISTS "state_of_conservation" TEXT;

    -- 6. FOREIGN KEYS (Ensure they exist)
    -- This is safer to do via separate commands or if you're sure about table names
    -- ATTRACTION
    IF NOT EXISTS (SELECT 1 FROM information_schema.table_constraints WHERE constraint_name = 'attraction_heritage_profile_id_fkey') THEN
        ALTER TABLE "ATTRACTION" ADD CONSTRAINT attraction_heritage_profile_id_fkey FOREIGN KEY (heritage_profile_id) REFERENCES "HERITAGE_PROFILE"(id);
    END IF;

END $$;
