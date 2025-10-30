FROM python:3.11-slim

WORKDIR /app

# Copy and install dependencies
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy application
COPY . .

# Start command
CMD ["python3", "backend/run_server.py"]