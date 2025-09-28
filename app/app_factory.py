import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config.config import settings
from app.routes.access_routes import router as access_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print("🚀 Starting DoorGuardian API...")
    
    # Create upload directories
    upload_folder = settings.UPLOAD_FOLDER
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder, exist_ok=True)
        print(f"📁 Created upload directory: {upload_folder}")
    
    print("✅ DoorGuardian API started successfully!")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down DoorGuardian API...")

def create_app() -> FastAPI:
    """Create FastAPI application with configuration"""
    
    # Create FastAPI app
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="REST API for intelligent door access management with Supabase backend",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(access_router)
    
    # Global exception handlers
    @app.exception_handler(404)
    async def not_found_handler(request, exc):
        return JSONResponse(
            status_code=404,
            content={"error": "Resource not found"}
        )
    
    @app.exception_handler(405)
    async def method_not_allowed_handler(request, exc):
        return JSONResponse(
            status_code=405,
            content={"error": "Method not allowed"}
        )
    
    @app.exception_handler(413)
    async def payload_too_large_handler(request, exc):
        return JSONResponse(
            status_code=413,
            content={"error": "File too large"}
        )
    
    @app.exception_handler(500)
    async def internal_server_error_handler(request, exc):
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error"}
        )
    
    # Root endpoint
    @app.get("/")
    async def root():
        return {
            "name": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "description": "REST API for intelligent door access management",
            "docs": "/docs",
            "health": "/api/v1/health"
        }
    
    # API info endpoint
    @app.get(settings.API_V1_STR)
    async def api_info():
        return {
            "name": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "description": "REST API for intelligent door access management",
            "endpoints": {
                "GET /api/v1/history": "Retrieve access history with pagination and filtering",
                "POST /api/v1/register": "Register new access record with optional image",
                "DELETE /api/v1/history/{id}": "Delete access record by ID",
                "GET /api/v1/health": "Health check endpoint"
            },
            "docs": "/docs",
            "redoc": "/redoc"
        }
    
    return app