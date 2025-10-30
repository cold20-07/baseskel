#!/usr/bin/env python3
"""
Startup script with monitoring for Dr. Kishan Bhalani Medical Services
Addresses upstream server issues and prevents 502 errors
"""

import os
import sys
import time
import signal
import subprocess
import logging
from pathlib import Path
from datetime import datetime, timezone

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

class StartupManager:
    """Manages server startup with monitoring and error recovery"""
    
    def __init__(self):
        self.server_process = None
        self.monitor_process = None
        self.should_exit = False
        
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}, shutting down...")
        self.should_exit = True
        self.cleanup()
        sys.exit(0)
    
    def cleanup(self):
        """Clean up processes"""
        if self.server_process:
            logger.info("Terminating server process...")
            self.server_process.terminate()
            try:
                self.server_process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                logger.warning("Server process didn't terminate, killing...")
                self.server_process.kill()
        
        if self.monitor_process:
            logger.info("Terminating monitor process...")
            self.monitor_process.terminate()
    
    def check_dependencies(self):
        """Check if required dependencies are available"""
        logger.info("🔍 Checking dependencies...")
        
        required_packages = ['fastapi', 'uvicorn', 'supabase', 'pydantic']
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package)
                logger.info(f"✅ {package}: Available")
            except ImportError:
                logger.error(f"❌ {package}: Missing")
                missing_packages.append(package)
        
        if missing_packages:
            logger.error(f"Missing required packages: {missing_packages}")
            logger.info("Attempting to install missing packages...")
            try:
                subprocess.check_call([
                    sys.executable, '-m', 'pip', 'install', '--upgrade'
                ] + missing_packages)
                logger.info("✅ Packages installed successfully")
            except subprocess.CalledProcessError as e:
                logger.error(f"❌ Failed to install packages: {e}")
                return False
        
        return True
    
    def check_environment(self):
        """Check environment variables"""
        logger.info("🔍 Checking environment variables...")
        
        required_vars = ['SUPABASE_URL', 'SUPABASE_KEY']
        missing_vars = []
        
        for var in required_vars:
            if not os.environ.get(var):
                missing_vars.append(var)
                logger.error(f"❌ {var}: Not set")
            else:
                logger.info(f"✅ {var}: Set")
        
        # Set defaults for optional vars
        if not os.environ.get('PORT'):
            os.environ['PORT'] = '8000'
            logger.info("ℹ️ PORT: Set to default 8000")
        
        if not os.environ.get('CORS_ORIGINS'):
            os.environ['CORS_ORIGINS'] = '*'
            logger.info("ℹ️ CORS_ORIGINS: Set to default *")
        
        return len(missing_vars) == 0
    
    def test_server_startup(self):
        """Test if server can start successfully"""
        logger.info("🧪 Testing server startup...")
        
        # Try importing the server modules
        try:
            sys.path.insert(0, str(Path(__file__).parent))
            backend_dir = Path(__file__).parent / "backend"
            if backend_dir.exists():
                sys.path.insert(0, str(backend_dir))
            
            # Test imports
            try:
                from robust_server import create_robust_app
                app = create_robust_app()
                logger.info("✅ Robust server can be imported and created")
                return "robust_server.py"
            except ImportError:
                logger.warning("Robust server import failed, trying k8s_server...")
                
                try:
                    from k8s_server import create_k8s_optimized_app
                    app = create_k8s_optimized_app()
                    logger.info("✅ K8s server can be imported and created")
                    return "k8s_server.py"
                except ImportError:
                    logger.warning("K8s server import failed, trying simple_server...")
                    
                    try:
                        from simple_server import log
                        logger.info("✅ Simple server can be imported")
                        return "simple_server.py"
                    except ImportError:
                        logger.error("❌ No server modules can be imported")
                        return None
        
        except Exception as e:
            logger.error(f"❌ Server startup test failed: {e}")
            return None
    
    def start_server(self, server_script):
        """Start the server process"""
        logger.info(f"🚀 Starting server with {server_script}...")
        
        try:
            # Start server process
            self.server_process = subprocess.Popen([
                sys.executable, server_script
            ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            
            # Give server time to start
            time.sleep(5)
            
            # Check if process is still running
            if self.server_process.poll() is None:
                logger.info("✅ Server process started successfully")
                return True
            else:
                logger.error("❌ Server process exited immediately")
                # Get output
                stdout, _ = self.server_process.communicate()
                logger.error(f"Server output: {stdout}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Failed to start server: {e}")
            return False
    
    def monitor_server(self):
        """Monitor server health"""
        port = int(os.environ.get('PORT', 8000))
        
        while not self.should_exit:
            try:
                # Check if server process is still running
                if self.server_process and self.server_process.poll() is not None:
                    logger.error("❌ Server process died, attempting restart...")
                    return False
                
                # Test health endpoint
                import requests
                try:
                    response = requests.get(f"http://localhost:{port}/health", timeout=5)
                    if response.status_code == 200:
                        logger.info("✅ Server health check passed")
                    else:
                        logger.warning(f"⚠️ Server health check returned {response.status_code}")
                except requests.exceptions.ConnectionError:
                    logger.error("❌ Server health check failed - connection refused")
                    return False
                except requests.exceptions.Timeout:
                    logger.error("❌ Server health check failed - timeout")
                    return False
                
                # Wait before next check
                time.sleep(30)
                
            except Exception as e:
                logger.error(f"❌ Monitor error: {e}")
                time.sleep(10)
        
        return True
    
    def run(self):
        """Main startup and monitoring loop"""
        logger.info("🏥 Dr. Kishan Bhalani Medical Services - Startup Manager")
        logger.info("=" * 60)
        
        # Setup signal handlers
        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGINT, self.signal_handler)
        
        # Pre-flight checks
        if not self.check_dependencies():
            logger.error("❌ Dependency check failed")
            sys.exit(1)
        
        if not self.check_environment():
            logger.error("❌ Environment check failed")
            sys.exit(1)
        
        # Test server startup
        server_script = self.test_server_startup()
        if not server_script:
            logger.error("❌ No working server found")
            sys.exit(1)
        
        # Main loop with restart capability
        max_restarts = 5
        restart_count = 0
        
        while not self.should_exit and restart_count < max_restarts:
            logger.info(f"Starting server (attempt {restart_count + 1}/{max_restarts})...")
            
            # Start server
            if not self.start_server(server_script):
                restart_count += 1
                logger.error(f"Server startup failed, restart count: {restart_count}")
                if restart_count < max_restarts:
                    logger.info("Waiting 10 seconds before restart...")
                    time.sleep(10)
                continue
            
            # Monitor server
            if not self.monitor_server():
                restart_count += 1
                logger.error(f"Server monitoring failed, restart count: {restart_count}")
                if restart_count < max_restarts:
                    logger.info("Waiting 10 seconds before restart...")
                    time.sleep(10)
                continue
            
            # If we get here, monitoring was stopped by signal
            break
        
        if restart_count >= max_restarts:
            logger.error("❌ Maximum restart attempts reached, giving up")
            sys.exit(1)
        
        logger.info("✅ Startup manager shutting down normally")

def main():
    """Main entry point"""
    manager = StartupManager()
    manager.run()

if __name__ == "__main__":
    main()