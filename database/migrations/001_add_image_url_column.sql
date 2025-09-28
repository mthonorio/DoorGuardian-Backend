-- Migration: Add image_url column to access table
-- Created: 2025-09-28
-- Description: Adds image_url column to store the public URL of the image from Supabase Storage

-- 1. Add the new column
ALTER TABLE access 
ADD COLUMN image_url TEXT;

-- 2. Create an index for better performance on image_url queries
CREATE INDEX IF NOT EXISTS idx_access_image_url ON access(image_url);

-- 3. Update existing records with image URLs (if any exist)
-- This will populate the image_url for existing records that have images
UPDATE access 
SET image_url = CONCAT(
    'https://<project-name>.supabase.co/storage/v1/object/public/images/', 
    images.file_path
)
FROM images 
WHERE access.image_id = images.id 
AND access.image_url IS NULL;

-- 4. Optional: Create a function to automatically update image_url when image_id changes
CREATE OR REPLACE FUNCTION update_access_image_url()
RETURNS TRIGGER AS $$
BEGIN
    -- If image_id is being set or changed
    IF NEW.image_id IS NOT NULL THEN
        -- Get the image URL from the images table
        SELECT CONCAT(
            'https://<project-name>.supabase.co/storage/v1/object/public/images/', 
            file_path
        )
        INTO NEW.image_url
        FROM images 
        WHERE id = NEW.image_id;
    ELSE
        -- If image_id is NULL, set image_url to NULL
        NEW.image_url := NULL;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 5. Create trigger to automatically update image_url
DROP TRIGGER IF EXISTS trigger_update_access_image_url ON access;
CREATE TRIGGER trigger_update_access_image_url
    BEFORE INSERT OR UPDATE OF image_id ON access
    FOR EACH ROW
    EXECUTE FUNCTION update_access_image_url();

-- 6. Comment the changes
COMMENT ON COLUMN access.image_url IS 'Public URL of the image stored in Supabase Storage';
COMMENT ON FUNCTION update_access_image_url() IS 'Automatically updates image_url when image_id changes';
COMMENT ON TRIGGER trigger_update_access_image_url ON access IS 'Trigger to automatically populate image_url from images table';