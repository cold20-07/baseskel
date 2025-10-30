# Multi-stage Docker build for Dr. Kishan Bhalani Medical Documentation Services

# Stage 1: Build frontend
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy package files
COPY frontend/package*.json ./

# Install dependencies with legacy peer deps to handle conflicts
RUN npm ci --legacy-peer-deps

# Copy frontend source code
COPY frontend/ ./

# Build the frontend
RUN npm run build

# Stage 2: Backend with frontend assets
FROM python:3.11-slim

# Install system dependencies including curl for health checks
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy backend requirements and install Python dependencies
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Copy built frontend assets
COPY --from=frontend-builder /app/frontend/build ./frontend/build

# Create uploads directory
RUN mkdir -p backend/uploads/{medical_record,service_record,photo,document,other}

# Set environment variables
ENV PYTHONPATH=/app/backend
ENV PORT=8000
ENV ENVIRONMENT=production

# Expose both common ports (Railway might use 8080)
EXPOSE 8000
EXPOSE 8080

# Health check that works with dynamic port
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT}/api/health || curl -f http://localhost:8000/api/health || curl -f http://localhost:8080/api/health || exit 1

# Start the application
CMD ["python", "backend/run_server.py"]