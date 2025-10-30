#!/usr/bin/env python3
"""
WSGI entry point for Railway deployment
Dr. Kishan Bhalani Medical Documentation Services
"""

import sys
import os
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

# Change working directory to backend
os.chdir(backend_dir)

# Import the FastAPI app
from server import app

# WSGI application
application = app