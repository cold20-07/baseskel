#!/usr/bin/env python3
"""
Development startup script - starts both backend and frontend
"""

import subprocess
import sys
import time
import os
import signal
from pathlib import Path

def start_backend():
    """Start backend server"""
    backend_path = Path("backend")
    
    if not backend_path.exists():
        print("❌ Backend directory not found")
        return None
    
    print("🚀 Starting backend server...")
    try:
        process = subprocess.Popen([
            sys.executable, "run_server.py"
        ], cwd=backend_path)
        
        print("⏳ Backend starting on http://localhost:8000")
        time.sleep(5)
        return process
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return None

def start_frontend():
    """Start frontend development server"""
    frontend_path = Path("frontend")
    
    if not frontend_path.exists():
        print("❌ Frontend directory not found")
        return None
    
    print("🎨 Starting frontend server...")
    try:
        # Check if node_modules exists
        if not (frontend_path / "node_modules").exists():
            print("📦 Installing frontend dependencies...")
            subprocess.run(["npm", "install"], cwd=frontend_path, check=True)
        
        process = subprocess.Popen([
            "npm", "start"
        ], cwd=frontend_path)
        
        print("⏳ Frontend starting on http://localhost:3000")
        return process
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")
        return None

def main():
    print("🏥 Dr. Kishan Bhalani Medical Documentation Services")
    print("🚀 Development Environment Startup")
    print("=" * 50)
    
    backend_process = None
    frontend_process = None
    
    try:
        # Start backend
        backend_process = start_backend()
        if not backend_process:
            return
        
        # Start frontend
        frontend_process = start_frontend()
        if not frontend_process:
            if backend_process:
                backend_process.terminate()
            return
        
        print("\n✅ Both servers started successfully!")
        print("\n🔗 Available URLs:")
        print("• Frontend: http://localhost:3000")
        print("• Backend API: http://localhost:8000/docs")
        print("• Health check: http://localhost:8000/api/health")
        
        print("\n💡 Press Ctrl+C to stop both servers")
        
        # Wait for processes
        while True:
            time.sleep(1)
            
            # Check if processes are still running
            if backend_process.poll() is not None:
                print("❌ Backend process stopped")
                break
            if frontend_process.poll() is not None:
                print("❌ Frontend process stopped")
                break
    
    except KeyboardInterrupt:
        print("\n🛑 Stopping servers...")
        
        if frontend_process:
            frontend_process.terminate()
            print("✅ Frontend stopped")
        
        if backend_process:
            backend_process.terminate()
            print("✅ Backend stopped")
        
        print("✅ All servers stopped")

if __name__ == "__main__":
    main()