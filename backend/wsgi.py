#!/usr/bin/env python3
"""
WSGI entry point for Dr. Kishan Bhalani Medical Documentation Services
Compatible with Gunicorn and other WSGI servers
"""

import os
import sys
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Import the FastAPI app
try:
    from server import app
    print("✅ Main server loaded successfully")
except ImportError:
    try:
        from server_simple import app
        print("✅ Simplified server loaded successfully")
    except ImportError as e:
        print(f"❌ Failed to import server: {e}")
        raise

# Export for WSGI servers
application = app

# For compatibility with different deployment platforms
def create_app():
    return app