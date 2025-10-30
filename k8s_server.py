#!/usr/bin/env python3
"""
Kubernetes-optimized server for Dr. Kishan Bhalani Medical Documentation Services
Addresses common 502 Bad Gateway issues
"""

import os
import sys
import logging
from pathlib import Path
from datetime import datetime, timezone

# Configure logging for Kubernetes
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def setup_paths():
    """Setup Python paths for imports"""
    root_dir = Path(__file__).parent
    backend_dir = root_dir / "backend"
    
    # Add paths
    for path in [str(root_dir), str(backend_dir)]:
        if path not in sys.path:
            sys.path.insert(0, path)
    
    # Change to backend directory if it exists
    if backend_dir.exists():
        os.chdir(backend_dir)
        logger.info(f"Changed to backend directory: {backend_dir}")
    
    return backend_dir.exists()

def create_k8s_optimized_app():
    """Create a Kubernetes-optimized FastAPI application"""
    from fastapi import FastAPI, Request
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
    import uvicorn
    
    # Create app with proper configuration for K8s
    app = FastAPI(
        title="Dr. Kishan Bhalani Medical Services",
        description="HIPAA-compliant medical documentation services",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # CORS middleware - important for K8s ingress
    cors_origins = os.environ.get('CORS_ORIGINS', '*').split(',')
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )
    
    # Health check endpoints - critical for K8s probes
    @app.get("/health")
    @app.get("/api/health")
    @app.get("/healthz")  # K8s standard
    @app.get("/ready")    # K8s readiness
    async def health_check():
        """Health check endpoint for Kubernetes probes"""
        return {
            "status": "healthy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "service": "dr-kishan-medical-services",
            "version": "1.0.0"
        }
    
    # Liveness probe - simpler check
    @app.get("/alive")
    async def liveness_check():
        """Liveness probe for Kubernetes"""
        return {"status": "alive"}
    
    # Root endpoint
    @app.get("/")
    async def root():
        """Root endpoint"""
        return {
            "message": "Dr. Kishan Bhalani Medical Documentation Services",
            "status": "running",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "endpoints": {
                "health": "/health",
                "api_health": "/api/health",
                "services": "/api/services",
                "blog": "/api/blog",
                "contact": "/api/contact"
            }
        }
    
    # Try to import and add the full API
    try:
        logger.info("Attempting to import full server module...")
        
        # Try different import methods
        try:
            from server import api_router
            app.include_router(api_router)
            logger.info("✅ Full API imported successfully")
        except ImportError:
            logger.warning("Main server import failed, trying railway_server...")
            try:
                # Import railway server components
                sys.path.insert(0, str(Path(__file__).parent))
                from railway_server import api_router
                app.include_router(api_router)
                logger.info("✅ Railway server API imported successfully")
            except ImportError as e:
                logger.warning(f"Railway server import failed: {e}")
                logger.info("Creating minimal API endpoints...")
                
                # Create minimal API endpoints
                from fastapi import APIRouter, HTTPException
                from typing import List
                
                api_router = APIRouter(prefix="/api")
                
                @api_router.get("/services")
                async def get_services():
                    return [{
                        "id": "1",
                        "slug": "nexus-rebuttal-letters",
                        "title": "Nexus & Rebuttal Letters",
                        "shortDescription": "Professional medical opinions for VA claims",
                        "basePriceInUSD": 1499,
                        "duration": "7-10 business days",
                        "category": "nexus-letter"
                    }]
                
                @api_router.get("/blog")
                async def get_blog():
                    return [{
                        "id": "1",
                        "slug": "nexus-letters-explained",
                        "title": "Understanding Nexus Letters",
                        "excerpt": "Learn about nexus letters for VA claims",
                        "authorName": "Dr. Kishan Bhalani"
                    }]
                
                @api_router.post("/contact")
                async def create_contact(contact_data: dict):
                    return {
                        "id": "temp-id",
                        "status": "received",
                        "message": "Contact form received (minimal mode)"
                    }
                
                app.include_router(api_router)
                logger.info("✅ Minimal API endpoints created")
    
    except Exception as e:
        logger.error(f"Failed to setup API: {e}")
        # App will still work with basic health checks
    
    return app

def main():
    """Main entry point optimized for Kubernetes"""
    logger.info("🏥 Starting Dr. Kishan Bhalani Medical Services (K8s optimized)")
    
    # Setup paths
    backend_available = setup_paths()
    logger.info(f"Backend directory available: {backend_available}")
    
    # Get configuration from environment
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"  # Critical: must bind to all interfaces for K8s
    
    # Log environment info
    logger.info(f"Server configuration: {host}:{port}")
    logger.info(f"Environment: {os.environ.get('ENVIRONMENT', 'development')}")
    
    # Create the application
    try:
        app = create_k8s_optimized_app()
        logger.info("✅ Application created successfully")
        
        # Start the server with K8s-friendly configuration
        import uvicorn
        
        logger.info(f"🚀 Starting server on {host}:{port}")
        logger.info("Health endpoints available at:")
        logger.info(f"  - http://{host}:{port}/health")
        logger.info(f"  - http://{host}:{port}/healthz")
        logger.info(f"  - http://{host}:{port}/ready")
        logger.info(f"  - http://{host}:{port}/alive")
        
        uvicorn.run(
            app,
            host=host,
            port=port,
            log_level="info",
            access_log=True,
            # K8s-friendly settings
            timeout_keep_alive=30,
            timeout_graceful_shutdown=30
        )
        
    except Exception as e:
        logger.error(f"❌ Server startup failed: {e}")
        logger.error("Available files in current directory:")
        for file in os.listdir("."):
            logger.error(f"  - {file}")
        sys.exit(1)

if __name__ == "__main__":
    main()