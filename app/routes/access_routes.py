import os
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Query, HTTPException, UploadFile, File, Form, Depends
from fastapi.responses import JSONResponse

from app.models.access import AccessCreate, AccessListResponse, AccessCreateResponse, AccessWithImage
from app.models.image import ImageCreate
from app.services.database_service import AccessService
from app.services.image_service import ImageService
from app.utils.file_utils import (
    allowed_file, 
    allowed_mime_type, 
    validate_image_content, 
    generate_unique_filename, 
    get_file_info_from_upload
)
from app.config.config import settings

# Create router
router = APIRouter(prefix="/api/v1", tags=["access"])

@router.get("/history", response_model=AccessListResponse)
async def get_history(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page (max 100)"),
    sort_by: str = Query("date", description="Sort field (date or created_at)"),
    sort_order: str = Query("desc", description="Sort order (asc or desc)"),
    access: Optional[bool] = Query(None, description="Filter by access status"),
    date_from: Optional[datetime] = Query(None, description="Filter from date (ISO format)"),
    date_to: Optional[datetime] = Query(None, description="Filter to date (ISO format)")
):
    """
    Get access history with pagination and filtering support.
    
    - **page**: Page number (starting from 1)
    - **per_page**: Number of items per page (maximum 100)
    - **sort_by**: Field to sort by ('date' or 'created_at')
    - **sort_order**: Sort order ('asc' or 'desc')
    - **access**: Filter by access status (true/false)
    - **date_from**: Filter records from this date
    - **date_to**: Filter records up to this date
    """
    try:
        # Validate sort parameters
        if sort_by not in ["date", "created_at"]:
            raise HTTPException(status_code=400, detail="sort_by must be 'date' or 'created_at'")
        
        if sort_order not in ["asc", "desc"]:
            raise HTTPException(status_code=400, detail="sort_order must be 'asc' or 'desc'")
        
        result = await AccessService.get_access_history(
            page=page,
            per_page=per_page,
            sort_by=sort_by,
            sort_order=sort_order,
            access_filter=access,
            date_from=date_from,
            date_to=date_to
        )
        
        return AccessListResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/register", response_model=AccessCreateResponse)
async def register_access(
    access: bool = Form(..., description="Access granted (true) or denied (false)"),
    date: Optional[datetime] = Form(None, description="Access date (ISO format, optional)"),
    image: Optional[UploadFile] = File(None, description="Optional access image")
):
    """
    Register a new access record with optional image.
    
    - **access**: Boolean indicating if access was granted or denied
    - **date**: Date and time of access (optional, defaults to current time)
    - **image**: Optional image file (PNG, JPG, JPEG, GIF, WEBP)
    """
    try:
        # Use current time if date not provided
        access_date = date if date else datetime.utcnow()
        
        # Handle image upload if present
        image_id = None
        if image and image.filename:
            # Validate file type
            if not allowed_file(image.filename):
                raise HTTPException(
                    status_code=400, 
                    detail="Invalid file type. Allowed: png, jpg, jpeg, gif, webp"
                )
            
            # Read file content
            file_content = await image.read()
            
            # Get file info with content for better MIME type detection
            file_info = get_file_info_from_upload(image, len(file_content), file_content)
            
            # Validate MIME type
            if not allowed_mime_type(file_info['mime_type']):
                raise HTTPException(
                    status_code=400, 
                    detail=f"Invalid file MIME type: {file_info['mime_type']}. Allowed: {settings.ALLOWED_FILE_TYPES}"
                )
            
            # Validate file size
            if file_info['size'] > settings.MAX_FILE_SIZE:
                raise HTTPException(status_code=413, detail="File too large")
            
            # Validate image content
            if not validate_image_content(file_content):
                raise HTTPException(status_code=400, detail="Invalid or corrupted image file")
            
            # Generate unique filename
            unique_filename = generate_unique_filename(image.filename)
            file_path = f"access_images/{unique_filename}"
            
            # Upload to Supabase storage
            await ImageService.upload_image_to_storage(file_content, file_path, file_info['mime_type'])
            
            # Create image record
            image_data = ImageCreate(
                filename=unique_filename,
                original_filename=file_info['original_filename'],
                file_path=file_path,
                file_size=file_info['size'],
                mime_type=file_info['mime_type']
            )
            
            image_record = await ImageService.create_image(image_data)
            image_id = image_record.id
        
        # Create access record
        access_data = AccessCreate(
            access=access,
            date=access_date,
            image_id=image_id
        )
        
        access_record = await AccessService.create_access(access_data)
        
        return AccessCreateResponse(
            message="Access record created successfully",
            access_record=access_record
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.delete("/history/{access_id}")
async def delete_access(access_id: str):
    """
    Delete an access record by ID.
    
    - **access_id**: Unique identifier of the access record to delete
    """
    try:
        success = await AccessService.delete_access(access_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Access record not found")
        
        return {
            "message": "Access record deleted successfully",
            "deleted_id": access_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Health check endpoint
@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "DoorGuardian API is running",
        "version": settings.VERSION
    }