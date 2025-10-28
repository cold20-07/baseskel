# MongoDB to Supabase Migration Guide

This guide explains the changes made to migrate from MongoDB to Supabase for Dr. Kishan Bhalani Medical Documentation Services.

## What Changed

### 1. Database Technology
- **Before**: MongoDB (NoSQL document database)
- **After**: Supabase (PostgreSQL with REST API)

### 2. Python Dependencies
- **Removed**: `pymongo`, `motor` (MongoDB drivers)
- **Added**: `supabase`, `postgrest` (Supabase client)

### 3. Environment Variables
- **Before**: `MONGO_URL`, `DB_NAME`
- **After**: `SUPABASE_URL`, `SUPABASE_KEY`

### 4. Database Schema
- **Before**: Flexible JSON documents in collections
- **After**: Structured tables with defined columns and types

## File Changes

### `backend/requirements.txt`
```diff
- pymongo==4.5.0
- motor==3.3.1
+ supabase>=2.3.4
+ postgrest>=0.16.0
```

### `backend/.env`
```diff
- MONGO_URL="mongodb://localhost:27017"
- DB_NAME="test_database"
+ SUPABASE_URL="your_supabase_project_url"
+ SUPABASE_KEY="your_supabase_anon_key"
```

### `backend/server.py`
- Replaced MongoDB async client with Supabase client
- Updated all database queries to use Supabase table operations
- Changed search queries to use PostgreSQL `ilike` instead of MongoDB regex
- Removed database connection cleanup (not needed with Supabase)

### `backend/seed_data.py`
- Replaced MongoDB operations with Supabase table operations
- Removed async/await (Supabase client is synchronous)
- Updated error handling for Supabase operations

## New Files Added

1. **`backend/supabase_schema.sql`** - SQL schema for creating tables
2. **`SUPABASE_SETUP.md`** - Detailed setup instructions
3. **`MIGRATION_GUIDE.md`** - This migration guide

## API Behavior Changes

The API endpoints remain the same, but there are some subtle differences:

### Search Functionality
- **Before**: MongoDB regex search (`$regex`)
- **After**: PostgreSQL case-insensitive search (`ilike`)

### Data Types
- **Before**: Flexible JSON documents
- **After**: Structured data with JSONB for arrays (features, tags, faqs)

### Error Handling
- **Before**: MongoDB-specific errors
- **After**: Supabase/PostgreSQL errors with better HTTP status codes

## Benefits of Supabase

1. **Built-in REST API**: No need to write custom database queries
2. **Real-time capabilities**: Built-in subscriptions for live updates
3. **Authentication**: Ready-to-use auth system
4. **Dashboard**: Visual interface for data management
5. **Row Level Security**: Built-in security policies
6. **Automatic API documentation**: Generated OpenAPI specs
7. **Better performance**: PostgreSQL is optimized for relational queries

## Migration Steps

If you're migrating existing data:

1. Export data from MongoDB
2. Set up Supabase project and run schema
3. Transform data format if needed (especially for nested objects)
4. Import data using the seed script or Supabase dashboard
5. Update environment variables
6. Test all API endpoints

## Rollback Plan

If you need to rollback to MongoDB:

1. Keep the old `requirements.txt` and `server.py` files
2. Restore MongoDB connection settings
3. Re-import data to MongoDB
4. Update environment variables back to MongoDB settings

## Testing

After migration, test these key areas:

1. **Services API**: GET `/api/services` and `/api/services/{slug}`
2. **Blog API**: GET `/api/blog` with search and category filters
3. **Contact API**: POST `/api/contact` with form data
4. **Search functionality**: Test blog search with various queries
5. **Error handling**: Test with invalid slugs and malformed requests

## Performance Considerations

- Supabase has built-in connection pooling
- PostgreSQL indexes are created for frequently queried columns
- JSONB fields (features, tags, faqs) are efficiently stored and queryable
- Row Level Security policies are optimized for public read access

## Future Enhancements

With Supabase, you can easily add:

- User authentication and authorization
- Real-time updates for admin dashboard
- File storage for document uploads
- Edge functions for custom business logic
- Advanced search with full-text search capabilities