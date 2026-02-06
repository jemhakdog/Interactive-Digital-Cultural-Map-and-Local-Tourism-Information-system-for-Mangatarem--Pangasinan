-- Supabase/PostgreSQL Schema for Content Approval
-- Add approval fields to existing tables

-- Create an ENUM type for content approval status if it doesn't exist
DO $$ BEGIN
    CREATE TYPE approval_status AS ENUM ('pending', 'approved', 'rejected');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- ATTRACTIONS
ALTER TABLE attractions 
ADD COLUMN IF NOT EXISTS status approval_status DEFAULT 'pending',
ADD COLUMN IF NOT EXISTS reviewed_by UUID REFERENCES auth.users(id),
ADD COLUMN IF NOT EXISTS reviewed_at TIMESTAMP WITH TIME ZONE;

-- EVENTS
ALTER TABLE events 
ADD COLUMN IF NOT EXISTS status approval_status DEFAULT 'pending',
ADD COLUMN IF NOT EXISTS reviewed_by UUID REFERENCES auth.users(id),
ADD COLUMN IF NOT EXISTS reviewed_at TIMESTAMP WITH TIME ZONE;

-- GALLERY ITEMS
ALTER TABLE gallery_item 
ADD COLUMN IF NOT EXISTS status approval_status DEFAULT 'pending',
ADD COLUMN IF NOT EXISTS reviewed_by UUID REFERENCES auth.users(id),
ADD COLUMN IF NOT EXISTS reviewed_at TIMESTAMP WITH TIME ZONE;

-- REVIEWS
ALTER TABLE review 
ADD COLUMN IF NOT EXISTS status approval_status DEFAULT 'pending',
ADD COLUMN IF NOT EXISTS reviewed_by UUID REFERENCES auth.users(id),
ADD COLUMN IF NOT EXISTS reviewed_at TIMESTAMP WITH TIME ZONE;

-- Row Level Security (RLS) Example:
-- 1. Public can only see 'approved' content
CREATE POLICY IF NOT EXISTS "Public can view approved attractions" 
ON attractions FOR SELECT 
USING (status = 'approved');

CREATE POLICY IF NOT EXISTS "Public can view approved events" 
ON events FOR SELECT 
USING (status = 'approved');

-- 2. Admins and Contributors can see everything (simplified)
CREATE POLICY IF NOT EXISTS "Admins and Contributors can view all" 
ON attractions FOR SELECT 
USING (
  EXISTS (
    SELECT 1 FROM user_roles 
    WHERE user_id = auth.uid() 
    AND role IN ('admin', 'contributor')
  )
);

-- Indices for performance
CREATE INDEX IF NOT EXISTS idx_attractions_status ON attractions(status);
CREATE INDEX IF NOT EXISTS idx_events_status ON events(status);
CREATE INDEX IF NOT EXISTS idx_gallery_item_status ON gallery_item(status);
CREATE INDEX IF NOT EXISTS idx_review_status ON review(status);
