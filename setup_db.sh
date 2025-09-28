#!/bin/bash

# Database setup script for DoorGuardian

echo "🔧 Setting up DoorGuardian Database..."

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "❌ .env file not found. Please copy .env.example to .env and configure it."
    exit 1
fi

# Initialize Flask-Migrate if not already done
if [ ! -d "migrations" ]; then
    echo "📦 Initializing database migrations..."
    flask db init
fi

# Create migration
echo "🔄 Creating database migration..."
flask db migrate -m "Initial migration - Access and Image models"

# Apply migration
echo "⬆️ Applying database migration..."
flask db upgrade

# Create upload directory
echo "📁 Creating upload directories..."
mkdir -p uploads/images

echo "✅ Database setup completed successfully!"
echo "🚀 You can now run the application with: python app.py"