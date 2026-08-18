-- PostGIS Extension and Spatial Indexes for MVT Support
-- Run this in your Supabase SQL Editor to enable vector tile generation

-- =====================================================
-- 1. ENABLE POSTGIS EXTENSION
-- =====================================================
-- This enables ST_AsMVT, ST_AsMVTGeom, and spatial functions
CREATE EXTENSION IF NOT EXISTS postgis;

-- Verify installation
SELECT postgis_version();

-- =====================================================
-- 2. ADD GEOMETRY COLUMNS TO CORE TABLES
-- =====================================================

-- Attractions table
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'ATTRACTION' AND column_name = 'geom') THEN
        ALTER TABLE "ATTRACTION" ADD COLUMN geom geometry(Point, 4326);
        
        UPDATE "ATTRACTION" 
        SET geom = ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)
        WHERE geom IS NULL AND latitude IS NOT NULL AND longitude IS NOT NULL;
    END IF;
END $$;

-- Heritage Profile table (Primary table for all cultural assets)
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'HERITAGE_PROFILE' AND column_name = 'geom') THEN
        ALTER TABLE "HERITAGE_PROFILE" ADD COLUMN geom geometry(Point, 4326);
        
        UPDATE "HERITAGE_PROFILE" 
        SET geom = ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)
        WHERE geom IS NULL AND latitude IS NOT NULL AND longitude IS NOT NULL;
    END IF;
END $$;

-- Establishment table (Accommodations and Dining)
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'ESTABLISHMENT' AND column_name = 'geom') THEN
        ALTER TABLE "ESTABLISHMENT" ADD COLUMN geom geometry(Point, 4326);
        
        UPDATE "ESTABLISHMENT" 
        SET geom = ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)
        WHERE geom IS NULL AND latitude IS NOT NULL AND longitude IS NOT NULL;
    END IF;
END $$;

-- =====================================================
-- 3. CREATE SPATIAL INDEXES
-- =====================================================
CREATE INDEX IF NOT EXISTS idx_attraction_geom ON "ATTRACTION" USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_heritage_profile_geom ON "HERITAGE_PROFILE" USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_establishment_geom ON "ESTABLISHMENT" USING GIST (geom);

-- =====================================================
-- 4. CREATE TRIGGERS FOR AUTO-UPDATE
-- =====================================================

-- Shared trigger function for geometry update
CREATE OR REPLACE FUNCTION update_geom_from_latlng()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'INSERT') OR 
       (NEW.latitude IS DISTINCT FROM OLD.latitude) OR 
       (NEW.longitude IS DISTINCT FROM OLD.longitude) THEN
        
        IF NEW.latitude IS NOT NULL AND NEW.longitude IS NOT NULL THEN
            NEW.geom := ST_SetSRID(ST_MakePoint(NEW.longitude, NEW.latitude), 4326);
        ELSE
            NEW.geom := NULL;
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Attractions Trigger
DROP TRIGGER IF EXISTS trg_attraction_geom ON "ATTRACTION";
CREATE TRIGGER trg_attraction_geom
    BEFORE INSERT OR UPDATE ON "ATTRACTION"
    FOR EACH ROW EXECUTE FUNCTION update_geom_from_latlng();

-- Heritage Profile Trigger
DROP TRIGGER IF EXISTS trg_heritage_profile_geom ON "HERITAGE_PROFILE";
CREATE TRIGGER trg_heritage_profile_geom
    BEFORE INSERT OR UPDATE ON "HERITAGE_PROFILE"
    FOR EACH ROW EXECUTE FUNCTION update_geom_from_latlng();

-- Establishment Trigger
DROP TRIGGER IF EXISTS trg_establishment_geom ON "ESTABLISHMENT";
CREATE TRIGGER trg_establishment_geom
    BEFORE INSERT OR UPDATE ON "ESTABLISHMENT"
    FOR EACH ROW EXECUTE FUNCTION update_geom_from_latlng();

-- =====================================================
-- 5. VERIFICATION QUERY
-- =====================================================
SELECT 
    table_name, 
    column_name, 
    udt_name as type 
FROM information_schema.columns 
WHERE column_name = 'geom' AND table_name IN ('ATTRACTION', 'HERITAGE_PROFILE', 'ESTABLISHMENT');
