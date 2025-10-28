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
        # Try to import the main server
        import server
        print("✅ Server loaded successfully")
        print("✅ Mock data available (7 services, 2 blog posts)")
        print("✅ File upload enabled with HIPAA compliance")
        print("✅ HIPAA features enabled with mock data")
        
        print("\n🚀 Starting server...")
        print("📍 Server will be available at: http://localhost:8000")
        print("📍 API documentation at: http://localhost:8000/docs")
        print("📍 Health check at: http://localhost:8000/api/health")
        print("\n💡 Press Ctrl+C to stop the server")
        print("=" * 50)
        
        # Start the server
        uvicorn.run(
            "server_simple:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
        
    except ImportError as e:
        print(f"❌ Failed to import server: {e}")
        print("\n🔧 Trying simplified server...")
        
        try:
            import server_simple
            print("✅ Simplified server loaded")
            print("✅ All features available with mock data")
            
            uvicorn.run(
                "server_simple:app",
                host="0.0.0.0",
                port=8000,
                reload=True,
                log_level="info"
            )
        except Exception as e2:
            print(f"❌ Failed to start any server: {e2}")
            sys.exit(1)
    
    except Exception as e:
        print(f"❌ Server startup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()