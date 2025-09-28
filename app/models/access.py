from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
import uuid
from .image import Image

class AccessBase(BaseModel):
    """Base Access model with common fields"""
    access: bool = Field(..., description="Access granted (true) or denied (false)")
    date: datetime = Field(default_factory=datetime.utcnow, description="Date and time of access attempt")

class AccessCreate(AccessBase):
    """Access model for creation"""
    image_id: Optional[str] = Field(None, description="Optional image ID associated with this access")

class AccessUpdate(BaseModel):
    """Access model for updates"""
    access: Optional[bool] = None
    date: Optional[datetime] = None
    image_id: Optional[str] = None

class Access(AccessBase):
    """Complete Access model with database fields"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique identifier")
    image_id: Optional[str] = Field(None, description="Associated image ID")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "access": True,
                "date": "2023-12-07T10:30:00Z",
                "image_id": "789e0123-e89b-12d3-a456-426614174001",
                "created_at": "2023-12-07T10:30:00Z",
                "updated_at": "2023-12-07T10:30:00Z"
            }
        }

class AccessWithImage(Access):
    """Access model with embedded image data"""
    image: Optional[Image] = Field(None, description="Associated image data")
    
    class Config:
        from_attributes = True

# Response models
class AccessListResponse(BaseModel):
    """Response model for access list with pagination"""
    access_records: list[AccessWithImage]
    pagination: dict
    
class AccessCreateResponse(BaseModel):
    """Response model for access creation"""
    message: str
    access_record: AccessWithImage