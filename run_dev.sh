#!/bin/bash

# Development server startup script for FastAPI

echo "🚀 Starting DoorGuardian FastAPI Development Server..."

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Warning: No virtual environment detected."
    echo "   Consider activating your virtual environment first:"
    echo "   source venv/bin/activate"
    echo ""
fi

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
    echo "✅ Environment variables loaded from .env"
else
    echo "❌ .env file not found. Using defaults."
fi

echo "🌐 Starting FastAPI development server with uvicorn..."
echo "   URL: http://localhost:8000"
echo "   API: http://localhost:8000/api/v1"
echo "   Health: http://localhost:8000/api/v1/health"
echo "   Docs: http://localhost:8000/docs"
echo "   ReDoc: http://localhost:8000/redoc"
echo ""
echo "Press Ctrl+C to stop the server"

# Start the FastAPI development server with uvicorn using main.py
uvicorn main:app --host 0.0.0.0 --port 8000 --reload --log-level info