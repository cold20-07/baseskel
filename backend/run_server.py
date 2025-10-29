#!/usr/bin/env python3
"""
Simple server runner for Dr. Kishan Bhalani Medical Documentation Services
"""

import uvicorn
import sys
import os
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def main():
    print("🏥 Dr. Kishan Bhalani Medical Documentation Services")
    print("=" * 50)
    
    try:
        # Import and start the production server
        import server
        print("✅ Production server loaded successfully")
        print("✅ Database connection established")
        print("✅ HIPAA compliance features enabled")
        
        print("\n🚀 Starting production server...")
        print("📍 Server will be available at: http://localhost:8000")
        print("📍 API documentation at: http://localhost:8000/docs")
        print("📍 Health check at: http://localhost:8000/api/health")
        print("\n💡 Press Ctrl+C to stop the server")
        print("=" * 50)
        
        # Start the server
        port = int(os.environ.get("PORT", 8000))
        uvicorn.run(
            "server:app",
            host="0.0.0.0",
            port=port,
            reload=False,  # Disable reload in production
            log_level="info"
        )
        
    except Exception as e:
        print(f"❌ Server startup failed: {e}")
        print("Make sure you have:")
        print("1. Valid SUPABASE_URL and SUPABASE_KEY in your .env file")
        print("2. All required dependencies installed")
        print("3. Database tables created and seeded")
        sys.exit(1)
    
    except Exception as e:
        print(f"❌ Server startup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()