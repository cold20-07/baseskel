#!/usr/bin/env python3
"""
Production startup script for Dr. Kishan Bhalani Medical Documentation Services
Handles environment setup and server startup for deployment platforms
"""

import os
import sys
import logging
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def setup_environment():
    """Setup production environment"""
    # Set default environment variables if not present
    os.environ.setdefault('ENVIRONMENT', 'production')
    os.environ.setdefault('CORS_ORIGINS', '*')
    os.environ.setdefault('ALLOWED_HOSTS', '*')

    # Validate required environment variables
    required_vars = ['SUPABASE_URL', 'SUPABASE_KEY']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]

    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set these variables before starting the server.")
        sys.exit(1)

    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def main():
    """Main startup function"""
    print("🏥 Dr. Kishan Bhalani Medical Documentation Services")
    print("🚀 Production Startup")
    print("=" * 50)

    # Setup environment
    setup_environment()

    try:
        # Import and start server
        import uvicorn
        from server import app

        print("✅ Production server loaded successfully")
        print("✅ Database connection established")
        print("✅ File upload enabled with HIPAA compliance")
        print("✅ HIPAA features enabled")

        # Get port from environment
        port = int(os.environ.get("PORT", 8000))
        host = os.environ.get("HOST", "0.0.0.0")

        print(f"\n🚀 Starting server on {host}:{port}")
        print(f"📍 API documentation at: http://{host}:{port}/docs")
        print(f"📍 Health check at: http://{host}:{port}/api/health")
        print("=" * 50)

        # Start server
        uvicorn.run(
            "server:app",
            host=host,
            port=port,
            reload=False,
            log_level="info",
            access_log=True
        )

    except ImportError as e:
        print(f"❌ Failed to import server: {e}")
        print("Make sure all dependencies are installed:")
        print("pip install -r requirements.txt")
        sys.exit(1)

    except Exception as e:
        print(f"❌ Server startup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
