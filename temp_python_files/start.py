#!/usr/bin/env python3
"""
Startup script for Dr. Kishan Bhalani Medical Documentation Services
Works with Railway, Heroku, and other deployment platforms
"""

import sys
import os
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_python_path():
    """Setup Python path for imports"""
    # Get the directory containing this script
    root_dir = Path(__file__).parent
    backend_dir = root_dir / "backend"
    
    # Add directories to Python path
    paths_to_add = [str(root_dir), str(backend_dir)]
    
    for path in paths_to_add:
        if path not in sys.path:
            sys.path.insert(0, path)
            logger.info(f"Added to Python path: {path}")
    
    # Change working directory to backend if it exists
    if backend_dir.exists():
        os.chdir(backend_dir)
        logger.info(f"Changed working directory to: {backend_dir}")
    else:
        logger.warning(f"Backend directory not found: {backend_dir}")

def main():
    """Main startup function"""
    logger.info("🏥 Starting Dr. Kishan Bhalani Medical Documentation Services")
    
    # Setup Python path
    setup_python_path()
    
    # Get port from environment
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    
    logger.info(f"Server configuration: {host}:{port}")
    
    try:
        # Try to import the server module
        logger.info("Importing server module...")
        from server import app
        logger.info("✅ Server module imported successfully")
        
        # Start the server
        import uvicorn
        logger.info(f"🚀 Starting server on {host}:{port}")
        
        uvicorn.run(
            app,
            host=host,
            port=port,
            log_level="info",
            access_log=True
        )
        
    except ImportError as e:
        logger.error(f"❌ Failed to import server module: {e}")
        logger.info("Trying alternative import method...")
        
        try:
            # Alternative: try importing from current directory
            import server
            app = server.app
            logger.info("✅ Alternative import successful")
            
            import uvicorn
            uvicorn.run(app, host=host, port=port, log_level="info")
            
        except Exception as e2:
            logger.error(f"❌ Alternative import also failed: {e2}")
            logger.error("Available files in current directory:")
            for file in os.listdir("."):
                logger.error(f"  - {file}")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"❌ Server startup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()