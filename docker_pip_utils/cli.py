#!/usr/bin/env python3
"""
Command-line interface for Docker Pip Utils
"""

import argparse
import sys
from .installer import PipInstaller
from .validator import print_environment_report
from .dockerfile_generator import generate_dockerfile, generate_nixpacks_toml, generate_railway_json


def main():
    parser = argparse.ArgumentParser(
        description="Docker Pip Utils - Reliable pip installation for Docker")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Install command
    install_parser = subparsers.add_parser('install', help='Install pip and packages')
    install_parser.add_argument('-r', '--requirements', default='requirements.txt',
                                help='Requirements file path')
    install_parser.add_argument('--upgrade-pip', action='store_true',
                                help='Upgrade pip before installing packages')

    # Validate command
    subparsers.add_parser('validate', help='Validate environment')

    # Generate command
    generate_parser = subparsers.add_parser('generate', help='Generate configuration files')
    generate_parser.add_argument('--dockerfile', action='store_true',
                                 help='Generate Dockerfile')
    generate_parser.add_argument('--nixpacks', action='store_true',
                                 help='Generate nixpacks.toml')
    generate_parser.add_argument('--railway', action='store_true',
                                 help='Generate railway.json')
    generate_parser.add_argument('--python-version', default='3.9-slim',
                                 help='Python version for Dockerfile')
    generate_parser.add_argument('--requirements-file', default='requirements.txt',
                                 help='Requirements file path')
    generate_parser.add_argument('--start-command', default='python3 app.py',
                                 help='Start command')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == 'install':
        installer = PipInstaller(verbose=True)

        if args.upgrade_pip:
            if not installer.upgrade_pip():
                sys.exit(1)

        if not installer.install_packages(args.requirements):
            sys.exit(1)

        print("✅ Installation completed successfully")

    elif args.command == 'validate':
        print_environment_report()

    elif args.command == 'generate':
        if args.dockerfile:
            dockerfile_content = generate_dockerfile(
                python_version=args.python_version,
                requirements_file=args.requirements_file,
                start_command=args.start_command.split()
            )
            with open('Dockerfile', 'w') as f:
                f.write(dockerfile_content)
            print("✅ Generated Dockerfile")

        if args.nixpacks:
            nixpacks_content = generate_nixpacks_toml(
                requirements_file=args.requirements_file,
                start_command=args.start_command
            )
            with open('nixpacks.toml', 'w') as f:
                f.write(nixpacks_content)
            print("✅ Generated nixpacks.toml")

        if args.railway:
            railway_content = generate_railway_json(use_dockerfile=True)
            with open('railway.json', 'w') as f:
                f.write(railway_content)
            print("✅ Generated railway.json")


if __name__ == '__main__':
    main()
