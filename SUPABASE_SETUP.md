# Supabase Setup Guide

This guide will help you set up Supabase as the database for the Dr. Kishan Bhalani Medical Documentation Services application.

## Step 1: Create a Supabase Project

1. Go to [supabase.com](https://supabase.com) and sign up/login
2. Click "New Project"
3. Choose your organization
4. Enter project details:
   - Name: `dr-kishan-bhalani-services`
   - Database Password: (generate a strong password)
   - Region: Choose closest to your users
5. Click "Create new project"

## Step 2: Set Up Database Schema

1. Wait for your project to be ready (usually 1-2 minutes)
2. Go to the "SQL Editor" in the left sidebar
3. Copy the contents of `backend/supabase_schema.sql`
4. Paste it into the SQL editor
5. Click "Run" to execute the schema

This will create three tables:
- `services` - For service offerings
- `blog_posts` - For blog content
- `contacts` - For contact form submissions

## Step 3: Get Your API Credentials

1. Go to "Settings" > "API" in the left sidebar
2. Copy the following values:
   - **Project URL** (looks like: `https://xxxxx.supabase.co`)
   - **Anon public key** (starts with `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`)

## Step 4: Update Environment Variables

Update your `backend/.env` file:

```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-key-here
CORS_ORIGINS=*
```

## Step 5: Seed the Database

Run the seeding script to populate your database with sample data:

```bash
cd backend
python seed_data.py
```

## Step 6: Verify Setup

You can verify your setup by:

1. Going to "Table Editor" in Supabase dashboard
2. Check that you have data in `services` and `blog_posts` tables
3. Test the API endpoints:
   ```bash
   curl http://localhost:8000/api/services
   ```

## Row Level Security (RLS)

The schema automatically sets up Row Level Security with these policies:
- **Services & Blog Posts**: Public read access (anyone can view)
- **Contacts**: Public insert access (anyone can submit contact forms)

For production, you may want to add authentication and admin-only policies for managing content.

## Optional: Supabase Dashboard Features

Your Supabase project also includes:
- **Authentication** (if you want to add user login later)
- **Storage** (for file uploads)
- **Edge Functions** (for serverless functions)
- **Real-time subscriptions** (for live updates)

These features are not used in the current MVP but can be added later.

## Troubleshooting

### Common Issues:

1. **"relation does not exist" error**: Make sure you ran the SQL schema
2. **"Invalid API key" error**: Check your SUPABASE_KEY in .env
3. **CORS errors**: Make sure CORS_ORIGINS is set correctly
4. **Connection timeout**: Check your SUPABASE_URL is correct

### Getting Help:

- [Supabase Documentation](https://supabase.com/docs)
- [Supabase Discord Community](https://discord.supabase.com)
- Check the browser console and server logs for detailed error messages