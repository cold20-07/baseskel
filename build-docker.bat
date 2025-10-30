@echo off
REM Docker Build Script for Dr. Kishan Bhalani Medical Documentation Services
REM This script builds and optionally runs the Docker container

echo 🐳 Building Dr. Kishan Bhalani Medical Documentation Services Docker Image...

REM Build the Docker image
docker build -t dr-kishan-medical-services:latest .

if %ERRORLEVEL% neq 0 (
    echo ❌ Docker build failed!
    pause
    exit /b 1
)

echo ✅ Docker image built successfully!

REM Ask if user wants to run the container
set /p run_container="Do you want to run the container now? (y/n): "

if /i "%run_container%"=="y" (
    echo 🚀 Starting container...
    
    REM Stop any existing container
    docker stop dr-kishan-medical 2>nul
    docker rm dr-kishan-medical 2>nul
    
    REM Run the new container
    docker run -d ^
        --name dr-kishan-medical ^
        -p 8000:8000 ^
        -e SUPABASE_URL=https://cwjsyxxzdwphhlpppxau.supabase.co ^
        -e SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN3anN5eHh6ZHdwaGhscHBweGF1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE2MzA2MTUsImV4cCI6MjA3NzIwNjYxNX0.7qmRxFhZr_rHwKRp_YaD3HB4D30feclY3xNPipoJvr0 ^
        -e CORS_ORIGINS=* ^
        -e HIPAA_ENCRYPTION_KEY=bw7Y9P3w4QJFVJatMqu8+gv8mRlWmlhAB7FHLvR8c8M= ^
        -e ENVIRONMENT=production ^
        -e ALLOWED_HOSTS=* ^
        dr-kishan-medical-services:latest
    
    if %ERRORLEVEL% neq 0 (
        echo ❌ Failed to start container!
        pause
        exit /b 1
    )
    
    echo ✅ Container started successfully!
    echo 🌐 Application available at: http://localhost:8000
    echo 🏥 Health check: http://localhost:8000/api/health
    echo 📋 Services API: http://localhost:8000/api/services
    
    REM Show container logs
    echo 📋 Container logs:
    docker logs -f dr-kishan-medical
) else (
    echo ℹ️  To run the container later, use:
    echo    docker run -d --name dr-kishan-medical -p 8000:8000 dr-kishan-medical-services:latest
)

pause