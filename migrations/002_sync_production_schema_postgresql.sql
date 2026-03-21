-- Production Schema Sync for Vercel/Supabase
-- Streamlined to handle renames and missing columns only.

DO $$ 
BEGIN
    -- 1. UTILITY: RENAME TABLES to Quoted Uppercase
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'user') THEN
        ALTER TABLE "user" RENAME TO "USER";
    END IF;
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'attraction') THEN
        ALTER TABLE "attraction" RENAME TO "ATTRACTION";
    END IF;
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'event') THEN
        ALTER TABLE "event" RENAME TO "EVENT";
    END IF;
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'barangay_info') THEN
        ALTER TABLE "barangay_info" RENAME TO "BARANGAY_INFO";
    END IF;
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'heritage_profile') THEN
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

    -- EVENT
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'EVENT' AND column_name = 'title') THEN
        ALTER TABLE "EVENT" RENAME COLUMN title TO name;
    END IF;
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'EVENT' AND column_name = 'barangay') THEN
        ALTER TABLE "EVENT" RENAME COLUMN "barangay" TO "old_barangay";
    END IF;
    ALTER TABLE "EVENT" ADD COLUMN IF NOT EXISTS "name" VARCHAR(200);
    ALTER TABLE "EVENT" ADD COLUMN IF NOT EXISTS "barangay_id" INTEGER;

    -- BARANGAY_INFO
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'BARANGAY_INFO' AND column_name = 'barangay_name') THEN
        ALTER TABLE "BARANGAY_INFO" RENAME COLUMN "barangay_name" TO "name";
    END IF;
    ALTER TABLE "BARANGAY_INFO" ADD COLUMN IF NOT EXISTS "name" VARCHAR(100);
    ALTER TABLE "BARANGAY_INFO" ADD COLUMN IF NOT EXISTS "map_geo_json" TEXT;

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

END $$;
