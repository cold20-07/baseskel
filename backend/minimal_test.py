#!/usr/bin/env python3
"""
Try to insert with minimal data to see what columns exist
"""

import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

# Try with just the most basic columns
minimal_service = {
    "id": "test-minimal",
    "title": "Test"
}

try:
    print("Attempting minimal insert...")
    result = supabase.table('services').insert(minimal_service).execute()
    print(f"✅ Success! Basic schema works: {result.data}")
    
    # Clean up
    supabase.table('services').delete().eq('id', 'test-minimal').execute()
    
except Exception as e:
    print(f"❌ Even minimal insert failed: {e}")
    print("The table might not exist or have a completely different structure")
    
    # Let's try to see if we can query the table structure
    try:
        print("\nTrying to query existing data...")
        result = supabase.table('services').select('*').limit(1).execute()
        print(f"Query successful, but no data: {result.data}")
    except Exception as e2:
        print(f"Query also failed: {e2}")