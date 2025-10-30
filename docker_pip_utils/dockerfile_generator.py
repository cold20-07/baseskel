"""
Dockerfile generator with reliable pip installation
"""

from typing import List


def generate_dockerfile(
    python_version: str = "3.9-slim",
    requirements_file: str = "requirements.txt",
    app_dir: str = "/app",
    start_command: List[str] = None,
    additional_packages: List[str] = None,
    use_nixpacks_fallback: bool = False
) -> str:
    """
    Generate a Dockerfile with reliable pip installation
    
    Args:
        python_version: Python Docker image version
        requirements_file: Path to requirements file
        app_dir: Working directory in container
        start_command: Command to start the application
        additional_packages: Additional system packages to install
        use_nixpacks_fallback: Include nixpacks fallback methods
    
    Returns:
        Dockerfile content as string
    """
    
    if start_command is None:
        start_command = ["python3", "app.py"]
    
    if additional_packages is None:
        additional_packages = []
    
    dockerfile_lines = [
        f"FROM python:{python_version}",
        "",
        f"WORKDIR {app_dir}",
        ""
    ]
    
    # Add system packages if needed
    if additional_packages:
        dockerfile_lines.extend([
            "# Install system dependencies",
            "RUN apt-get update && apt-get install -y \\",
            "    " + " \\\n    ".join(additional_packages) + " \\",
            "    && rm -rf /var/lib/apt/lists/*",
            ""
        ])
    
    # Add reliable pip installation
    if use_nixpacks_fallback:
        dockerfile_lines.extend([
            "# Ensure pip is available with multiple fallback methods",
            "RUN python3 -m ensurepip --upgrade || \\",
            "    (curl -sSL https://bootstrap.pypa.io/get-pip.py | python3) || \\",
            "    (apt-get update && apt-get install -y python3-pip)",
            "",
            "# Verify pip installation",
            "RUN python3 -m pip --version",
            ""
        ])
    
    # Copy and install requirements
    dockerfile_lines.extend([
        "# Copy requirements and install dependencies",
        f"COPY {requirements_file} ./",
        "RUN python3 -m pip install --upgrade pip setuptools wheel",
        f"RUN python3 -m pip install --no-cache-dir -r {requirements_file.split('/')[-1]}",
        ""
    ])
    
    # Copy application
    dockerfile_lines.extend([
        "# Copy application code",
        "COPY . .",
        ""
    ])
    
    # Set start command
    cmd_str = '["' + '", "'.join(start_command) + '"]'
    dockerfile_lines.extend([
        "# Start application",
        f"CMD {cmd_str}"
    ])
    
    return "\n".join(dockerfile_lines)


def generate_nixpacks_toml(
    requirements_file: str = "backend/requirements.txt",
    start_command: str = "python3 app.py",
    use_apt: bool = True
) -> str:
    """
    Generate a nixpacks.toml with reliable pip installation
    
    Args:
        requirements_file: Path to requirements file
        start_command: Command to start the application
        use_apt: Use apt packages instead of nix packages
    
    Returns:
        nixpacks.toml content as string
    """
    
    if use_apt:
        config = f'''[phases.setup]
aptPkgs = ["python3", "python3-pip", "python3-dev", "python3-venv", "curl", "build-essential"]
nixPkgs = []

[phases.install]
cmds = [
    "# Multiple fallback methods to ensure pip is available",
    "python3 -m ensurepip --upgrade || echo 'ensurepip failed, continuing...'",
    "curl -sSL https://bootstrap.pypa.io/get-pip.py -o get-pip.py || echo 'curl failed, continuing...'",
    "python3 get-pip.py || echo 'get-pip.py failed, continuing...'",
    "# Verify pip is available",
    "python3 -m pip --version || pip3 --version || pip --version",
    "# Install requirements",
    "python3 -m pip install --upgrade pip setuptools wheel",
    "python3 -m pip install -r {requirements_file}"
]

[start]
cmd = "{start_command}"'''
    else:
        config = f'''[phases.setup]
nixPkgs = ["python311", "python311Packages.pip", "python311Packages.setuptools", "python311Packages.wheel"]

[phases.install]
cmds = [
    "python3 -m pip install --upgrade pip setuptools wheel",
    "python3 -m pip install -r {requirements_file}"
]

[start]
cmd = "{start_command}"'''
    
    return config


def generate_railway_json(use_dockerfile: bool = True, dockerfile_path: str = "Dockerfile") -> str:
    """
    Generate railway.json configuration
    
    Args:
        use_dockerfile: Use Dockerfile builder instead of nixpacks
        dockerfile_path: Path to Dockerfile
    
    Returns:
        railway.json content as string
    """
    
    if use_dockerfile:
        config = f'''{{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {{
    "builder": "DOCKERFILE",
    "dockerfilePath": "./{dockerfile_path}"
  }},
  "deploy": {{
    "healthcheckPath": "/health",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }}
}}'''
    else:
        config = '''{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "healthcheckPath": "/health",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}'''
    
    return config