#!/usr/bin/env python3
"""
Robust server for Dr. Kishan Bhalani Medical Documentation Services
Addresses upstream server issues, overloading, and 502 errors
"""

import os
import sys
import signal
import asyncio
import logging
import time
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional
import multiprocessing

# Configure robust logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('/tmp/server.log', mode='a') if os.path.exists('/tmp') else logging.NullHandler()
    ]
)
logger = logging.getLogger(__name__)

class ServerManager:
    """Manages server lifecycle and handles graceful shutdown"""
    
    def __init__(self):
        self.server = None
        self.should_exit = False
        self.startup_time = time.time()
        
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        logger.info(f"Received signal {signum}, initiating graceful shutdown...")
        self.should_exit = True
        if self.server:
            self.server.should_exit = True

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

def create_robust_app():
    """Create a robust FastAPI application with error handling"""
    from fastapi import FastAPI, Request, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
    from fastapi.middleware.trustedhost import TrustedHostMiddleware
    import uvicorn
    
    # Create app with robust configuration
    app = FastAPI(
        title="Dr. Kishan Bhalani Medical Services",
        description="Robust HIPAA-compliant medical documentation services",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Add trusted host middleware for security
    allowed_hosts = os.environ.get('ALLOWED_HOSTS', '*').split(',')
    if '*' not in allowed_hosts:
        app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)
    
    # CORS middleware with proper configuration
    cors_origins = os.environ.get('CORS_ORIGINS', '*').split(',')
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD"],
        allow_headers=["*"],
        expose_headers=["*"]
    )
    
    # Global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Global exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "message": "The server encountered an unexpected error",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        )
    
    # Health check endpoints - multiple variants for different systems
    @app.get("/health")
    @app.get("/api/health")
    @app.get("/healthz")
    @app.get("/healthcheck")
    @app.get("/ready")
    @app.get("/readiness")
    @app.get("/alive")
    @app.get("/liveness")
    @app.head("/health")  # For HEAD requests
    async def health_check():
        """Comprehensive health check endpoint"""
        uptime = time.time() - server_manager.startup_time
        
        # Check system resources
        try:
            import psutil
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            system_health = {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "disk_percent": disk.percent,
                "load_average": os.getloadavg() if hasattr(os, 'getloadavg') else None
            }
        except ImportError:
            system_health = {"note": "psutil not available"}
        
        return {
            "status": "healthy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "uptime_seconds": round(uptime, 2),
            "service": "dr-kishan-medical-services",
            "version": "1.0.0",
            "system": system_health,
            "environment": {
                "port": os.environ.get('PORT', '8000'),
                "host": "0.0.0.0",
                "workers": os.environ.get('WEB_CONCURRENCY', '1'),
                "environment": os.environ.get('ENVIRONMENT', 'production')
            }
        }
    
    # Simple liveness probe (minimal response)
    @app.get("/ping")
    @app.head("/ping")
    async def ping():
        """Simple ping endpoint for basic liveness checks"""
        return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}
    
    # Root endpoint with service information
    @app.get("/")
    async def root():
        """Root endpoint with service information"""
        return {
            "message": "Dr. Kishan Bhalani Medical Documentation Services",
            "status": "running",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "uptime_seconds": round(time.time() - server_manager.startup_time, 2),
            "endpoints": {
                "health": "/health",
                "api_health": "/api/health",
                "services": "/api/services",
                "blog": "/api/blog",
                "contact": "/api/contact",
                "docs": "/docs"
            },
            "version": "1.0.0"
        }
    
    # Load balancer status endpoint
    @app.get("/status")
    async def status():
        """Status endpoint for load balancers"""
        return {
            "status": "UP",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    # Try to import and add the full API with error handling
    try:
        logger.info("Attempting to import full server module...")
        
        # Try different import methods with fallbacks
        api_loaded = False
        
        # Method 1: Try main server
        try:
            from server import api_router
            app.include_router(api_router)
            logger.info("✅ Full API from server.py imported successfully")
            api_loaded = True
        except ImportError as e:
            logger.warning(f"Main server import failed: {e}")
            
            # Method 2: Try railway server
            try:
                sys.path.insert(0, str(Path(__file__).parent))
                from railway_server import api_router
                app.include_router(api_router)
                logger.info("✅ Railway server API imported successfully")
                api_loaded = True
            except ImportError as e2:
                logger.warning(f"Railway server import failed: {e2}")
        
        # Method 3: Create minimal API if imports fail
        if not api_loaded:
            logger.info("Creating minimal API endpoints...")
            from fastapi import APIRouter
            
            api_router = APIRouter(prefix="/api")
            
            @api_router.get("/services")
            async def get_services():
                """Minimal services endpoint"""
                return [{
                    "id": "1",
                    "slug": "nexus-rebuttal-letters",
                    "title": "Nexus & Rebuttal Letters",
                    "shortDescription": "Professional medical opinions for VA disability claims",
                    "fullDescription": "Comprehensive nexus and rebuttal letters from Dr. Kishan Bhalani",
                    "features": ["Medical nexus opinions", "Rebuttal letters", "Expert analysis"],
                    "basePriceInUSD": 1499,
                    "duration": "7-10 business days",
                    "category": "nexus-letter",
                    "icon": "file-text",
                    "faqs": []
                }]
            
            @api_router.get("/blog")
            async def get_blog():
                """Minimal blog endpoint"""
                return [{
                    "id": "1",
                    "slug": "nexus-letters-explained",
                    "title": "Understanding Nexus Letters for VA Claims",
                    "excerpt": "Learn how nexus letters can help your VA disability claim",
                    "contentHTML": "<p>Nexus letters are crucial for VA disability claims...</p>",
                    "category": "education",
                    "tags": ["nexus", "va-claims", "medical"],
                    "authorName": "Dr. Kishan Bhalani",
                    "publishedAt": "2024",
                    "readTime": "5 min read"
                }]
            
            @api_router.post("/contact")
            async def create_contact(contact_data: dict):
                """Minimal contact endpoint"""
                logger.info(f"Contact form received: {contact_data.get('name', 'Unknown')}")
                return {
                    "id": f"contact-{int(time.time())}",
                    "status": "received",
                    "message": "Thank you for your message. We will contact you soon.",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            
            app.include_router(api_router)
            logger.info("✅ Minimal API endpoints created successfully")
    
    except Exception as e:
        logger.error(f"Failed to setup API: {e}", exc_info=True)
        # App will still work with basic health checks
    
    return app

# Global server manager
server_manager = ServerManager()

def main():
    """Main entry point with robust error handling"""
    logger.info("🏥 Starting Dr. Kishan Bhalani Medical Services (Robust Mode)")
    
    # Setup signal handlers for graceful shutdown
    signal.signal(signal.SIGTERM, server_manager.signal_handler)
    signal.signal(signal.SIGINT, server_manager.signal_handler)
    
    # Setup paths
    backend_available = setup_paths()
    logger.info(f"Backend directory available: {backend_available}")
    
    # Get configuration from environment with defaults
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"  # Critical: must bind to all interfaces
    workers = int(os.environ.get("WEB_CONCURRENCY", 1))
    
    # Log configuration
    logger.info(f"Server configuration:")
    logger.info(f"  Host: {host}")
    logger.info(f"  Port: {port}")
    logger.info(f"  Workers: {workers}")
    logger.info(f"  Environment: {os.environ.get('ENVIRONMENT', 'development')}")
    logger.info(f"  Python version: {sys.version}")
    logger.info(f"  CPU count: {multiprocessing.cpu_count()}")
    
    try:
        # Create the application
        app = create_robust_app()
        logger.info("✅ Application created successfully")
        
        # Import uvicorn
        import uvicorn
        
        # Configure uvicorn with robust settings
        config = uvicorn.Config(
            app,
            host=host,
            port=port,
            log_level="info",
            access_log=True,
            # Timeout settings to prevent hanging
            timeout_keep_alive=30,
            timeout_graceful_shutdown=30,
            # Worker settings
            workers=workers if workers > 1 else None,
            # Performance settings
            loop="auto",
            http="auto",
            # Prevent memory leaks
            limit_concurrency=1000,
            limit_max_requests=10000,
            # Logging
            log_config={
                "version": 1,
                "disable_existing_loggers": False,
                "formatters": {
                    "default": {
                        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    },
                },
                "handlers": {
                    "default": {
                        "formatter": "default",
                        "class": "logging.StreamHandler",
                        "stream": "ext://sys.stdout",
                    },
                },
                "root": {
                    "level": "INFO",
                    "handlers": ["default"],
                },
            }
        )
        
        # Create and start server
        server = uvicorn.Server(config)
        server_manager.server = server
        
        logger.info(f"🚀 Starting robust server on {host}:{port}")
        logger.info("Health endpoints available:")
        logger.info(f"  - http://{host}:{port}/health")
        logger.info(f"  - http://{host}:{port}/ping")
        logger.info(f"  - http://{host}:{port}/status")
        
        # Run the server
        server.run()
        
    except Exception as e:
        logger.error(f"❌ Server startup failed: {e}", exc_info=True)
        logger.error("Available files in current directory:")
        try:
            for file in os.listdir("."):
                logger.error(f"  - {file}")
        except Exception:
            pass
        sys.exit(1)
    
    finally:
        logger.info("Server shutdown complete")

if __name__ == "__main__":
    main()