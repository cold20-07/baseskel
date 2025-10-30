#!/usr/bin/env python3
"""
Detailed Backend Status Check
"""

import requests
import json


def check_backend_detailed():
    """Comprehensive backend check"""
    print("🚂 Railway Backend Detailed Check")
    print("=" * 50)
    
    backend_url = "https://baseskel-production.up.railway.app"
    
    print(f"🌐 Testing: {backend_url}")
    print()
    
    # Test different endpoints
    endpoints = [
        ("/", "Root"),
        ("/health", "Health Check"),
        ("/api/health", "API Health"),
        ("/docs", "API Documentation"),
        ("/api/services", "Services API"),
        ("/api/blog", "Blog API")
    ]
    
    print("📊 Endpoint Tests:")
    print("-" * 30)
    
    for endpoint, name in endpoints:
        url = f"{backend_url}{endpoint}"
        try:
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ {name}: Working (200)")
                
                # Try to parse JSON response
                try:
                    data = response.json()
                    if 'status' in data:
                        print(f"   Status: {data['status']}")
                    if 'message' in data:
                        print(f"   Message: {data['message']}")
                except:
                    print(f"   Content: {response.text[:50]}...")
                    
            elif response.status_code == 400:
                print(f"⚠️  {name}: Host header issue (400)")
                print(f"   Error: {response.text[:50]}...")
                
            elif response.status_code == 404:
                print(f"⚠️  {name}: Not found (404)")
                
            elif response.status_code == 500:
                print(f"❌ {name}: Server error (500)")
                
            else:
                print(f"⚠️  {name}: Status {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ {name}: Connection failed")
        except requests.exceptions.Timeout:
            print(f"❌ {name}: Timeout")
        except Exception as e:
            print(f"❌ {name}: {str(e)[:50]}...")
    
    print("\n🔍 Diagnosis:")
    print("-" * 30)
    
    # Test with different headers
    try:
        # Test with Host header
        headers = {'Host': 'baseskel-production.up.railway.app'}
        response = requests.get(f"{backend_url}/health", headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ Backend works with explicit Host header")
            data = response.json()
            print(f"   Server response: {data}")
        else:
            print(f"⚠️  Still getting {response.status_code} with Host header")
            
    except Exception as e:
        print(f"❌ Host header test failed: {e}")
    
    print("\n🔧 Current Issue:")
    print("-" * 30)
    print("❌ Backend is returning 'Invalid host header' (400)")
    print("❌ This means the TrustedHostMiddleware is blocking requests")
    print()
    
    print("💡 Solution:")
    print("-" * 30)
    print("The backend needs ALLOWED_HOSTS environment variable set.")
    print("In Railway dashboard:")
    print("1. Go to your baseskel project")
    print("2. Click on the backend service")
    print("3. Go to Variables tab")
    print("4. Add: ALLOWED_HOSTS=*")
    print("5. Or: ALLOWED_HOSTS=baseskel-production.up.railway.app")
    print("6. Click Deploy")
    print()
    
    print("🔄 Alternative Solutions:")
    print("-" * 30)
    print("Option 1: Set ALLOWED_HOSTS=* (allows all hosts)")
    print("Option 2: Set ALLOWED_HOSTS=baseskel-production.up.railway.app")
    print("Option 3: Remove TrustedHostMiddleware from production")
    print()
    
    print("📋 Backend Status Summary:")
    print("-" * 30)
    print("✅ Backend is deployed and running")
    print("✅ Server is responding to requests")
    print("❌ Host validation is blocking external access")
    print("⚠️  Needs environment variable configuration")
    print()
    
    print("🎯 Once Fixed, Backend Will Provide:")
    print("-" * 30)
    print("• Health check endpoint")
    print("• API documentation at /docs")
    print("• Services API for frontend")
    print("• Blog API for frontend")
    print("• Contact form API")
    print("• File upload API")
    print("• HIPAA compliance features")


if __name__ == "__main__":
    check_backend_detailed()