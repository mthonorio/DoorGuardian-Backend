import os
import uuid
import mimetypes
from io import BytesIO
from PIL import Image
from typing import Dict, Any
from fastapi import UploadFile
from app.config.config import settings

def allowed_file(filename: str) -> bool:
    """Check if file has allowed extension"""
    if not filename or '.' not in filename:
        return False
    
    extension = filename.rsplit('.', 1)[1].lower()
    return extension in settings.ALLOWED_EXTENSIONS

def allowed_mime_type(mime_type: str) -> bool:
    """Check if mime type is allowed"""
    return mime_type in settings.ALLOWED_FILE_TYPES

def validate_image_content(file_content: bytes) -> bool:
    """Validate if file content is a valid image"""
    try:
        with Image.open(BytesIO(file_content)) as img:
            img.verify()  # Verify it's a valid image
        return True
    except Exception:
        return False

def generate_unique_filename(original_filename: str) -> str:
    """Generate unique filename while preserving extension"""
    if not original_filename:
        return f"{uuid.uuid4()}.jpg"
    
    # Get file extension
    filename, file_extension = os.path.splitext(original_filename)
    
    # Generate UUID for filename
    unique_id = str(uuid.uuid4())
    
    # Return secure filename with UUID
    return f"{unique_id}{file_extension.lower()}"

def get_file_info_from_upload(file: UploadFile, file_size: int, file_content: bytes = None) -> Dict[str, Any]:
    """Get file information from FastAPI UploadFile with improved MIME type detection"""
    
    # Try to get MIME type from multiple sources
    mime_type = None
    
    # 1. First try the content_type from the upload
    if file.content_type and file.content_type != 'text/plain':
        mime_type = file.content_type
    
    # 2. If not available or is text/plain, guess from filename
    if not mime_type or mime_type == 'text/plain':
        guessed_type = mimetypes.guess_type(file.filename)[0] if file.filename else None
        if guessed_type:
            mime_type = guessed_type
    
    # 3. For images, try to detect from file content if available
    if file_content and (not mime_type or mime_type == 'text/plain'):
        try:
            with Image.open(BytesIO(file_content)) as img:
                format_map = {
                    'JPEG': 'image/jpeg',
                    'PNG': 'image/png', 
                    'GIF': 'image/gif',
                    'WEBP': 'image/webp'
                }
                if img.format in format_map:
                    mime_type = format_map[img.format]
        except Exception:
            pass
    
    # 4. Default fallback
    if not mime_type:
        mime_type = 'application/octet-stream'
    
    return {
        'size': file_size,
        'mime_type': mime_type,
        'original_filename': file.filename
    }

def create_upload_directory(upload_path: str) -> None:
    """Create upload directory if it doesn't exist"""
    os.makedirs(upload_path, exist_ok=True)

def secure_filename(filename: str) -> str:
    """Secure a filename by removing potentially dangerous characters"""
    # Remove path separators and other dangerous characters
    filename = filename.replace('/', '_').replace('\\', '_')
    filename = ''.join(c for c in filename if c.isalnum() or c in '._-')
    
    # Limit length
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:255-len(ext)] + ext
    
    return filename