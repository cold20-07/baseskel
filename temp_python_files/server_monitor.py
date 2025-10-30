#!/usr/bin/env python3
"""
Server monitoring and resource management for Dr. Kishan Bhalani Medical Services
Helps prevent 502 errors by monitoring upstream server health
"""

import os
import sys
import time
import requests
import subprocess
import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ServerMonitor:
    """Monitor server health and resources"""
    
    def __init__(self, port: int = None):
        self.port = port or int(os.environ.get('PORT', 8000))
        self.base_url = f"http://localhost:{self.port}"
        self.health_endpoints = [
            "/health",
            "/api/health", 
            "/healthz",
            "/ping",
            "/status"
        ]
        
    def check_server_health(self) -> Dict:
        """Check if server is responding to health checks"""
        results = {}
        
        for endpoint in self.health_endpoints:
            url = f"{self.base_url}{endpoint}"
            try:
                response = requests.get(url, timeout=5)
                results[endpoint] = {
                    "status": "healthy" if response.status_code == 200 else "unhealthy",
                    "status_code": response.status_code,
                    "response_time": response.elapsed.total_seconds(),
                    "content_length": len(response.content)
                }
                if response.status_code == 200:
                    logger.info(f"✅ {endpoint}: {response.status_code} ({response.elapsed.total_seconds():.3f}s)")
                else:
                    logger.warning(f"⚠️ {endpoint}: {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                results[endpoint] = {"status": "connection_refused", "error": "Connection refused"}
                logger.error(f"❌ {endpoint}: Connection refused")
            except requests.exceptions.Timeout:
                results[endpoint] = {"status": "timeout", "error": "Request timeout"}
                logger.error(f"❌ {endpoint}: Timeout")
            except Exception as e:
                results[endpoint] = {"status": "error", "error": str(e)}
                logger.error(f"❌ {endpoint}: {e}")
        
        return results
    
    def check_system_resources(self) -> Dict:
        """Check system resource usage"""
        try:
            import psutil
            
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            
            # Memory usage
            memory = psutil.virtual_memory()
            
            # Disk usage
            disk = psutil.disk_usage('/')
            
            # Load average (Unix only)
            load_avg = None
            if hasattr(os, 'getloadavg'):
                load_avg = os.getloadavg()
            
            # Process count
            process_count = len(psutil.pids())
            
            resources = {
                "cpu": {
                    "percent": cpu_percent,
                    "count": cpu_count,
                    "load_average": load_avg
                },
                "memory": {
                    "total": memory.total,
                    "available": memory.available,
                    "percent": memory.percent,
                    "used": memory.used
                },
                "disk": {
                    "total": disk.total,
                    "free": disk.free,
                    "percent": disk.percent,
                    "used": disk.used
                },
                "processes": process_count
            }
            
            # Log warnings for high usage
            if cpu_percent > 80:
                logger.warning(f"⚠️ High CPU usage: {cpu_percent}%")
            if memory.percent > 80:
                logger.warning(f"⚠️ High memory usage: {memory.percent}%")
            if disk.percent > 80:
                logger.warning(f"⚠️ High disk usage: {disk.percent}%")
            
            return resources
            
        except ImportError:
            logger.warning("psutil not available, cannot check system resources")
            return {"error": "psutil not available"}
        except Exception as e:
            logger.error(f"Error checking system resources: {e}")
            return {"error": str(e)}
    
    def check_process_status(self) -> Dict:
        """Check if server processes are running"""
        try:
            import psutil
            
            # Find Python processes that might be our server
            server_processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cpu_percent', 'memory_percent']):
                try:
                    if proc.info['name'] == 'python' or proc.info['name'] == 'python3':
                        cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                        if any(server_file in cmdline for server_file in ['server.py', 'k8s_server.py', 'robust_server.py', 'uvicorn']):
                            server_processes.append({
                                "pid": proc.info['pid'],
                                "cmdline": cmdline,
                                "cpu_percent": proc.info['cpu_percent'],
                                "memory_percent": proc.info['memory_percent']
                            })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            return {
                "server_processes": server_processes,
                "process_count": len(server_processes)
            }
            
        except ImportError:
            return {"error": "psutil not available"}
        except Exception as e:
            return {"error": str(e)}
    
    def test_nginx_config(self) -> Dict:
        """Test nginx configuration if available"""
        try:
            # Try to test nginx config
            result = subprocess.run(['nginx', '-t'], capture_output=True, text=True, timeout=10)
            return {
                "nginx_config_test": {
                    "success": result.returncode == 0,
                    "stdout": result.stdout,
                    "stderr": result.stderr
                }
            }
        except FileNotFoundError:
            return {"nginx_config_test": {"error": "nginx not found"}}
        except subprocess.TimeoutExpired:
            return {"nginx_config_test": {"error": "nginx test timeout"}}
        except Exception as e:
            return {"nginx_config_test": {"error": str(e)}}
    
    def get_server_logs(self, lines: int = 50) -> List[str]:
        """Get recent server logs"""
        log_files = [
            '/tmp/server.log',
            '/var/log/nginx/error.log',
            '/var/log/nginx/access.log'
        ]
        
        logs = {}
        for log_file in log_files:
            if os.path.exists(log_file):
                try:
                    with open(log_file, 'r') as f:
                        logs[log_file] = f.readlines()[-lines:]
                except Exception as e:
                    logs[log_file] = [f"Error reading log: {e}"]
            else:
                logs[log_file] = ["Log file not found"]
        
        return logs
    
    def run_comprehensive_check(self) -> Dict:
        """Run all monitoring checks"""
        logger.info("🔍 Running comprehensive server health check...")
        
        results = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "server_health": self.check_server_health(),
            "system_resources": self.check_system_resources(),
            "process_status": self.check_process_status(),
            "nginx_config": self.test_nginx_config(),
            "environment": {
                "port": self.port,
                "python_version": sys.version,
                "platform": sys.platform,
                "cwd": os.getcwd()
            }
        }
        
        # Determine overall health
        health_checks = results["server_health"]
        healthy_endpoints = sum(1 for check in health_checks.values() if check.get("status") == "healthy")
        total_endpoints = len(health_checks)
        
        if healthy_endpoints == 0:
            results["overall_status"] = "critical"
            logger.error("❌ CRITICAL: No health endpoints responding")
        elif healthy_endpoints < total_endpoints:
            results["overall_status"] = "degraded"
            logger.warning(f"⚠️ DEGRADED: {healthy_endpoints}/{total_endpoints} endpoints healthy")
        else:
            results["overall_status"] = "healthy"
            logger.info(f"✅ HEALTHY: All {total_endpoints} endpoints responding")
        
        return results

def main():
    """Main monitoring function"""
    logger.info("🏥 Dr. Kishan Bhalani Medical Services - Server Monitor")
    logger.info("=" * 60)
    
    # Get port from environment or command line
    port = int(sys.argv[1]) if len(sys.argv) > 1 else int(os.environ.get('PORT', 8000))
    
    monitor = ServerMonitor(port)
    
    if len(sys.argv) > 2 and sys.argv[2] == "continuous":
        # Continuous monitoring mode
        logger.info("Starting continuous monitoring (Ctrl+C to stop)...")
        try:
            while True:
                results = monitor.run_comprehensive_check()
                time.sleep(30)  # Check every 30 seconds
        except KeyboardInterrupt:
            logger.info("Monitoring stopped by user")
    else:
        # Single check mode
        results = monitor.run_comprehensive_check()
        
        # Print summary
        print("\n" + "=" * 60)
        print("HEALTH CHECK SUMMARY")
        print("=" * 60)
        print(f"Overall Status: {results['overall_status'].upper()}")
        print(f"Timestamp: {results['timestamp']}")
        print(f"Port: {results['environment']['port']}")
        
        print("\nHealth Endpoints:")
        for endpoint, status in results['server_health'].items():
            status_icon = "✅" if status.get('status') == 'healthy' else "❌"
            print(f"  {status_icon} {endpoint}: {status.get('status', 'unknown')}")
        
        if 'cpu' in results['system_resources']:
            resources = results['system_resources']
            print(f"\nSystem Resources:")
            print(f"  CPU: {resources['cpu']['percent']:.1f}%")
            print(f"  Memory: {resources['memory']['percent']:.1f}%")
            print(f"  Disk: {resources['disk']['percent']:.1f}%")
        
        processes = results['process_status']
        if 'server_processes' in processes:
            print(f"\nServer Processes: {len(processes['server_processes'])}")
            for proc in processes['server_processes']:
                print(f"  PID {proc['pid']}: CPU {proc['cpu_percent']:.1f}%, Memory {proc['memory_percent']:.1f}%")

if __name__ == "__main__":
    main()