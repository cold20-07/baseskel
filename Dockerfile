FROM python:3.11-slim

WORKDIR /app

# Ensure pip is available with multiple methods
RUN python3 -m ensurepip --upgrade || \
    (curl -sSL https://bootstrap.pypa.io/get-pip.py | python3) || \
    apt-get update && apt-get install -y python3-pip

# Verify pip installation
RUN python3 -m pip --version

# Copy and install dependencies
COPY backend/requirements.txt ./backend/requirements.txt
RUN python3 -m pip install --no-cache-dir --upgrade pip setuptools wheel
RUN python3 -m pip install --no-cache-dir -r backend/requirements.txt

# Copy application
COPY . .

# Start command
CMD ["python3", "backend/run_server.py"]