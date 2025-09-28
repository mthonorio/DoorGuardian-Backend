@echo off
REM Database setup script for DoorGuardian (Windows)

echo 🔧 Setting up DoorGuardian Database...

REM Check if .env file exists
if not exist .env (
    echo ❌ .env file not found. Please copy .env.example to .env and configure it.
    exit /b 1
)

REM Initialize Flask-Migrate if not already done
if not exist migrations (
    echo 📦 Initializing database migrations...
    flask db init
)

REM Create migration
echo 🔄 Creating database migration...
flask db migrate -m "Initial migration - Access and Image models"

REM Apply migration
echo ⬆️ Applying database migration...
flask db upgrade

REM Create upload directory
echo 📁 Creating upload directories...
if not exist uploads\images mkdir uploads\images

echo ✅ Database setup completed successfully!
echo 🚀 You can now run the application with: python app.py