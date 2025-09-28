from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
import uuid

class ImageBase(BaseModel):
    """Base Image model with common fields"""
    filename: str = Field(..., description="Unique filename for the image")
    original_filename: Optional[str] = Field(None, description="Original filename as uploaded")
    file_size: int = Field(..., gt=0, description="File size in bytes")
    mime_type: str = Field(..., description="MIME type of the image")

class ImageCreate(ImageBase):
    """Image model for creation"""
    file_path: str = Field(..., description="Storage path of the image")

class ImageUpdate(BaseModel):
    """Image model for updates"""
    filename: Optional[str] = None
    original_filename: Optional[str] = None

class Image(ImageBase):
    """Complete Image model with database fields"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique identifier")
    file_path: str = Field(..., description="Storage path of the image")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "filename": "uuid-generated-name.jpg",
                "original_filename": "person.jpg",
                "file_path": "uploads/images/uuid-generated-name.jpg",
                "file_size": 1024567,
                "mime_type": "image/jpeg",
                "created_at": "2023-12-07T10:30:00Z",
                "updated_at": "2023-12-07T10:30:00Z"
            }
        }