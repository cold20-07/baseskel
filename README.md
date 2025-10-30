# Docker Pip Utils

A comprehensive Python utility module for reliable pip installation in Docker environments, specifically designed to solve the common "No module named pip" error in nixpacks and other containerized environments.

## Features

- 🔧 **Multiple Fallback Methods**: Tries ensurepip, get-pip.py, and apt-get installation
- 🐳 **Docker-Optimized**: Works with official Python images, nixpacks, and custom environments
- 🚀 **Railway/Deployment Ready**: Includes configuration generators for Railway, nixpacks, and Docker
- 📊 **Environment Validation**: Comprehensive environment analysis and recommendations
- 🛠️ **CLI Interface**: Easy-to-use command-line tools
- 📦 **Zero Dependencies**: Uses only Python standard library

## Quick Start

### Installation

```bash
pip install docker-pip-utils
```

### Basic Usage

```python
from docker_pip_utils import PipInstaller

# Create installer instance
installer = PipInstaller(verbose=True)

# Ensure pip is available
installer.ensure_pip()

# Install packages from requirements.txt
installer.install_packages("requirements.txt")
```

### Command Line Interface

```bash
# Validate current environment
docker-pip-utils validate

# Install packages with pip fallbacks
docker-pip-utils install -r requirements.txt --upgrade-pip

# Generate configuration files
docker-pip-utils generate --dockerfile --railway --nixpacks
```

## Problem Solved

This module specifically addresses the common Docker deployment error:

```
/root/.nix-profile/bin/python3: No module named pip
```

This error occurs when:
- Using nixpacks with incomplete Python packages
- Working with minimal Python Docker images
- Deploying to platforms like Railway with auto-detection issues

## Core Components

### 1. PipInstaller

Reliable pip installation with multiple fallback methods:

```python
from docker_pip_utils import PipInstaller

installer = PipInstaller(verbose=True)

# This will try multiple methods until pip is available
if installer.ensure_pip():
    installer.install_packages("requirements.txt")
```

### 2. Environment Validator

Analyze your environment and get recommendations:

```python
from docker_pip_utils import validate_environment, print_environment_report

# Get detailed environment info
results = validate_environment()

# Print comprehensive report
print_environment_report()
```

### 3. Configuration Generators

Generate optimized configuration files:

```python
from docker_pip_utils import generate_dockerfile, generate_nixpacks_toml

# Generate Dockerfile with reliable pip installation
dockerfile = generate_dockerfile(
    python_version="3.9-slim",
    requirements_file="requirements.txt",
    start_command=["python3", "app.py"]
)

# Generate nixpacks.toml with fallback methods
nixpacks = generate_nixpacks_toml(
    requirements_file="backend/requirements.txt",
    start_command="python3 backend/run_server.py"
)
```

## Installation Methods

The module tries these methods in order:

1. **Check Existing**: Verify if pip is already available
2. **ensurepip**: Use Python's built-in pip installer
3. **get-pip.py**: Download and run the official pip installer
4. **apt-get**: Install via system package manager (Ubuntu/Debian)

## Configuration Examples

### Dockerfile (Recommended)

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY . /app/

RUN python3 -m pip install --upgrade pip setuptools wheel
RUN python3 -m pip install -r requirements.txt

CMD ["python3", "app.py"]
```

### nixpacks.toml (Alternative)

```toml
[phases.setup]
aptPkgs = ["python3", "python3-pip", "python3-dev", "curl", "build-essential"]
nixPkgs = []

[phases.install]
cmds = [
    "python3 -m ensurepip --upgrade || echo 'ensurepip failed'",
    "curl -sSL https://bootstrap.pypa.io/get-pip.py | python3 || echo 'get-pip failed'",
    "python3 -m pip install --upgrade pip setuptools wheel",
    "python3 -m pip install -r requirements.txt"
]

[start]
cmd = "python3 app.py"
```

### railway.json

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "./Dockerfile"
  },
  "deploy": {
    "healthcheckPath": "/health",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

## Environment Detection

The module automatically detects:

- **Nix environments** (`/nix/store` in Python path)
- **Nixpacks environments** (`.nixpacks` directory)
- **Docker containers** (`/.dockerenv` file)
- **Ubuntu/Debian systems** (apt availability)

## Best Practices

1. **Use Official Python Images**: `python:3.9-slim` has pip pre-installed
2. **Avoid Nixpacks for Python**: Use Dockerfile approach when possible
3. **Multiple Fallbacks**: Always have backup installation methods
4. **Validate Environment**: Check your environment before deployment

## Troubleshooting

### Common Issues

**"No module named pip"**
- Use `docker-pip-utils validate` to analyze your environment
- Try `docker-pip-utils install` with fallback methods

**Nixpacks Detection Issues**
- Create `.nixpacksignore` with `*` to disable nixpacks
- Use `railway.json` with `"builder": "DOCKERFILE"`

**Permission Errors**
- Ensure Docker container has proper permissions
- Use `--user root` in Docker commands if needed

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details.

## Support

- 📧 Email: docker-pip-utils@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/docker-pip-utils/docker-pip-utils/issues)
- 📖 Documentation: [GitHub Wiki](https://github.com/docker-pip-utils/docker-pip-utils/wiki)