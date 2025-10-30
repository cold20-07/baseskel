#!/usr/bin/env python3
"""
Seed database with RLS-compatible approach
This script temporarily disables RLS or uses service role for seeding
"""

import os
from dotenv import load_dotenv
from supabase import create_client
from seed_data import SERVICES, BLOG_POSTS

load_dotenv()

# For seeding, we need to use the service role key (not anon key)
# The service role key bypasses RLS
supabase_url = os.environ['SUPABASE_URL']

# Try to use service role key if available, otherwise use anon key
service_key = os.environ.get('SUPABASE_SERVICE_KEY')
anon_key = os.environ.get('SUPABASE_KEY')

if service_key:
    print("Using service role key for seeding...")
    supabase = create_client(supabase_url, service_key)
else:
    print("Service role key not found, using anon key...")
    print("Note: This might fail due to RLS policies")
    supabase = create_client(supabase_url, anon_key)

def seed_database():
    print("Starting database seeding...")
    
    try:
        # First, let's try to clear existing data (if we have permission)
        try:
            print("Attempting to clear existing data...")
            supabase.table('services').delete().neq('id', '').execute()
            supabase.table('blog_posts').delete().neq('id', '').execute()
            print("✅ Cleared existing data")
        except Exception as e:
            print(f"⚠️ Could not clear existing data: {e}")
            print("Continuing with insert...")
        
        # Insert services one by one to see which ones fail
        print(f"Inserting {len(SERVICES)} services...")
        successful_services = 0
        for service in SERVICES:
            try:
                result = supabase.table('services').insert(service).execute()
                successful_services += 1
                print(f"✅ Inserted service: {service['title']}")
            except Exception as e:
                print(f"❌ Failed to insert service '{service['title']}': {e}")
        
        # Insert blog posts
        print(f"Inserting {len(BLOG_POSTS)} blog posts...")
        successful_posts = 0
        for post in BLOG_POSTS:
            try:
                result = supabase.table('blog_posts').insert(post).execute()
                successful_posts += 1
                print(f"✅ Inserted blog post: {post['title']}")
            except Exception as e:
                print(f"❌ Failed to insert blog post '{post['title']}': {e}")
        
        print(f"\n📊 Seeding Summary:")
        print(f"Services: {successful_services}/{len(SERVICES)} successful")
        print(f"Blog posts: {successful_posts}/{len(BLOG_POSTS)} successful")
        
        if successful_services == 0 and successful_posts == 0:
            print("\n❌ No data was inserted. This is likely due to:")
            print("1. Row Level Security (RLS) policies blocking inserts")
            print("2. Missing service role key")
            print("3. Schema mismatch")
            print("\nSolutions:")
            print("1. Add SUPABASE_SERVICE_KEY to your .env file")
            print("2. Or temporarily disable RLS in Supabase dashboard")
            print("3. Or create proper RLS policies for data insertion")
        
    except Exception as e:
        print(f"❌ Database seeding failed: {e}")

if __name__ == "__main__":
    seed_database()