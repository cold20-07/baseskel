#!/usr/bin/env python3
"""
Simple Backend Status Check
"""

import subprocess
import sys
import os


def check_server_process():
    """Check if the server process is running"""
    try:
        # Check if uvicorn process is running
        result = subprocess.run(['pgrep', '-f', 'uvicorn'], capture_output=True, text=True)
        if result.returncode == 0:
            pids = result.stdout.strip().split('\n')
            print(f"✅ Server process running (PIDs: {', '.join(pids)})")
            return True
        else:
            print("❌ No uvicorn process found")
            return False
    except FileNotFoundError:
        # pgrep not available, try ps
        try:
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            if 'uvicorn' in result.stdout:
                print("✅ Server process detected in process list")
                return True
            else:
                print("❌ No uvicorn process in process list")
                return False
        except:
            print("⚠️  Cannot check process status")
            return None


def check_port_listening():
    """Check if port 8080 is listening"""
    try:
        result = subprocess.run(['netstat', '-ln'], capture_output=True, text=True)
        if ':8080' in result.stdout:
            print("✅ Port 8080 is listening")
            return True
        else:
            print("❌ Port 8080 not found in netstat")
            return False
    except FileNotFoundError:
        try:
            result = subprocess.run(['ss', '-ln'], capture_output=True, text=True)
            if ':8080' in result.stdout:
                print("✅ Port 8080 is listening (ss)")
                return True
            else:
                print("❌ Port 8080 not found in ss")
                return False
        except:
            print("⚠️  Cannot check port status")
            return None


def check_backend_files():
    """Check if backend files are present"""
    backend_files = [
        'backend/server.py',
        'backend/run_server.py',
        'backend/requirements.txt'
    ]
    
    print("📁 Backend Files:")
    all_present = True
    for file in backend_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} (missing)")
            all_present = False
    
    return all_present


def main():
    """Check backend status"""
    print("🏥 Dr. Kishan Bhalani Medical Documentation Services")
    print("🔍 Backend Status Check")
    print("=" * 50)
    
    # Check backend files
    files_ok = check_backend_files()
    print()
    
    # Check server process
    print("🔄 Process Status:")
    process_ok = check_server_process()
    print()
    
    # Check port
    print("🌐 Network Status:")
    port_ok = check_port_listening()
    print()
    
    # Summary
    print("📊 Status Summary:")
    print(f"   Backend Files: {'✅ OK' if files_ok else '❌ Issues'}")
    print(f"   Server Process: {'✅ Running' if process_ok else '❌ Not Running' if process_ok is False else '⚠️  Unknown'}")
    print(f"   Port 8080: {'✅ Listening' if port_ok else '❌ Not Listening' if port_ok is False else '⚠️  Unknown'}")
    
    if files_ok and process_ok and port_ok:
        print("\n🎉 Backend appears to be running successfully!")
        print("💡 Server should be accessible on port 8080")
    else:
        print("\n⚠️  Some issues detected with backend status")
    
    # Show recent logs if available
    print("\n📋 Recent Server Output:")
    print("(From your terminal where you see the uvicorn messages)")


if __name__ == "__main__":
    main()