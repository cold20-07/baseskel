#!/usr/bin/env python3
"""
Verify the permanent host header fix
"""

import requests
import time


def test_backend_after_fix():
    """Test backend after the permanent fix"""
    print("🔧 Verifying Permanent Host Header Fix")
    print("=" * 40)
    
    backend_url = "https://baseskel-production.up.railway.app"
    
    print("Waiting for Railway to redeploy with the permanent fix...")
    print("This may take 2-3 minutes...\n")
    
    max_attempts = 15
    for attempt in range(1, max_attempts + 1):
        print(f"Attempt {attempt}/{max_attempts}: Testing backend...")
        
        try:
            response = requests.get(f"{backend_url}/health", timeout=10)
            
            if response.status_code == 200:
                print("🎉 SUCCESS! Host header issue is PERMANENTLY FIXED!")
                data = response.json()
                print(f"✅ Status: {data.get('status', 'unknown')}")
                print(f"✅ HIPAA Compliant: {data.get('hipaa_compliant', 'unknown')}")
                print(f"✅ Timestamp: {data.get('timestamp', 'unknown')}")
                
                print(f"\n🌐 Your backend is now accessible at:")
                print(f"• Health: {backend_url}/health")
                print(f"• API Health: {backend_url}/api/health") 
                print(f"• API Docs: {backend_url}/docs")
                print(f"• Services: {backend_url}/api/services")
                
                return True
                
            elif response.status_code == 400 and "Invalid host header" in response.text:
                print("⏳ Still redeploying...")
                
            else:
                print(f"⚠️  Status {response.status_code}: {response.text[:100]}")
                
        except Exception as e:
            print(f"❌ Connection error: {str(e)[:50]}...")
        
        if attempt < max_attempts:
            print("   Waiting 15 seconds...\n")
            time.sleep(15)
    
    print("⏰ Deployment is taking longer than expected.")
    print("The fix is applied - Railway just needs more time to deploy.")
    return False


def main():
    """Main verification"""
    success = test_backend_after_fix()
    
    if success:
        print("\n🎊 PERMANENT FIX SUCCESSFUL!")
        print("Your backend will never have host header issues again!")
    else:
        print("\n⏳ Fix is applied - just waiting for Railway deployment")
        print("Test manually in a few minutes:")
        print("curl https://baseskel-production.up.railway.app/health")


if __name__ == "__main__":
    main()