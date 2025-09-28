from typing import List, Optional
from app.config.extensions import get_supabase_client, get_supabase_admin_client
from app.models.image import ImageCreate, Image
import logging

logger = logging.getLogger(__name__)

class ImageService:
    """Service for managing image operations with Supabase"""
    
    @staticmethod
    async def create_image(image_data: ImageCreate) -> Image:
        """Create a new image record in the database"""
        try:
            # Use service role client to bypass RLS
            supabase = get_supabase_admin_client()
            
            # Convert Pydantic model to dict
            image_dict = image_data.model_dump()
            
            # Insert into database
            result = supabase.table("images").insert(image_dict).execute()
            
            if not result.data:
                raise Exception("Failed to create image record")
            
            return Image(**result.data[0])
            
        except Exception as e:
            logger.error(f"Error creating image: {e}")
            raise Exception(f"Failed to create image: {e}")
    
    @staticmethod
    async def get_image_by_id(image_id: str) -> Optional[Image]:
        """Get an image by its ID"""
        try:
            # Use service role client to bypass RLS
            supabase = get_supabase_admin_client()
            
            result = supabase.table("images").select("*").eq("id", image_id).execute()
            
            if result.data:
                return Image(**result.data[0])
            
            return None
            
        except Exception as e:
            logger.error(f"Error fetching image: {e}")
            raise Exception(f"Failed to fetch image: {e}")
    
    @staticmethod
    async def delete_image(image_id: str) -> bool:
        """Delete an image record and its file from storage"""
        try:
            # Use service role client to bypass RLS
            supabase = get_supabase_admin_client()
            
            # First get the image to know the file path
            image = await ImageService.get_image_by_id(image_id)
            if not image:
                return False
            
            # Delete from storage
            try:
                await ImageService.delete_image_from_storage(image.file_path)
            except Exception as e:
                logger.warning(f"Could not delete file from storage: {e}")
            
            # Delete from database
            result = supabase.table("images").delete().eq("id", image_id).execute()
            
            return len(result.data) > 0
            
        except Exception as e:
            logger.error(f"Error deleting image: {e}")
            raise Exception(f"Failed to delete image: {e}")
    
    @staticmethod
    async def upload_image_to_storage(file_content: bytes, file_path: str, mime_type: str = None) -> str:
        """Upload image to Supabase Storage"""
        try:
            # Use service role client for uploads (now that we have the correct key)
            supabase = get_supabase_admin_client()
            
            # Prepare file options with correct content-type
            file_options = {}
            if mime_type:
                file_options["content-type"] = mime_type
            
            # Upload to the 'images' bucket
            result = supabase.storage.from_("images").upload(
                path=file_path,
                file=file_content,
                file_options=file_options
            )
            
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Storage upload error: {result.error}")
            
            # Get public URL
            public_url = supabase.storage.from_("images").get_public_url(file_path)
            
            logger.info(f"Successfully uploaded image to: {file_path}")
            return public_url
            
        except Exception as e:
            logger.error(f"Error uploading to storage: {e}")
            raise Exception(f"Storage upload failed: {e}")
    
    @staticmethod
    async def delete_image_from_storage(file_path: str) -> bool:
        """Delete image from Supabase Storage"""
        try:
            supabase = get_supabase_admin_client()
            
            result = supabase.storage.from_("images").remove([file_path])
            
            if hasattr(result, 'error') and result.error:
                logger.error(f"Storage delete error: {result.error}")
                return False
            
            logger.info(f"Successfully deleted image from storage: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting from storage: {e}")
            return False
    
    @staticmethod
    async def get_image_url(file_path: str) -> str:
        """Get public URL for an image"""
        try:
            supabase = get_supabase_client()
            
            public_url = supabase.storage.from_("images").get_public_url(file_path)
            return public_url
            
        except Exception as e:
            logger.error(f"Error getting image URL: {e}")
            raise Exception(f"Failed to get image URL: {e}")