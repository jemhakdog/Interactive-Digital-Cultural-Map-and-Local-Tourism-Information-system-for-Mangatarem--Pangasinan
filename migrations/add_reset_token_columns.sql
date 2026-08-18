-- Add missing reset_token columns to USER table
-- Run in Supabase SQL Editor

ALTER TABLE "USER" ADD COLUMN IF NOT EXISTS reset_token VARCHAR(128) UNIQUE;
ALTER TABLE "USER" ADD COLUMN IF NOT EXISTS reset_token_expires_at TIMESTAMP;
ALTER TABLE "USER" ADD COLUMN IF NOT EXISTS reset_token_used BOOLEAN DEFAULT FALSE;
