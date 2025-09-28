-- DoorGuardian Database Schema for Supabase
-- Run this SQL in your Supabase SQL editor to create the required tables

-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create images table
CREATE TABLE IF NOT EXISTS public.images (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255),
    file_path VARCHAR(500) NOT NULL,
    file_size INTEGER NOT NULL CHECK (file_size > 0),
    mime_type VARCHAR(100) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Create access table
CREATE TABLE IF NOT EXISTS public.access (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    access BOOLEAN NOT NULL DEFAULT FALSE,
    image_id UUID REFERENCES public.images(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_access_date ON public.access(date);
CREATE INDEX IF NOT EXISTS idx_access_access ON public.access(access);
CREATE INDEX IF NOT EXISTS idx_access_created_at ON public.access(created_at);
CREATE INDEX IF NOT EXISTS idx_access_image_id ON public.access(image_id);
CREATE INDEX IF NOT EXISTS idx_images_filename ON public.images(filename);

-- Enable Row Level Security (RLS)
ALTER TABLE public.images ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.access ENABLE ROW LEVEL SECURITY;

-- Create policies for service role access (adjust as needed for your security requirements)
-- These policies allow full access to service role key
CREATE POLICY "Service role can do everything on images" ON public.images
    FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY "Service role can do everything on access" ON public.access
    FOR ALL USING (auth.role() = 'service_role');

-- Optional: Create policies for authenticated users (uncomment if needed)
-- CREATE POLICY "Authenticated users can read images" ON public.images
--     FOR SELECT USING (auth.role() = 'authenticated');
-- 
-- CREATE POLICY "Authenticated users can read access" ON public.access
--     FOR SELECT USING (auth.role() = 'authenticated');

-- Create a function to automatically update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers to automatically update updated_at
DROP TRIGGER IF EXISTS update_images_updated_at ON public.images;
CREATE TRIGGER update_images_updated_at 
    BEFORE UPDATE ON public.images 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_access_updated_at ON public.access;
CREATE TRIGGER update_access_updated_at 
    BEFORE UPDATE ON public.access 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Create storage bucket for images (run this separately in Supabase Storage)
-- INSERT INTO storage.buckets (id, name, public)
-- VALUES ('images', 'images', true);

-- Create storage policies (run this after creating the bucket)
-- CREATE POLICY "Service role can upload images" ON storage.objects
--     FOR INSERT WITH CHECK (bucket_id = 'images' AND auth.role() = 'service_role');
-- 
-- CREATE POLICY "Service role can delete images" ON storage.objects
--     FOR DELETE USING (bucket_id = 'images' AND auth.role() = 'service_role');
-- 
-- CREATE POLICY "Anyone can view images" ON storage.objects
--     FOR SELECT USING (bucket_id = 'images');

-- Example data (optional - remove in production)
-- INSERT INTO public.access (access, date) VALUES 
-- (true, NOW() - INTERVAL '1 day'),
-- (false, NOW() - INTERVAL '2 days'),
-- (true, NOW() - INTERVAL '3 days');

COMMENT ON TABLE public.images IS 'Stores metadata for uploaded access images';
COMMENT ON TABLE public.access IS 'Stores door access records with optional associated images';
COMMENT ON COLUMN public.access.access IS 'True if access was granted, false if denied';
COMMENT ON COLUMN public.access.date IS 'Date and time when the access attempt occurred';
COMMENT ON COLUMN public.access.image_id IS 'Optional reference to associated image';
COMMENT ON COLUMN public.images.file_path IS 'Path to file in Supabase storage';
COMMENT ON COLUMN public.images.mime_type IS 'MIME type of the uploaded file';