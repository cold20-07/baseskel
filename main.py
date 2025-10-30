#!/usr/bin/env python3
"""
Railway entry point - uses simplified server for reliable deployment
"""

import os

# Set environment variables for production
os.environ.setdefault('ENVIRONMENT', 'production')
os.environ.setdefault('CORS_ORIGINS', '*')
os.environ.setdefault('ALLOWED_HOSTS', '*')

if __name__ == "__main__":
    # Use the simplified railway server
    exec(open('railway_server.py').read())