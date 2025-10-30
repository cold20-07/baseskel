"""
Environment validation utilities for Docker pip installations
"""

import subprocess
import sys
import os
from typing import Dict, Tuple


def check_pip_availability() -> Tuple[bool, str]:
    """
    Check if pip is available and return status with details
    Returns (is_available, details)
    """
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "--version"],
                                                            capture_output=True, text=True)
        if result.returncode == 0:
            return True, result.stdout.strip()
        else:
            return False, result.stderr.strip()
    except Exception as e:
        return False, str(e)


def validate_environment() -> Dict[str, str]:
    """
    Validate the current environment for pip installation
    Returns a dictionary with validation results
    """
    results = {
        "python_version": sys.version,
        "python_executable": sys.executable,
        "pip_available": False,
        "pip_details": "",
        "ensurepip_available": False,
        "internet_access": False,
        "apt_available": False,
        "environment_type": "unknown"
    }

    # Check pip availability
    pip_available, pip_details = check_pip_availability()
    results["pip_available"] = pip_available
    results["pip_details"] = pip_details

    # Check ensurepip availability
    try:
        result = subprocess.run([sys.executable, "-m", "ensurepip", "--help"],
                                                            capture_output=True, text=True)
        results["ensurepip_available"] = result.returncode == 0
    except Exception:
        results["ensurepip_available"] = False

    # Check internet access
    try:
        import urllib.request
        urllib.request.urlopen("https://pypi.org", timeout=5)
        results["internet_access"] = True
    except Exception:
        results["internet_access"] = False

    # Check apt availability (Ubuntu/Debian)
    try:
        result = subprocess.run(["which", "apt-get"], capture_output=True)
        results["apt_available"] = result.returncode == 0
    except Exception:
        results["apt_available"] = False

    # Detect environment type
    if "/nix/store" in sys.executable:
        results["environment_type"] = "nix"
    elif "/.nixpacks/" in os.getcwd():
        results["environment_type"] = "nixpacks"
    elif os.path.exists("/.dockerenv"):
        results["environment_type"] = "docker"
    elif results["apt_available"]:
        results["environment_type"] = "ubuntu/debian"

    return results


def print_environment_report():
    """Print a detailed environment validation report"""
    results = validate_environment()

    print("🔍 Docker Pip Environment Validation Report")
    print("=" * 50)

    print(f"Python Version: {results['python_version'].split()[0]}")
    print(f"Python Executable: {results['python_executable']}")
    print(f"Environment Type: {results['environment_type']}")

    print("\n📦 Pip Status:")
    if results["pip_available"]:
        print(f"✅ pip available: {results['pip_details']}")
    else:
        print(f"❌ pip not available: {results['pip_details']}")

    print("\n🛠️ Available Installation Methods:")
    print(f"{'✅' if results['ensurepip_available'] else '❌'} ensurepip")
    print(f"{'✅' if results['internet_access'] else '❌'} Internet access (get-pip.py)")
    print(f"{'✅' if results['apt_available'] else '❌'} apt-get (Ubuntu/Debian)")

    print("\n💡 Recommendations:")
    if results["pip_available"]:
        print("✅ pip is working - no action needed")
    elif results["environment_type"] == "nix" or results["environment_type"] == "nixpacks":
        print("⚠️  Nix environment detected - consider using official Python Docker image")
        print("   Add python311Packages.pip to nixPkgs or switch to Dockerfile")
    elif results["ensurepip_available"]:
        print("💡 Use: python3 -m ensurepip --upgrade")
    elif results["internet_access"]:
        print("💡 Use: curl https://bootstrap.pypa.io/get-pip.py | python3")
    elif results["apt_available"]:
        print("💡 Use: apt-get update && apt-get install -y python3-pip")
    else:
        print("❌ No viable pip installation method found")

    print("=" * 50)
