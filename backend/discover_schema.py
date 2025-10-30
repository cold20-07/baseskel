#!/usr/bin/env python3
"""
Try to discover the actual database schema by testing different column combinations
"""

import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

# Different possible schemas to test
schema_variations = [
    # Variation 1: All camelCase (our current data)
    {
        "name": "camelCase",
        "service": {
            "id": "test-1",
            "slug": "test",
            "title": "Test",
            "shortDescription": "Test",
            "fullDescription": "Test",
            "features": ["test"],
            "basePriceInUSD": 100,
            "duration": "1 day",
            "category": "test",
            "icon": "test",
            "faqs": []
        },
        "blog": {
            "id": "test-1",
            "slug": "test",
            "title": "Test",
            "excerpt": "Test",
            "contentHTML": "Test",
            "category": "test",
            "tags": ["test"],
            "authorName": "Test",
            "publishedAt": "Test",
            "readTime": "Test"
        }
    },
    # Variation 2: All snake_case
    {
        "name": "snake_case",
        "service": {
            "id": "test-2",
            "slug": "test",
            "title": "Test",
            "short_description": "Test",
            "full_description": "Test", 
            "features": ["test"],
            "base_price_in_usd": 100,
            "duration": "1 day",
            "category": "test",
            "icon": "test",
            "faqs": []
        },
        "blog": {
            "id": "test-2",
            "slug": "test",
            "title": "Test",
            "excerpt": "Test",
            "content_html": "Test",
            "category": "test",
            "tags": ["test"],
            "author_name": "Test",
            "published_at": "Test",
            "read_time": "Test"
        }
    },
    # Variation 3: Mixed case (some common variations)
    {
        "name": "mixed",
        "service": {
            "id": "test-3",
            "slug": "test",
            "title": "Test",
            "description": "Test",  # simplified
            "price": 100,  # simplified
            "duration": "1 day",
            "category": "test",
            "icon": "test"
        },
        "blog": {
            "id": "test-3",
            "slug": "test", 
            "title": "Test",
            "content": "Test",  # simplified
            "category": "test",
            "author": "Test"  # simplified
        }
    }
]

def test_schema_variations():
    print("🔍 Discovering database schema...")
    
    for variation in schema_variations:
        print(f"\n--- Testing {variation['name']} schema ---")
        
        # Test service schema
        try:
            print(f"Testing service insert with {variation['name']}...")
            result = supabase.table('services').insert(variation['service']).execute()
            print(f"✅ SUCCESS! Services table uses {variation['name']} schema")
            print(f"Working columns: {list(variation['service'].keys())}")
            
            # Clean up
            supabase.table('services').delete().eq('id', variation['service']['id']).execute()
            
            # If service worked, test blog with same pattern
            try:
                print(f"Testing blog insert with {variation['name']}...")
                result = supabase.table('blog_posts').insert(variation['blog']).execute()
                print(f"✅ SUCCESS! Blog posts table also uses {variation['name']} schema")
                print(f"Working columns: {list(variation['blog'].keys())}")
                
                # Clean up
                supabase.table('blog_posts').delete().eq('id', variation['blog']['id']).execute()
                
                print(f"\n🎉 FOUND WORKING SCHEMA: {variation['name']}")
                return variation['name']
                
            except Exception as e:
                print(f"❌ Blog failed with {variation['name']}: {e}")
                
        except Exception as e:
            print(f"❌ Service failed with {variation['name']}: {e}")
    
    print("\n❌ No working schema found. The database might have a completely custom schema.")
    return None

if __name__ == "__main__":
    working_schema = test_schema_variations()
    if working_schema:
        print(f"\n✅ Use {working_schema} column names for your data!")
    else:
        print("\n❌ Need to check Supabase dashboard for actual table structure")