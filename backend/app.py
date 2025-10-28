#!/usr/bin/env python3
"""
Production entry point for Dr. Kishan Bhalani Medical Documentation Services
This file is used by hosting platforms like Railway, Render, etc.
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

# Export the app for WSGI/ASGI servers
application = app

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)