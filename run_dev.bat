@echo off
REM Development server startup script for FastAPI (Windows)

echo 🚀 Starting DoorGuardian FastAPI Development Server...

REM Check if .env file exists
if not exist .env (
    echo ❌ .env file not found. Using defaults.
) else (
    echo ✅ Environment variables will be loaded from .env
)

echo 🌐 Starting FastAPI development server with uvicorn...
echo    URL: http://localhost:8000
echo    API: http://localhost:8000/api/v1
echo    Health: http://localhost:8000/api/v1/health
echo    Docs: http://localhost:8000/docs
echo    ReDoc: http://localhost:8000/redoc
echo.
echo Press Ctrl+C to stop the server

REM Start the FastAPI development server with uvicorn using main.py
uvicorn main:app --host 0.0.0.0 --port 8000 --reload --log-level info