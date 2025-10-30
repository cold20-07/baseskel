FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY backend/requirements.txt ./backend/requirements.txt

# Install pip first (ensure it's available)
RUN python3 -m ensurepip --upgrade

# Install Python dependencies
RUN python3 -m pip install --upgrade pip setuptools wheel
RUN python3 -m pip install --no-cache-dir -r backend/requirements.txt

# Copy the rest of the application
COPY . .

# Expose port
EXPOSE 8000

# Start the application
CMD ["python3", "backend/run_server.py"]