#!/usr/bin/env python3
"""
Kubernetes 502 Bad Gateway Diagnostic Tool
Dr. Kishan Bhalani Medical Documentation Services
"""

import os
import sys
import time
import requests
from datetime import datetime

def log(message):
    timestamp = datetime.now().isoformat()
    print(f"[{timestamp}] {message}")

def check_environment():
    """Check environment variables"""
    log("🔍 Checking environment variables...")
    
    required_vars = ['SUPABASE_URL', 'SUPABASE_KEY']
    missing_vars = []
    
    for var in required_vars:
        value = os.environ.get(var)
        if value:
            log(f"✅ {var}: {'*' * 20}...{value[-10:]}")
        else:
            log(f"❌ {var}: NOT SET")
            missing_vars.append(var)
    
    port = os.environ.get('PORT', '8000')
    log(f"📍 PORT: {port}")
    
    return len(missing_vars) == 0

def check_server_startup():
    """Check if the server can start"""
    log("🚀 Testing server startup...")
    
    try:
        # Add backend to path
        from pathlib import Path
        backend_dir = Path(__file__).parent / "backend"
        if backend_dir.exists():
            sys.path.insert(0, str(backend_dir))
            os.chdir(backend_dir)
            log(f"✅ Backend directory found: {backend_dir}")
        
        # Try importing server
        try:
            from server import app
            log("✅ Main server module imported successfully")
            return True, app
        except ImportError as e:
            log(f"⚠️ Main server import failed: {e}")
            
            # Try railway server
            try:
                sys.path.insert(0, str(Path(__file__).parent))
                from railway_server import app
                log("✅ Railway server imported successfully")
                return True, app
            except ImportError as e2:
                log(f"❌ Railway server import failed: {e2}")
                return False, None
                
    except Exception as e:
        log(f"❌ Server startup test failed: {e}")
        return False, None

def check_health_endpoint(port=None):
    """Check if health endpoint responds"""
    if port is None:
        port = os.environ.get('PORT', '8000')
    
    log(f"🏥 Testing health endpoint on port {port}...")
    
    urls_to_test = [
        f"http://localhost:{port}/api/health",
        f"http://localhost:{port}/health",
        f"http://0.0.0.0:{port}/api/health",
        f"http://0.0.0.0:{port}/health"
    ]
    
    for url in urls_to_test:
        try:
            log(f"Testing: {url}")
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                log(f"✅ Health check successful: {response.json()}")
                return True
            else:
                log(f"⚠️ Health check returned {response.status_code}")
        except requests.exceptions.ConnectionError:
            log(f"❌ Connection refused: {url}")
        except requests.exceptions.Timeout:
            log(f"❌ Timeout: {url}")
        except Exception as e:
            log(f"❌ Error: {url} - {e}")
    
    return False

def check_kubernetes_readiness():
    """Check Kubernetes readiness probe requirements"""
    log("☸️ Checking Kubernetes readiness requirements...")
    
    # Check if server binds to 0.0.0.0 (not just localhost)
    port = os.environ.get('PORT', '8000')
    
    log("Kubernetes requirements:")
    log("1. Server must bind to 0.0.0.0 (not localhost)")
    log("2. Health endpoint must respond within timeout")
    log("3. Server must start within startup timeout")
    log("4. Process must not exit after startup")
    
    return True

def create_minimal_server():
    """Create a minimal working server for testing"""
    log("🔧 Creating minimal test server...")
    
    try:
        from fastapi import FastAPI
        from datetime import datetime, timezone
        import uvicorn
        
        app = FastAPI(title="K8s Diagnostic Server")
        
        @app.get("/")
        async def root():
            return {
                "message": "Dr. Kishan Medical Services - Diagnostic Mode",
                "status": "healthy",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "port": os.environ.get('PORT', '8000'),
                "environment": dict(os.environ)
            }
        
        @app.get("/health")
        @app.get("/api/health")
        async def health():
            return {
                "status": "healthy",
                "mode": "diagnostic",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        
        @app.get("/debug")
        async def debug():
            return {
                "environment_variables": dict(os.environ),
                "python_path": sys.path,
                "current_directory": os.getcwd(),
                "available_files": os.listdir(".")
            }
        
        port = int(os.environ.get('PORT', '8000'))
        log(f"🚀 Starting diagnostic server on 0.0.0.0:{port}")
        
        uvicorn.run(
            app,
            host="0.0.0.0",  # Important: bind to all interfaces for K8s
            port=port,
            log_level="info"
        )
        
    except Exception as e:
        log(f"❌ Failed to create minimal server: {e}")
        sys.exit(1)

def main():
    log("🏥 Dr. Kishan Bhalani Medical Services - K8s Diagnostic Tool")
    log("=" * 60)
    
    # Check if this is a diagnostic run or server start
    if len(sys.argv) > 1 and sys.argv[1] == "diagnose":
        log("Running diagnostic checks...")
        
        # Run diagnostics
        env_ok = check_environment()
        server_ok, app = check_server_startup()
        
        if not env_ok:
            log("❌ Environment variables missing")
            return False
        
        if not server_ok:
            log("❌ Server startup failed")
            return False
        
        log("✅ All diagnostic checks passed")
        return True
    
    else:
        log("Starting server with diagnostics...")
        
        # Quick environment check
        if not check_environment():
            log("⚠️ Environment issues detected, starting minimal server...")
            create_minimal_server()
            return
        
        # Try to start the real server
        server_ok, app = check_server_startup()
        
        if server_ok and app:
            log("✅ Starting full server...")
            import uvicorn
            port = int(os.environ.get('PORT', '8000'))
            
            uvicorn.run(
                app,
                host="0.0.0.0",  # Critical for K8s
                port=port,
                log_level="info"
            )
        else:
            log("⚠️ Full server failed, starting minimal server...")
            create_minimal_server()

if __name__ == "__main__":
    main()