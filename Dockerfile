FROM python:3.11-slim

WORKDIR /app

# Install dependencies first (better caching)
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy the rest of the application
COPY . .

# Railway provides PORT automatically
CMD uvicorn backend.server:app --host 0.0.0.0 --port ${PORT:-8000}