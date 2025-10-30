"""
Pip installer with multiple fallback methods for Docker environments
"""

import subprocess
import sys
import urllib.request
import os


class DockerPipError(Exception):
    """Custom exception for Docker pip installation issues"""
    pass


class PipInstaller:
    """Reliable pip installer with multiple fallback methods"""

    def __init__(self, verbose: bool = True):
        self.verbose = verbose

    def log(self, message: str):
        """Log message if verbose mode is enabled"""
        if self.verbose:
            print(f"[DockerPipUtils] {message}")

    def ensure_pip(self) -> bool:
        """
        Ensure pip is available using multiple fallback methods
        Returns True if pip is successfully available
        """
        methods = [
            self._check_existing_pip,
            self._try_ensurepip,
            self._download_get_pip,
            self._install_via_apt
        ]

        for method in methods:
            try:
                if method():
                    self.log("✅ pip is now available")
                    return True
            except Exception as e:
                self.log(f"❌ Method failed: {e}")
                continue

        raise DockerPipError("All pip installation methods failed")

    def _check_existing_pip(self) -> bool:
        """Check if pip is already available"""
        try:
            result = subprocess.run([sys.executable, "-m", "pip", "--version"],
                                                                capture_output=True, text=True)
            if result.returncode == 0:
                self.log("✅ pip already available")
                return True
        except Exception:
            pass
        return False

    def _try_ensurepip(self) -> bool:
        """Try to install pip using ensurepip"""
        try:
            self.log("Trying ensurepip...")
            result = subprocess.run([sys.executable, "-m", "ensurepip", "--upgrade"],
                                                                capture_output=True, text=True)
            if result.returncode == 0:
                self.log("✅ pip installed via ensurepip")
                return True
        except Exception:
            pass
        return False

    def _download_get_pip(self) -> bool:
        """Download and run get-pip.py"""
        try:
            self.log("Downloading get-pip.py...")
            urllib.request.urlretrieve("https://bootstrap.pypa.io/get-pip.py", "get-pip.py")

            result = subprocess.run([sys.executable, "get-pip.py"],
                                                                capture_output=True, text=True)

            # Clean up
            if os.path.exists("get-pip.py"):
                os.remove("get-pip.py")

            if result.returncode == 0:
                self.log("✅ pip installed via get-pip.py")
                return True
        except Exception:
            pass
        return False

    def _install_via_apt(self) -> bool:
        """Try to install pip via apt (Ubuntu/Debian)"""
        try:
            self.log("Trying apt-get install python3-pip...")
            result = subprocess.run(["apt-get", "update"], capture_output=True)
            if result.returncode == 0:
                result = subprocess.run(["apt-get", "install", "-y", "python3-pip"],
                                      capture_output=True)
                if result.returncode == 0:
                    self.log("✅ pip installed via apt")
                    return True
        except Exception:
            pass
        return False

    def install_packages(self, requirements_file: str) -> bool:
        """
        Install packages from requirements file
        """
        if not self.ensure_pip():
            return False

        try:
            self.log(f"Installing packages from {requirements_file}...")
            result = subprocess.run([
                sys.executable, "-m", "pip", "install",
                "--no-cache-dir", "-r", requirements_file
            ], capture_output=True, text=True)

            if result.returncode == 0:
                self.log("✅ Packages installed successfully")
                return True
            else:
                self.log(f"❌ Package installation failed: {result.stderr}")
                return False
        except Exception as e:
            self.log(f"❌ Package installation error: {e}")
            return False

    def upgrade_pip(self) -> bool:
        """Upgrade pip to latest version"""
        if not self.ensure_pip():
            return False

        try:
            self.log("Upgrading pip...")
            result = subprocess.run([
                sys.executable, "-m", "pip", "install",
                "--upgrade", "pip", "setuptools", "wheel"
            ], capture_output=True, text=True)

            if result.returncode == 0:
                self.log("✅ pip upgraded successfully")
                return True
            else:
                self.log(f"❌ pip upgrade failed: {result.stderr}")
                return False
        except Exception as e:
            self.log(f"❌ pip upgrade error: {e}")
            return False
