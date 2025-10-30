#!/usr/bin/env python3
"""
Check the actual database schema
"""

import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

# Try different column name variations
test_variations = [
    {
        "id": "test-1",
        "slug": "test-service", 
        "title": "Test Service",
        "short_description": "Test description",  # snake_case
        "full_description": "Test full description",
        "features": ["Test feature"],
        "base_price_in_usd": 100,  # snake_case
        "duration": "1 day",
        "category": "test",
        "icon": "test",
        "faqs": []
    },
    {
        "id": "test-2",
        "slug": "test-service-2",
        "title": "Test Service 2", 
        "shortdescription": "Test description",  # no underscore
        "fulldescription": "Test full description",
        "features": ["Test feature"],
        "basepriceinusd": 100,  # no underscore
        "duration": "1 day",
        "category": "test",
        "icon": "test",
        "faqs": []
    }
]

for i, test_service in enumerate(test_variations):
    try:
        print(f"Attempting variation {i+1}...")
        result = supabase.table('services').insert(test_service).execute()
        print(f"✅ Success with variation {i+1}! Schema uses these column names:")
        for key in test_service.keys():
            print(f"  - {key}")
        
        # Clean up
        supabase.table('services').delete().eq('id', test_service['id']).execute()
        break
        
    except Exception as e:
        print(f"❌ Variation {i+1} failed: {e}")
        continue

print("\nIf all variations failed, the table might not exist or have a completely different schema.")