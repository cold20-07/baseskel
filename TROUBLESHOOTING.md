# 🔧 Troubleshooting Guide
## Dr. Kishan Bhalani Medical Documentation Services

### 🐳 Docker Issues

#### **Error: Docker Desktop Not Running**
```
ERROR: error during connect: Head "http://%2F%2F.%2Fpipe%2FdockerDesktopLinuxEngine/_ping"
```

**Solution:**
1. **Start Docker Desktop** from Windows Start menu
2. **Wait for Docker to fully start** (whale icon in system tray)
3. **Try the build command again**

#### **Error: Docker Not Installed**
**Solution:**
1. **Download Docker Desktop**: https://www.docker.com/products/docker-desktop/
2. **Install** and restart your computer
3. **Launch Docker Desktop**

### 🚀 Alternative: Run Without Docker

If Docker issues persist, run locally:

```bash
# Use the local development script
./run-local.bat

# Or manually:
cd backend
pip install -r requirements.txt
python run_server.py
```

### 🔍 Port Issues

#### **Server Running on Port 8080 Instead of 8000**
This is **normal** for Railway deployments. Railway sets the `PORT` environment variable.

**Check which port is active:**
```bash
python check-port.py
```

**Test endpoints:**
```bash
# Try both ports
curl http://localhost:8000/api/health
curl http://localhost:8080/api/health
```

### 📦 Dependency Issues

#### **npm Install Fails**
```bash
# Use legacy peer deps
cd frontend
npm install --legacy-peer-deps
```

#### **Python Dependencies Fail**
```bash
# Upgrade pip first
pip install --upgrade pip
cd backend
pip install -r requirements.txt
```

### 🔐 Environment Variable Issues

#### **Supabase Connection Fails**
Check your `.env` file has:
```env
SUPABASE_URL=https://cwjsyxxzdwphhlpppxau.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN3anN5eHh6ZHdwaGhscHBweGF1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE2MzA2MTUsImV4cCI6MjA3NzIwNjYxNX0.7qmRxFhZr_rHwKRp_YaD3HB4D30feclY3xNPipoJvr0
HIPAA_ENCRYPTION_KEY=bw7Y9P3w4QJFVJatMqu8+gv8mRlWmlhAB7FHLvR8c8M=
```

### 🌐 CORS Issues

#### **Frontend Can't Connect to Backend**
Add to backend `.env`:
```env
CORS_ORIGINS=http://localhost:3000,http://localhost:3001,*
```

### 🏥 Health Check Fails

#### **Health Endpoint Returns 500**
1. **Check Supabase credentials** are correct
2. **Verify database tables** exist
3. **Check server logs** for specific errors

### 📋 Quick Diagnostic Commands

```bash
# Check what's running
python check-port.py

# Test health endpoint
curl http://localhost:8000/api/health

# Test services endpoint  
curl http://localhost:8000/api/services

# Check Docker status
docker --version
docker ps

# Check Python/Node versions
python --version
node --version
npm --version
```

### 🆘 Still Having Issues?

1. **Run the quick test**: `./quick-test.bat`
2. **Check the logs** in your terminal
3. **Verify all prerequisites** are installed:
   - Python 3.11+
   - Node.js 18+
   - Docker Desktop (for containerized deployment)

### ✅ Success Indicators

When everything is working, you should see:
```
✅ Server responding on port 8000 (or 8080)
✅ Health check returns: {"status": "healthy"}
✅ Services API returns array of medical services
✅ No CORS errors in browser console
```

### 🔄 Reset Everything

If all else fails, clean reset:
```bash
# Clean Docker
docker system prune -a

# Clean Node modules
cd frontend
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps

# Clean Python cache
cd ../backend
rm -rf __pycache__
pip install -r requirements.txt --force-reinstall
```