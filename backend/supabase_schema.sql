-- Supabase SQL Schema for Dr. Kishan Bhalani Medical Documentation Services
-- Run this in your Supabase SQL editor to create the required tables

-- Services table
CREATE TABLE IF NOT EXISTS services (
    id TEXT PRIMARY KEY,
    slug TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    shortDescription TEXT NOT NULL,
    fullDescription TEXT NOT NULL,
    features JSONB NOT NULL DEFAULT '[]',
    basePriceInINR INTEGER NOT NULL,
    duration TEXT NOT NULL,
    category TEXT NOT NULL,
    icon TEXT NOT NULL,
    faqs JSONB NOT NULL DEFAULT '[]',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Blog posts table
CREATE TABLE IF NOT EXISTS blog_posts (
    id TEXT PRIMARY KEY,
    slug TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    excerpt TEXT NOT NULL,
    contentHTML TEXT NOT NULL,
    category TEXT NOT NULL,
    tags JSONB NOT NULL DEFAULT '[]',
    authorName TEXT NOT NULL,
    publishedAt TEXT NOT NULL,
    readTime TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Contacts table
CREATE TABLE IF NOT EXISTS contacts (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT,
    subject TEXT NOT NULL,
    message TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'new',
    createdAt TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_services_slug ON services(slug);
CREATE INDEX IF NOT EXISTS idx_services_category ON services(category);
CREATE INDEX IF NOT EXISTS idx_blog_posts_slug ON blog_posts(slug);
CREATE INDEX IF NOT EXISTS idx_blog_posts_category ON blog_posts(category);
CREATE INDEX IF NOT EXISTS idx_contacts_status ON contacts(status);
CREATE INDEX IF NOT EXISTS idx_contacts_created_at ON contacts(created_at);

-- Enable Row Level Security (RLS)
ALTER TABLE services ENABLE ROW LEVEL SECURITY;
ALTER TABLE blog_posts ENABLE ROW LEVEL SECURITY;
ALTER TABLE contacts ENABLE ROW LEVEL SECURITY;

-- Create policies for public read access to services and blog posts
CREATE POLICY "Allow public read access to services" ON services
    FOR SELECT USING (true);

CREATE POLICY "Allow public read access to blog posts" ON blog_posts
    FOR SELECT USING (true);

-- Create policy for public insert access to contacts
CREATE POLICY "Allow public insert access to contacts" ON contacts
    FOR INSERT WITH CHECK (true);

-- Optional: Create policies for authenticated users to manage data
-- Uncomment these if you want to add admin functionality later
-- CREATE POLICY "Allow authenticated users to manage services" ON services
--     FOR ALL USING (auth.role() = 'authenticated');

-- CREATE POLICY "Allow authenticated users to manage blog posts" ON blog_posts
--     FOR ALL USING (auth.role() = 'authenticated');

-- CREATE POLICY "Allow authenticated users to manage contacts" ON contacts
--     FOR ALL USING (auth.role() = 'authenticated');