#!/usr/bin/env python3
"""
Example usage of Docker Pip Utils
"""

from docker_pip_utils import PipInstaller, validate_environment, print_environment_report
from docker_pip_utils import generate_dockerfile, generate_nixpacks_toml, generate_railway_json


def main():
    print("🐳 Docker Pip Utils - Example Usage")
    print("=" * 50)
    
    # 1. Validate current environment
    print("\n1. Environment Validation:")
    print_environment_report()
    
    # 2. Ensure pip is available
    print("\n2. Ensuring pip is available:")
    installer = PipInstaller(verbose=True)
    
    try:
        if installer.ensure_pip():
            print("✅ pip is ready to use!")
            
            # Upgrade pip
            installer.upgrade_pip()
            
            # Install packages (if requirements.txt exists)
            import os
            if os.path.exists("backend/requirements.txt"):
                installer.install_packages("backend/requirements.txt")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 3. Generate configuration files
    print("\n3. Generating configuration files:")
    
    # Generate Dockerfile
    dockerfile_content = generate_dockerfile(
        python_version="3.9-slim",
        requirements_file="backend/requirements.txt",
        start_command=["python3", "backend/run_server.py"],
        use_nixpacks_fallback=True
    )
    
    with open("generated_Dockerfile", "w") as f:
        f.write(dockerfile_content)
    print("✅ Generated Dockerfile -> generated_Dockerfile")
    
    # Generate nixpacks.toml
    nixpacks_content = generate_nixpacks_toml(
        requirements_file="backend/requirements.txt",
        start_command="python3 backend/run_server.py",
        use_apt=True
    )
    
    with open("generated_nixpacks.toml", "w") as f:
        f.write(nixpacks_content)
    print("✅ Generated nixpacks.toml -> generated_nixpacks.toml")
    
    # Generate railway.json
    railway_content = generate_railway_json(use_dockerfile=True)
    
    with open("generated_railway.json", "w") as f:
        f.write(railway_content)
    print("✅ Generated railway.json -> generated_railway.json")
    
    print("\n🎉 Example completed successfully!")
    print("\nGenerated files:")
    print("- generated_Dockerfile")
    print("- generated_nixpacks.toml") 
    print("- generated_railway.json")


if __name__ == "__main__":
    main()