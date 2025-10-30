#!/usr/bin/env python3
"""
502 Bad Gateway Fix Script for Dr. Kishan Bhalani Medical Services
Implements all the troubleshooting steps you mentioned
"""

import os
import sys
import subprocess
import time
import requests
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Fix502:
    """Comprehensive 502 error fixing tool"""
    
    def __init__(self):
        self.port = int(os.environ.get('PORT', 8000))
        self.base_url = f"http://localhost:{self.port}"
    
    def check_upstream_server(self):
        """Check if the application server is running and not overloaded"""
        logger.info("🔍 Checking upstream server status...")
        
        # Check if server process is running
        try:
            import psutil
            python_processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cpu_percent', 'memory_percent']):
                try:
                    if proc.info['name'] in ['python', 'python3']:
                        cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                        if any(server in cmdline for server in ['server.py', 'uvicorn', 'fastapi']):
                            python_processes.append({
                                'pid': proc.info['pid'],
                                'cmdline': cmdline,
                                'cpu': proc.info['cpu_percent'],
                                'memory': proc.info['memory_percent']
                            })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if python_processes:
                logger.info(f"✅ Found {len(python_processes)} server process(es)")
                for proc in python_processes:
                    logger.info(f"   PID {proc['pid']}: CPU {proc['cpu']:.1f}%, Memory {proc['memory']:.1f}%")
                    if proc['cpu'] > 80:
                        logger.warning(f"⚠️ Process {proc['pid']} has high CPU usage: {proc['cpu']:.1f}%")
                    if proc['memory'] > 80:
                        logger.warning(f"⚠️ Process {proc['pid']} has high memory usage: {proc['memory']:.1f}%")
                return True
            else:
                logger.error("❌ No server processes found")
                return False
                
        except ImportError:
            logger.warning("psutil not available, cannot check processes")
            return None
    
    def restart_services(self):
        """Restart the application server services"""
        logger.info("🔄 Restarting services...")
        
        # Kill existing server processes
        try:
            import psutil
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if proc.info['name'] in ['python', 'python3']:
                        cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                        if any(server in cmdline for server in ['server.py', 'uvicorn', 'fastapi']):
                            logger.info(f"Terminating process {proc.info['pid']}")
                            proc.terminate()
                            proc.wait(timeout=10)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
                    continue
        except ImportError:
            logger.warning("psutil not available, cannot restart processes")
        
        # Start new server process
        logger.info("Starting new server process...")
        try:
            # Try different server scripts in order of preference
            server_scripts = ['robust_server.py', 'k8s_server.py', 'simple_server.py']
            
            for script in server_scripts:
                if os.path.exists(script):
                    logger.info(f"Starting {script}...")
                    process = subprocess.Popen([sys.executable, script])
                    time.sleep(5)  # Give it time to start
                    
                    if process.poll() is None:
                        logger.info(f"✅ {script} started successfully")
                        return True
                    else:
                        logger.error(f"❌ {script} failed to start")
            
            logger.error("❌ No server scripts could be started")
            return False
            
        except Exception as e:
            logger.error(f"❌ Failed to restart services: {e}")
            return False
    
    def check_nginx_config(self):
        """Check Nginx configuration for syntax errors"""
        logger.info("🔍 Checking Nginx configuration...")
        
        try:
            # Test nginx configuration
            result = subprocess.run(['nginx', '-t'], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                logger.info("✅ Nginx configuration is valid")
                logger.info(f"Output: {result.stdout}")
                return True
            else:
                logger.error("❌ Nginx configuration has errors")
                logger.error(f"Errors: {result.stderr}")
                return False
                
        except FileNotFoundError:
            logger.warning("⚠️ Nginx not found (this is normal for Railway/Heroku deployments)")
            return None
        except subprocess.TimeoutExpired:
            logger.error("❌ Nginx configuration test timed out")
            return False
        except Exception as e:
            logger.error(f"❌ Error checking nginx config: {e}")
            return False
    
    def inspect_server_logs(self):
        """Look for errors in server logs"""
        logger.info("🔍 Inspecting server logs...")
        
        log_locations = [
            '/tmp/server.log',
            '/var/log/nginx/error.log',
            '/var/log/nginx/access.log',
            'server.log',
            'error.log'
        ]
        
        found_logs = False
        for log_file in log_locations:
            if os.path.exists(log_file):
                found_logs = True
                logger.info(f"📋 Checking {log_file}...")
                try:
                    with open(log_file, 'r') as f:
                        lines = f.readlines()
                        recent_lines = lines[-20:]  # Last 20 lines
                        
                        error_count = 0
                        for line in recent_lines:
                            if any(error_word in line.lower() for error_word in ['error', 'failed', 'exception', '502', '500']):
                                logger.error(f"   ERROR: {line.strip()}")
                                error_count += 1
                        
                        if error_count == 0:
                            logger.info(f"   ✅ No recent errors in {log_file}")
                        else:
                            logger.warning(f"   ⚠️ Found {error_count} error(s) in {log_file}")
                            
                except Exception as e:
                    logger.error(f"   ❌ Could not read {log_file}: {e}")
        
        if not found_logs:
            logger.warning("⚠️ No log files found")
        
        return found_logs
    
    def check_resources_and_increase(self):
        """Check if server is overloaded and suggest resource increases"""
        logger.info("🔍 Checking system resources...")
        
        try:
            import psutil
            
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            
            # Memory usage
            memory = psutil.virtual_memory()
            
            # Disk usage
            disk = psutil.disk_usage('/')
            
            # Load average
            load_avg = os.getloadavg() if hasattr(os, 'getloadavg') else None
            
            logger.info(f"📊 System Resources:")
            logger.info(f"   CPU: {cpu_percent:.1f}% ({cpu_count} cores)")
            logger.info(f"   Memory: {memory.percent:.1f}% ({memory.used // (1024**3):.1f}GB / {memory.total // (1024**3):.1f}GB)")
            logger.info(f"   Disk: {disk.percent:.1f}% ({disk.used // (1024**3):.1f}GB / {disk.total // (1024**3):.1f}GB)")
            if load_avg:
                logger.info(f"   Load Average: {load_avg[0]:.2f}, {load_avg[1]:.2f}, {load_avg[2]:.2f}")
            
            # Check for resource issues
            issues = []
            if cpu_percent > 80:
                issues.append(f"High CPU usage: {cpu_percent:.1f}%")
            if memory.percent > 80:
                issues.append(f"High memory usage: {memory.percent:.1f}%")
            if disk.percent > 90:
                issues.append(f"High disk usage: {disk.percent:.1f}%")
            if load_avg and load_avg[0] > cpu_count * 2:
                issues.append(f"High load average: {load_avg[0]:.2f}")
            
            if issues:
                logger.warning("⚠️ Resource issues detected:")
                for issue in issues:
                    logger.warning(f"   - {issue}")
                
                logger.info("💡 Recommendations:")
                logger.info("   - Consider upgrading to a higher tier plan")
                logger.info("   - Optimize application code for better performance")
                logger.info("   - Add caching to reduce database queries")
                logger.info("   - Use a CDN for static assets")
                return False
            else:
                logger.info("✅ System resources are within normal limits")
                return True
                
        except ImportError:
            logger.warning("psutil not available, cannot check system resources")
            return None
    
    def test_health_endpoints(self):
        """Test all health endpoints"""
        logger.info("🏥 Testing health endpoints...")
        
        endpoints = ['/health', '/api/health', '/healthz', '/ping', '/status', '/ready', '/alive']
        working_endpoints = []
        
        for endpoint in endpoints:
            url = f"{self.base_url}{endpoint}"
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    logger.info(f"✅ {endpoint}: OK ({response.elapsed.total_seconds():.3f}s)")
                    working_endpoints.append(endpoint)
                else:
                    logger.warning(f"⚠️ {endpoint}: HTTP {response.status_code}")
            except requests.exceptions.ConnectionError:
                logger.error(f"❌ {endpoint}: Connection refused")
            except requests.exceptions.Timeout:
                logger.error(f"❌ {endpoint}: Timeout")
            except Exception as e:
                logger.error(f"❌ {endpoint}: {e}")
        
        if working_endpoints:
            logger.info(f"✅ {len(working_endpoints)} health endpoint(s) working")
            return True
        else:
            logger.error("❌ No health endpoints are responding")
            return False
    
    def run_comprehensive_fix(self):
        """Run all 502 fixing steps"""
        logger.info("🚨 Starting comprehensive 502 Bad Gateway fix...")
        logger.info("=" * 60)
        
        steps = [
            ("Check upstream server", self.check_upstream_server),
            ("Restart services", self.restart_services),
            ("Check Nginx configuration", self.check_nginx_config),
            ("Inspect server logs", self.inspect_server_logs),
            ("Check resources", self.check_resources_and_increase),
            ("Test health endpoints", self.test_health_endpoints)
        ]
        
        results = {}
        for step_name, step_func in steps:
            logger.info(f"\n🔧 Step: {step_name}")
            try:
                result = step_func()
                results[step_name] = result
                if result is True:
                    logger.info(f"✅ {step_name}: PASSED")
                elif result is False:
                    logger.error(f"❌ {step_name}: FAILED")
                else:
                    logger.info(f"ℹ️ {step_name}: SKIPPED/N/A")
            except Exception as e:
                logger.error(f"❌ {step_name}: ERROR - {e}")
                results[step_name] = False
        
        # Summary
        logger.info("\n" + "=" * 60)
        logger.info("🏥 502 FIX SUMMARY")
        logger.info("=" * 60)
        
        passed = sum(1 for r in results.values() if r is True)
        failed = sum(1 for r in results.values() if r is False)
        skipped = sum(1 for r in results.values() if r is None)
        
        logger.info(f"✅ Passed: {passed}")
        logger.info(f"❌ Failed: {failed}")
        logger.info(f"ℹ️ Skipped: {skipped}")
        
        if failed == 0:
            logger.info("🎉 All checks passed! 502 errors should be resolved.")
        elif failed <= 2:
            logger.warning("⚠️ Some issues found, but server might still work.")
        else:
            logger.error("🚨 Multiple critical issues found. Manual intervention required.")
        
        return results

def main():
    """Main entry point"""
    fixer = Fix502()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "check":
            fixer.test_health_endpoints()
        elif sys.argv[1] == "restart":
            fixer.restart_services()
        elif sys.argv[1] == "logs":
            fixer.inspect_server_logs()
        elif sys.argv[1] == "resources":
            fixer.check_resources_and_increase()
        else:
            print("Usage: python fix_502.py [check|restart|logs|resources]")
    else:
        fixer.run_comprehensive_fix()

if __name__ == "__main__":
    main()