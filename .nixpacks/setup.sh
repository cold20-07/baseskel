#!/bin/bash
set -e

# Ensure Python and pip are available
python3 -m ensurepip --upgrade || echo "ensurepip failed, continuing..."

# Create virtual environment
python3 -m venv /opt/venv

# Activate virtual environment and install dependencies
source /opt/venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r backend/requirements.txt