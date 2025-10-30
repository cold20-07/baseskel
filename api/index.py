#!/usr/bin/env python3
"""
Vercel API handler for Military Disability Nexus Medical Documentation Services
"""

import sys
import os

# Add the backend directory to the Python path
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.insert(0, backend_path)

# Import the FastAPI app from the backend
from server import app

# Export the app for Vercel
app = app