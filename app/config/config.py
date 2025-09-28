import os
from typing import List, Union

try:
    from pydantic_settings import BaseSettings
    from pydantic import validator
except ImportError:
    from pydantic import BaseSettings, validator

class Settings(BaseSettings):
    """Application settings using Pydantic for validation"""
    
    # Environment (obrigatório do .env)
    ENVIRONMENT: str
    DEBUG: bool
    
    # API Configuration (obrigatório do .env)
    API_V1_STR: str
    PROJECT_NAME: str
    VERSION: str
    
    # Supabase Configuration (obrigatório do .env)
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_SERVICE_ROLE_KEY: str
    
    # Security (obrigatório do .env)
    SECRET_KEY: str
    
    # File Upload Configuration
    UPLOAD_FOLDER: str
    MAX_FILE_SIZE: int
    
    # File Types - podem ser sobrescritos via .env
    ALLOWED_FILE_TYPES: List[str] = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    ALLOWED_EXTENSIONS: List[str] = ["jpg", "jpeg", "png", "gif", "webp"]
    
    # CORS Configuration - podem ser sobrescritos via .env
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000", 
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000"
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        
    @validator('BACKEND_CORS_ORIGINS', pre=True)
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS origins from environment variable (comma-separated string)"""
        if isinstance(v, str):
            return [item.strip() for item in v.split(",") if item.strip()]
        return v
    
    @validator('ALLOWED_FILE_TYPES', pre=True)
    @classmethod 
    def parse_allowed_file_types(cls, v):
        """Parse file types from environment variable (comma-separated string)"""
        if isinstance(v, str):
            return [item.strip() for item in v.split(",") if item.strip()]
        return v
    
    @validator('ALLOWED_EXTENSIONS', pre=True)
    @classmethod 
    def parse_allowed_extensions(cls, v):
        """Parse file extensions from environment variable (comma-separated string)"""
        if isinstance(v, str):
            return [item.strip() for item in v.split(",") if item.strip()]
        return v

# Create settings instance
settings = Settings()