#!/usr/bin/env python3
"""
Main entry point for Railway deployment
Dr. Kishan Bhalani Medical Documentation Services
"""

import sys
import os
from pathlib import Path

# Add backend directory to Python path for Railway deployment
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

# Change working directory to backend
os.chdir(backend_dir)

# Import the FastAPI app from server module
from server import app

# This is the ASGI application that Railway will use
# Railway looks for 'app' variable in the main module
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)