#!/usr/bin/env python3
"""
Supabase Setup Script for Dr. Kishan Bhalani Medical Documentation Services
This script helps set up Supabase or provides instructions for manual setup
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def check_supabase_config():
    """Check if Supabase is properly configured"""
    load_dotenv()

    supabase_url = os.environ.get('SUPABASE_URL', '')
    supabase_key = os.environ.get('SUPABASE_KEY', '')

    print("🔍 Checking Supabase Configuration...")
    print("=" * 50)

    if not supabase_url or supabase_url == 'your_supabase_project_url':
        print("❌ SUPABASE_URL not configured")
        return False

    if not supabase_key or supabase_key == 'your_supabase_anon_key':
        print("❌ SUPABASE_KEY not configured")
        return False

    print(f"✅ SUPABASE_URL: {supabase_url[:30]}...")
    print(f"✅ SUPABASE_KEY: {supabase_key[:30]}...")

    return True

def create_demo_supabase_config():
    """Create a demo Supabase configuration for testing"""
    print("\n🛠️  Creating Demo Supabase Configuration...")
    print("=" * 50)

    # For demo purposes, we'll create a mock Supabase setup
    demo_config = """
# Demo Supabase Configuration
# Replace these with your actual Supabase project credentials

SUPABASE_URL=https://demo-project.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.demo-key-for-testing
CORS_ORIGINS=http://localhost:3000,*
HIPAA_ENCRYPTION_KEY=demo-encryption-key-change-in-production
ENVIRONMENT=development
ALLOWED_HOSTS=localhost,yourdomain.com
"""

    env_file = Path('.env')

    # Backup existing .env if it exists
    if env_file.exists():
        backup_file = Path('.env.backup')
        env_file.rename(backup_file)
        print(f"📁 Backed up existing .env to {backup_file}")

    # Write new demo config
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(demo_config.strip())

    print("✅ Created demo .env configuration")
    print("⚠️  This is for TESTING ONLY - replace with real Supabase credentials for production")

    return True

def setup_mock_supabase():
    """Set up a mock Supabase client for testing"""
    print("\n🎭 Setting up Mock Supabase Client...")
    print("=" * 50)

    mock_supabase_code = '''"""
Mock Supabase Client for Testing
This provides a fake Supabase interface for development without a real database
"""

class MockSupabaseResponse:
    def __init__(self, data):
        self.data = data

class MockSupabaseTable:
    def __init__(self, table_name, mock_data):
        self.table_name = table_name
        self.mock_data = mock_data

    def select(self, columns='*'):
        return self

    def eq(self, column, value):
        if self.table_name == 'services':
            filtered = [item for item in self.mock_data if item.get(column) == value]
            return MockSupabaseResponse(filtered)
        return MockSupabaseResponse([])

    def execute(self):
        return MockSupabaseResponse(self.mock_data)

    def insert(self, data):
        return MockSupabaseResponse([data] if isinstance(data, dict) else data)

    def update(self, data):
        return MockSupabaseResponse([data])

    def delete(self):
        return MockSupabaseResponse([])

class MockSupabaseClient:
    def __init__(self):
        # Mock services data
        self.services_data = [
            {
                "id": "1",
                "slug": "nexus-rebuttal-letters",
                "title": "Nexus & Rebuttal Letters",
                "shortDescription": "Comprehensive medical opinions for claims and appeals",
                "fullDescription": "Professional nexus and rebuttal letters that establish clear connections between your military service and medical conditions.",
                "features": ["Nexus opinion letters", "Rebuttal to VA denials", "Up to 4 claims per letter", "Clear medical rationale", "Rush service: +$500 USD (36-48 hours)"],
                "basePriceInUSD": 1499,
                "duration": "7-10 business days",
                "category": "nexus-letter",
                "icon": "file-text",
                "faqs": [{"question": "What is a nexus letter?", "answer": "A nexus letter establishes the connection between military service and a medical condition."}]
            }
            # Add more services as needed
        ]

        self.blog_data = [
            {
                "id": "1",
                "slug": "nexus-and-rebuttal-letters-explained",
                "title": "Nexus and Rebuttal Letters: Your Key to VA Claim Success",
                "excerpt": "Understanding the difference between nexus and rebuttal letters.",
                "contentHTML": "<h2>Understanding Nexus and Rebuttal Letters</h2><p>Both are crucial medical documents.</p>",
                "category": "nexus-letters",
                "tags": ["nexus", "rebuttal"],
                "authorName": "Dr. Kishan Bhalani",
                "publishedAt": "SEPT 2025",
                "readTime": "6 min read"
            }
        ]

    def table(self, table_name):
        if table_name == 'services':
            return MockSupabaseTable(table_name, self.services_data)
        elif table_name == 'blog_posts':
            return MockSupabaseTable(table_name, self.blog_data)
        elif table_name == 'contacts':
            return MockSupabaseTable(table_name, [])
        else:
            return MockSupabaseTable(table_name, [])

    def rpc(self, function_name, params=None):
        return MockSupabaseResponse([])

def create_client(url, key):
    """Mock create_client function"""
    print(f"🎭 Creating mock Supabase client for {url}")
    return MockSupabaseClient()
'''

    mock_file = Path('mock_supabase.py')
    with open(mock_file, 'w', encoding='utf-8') as f:
        f.write(mock_supabase_code)

    print(f"✅ Created {mock_file}")
    print("✅ Mock Supabase client ready for testing")

    return True

def provide_real_supabase_instructions():
    """Provide instructions for setting up real Supabase"""
    print("\n📋 Real Supabase Setup Instructions")
    print("=" * 50)

    instructions = """
To set up a real Supabase project:

1. 🌐 Go to https://supabase.com and create an account
2. 🆕 Create a new project:
   - Project name: dr-kishan-bhalani-services
   - Database password: (choose a strong password)
   - Region: (closest to your users)

3. 📊 Set up the database:
   - Go to SQL Editor in your Supabase dashboard
   - Run the schema from: backend/supabase_schema.sql
   - Run the HIPAA schema from: backend/hipaa_schema.sql
   - Run the file upload schema from: backend/file_upload_schema.sql

4. 🔑 Get your credentials:
   - Go to Settings > API
   - Copy your Project URL
   - Copy your anon/public key

5. ⚙️  Update your .env file:
   SUPABASE_URL=https://your-project-id.supabase.co
   SUPABASE_KEY=your-anon-key-here

6. 🌱 Seed the database:
   python seed_data.py

7. ✅ Test the connection:
   python -c "from supabase import create_client; print('Supabase connected!')"
"""

    print(instructions)

    # Also save instructions to file
    with open('SUPABASE_SETUP_INSTRUCTIONS.md', 'w', encoding='utf-8') as f:
        f.write("# Supabase Setup Instructions\n\n" + instructions)

    print("📄 Instructions saved to SUPABASE_SETUP_INSTRUCTIONS.md")

def main():
    print("🏥 Dr. Kishan Bhalani - Supabase Setup")
    print("=" * 50)

    if check_supabase_config():
        print("\n✅ Supabase is already configured!")

        # Test the connection
        try:
            from supabase import create_client
            import os

            supabase_url = os.environ.get('SUPABASE_URL')
            supabase_key = os.environ.get('SUPABASE_KEY')

            if 'demo-project' in supabase_url:
                print("⚠️  Using demo configuration - not a real Supabase instance")
            else:
                client = create_client(supabase_url, supabase_key)
                print("✅ Supabase connection test successful!")

        except Exception as e:
            print(f"⚠️  Supabase connection test failed: {e}")

    else:
        print("\n❌ Supabase not configured")

        choice = input("\nChoose setup option:\n1. Create demo config (for testing)\n2. Show real Supabase setup instructions\n3. Exit\n\nEnter choice (1-3): ")

        if choice == '1':
            create_demo_supabase_config()
            setup_mock_supabase()
            print("\n🎉 Demo setup complete! Restart your server to use the new configuration.")

        elif choice == '2':
            provide_real_supabase_instructions()

        else:
            print("👋 Exiting setup")
            sys.exit(0)

if __name__ == "__main__":
    main()
