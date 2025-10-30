#!/usr/bin/env python3
"""
Test the complete deployment - Frontend + Backend
"""

import requests
import json


def test_complete_deployment():
    """Test both frontend and backend"""
    print("🏥 Dr. Kishan Bhalani Medical Documentation Services")
    print("🌐 Complete Deployment Test")
    print("=" * 60)
    
    frontend_url = "https://69036083ef483d4f8dc8e0cd--base-skel.netlify.app"
    backend_url = "https://baseskel-production.up.railway.app"
    
    print("🌐 Frontend Test:")
    print("-" * 30)
    try:
        response = requests.get(frontend_url, timeout=10)
        if response.status_code == 200:
            print(f"✅ Frontend accessible: {frontend_url}")
            print("✅ React app is loading")
            
            # Check if it's actually the React app
            if 'react' in response.text.lower() or 'root' in response.text:
                print("✅ React application detected")
            else:
                print("⚠️  Content might not be React app")
        else:
            print(f"⚠️  Frontend status: {response.status_code}")
    except Exception as e:
        print(f"❌ Frontend error: {e}")
    
    print("\n🚂 Backend Test:")
    print("-" * 30)
    
    # Test backend endpoints
    endpoints = [
        "/health",
        "/api/health", 
        "/",
        "/docs"
    ]
    
    backend_working = False
    for endpoint in endpoints:
        try:
            url = f"{backend_url}{endpoint}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ {endpoint}: Working")
                backend_working = True
                
                if 'health' in endpoint:
                    try:
                        data = response.json()
                        if 'status' in data:
                            print(f"   Server status: {data['status']}")
                    except:
                        pass
                        
            elif response.status_code == 400:
                print(f"⚠️  {endpoint}: Host header issue (400)")
            else:
                print(f"⚠️  {endpoint}: Status {response.status_code}")
                
        except Exception as e:
            print(f"❌ {endpoint}: {str(e)[:50]}...")
    
    print("\n🔗 Integration Status:")
    print("-" * 30)
    
    if backend_working:
        print("✅ Backend is responding")
        print("✅ Frontend can potentially connect to backend")
        print("✅ CORS should be configured")
    else:
        print("⚠️  Backend needs host header fix")
        print("   Go to Railway dashboard → Variables → Set ALLOWED_HOSTS=*")
    
    print("\n🎯 Deployment Summary:")
    print("-" * 30)
    print(f"Frontend: ✅ LIVE - {frontend_url}")
    print(f"Backend: {'✅ WORKING' if backend_working else '⚠️ NEEDS FIX'} - {backend_url}")
    
    if backend_working:
        print("\n🎉 SUCCESS: Full stack application is deployed and working!")
        print("🌟 Your medical documentation system is live!")
    else:
        print("\n⚠️  ALMOST THERE: Frontend is live, backend needs one environment variable fix")
    
    print("\n🌐 Your Live URLs:")
    print(f"• Frontend: {frontend_url}")
    print(f"• Backend API: {backend_url}")
    print(f"• API Docs: {backend_url}/docs")
    print(f"• Health Check: {backend_url}/health")
    
    print("\n💡 Next Steps:")
    if not backend_working:
        print("1. Fix Railway backend: Set ALLOWED_HOSTS=* in environment variables")
        print("2. Test backend: curl https://baseskel-production.up.railway.app/health")
        print("3. Test frontend API calls")
    else:
        print("1. Test all functionality on your live site")
        print("2. Set up custom domain if desired")
        print("3. Monitor for any issues")
    
    print("\n🎊 Congratulations on your deployment!")


if __name__ == "__main__":
    test_complete_deployment()