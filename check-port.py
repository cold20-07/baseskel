#!/usr/bin/env python3
"""
Port diagnostic script for Dr. Kishan Bhalani Medical Documentation Services
Helps debug port configuration issues
"""

import os
import requests
import sys
from datetime import datetime

def check_port(port):
    """Check if the service is running on a specific port"""
    try:
        response = requests.get(f"http://localhost:{port}/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return True, data
        else:
            return False, f"HTTP {response.status_code}"
    except requests.exceptions.ConnectionError:
        return False, "Connection refused"
    except requests.exceptions.Timeout:
        return False, "Timeout"
    except Exception as e:
        return False, str(e)

def main():
    print("🔍 Dr. Kishan Bhalani Medical Services - Port Diagnostic")
    print("=" * 60)
    print(f"⏰ Timestamp: {datetime.now().isoformat()}")
    
    # Check environment variables
    print("\n📋 Environment Variables:")
    port_env = os.environ.get('PORT', 'Not set')
    print(f"   PORT: {port_env}")
    print(f"   SUPABASE_URL: {'Set' if os.environ.get('SUPABASE_URL') else 'Not set'}")
    print(f"   SUPABASE_KEY: {'Set' if os.environ.get('SUPABASE_KEY') else 'Not set'}")
    
    # Common ports to check
    ports_to_check = [8000, 8080, 3000, 5000]
    
    print(f"\n🔍 Checking common ports...")
    
    found_service = False
    for port in ports_to_check:
        print(f"   Port {port}: ", end="")
        is_running, result = check_port(port)
        
        if is_running:
            print(f"✅ RUNNING - {result.get('status', 'Unknown')}")
            print(f"      🌐 Service URL: http://localhost:{port}")
            print(f"      🏥 Health check: http://localhost:{port}/api/health")
            print(f"      📋 Services API: http://localhost:{port}/api/services")
            found_service = True
        else:
            print(f"❌ {result}")
    
    if not found_service:
        print(f"\n⚠️  No service found on common ports")
        print(f"   Make sure the server is running with:")
        print(f"   python backend/run_server.py")
        print(f"   or")
        print(f"   docker run -p 8000:8000 dr-kishan-medical-services")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()