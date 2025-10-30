#!/usr/bin/env python3
"""
Backend URL Finder - Help locate your deployed backend URL
"""

import os
import json
import subprocess
import sys


def check_railway_deployment():
    """Check Railway deployment status and URL"""
    print("🚂 Railway Deployment:")
    print("-" * 30)
    
    try:
        # Check if Railway CLI is installed
        result = subprocess.run(['railway', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Railway CLI installed")
            
            # Try to get project info
            try:
                result = subprocess.run(['railway', 'status'], capture_output=True, text=True)
                if result.returncode == 0:
                    print("✅ Railway project connected")
                    print(result.stdout)
                else:
                    print("⚠️  Not connected to Railway project")
                    print("Run: railway login && railway link")
            except:
                print("⚠️  Cannot get Railway status")
            
            # Try to get domain
            try:
                result = subprocess.run(['railway', 'domain'], capture_output=True, text=True)
                if result.returncode == 0 and result.stdout.strip():
                    print(f"🌐 Railway Domain: {result.stdout.strip()}")
                    return result.stdout.strip()
                else:
                    print("❌ No Railway domain configured")
            except:
                print("⚠️  Cannot get Railway domain")
                
        else:
            print("❌ Railway CLI not installed")
            print("Install: npm install -g @railway/cli")
            
    except FileNotFoundError:
        print("❌ Railway CLI not found")
        print("Install: npm install -g @railway/cli")
    
    return None


def check_environment_urls():
    """Check configured backend URLs in environment files"""
    print("\n🔧 Configured Backend URLs:")
    print("-" * 30)
    
    env_files = [
        'frontend/.env',
        'frontend/.env.production', 
        'frontend/.env.railway',
        'frontend/.env.render',
        'backend/.env',
        'backend/.env.production',
        'backend/.env.railway'
    ]
    
    found_urls = []
    
    for env_file in env_files:
        if os.path.exists(env_file):
            with open(env_file, 'r') as f:
                content = f.read()
                for line in content.split('\n'):
                    if ('BACKEND_URL' in line or 'API_URL' in line or 'BASE_URL' in line) and not line.startswith('#'):
                        if '=' in line:
                            url = line.split('=')[1].strip()
                            if url and url not in found_urls:
                                found_urls.append(url)
                                print(f"📍 {env_file}: {url}")
    
    if not found_urls:
        print("❌ No backend URLs found in environment files")
    
    return found_urls


def check_deployment_configs():
    """Check deployment configuration files"""
    print("\n📋 Deployment Configurations:")
    print("-" * 30)
    
    configs = []
    
    # Check railway.json
    if os.path.exists('railway.json'):
        print("✅ railway.json found")
        configs.append("Railway")
    
    # Check Dockerfile
    if os.path.exists('Dockerfile'):
        print("✅ Dockerfile found")
        configs.append("Docker")
    
    # Check package.json for deployment scripts
    if os.path.exists('package.json'):
        with open('package.json', 'r') as f:
            package_data = json.load(f)
            scripts = package_data.get('scripts', {})
            if any('deploy' in script for script in scripts.values()):
                print("✅ Deployment scripts found in package.json")
    
    return configs


def provide_deployment_instructions():
    """Provide instructions for getting backend URL"""
    print("\n🚀 How to Get Your Backend URL:")
    print("-" * 40)
    
    print("1️⃣  **If using Railway:**")
    print("   • Install Railway CLI: npm install -g @railway/cli")
    print("   • Login: railway login")
    print("   • Link project: railway link")
    print("   • Get domain: railway domain")
    print("   • Or check Railway dashboard: https://railway.app/dashboard")
    print()
    
    print("2️⃣  **If using other platforms:**")
    print("   • **Render**: Check your Render dashboard")
    print("   • **Heroku**: heroku apps:info")
    print("   • **Vercel**: vercel ls")
    print("   • **Netlify Functions**: Check Netlify dashboard")
    print()
    
    print("3️⃣  **If not deployed yet:**")
    print("   • Deploy to Railway: railway up")
    print("   • Deploy to Render: Connect GitHub repo")
    print("   • Deploy to Heroku: git push heroku main")
    print()
    
    print("4️⃣  **Local development:**")
    print("   • Backend URL: http://localhost:8080")
    print("   • Or: http://localhost:8000")
    print()


def test_backend_urls(urls):
    """Test if backend URLs are accessible"""
    print("\n🔍 Testing Backend URLs:")
    print("-" * 30)
    
    try:
        import requests
        
        for url in urls:
            try:
                # Test health endpoint
                health_url = f"{url}/health" if not url.endswith('/') else f"{url}health"
                response = requests.get(health_url, timeout=10)
                
                if response.status_code == 200:
                    print(f"✅ {url} - WORKING")
                    data = response.json()
                    if 'status' in data:
                        print(f"   Status: {data['status']}")
                    return url
                else:
                    print(f"⚠️  {url} - Status {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                print(f"❌ {url} - Not accessible ({str(e)[:50]}...)")
                
    except ImportError:
        print("⚠️  Cannot test URLs (requests module not available)")
        print("Install: pip install requests")
    
    return None


def main():
    """Find backend URL"""
    print("🏥 Dr. Kishan Bhalani Medical Documentation Services")
    print("🔍 Backend URL Finder")
    print("=" * 50)
    
    # Check Railway deployment
    railway_url = check_railway_deployment()
    
    # Check environment files
    env_urls = check_environment_urls()
    
    # Check deployment configs
    configs = check_deployment_configs()
    
    # Combine all found URLs
    all_urls = []
    if railway_url:
        all_urls.append(railway_url)
    all_urls.extend(env_urls)
    
    # Remove duplicates
    all_urls = list(set(all_urls))
    
    if all_urls:
        # Test URLs
        working_url = test_backend_urls(all_urls)
        
        if working_url:
            print(f"\n🎉 WORKING BACKEND URL FOUND:")
            print(f"   {working_url}")
            print(f"\n📝 Update your frontend .env.production:")
            print(f"   REACT_APP_BACKEND_URL={working_url}")
        else:
            print(f"\n⚠️  URLs found but none are accessible:")
            for url in all_urls:
                print(f"   {url}")
    else:
        print("\n❌ No backend URLs found")
    
    # Provide instructions
    provide_deployment_instructions()
    
    print("\n💡 Quick Commands:")
    print("   • Check Railway: railway status")
    print("   • Get Railway domain: railway domain") 
    print("   • Deploy to Railway: railway up")
    print("   • View Railway logs: railway logs")


if __name__ == "__main__":
    main()