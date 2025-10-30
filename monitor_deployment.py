#!/usr/bin/env python3
"""
Monitor deployment status after variable update
"""

import requests
import time
import sys


def test_backend():
    """Test backend health"""
    try:
        response = requests.get('https://baseskel-production.up.railway.app/health', timeout=10)
        return response.status_code, response.text[:200]
    except Exception as e:
        return None, str(e)


def main():
    print("🔍 Monitoring Backend Deployment...")
    print("=" * 40)
    print("Waiting for Railway to redeploy with new environment variables...")
    print()
    
    max_attempts = 12  # 2 minutes
    attempt = 0
    
    while attempt < max_attempts:
        attempt += 1
        print(f"Attempt {attempt}/{max_attempts}: Testing backend...")
        
        status_code, response = test_backend()
        
        if status_code == 200:
            print("🎉 SUCCESS! Backend is now working!")
            try:
                import json
                data = json.loads(response)
                print(f"✅ Health Status: {data.get('status', 'unknown')}")
                if 'timestamp' in data:
                    print(f"✅ Server Time: {data['timestamp']}")
                if 'hipaa_compliant' in data:
                    print(f"✅ HIPAA Compliant: {data['hipaa_compliant']}")
            except:
                print(f"✅ Response: {response}")
            
            print("\n🌐 Your Backend URLs:")
            print("• Health: https://baseskel-production.up.railway.app/health")
            print("• API Health: https://baseskel-production.up.railway.app/api/health")
            print("• API Docs: https://baseskel-production.up.railway.app/docs")
            print("• Services: https://baseskel-production.up.railway.app/api/services")
            
            print("\n🎊 Backend is fully operational!")
            return True
            
        elif status_code == 400 and "Invalid host header" in response:
            print("⏳ Still getting host header error - deployment in progress...")
            
        elif status_code:
            print(f"⚠️  Status {status_code}: {response}")
            
        else:
            print(f"❌ Connection error: {response}")
        
        if attempt < max_attempts:
            print("   Waiting 10 seconds before next attempt...")
            time.sleep(10)
        print()
    
    print("⏰ Deployment is taking longer than expected.")
    print("This is normal for Railway deployments.")
    print()
    print("💡 You can:")
    print("1. Check Railway dashboard for deployment status")
    print("2. Wait a few more minutes and test manually")
    print("3. Check Railway logs for any issues")
    
    return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)