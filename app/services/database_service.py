from typing import List, Optional, Dict, Any
from datetime import datetime
from app.config.extensions import get_supabase_client, get_supabase_admin_client
from app.models.access import Access, AccessCreate, AccessWithImage
from app.models.image import Image, ImageCreate

class AccessService:
    """Service for handling access operations with Supabase"""
    
    @staticmethod
    async def get_access_history(
        page: int = 1,
        per_page: int = 20,
        sort_by: str = "date",
        sort_order: str = "desc",
        access_filter: Optional[bool] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get paginated access history with filtering"""
        
        # Use service role client to bypass RLS
        supabase = get_supabase_admin_client()
        
        # Calculate offset for pagination
        offset = (page - 1) * per_page
        
        # Build base query following Supabase pattern
        response = (
            supabase.table("access")
            .select("*, images(*)")
            .execute()
        )
        
        # Get total count for pagination (without filters first)
        count_response = (
            supabase.table("access")
            .select("*", count="exact")
            .execute()
        )
        
        total = count_response.count if count_response.count else 0
        
        # Apply filters manually for now (can be optimized with Supabase queries)
        filtered_data = response.data
        
        if access_filter is not None:
            filtered_data = [r for r in filtered_data if r.get('access') == access_filter]
            
        if date_from:
            date_from_str = date_from.isoformat()
            filtered_data = [r for r in filtered_data if r.get('date', '') >= date_from_str]
            
        if date_to:
            date_to_str = date_to.isoformat()
            filtered_data = [r for r in filtered_data if r.get('date', '') <= date_to_str]
        
        # Apply sorting
        reverse_sort = sort_order == "desc"
        filtered_data.sort(key=lambda x: x.get(sort_by, ''), reverse=reverse_sort)
        
        # Apply pagination
        paginated_data = filtered_data[offset:offset + per_page]
        
        # Transform data
        access_records = []
        for record in paginated_data:
            try:
                access_data = AccessWithImage(**record)
                if record.get('images'):
                    access_data.image = Image(**record['images'])
                access_records.append(access_data)
            except Exception as e:
                # Skip invalid records
                continue
        
        # Calculate pagination info
        filtered_total = len(filtered_data)
        total_pages = (filtered_total + per_page - 1) // per_page if filtered_total > 0 else 1
        has_next = page < total_pages
        has_prev = page > 1
        
        return {
            'access_records': access_records,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': filtered_total,
                'pages': total_pages,
                'has_next': has_next,
                'has_prev': has_prev,
                'next_num': page + 1 if has_next else None,
                'prev_num': page - 1 if has_prev else None
            }
        }
    
    @staticmethod
    async def create_access(access_data: AccessCreate) -> AccessWithImage:
        """Create a new access record"""
        
        # Use service role client to bypass RLS
        supabase = get_supabase_admin_client()
        
        # Insert access record following Supabase pattern
        # The trigger will automatically populate image_url if image_id is provided
        insert_response = (
            supabase.table("access")
            .insert({
                "access": access_data.access,
                "date": access_data.date.isoformat(),
                "image_id": access_data.image_id,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            })
            .execute()
        )
        
        if not insert_response.data:
            raise Exception("Failed to create access record")
        
        created_record = insert_response.data[0]
        
        # Now fetch the complete record with image data and image_url populated by trigger
        response = (
            supabase.table("access")
            .select("*, images(*)")
            .eq("id", created_record["id"])
            .execute()
        )
        
        if not response.data:
            raise Exception("Failed to fetch created access record")
        
        access_record = response.data[0]
        
        # Extract image data if present
        image_data = None
        if access_record.get('images'):
            image_data = Image(**access_record['images'])
            # Remove the nested images data to avoid conflicts
            access_record.pop('images', None)
        
        # Create AccessWithImage instance
        result = AccessWithImage(**access_record)
        if image_data:
            result.image = image_data
            
        return result
    
    @staticmethod
    async def delete_access(access_id: str) -> bool:
        """Delete an access record and its associated image"""
        
        # Get Supabase client
        supabase = get_supabase_client()
        
        # First, get the access record to check for associated image
        access_response = (
            supabase.table("access")
            .select("*, images(*)")
            .eq("id", access_id)
            .execute()
        )
        
        if not access_response.data:
            return False
        
        access_record = access_response.data[0]
        
        # Delete associated image from storage and database if exists
        if access_record.get('images'):
            image = access_record['images']
            
            # Delete from Supabase storage
            try:
                supabase.storage.from_("images").remove([image['file_path']])
            except:
                pass  # Continue even if storage deletion fails
            
            # Delete image record
            (
                supabase.table("images")
                .delete()
                .eq("id", image['id'])
                .execute()
            )
        
        # Delete access record
        delete_response = (
            supabase.table("access")
            .delete()
            .eq("id", access_id)
            .execute()
        )
        
        return len(delete_response.data) > 0


class ImageService:
    """Service for handling image operations with Supabase"""
    
    @staticmethod
    async def create_image(image_data: ImageCreate) -> Image:
        """Create a new image record"""
        
        # Get Supabase client
        supabase = get_supabase_client()
        
        response = (
            supabase.table("images")
            .insert({
                "filename": image_data.filename,
                "original_filename": image_data.original_filename,
                "file_path": image_data.file_path,
                "file_size": image_data.file_size,
                "mime_type": image_data.mime_type,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            })
            .execute()
        )
        
        if not response.data:
            raise Exception("Failed to create image record")
        
        return Image(**response.data[0])
    
    @staticmethod
    async def upload_image_to_storage(file_content: bytes, file_path: str) -> str:
        """Upload image to Supabase storage"""
        
        # Get Supabase client
        supabase = get_supabase_client()
        
        response = supabase.storage.from_("images").upload(
            file_path, file_content
        )
        
        if response.get('error'):
            raise Exception(f"Failed to upload image: {response['error']}")
        
        return file_path
    
    @staticmethod
    async def get_image_url(file_path: str) -> str:
        """Get public URL for image"""
        
        # Get Supabase client
        supabase = get_supabase_client()
        
        response = supabase.storage.from_("images").get_public_url(file_path)
        return response.get('publicURL', '')