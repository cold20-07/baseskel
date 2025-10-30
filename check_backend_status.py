#!/usr/bin/env python3
"""
Backend Status Checker for Dr. Kishan Bhalani Medical Documentation Services
"""

import requests
import json
import sys
from datetime import datetime


def check_endpoint(url, endpoint_name, expected_status=200):
    """Check a specific endpoint and return status"""
    try:
        response = requests.get(url, timeout=10)
        status = "✅ HEALTHY" if response.status_code == expected_status else f"❌ ERROR ({response.status_code})"
        
        try:
            data = response.json()
            return {
                "endpoint": endpoint_name,
                "url": url,
                "status": status,
                "response_code": response.status_code,
                "data": data,
                "response_time": response.elapsed.total_seconds()
            }
        except:
            return {
                "endpoint": endpoint_name,
                "url": url,
                "status": status,
                "response_code": response.status_code,
                "data": response.text[:200] + "..." if len(response.text) > 200 else response.text,
                "response_time": response.elapsed.total_seconds()
            }
    except requests.exceptions.RequestException as e:
        return {
            "endpoint": endpoint_name,
            "url": url,
            "status": f"❌ CONNECTION ERROR",
            "error": str(e),
            "response_time": None
        }


def main():
    """Check backend status comprehensively"""
    print("🏥 Dr. Kishan Bhalani Medical Documentation Services")
    print("🔍 Backend Status Check")
    print("=" * 60)
    
    # Determine base URL (try different ports/hosts)
    possible_urls = [
        "http://localhost:8080",
        "http://localhost:8000", 
        "http://0.0.0.0:8080",
        "http://0.0.0.0:8000",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:8000"
    ]
    
    base_url = None
    for url in possible_urls:
        try:
            response = requests.get(f"{url}/health", timeout=5)
            if response.status_code == 200:
                base_url = url
                print(f"✅ Found server at: {base_url}")
                break
        except:
            continue
    
    if not base_url:
        print("❌ Server not accessible on any common ports")
        print("Make sure your server is running on one of these URLs:")
        for url in possible_urls:
            print(f"   - {url}")
        sys.exit(1)
    
    print(f"🌐 Base URL: {base_url}")
    print(f"⏰ Check Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Define endpoints to check
    endpoints = [
        ("/health", "Health Check"),
        ("/api/health", "API Health Check"),
        ("/", "Root Endpoint"),
        ("/api/services", "Services API"),
        ("/api/blog", "Blog API"),
    ]
    
    results = []
    
    print("📊 Endpoint Status:")
    print("-" * 60)
    
    for endpoint, name in endpoints:
        url = f"{base_url}{endpoint}"
        result = check_endpoint(url, name)
        results.append(result)
        
        print(f"{result['status']} {name}")
        print(f"   URL: {url}")
        if 'response_time' in result and result['response_time']:
            print(f"   Response Time: {result['response_time']:.3f}s")
        if 'error' in result:
            print(f"   Error: {result['error']}")
        elif 'data' in result and isinstance(result['data'], dict):
            if 'status' in result['data']:
                print(f"   Server Status: {result['data']['status']}")
            if 'timestamp' in result['data']:
                print(f"   Server Time: {result['data']['timestamp']}")
            if 'hipaa_compliant' in result['data']:
                print(f"   HIPAA Compliant: {result['data']['hipaa_compliant']}")
        print()
    
    # Summary
    healthy_count = sum(1 for r in results if "✅" in r['status'])
    total_count = len(results)
    
    print("📈 Summary:")
    print("-" * 60)
    print(f"Healthy Endpoints: {healthy_count}/{total_count}")
    print(f"Success Rate: {(healthy_count/total_count)*100:.1f}%")
    
    if healthy_count == total_count:
        print("🎉 All systems operational!")
    elif healthy_count > 0:
        print("⚠️  Some services may be unavailable")
    else:
        print("❌ Server appears to be down or misconfigured")
    
    print()
    print("💡 Available endpoints:")
    print(f"   - API Documentation: {base_url}/docs")
    print(f"   - Health Check: {base_url}/health")
    print(f"   - API Health: {base_url}/api/health")
    
    return healthy_count == total_count


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)