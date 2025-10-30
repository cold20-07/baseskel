#!/usr/bin/env python3
"""
Test deployment configuration for Dr. Kishan Bhalani Medical Documentation Services
"""

import requests
import sys
import time

def test_deployment(base_url):
    """Test deployment endpoints"""
    print(f"🧪 Testing deployment at: {base_url}")
    print("=" * 50)
    
    tests = [
        ("/", "Root endpoint"),
        ("/health", "Health check"),
        ("/api/", "API root"),
        ("/api/health", "API health check"),
        ("/api/services", "Services endpoint"),
        ("/api/blog", "Blog endpoint")
    ]
    
    results = []
    
    for endpoint, description in tests:
        try:
            url = f"{base_url.rstrip('/')}{endpoint}"
            print(f"Testing {description}: {url}")
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ {description}: OK ({response.status_code})")
                results.append(True)
            else:
                print(f"❌ {description}: Failed ({response.status_code})")
                results.append(False)
                
        except requests.exceptions.RequestException as e:
            print(f"❌ {description}: Error - {e}")
            results.append(False)
        
        time.sleep(0.5)  # Small delay between requests
    
    print("\n" + "=" * 50)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Deployment is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Check the deployment configuration.")
        return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python test_deployment.py <base_url>")
        print("Example: python test_deployment.py https://your-app.vercel.app")
        sys.exit(1)
    
    base_url = sys.argv[1]
    success = test_deployment(base_url)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()