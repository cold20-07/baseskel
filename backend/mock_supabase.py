"""
Production Supabase Client - No Mock Data
This module ensures only real Supabase connections are used in production
"""

def create_client(url, key):
    """Production create_client function that only works with real Supabase"""
    if not url or not key:
        raise ValueError("Supabase URL and key are required for production")

    if 'demo-project' in url or 'placeholder' in url or 'your-project' in url:
        raise ValueError("Production requires a real Supabase project URL, not a placeholder")

    # Only use real Supabase
    from supabase import create_client as real_create_client
    return real_create_client(url, key)
