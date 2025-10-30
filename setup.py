"""
Setup script for Docker Pip Utils
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="docker-pip-utils",
    version="1.0.0",
    author="Docker Pip Utils",
    author_email="docker-pip-utils@example.com",
    description="Reliable pip installation utilities for Docker environments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/docker-pip-utils/docker-pip-utils",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Installation/Setup",
    ],
    python_requires=">=3.7",
    install_requires=[
        # No external dependencies - uses only standard library
    ],
    entry_points={
        "console_scripts": [
            "docker-pip-utils=docker_pip_utils.cli:main",
        ],
    },
    keywords="docker pip installation deployment nixpacks railway",
    project_urls={
        "Bug Reports": "https://github.com/docker-pip-utils/docker-pip-utils/issues",
        "Source": "https://github.com/docker-pip-utils/docker-pip-utils",
    },
)