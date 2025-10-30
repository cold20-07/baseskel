#!/usr/bin/env python3
"""
Recreate tables with correct schema and seed data
"""

import os
from dotenv import load_dotenv
from supabase import create_client
from seed_data import SERVICES, BLOG_POSTS

load_dotenv()

supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

def recreate_and_seed():
    print("🔄 Recreating tables and seeding data...")
    
    # First, let's try to drop and recreate the tables using SQL
    # Note: This requires service role permissions
    
    drop_and_create_sql = """
    -- Drop existing tables if they exist
    DROP TABLE IF EXISTS services CASCADE;
    DROP TABLE IF EXISTS blog_posts CASCADE;
    DROP TABLE IF EXISTS contacts CASCADE;
    
    -- Create services table with correct schema
    CREATE TABLE services (
        id TEXT PRIMARY KEY,
        slug TEXT UNIQUE NOT NULL,
        title TEXT NOT NULL,
        "shortDescription" TEXT NOT NULL,
        "fullDescription" TEXT NOT NULL,
        features JSONB NOT NULL DEFAULT '[]',
        "basePriceInUSD" INTEGER NOT NULL,
        duration TEXT NOT NULL,
        category TEXT NOT NULL,
        icon TEXT NOT NULL,
        faqs JSONB NOT NULL DEFAULT '[]',
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    
    -- Create blog_posts table with correct schema
    CREATE TABLE blog_posts (
        id TEXT PRIMARY KEY,
        slug TEXT UNIQUE NOT NULL,
        title TEXT NOT NULL,
        excerpt TEXT NOT NULL,
        "contentHTML" TEXT NOT NULL,
        category TEXT NOT NULL,
        tags JSONB NOT NULL DEFAULT '[]',
        "authorName" TEXT NOT NULL,
        "publishedAt" TEXT NOT NULL,
        "readTime" TEXT NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    
    -- Create contacts table
    CREATE TABLE contacts (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT,
        subject TEXT NOT NULL,
        message TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'new',
        "createdAt" TEXT NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    
    -- Create indexes
    CREATE INDEX idx_services_slug ON services(slug);
    CREATE INDEX idx_services_category ON services(category);
    CREATE INDEX idx_blog_posts_slug ON blog_posts(slug);
    CREATE INDEX idx_blog_posts_category ON blog_posts(category);
    CREATE INDEX idx_contacts_status ON contacts(status);
    
    -- Enable RLS
    ALTER TABLE services ENABLE ROW LEVEL SECURITY;
    ALTER TABLE blog_posts ENABLE ROW LEVEL SECURITY;
    ALTER TABLE contacts ENABLE ROW LEVEL SECURITY;
    
    -- Create policies for public access
    CREATE POLICY "Allow public read access to services" ON services
        FOR SELECT USING (true);
    
    CREATE POLICY "Allow public read access to blog posts" ON blog_posts
        FOR SELECT USING (true);
    
    CREATE POLICY "Allow public insert access to contacts" ON contacts
        FOR INSERT WITH CHECK (true);
    
    -- Allow all operations for authenticated users (for seeding)
    CREATE POLICY "Allow all operations for authenticated users on services" ON services
        FOR ALL USING (true);
    
    CREATE POLICY "Allow all operations for authenticated users on blog_posts" ON blog_posts
        FOR ALL USING (true);
    """
    
    try:
        print("Executing SQL to recreate tables...")
        # Note: This might not work with anon key, but let's try
        result = supabase.rpc('exec_sql', {'sql': drop_and_create_sql}).execute()
        print("✅ Tables recreated successfully")
    except Exception as e:
        print(f"❌ Could not recreate tables via SQL: {e}")
        print("This requires service role permissions or manual execution in Supabase dashboard")
        return False
    
    # Now try to seed the data
    try:
        print("Seeding services...")
        for service in SERVICES:
            result = supabase.table('services').insert(service).execute()
            print(f"✅ Inserted: {service['title']}")
        
        print("Seeding blog posts...")
        for post in BLOG_POSTS:
            result = supabase.table('blog_posts').insert(post).execute()
            print(f"✅ Inserted: {post['title']}")
        
        print("🎉 Database seeded successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Seeding failed: {e}")
        return False

if __name__ == "__main__":
    success = recreate_and_seed()
    if not success:
        print("\n📋 Manual steps required:")
        print("1. Go to your Supabase dashboard")
        print("2. Go to SQL Editor")
        print("3. Run the SQL from supabase_schema.sql")
        print("4. Then run this script again to seed data")