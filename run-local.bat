@echo off
REM Local development script for Dr. Kishan Bhalani Medical Documentation Services
REM Runs the application without Docker

echo 🏥 Dr. Kishan Bhalani Medical Documentation Services - Local Development
echo ================================================================

echo 📋 Checking Python installation...
python --version
if %ERRORLEVEL% neq 0 (
    echo ❌ Python not found! Please install Python 3.11 or higher
    pause
    exit /b 1
)

echo 📋 Checking Node.js installation...
node --version
if %ERRORLEVEL% neq 0 (
    echo ❌ Node.js not found! Please install Node.js 18 or higher
    pause
    exit /b 1
)

echo ✅ Prerequisites check passed!

REM Install backend dependencies
echo 📦 Installing backend dependencies...
cd backend
pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo ❌ Failed to install backend dependencies!
    pause
    exit /b 1
)

echo ✅ Backend dependencies installed!

REM Install frontend dependencies
echo 📦 Installing frontend dependencies...
cd ..\frontend
npm install --legacy-peer-deps
if %ERRORLEVEL% neq 0 (
    echo ❌ Failed to install frontend dependencies!
    pause
    exit /b 1
)

echo ✅ Frontend dependencies installed!

REM Build frontend
echo 🔨 Building frontend...
npm run build
if %ERRORLEVEL% neq 0 (
    echo ❌ Frontend build failed!
    pause
    exit /b 1
)

echo ✅ Frontend built successfully!

REM Start backend server
echo 🚀 Starting backend server...
cd ..\backend
echo 🌐 Server will be available at: http://localhost:8000
echo 🏥 Health check at: http://localhost:8000/api/health
echo 📋 Services API at: http://localhost:8000/api/services
echo.
echo 💡 Press Ctrl+C to stop the server
echo ================================================================

python run_server.py

pause