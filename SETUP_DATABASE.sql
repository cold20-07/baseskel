-- Supabase SQL Schema for Dr. Kishan Bhalani Medical Documentation Services
-- Copy and paste this entire script into your Supabase SQL Editor and run it

-- Services table
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

-- Blog posts table
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

-- Contacts table
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

-- Create indexes for better performance
CREATE INDEX idx_services_slug ON services(slug);
CREATE INDEX idx_services_category ON services(category);
CREATE INDEX idx_blog_posts_slug ON blog_posts(slug);
CREATE INDEX idx_blog_posts_category ON blog_posts(category);
CREATE INDEX idx_contacts_status ON contacts(status);
CREATE INDEX idx_contacts_created_at ON contacts(created_at);

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

-- Create policies for data seeding (temporary - you can remove these later)
CREATE POLICY "Allow insert for seeding services" ON services
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Allow insert for seeding blog_posts" ON blog_posts
    FOR INSERT WITH CHECK (true);

-- Grant necessary permissions
GRANT ALL ON services TO anon;
GRANT ALL ON blog_posts TO anon;
GRANT ALL ON contacts TO anon;