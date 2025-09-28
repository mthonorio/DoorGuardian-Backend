"""
Development runner for DoorGuardian FastAPI application.
Use this file to run the application in development mode.

For production, use: uvicorn main:app
"""
import uvicorn

if __name__ == "__main__":
    print("🚀 Starting DoorGuardian API in development mode...")
    print("📚 Docs will be available at: http://localhost:8000/docs")
    print("🔧 API endpoints at: http://localhost:8000/api/v1")
    print("")
    
    # Run with uvicorn pointing to main.py
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )