-- SQLite Schema for Content Approval
-- Add approval fields to existing tables

-- ATTRACTIONS
ALTER TABLE attractions ADD COLUMN status TEXT DEFAULT 'pending';
ALTER TABLE attractions ADD COLUMN reviewed_by INTEGER REFERENCES user(id);
ALTER TABLE attractions ADD COLUMN reviewed_at DATETIME;

-- EVENTS
ALTER TABLE events ADD COLUMN status TEXT DEFAULT 'pending';
ALTER TABLE events ADD COLUMN reviewed_by INTEGER REFERENCES user(id);
ALTER TABLE events ADD COLUMN reviewed_at DATETIME;

-- GALLERY ITEMS
ALTER TABLE gallery_item ADD COLUMN status TEXT DEFAULT 'pending';
ALTER TABLE gallery_item ADD COLUMN reviewed_by INTEGER REFERENCES user(id);
ALTER TABLE gallery_item ADD COLUMN reviewed_at DATETIME;

-- REVIEWS
ALTER TABLE review ADD COLUMN status TEXT DEFAULT 'pending';
ALTER TABLE review ADD COLUMN reviewed_by INTEGER REFERENCES user(id);
ALTER TABLE review ADD COLUMN reviewed_at DATETIME;

-- Note: To enforce 'pending', 'approved', 'rejected' in SQLite,
-- we would typically need to recreate the table with CHECK constraints
-- or use triggers. Since SQLAlchemy handles validation, we use TEXT here.

-- Indices for performance
CREATE INDEX IF NOT EXISTS idx_attractions_status ON attractions(status);
CREATE INDEX IF NOT EXISTS idx_events_status ON events(status);
CREATE INDEX IF NOT EXISTS idx_gallery_item_status ON gallery_item(status);
CREATE INDEX IF NOT EXISTS idx_review_status ON review(status);
