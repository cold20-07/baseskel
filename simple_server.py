#!/usr/bin/env python3
"""
Simple server entry point for Railway deployment
Minimal dependencies version of Dr. Kishan Bhalani Medical Documentation Services
"""

import os
import sys
from pathlib import Path

# Simple logging
def log(message):
    print(f"[SIMPLE_SERVER] {message}")

log("Starting simple server...")

# Add backend to path
backend_dir = Path(__file__).parent / "backend"
if backend_dir.exists():
    sys.path.insert(0, str(backend_dir))
    os.chdir(backend_dir)
    log(f"Added backend directory: {backend_dir}")
else:
    log("Backend directory not found, using current directory")

# Try to import and run the server
try:
    log("Attempting to import server module...")
    
    # Try the main server first
    try:
        from server import app
        log("✅ Successfully imported main server")
    except ImportError as e:
        log(f"Main server import failed: {e}")
        log("Trying railway_server as fallback...")
        
        # Fallback to railway_server
        sys.path.insert(0, str(Path(__file__).parent))
        from railway_server import app
        log("✅ Successfully imported railway_server")
    
    # Start the server
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    
    log(f"🚀 Starting server on {host}:{port}")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )
    
except Exception as e:
    log(f"❌ Server startup failed: {e}")
    log("Available files:")
    for file in os.listdir("."):
        log(f"  - {file}")
    
    # Last resort: create a minimal FastAPI app
    log("Creating minimal FastAPI app as last resort...")
    
    try:
        from fastapi import FastAPI
        from datetime import datetime, timezone
        
        app = FastAPI(title="Dr. Kishan Medical Services - Minimal")
        
        @app.get("/")
        async def root():
            return {
                "message": "Dr. Kishan Bhalani Medical Documentation Services",
                "status": "minimal_mode",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        
        @app.get("/api/health")
        async def health():
            return {
                "status": "healthy",
                "mode": "minimal",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        
        import uvicorn
        port = int(os.environ.get("PORT", 8000))
        log(f"🚀 Starting minimal server on 0.0.0.0:{port}")
        
        uvicorn.run(app, host="0.0.0.0", port=port)
        
    except Exception as e2:
        log(f"❌ Even minimal server failed: {e2}")
        sys.exit(1)