@echo off
REM Quick test script to check if the application is working

echo 🔍 Quick Test - Dr. Kishan Bhalani Medical Documentation Services
echo ================================================================

echo 📋 Testing backend server...
python check-port.py

echo.
echo 📋 Manual test commands:
echo   curl http://localhost:8000/api/health
echo   curl http://localhost:8080/api/health
echo.

REM Try to test the health endpoint
echo 🏥 Testing health endpoint...
curl -s http://localhost:8000/api/health 2>nul
if %ERRORLEVEL% equ 0 (
    echo ✅ Server responding on port 8000
) else (
    curl -s http://localhost:8080/api/health 2>nul
    if %ERRORLEVEL% equ 0 (
        echo ✅ Server responding on port 8080
    ) else (
        echo ❌ Server not responding on common ports
        echo    Make sure the server is running with: python backend/run_server.py
    )
)

pause