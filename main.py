#!/usr/bin/env python3
"""
Railway entry point for Dr. Kishan Bhalani Medical Documentation Services
This file helps Railway detect this as a Python project and start correctly.
"""

import sys
import os
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

# Change to backend directory
os.chdir(backend_dir)

# Import and run the server
if __name__ == "__main__":
    try:
        from run_server import main
        main()
    except ImportError:
        # Fallback to direct server import
        import uvicorn
        import server
        
        port = int(os.environ.get("PORT", 8000))
        uvicorn.run(
            "server:app",
            host="0.0.0.0",
            port=port,
            reload=False
        )