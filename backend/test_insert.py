#!/usr/bin/env python3
"""
Test script to check database schema and insert a single service
"""

import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

# Test service data with minimal fields first
test_service = {
    "id": "test-1",
    "slug": "test-service",
    "title": "Test Service",
    "shortDescription": "Test description",
    "fullDescription": "Test full description",
    "features": ["Test feature"],
    "basePriceInUSD": 100,
    "duration": "1 day",
    "category": "test",
    "icon": "test",
    "faqs": []
}

try:
    print("Attempting to insert test service...")
    result = supabase.table('services').insert(test_service).execute()
    print(f"✅ Success! Inserted: {result.data}")
    
    # Clean up - delete the test service
    supabase.table('services').delete().eq('id', 'test-1').execute()
    print("✅ Test service cleaned up")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("This will help us understand the schema mismatch")