"""
Main entry point for the DoorGuardian FastAPI application.
This module creates and exports the FastAPI app instance for uvicorn.
"""
import os
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Now import the app factory
from app.app_factory import create_app

# Create the FastAPI app instance at module level
app = create_app()

# Export for uvicorn
__all__ = ["app"]