#!/bin/bash

# Docker Build Script for Dr. Kishan Bhalani Medical Documentation Services
# This script builds and optionally runs the Docker container

set -e

echo "🐳 Building Dr. Kishan Bhalani Medical Documentation Services Docker Image..."

# Build the Docker image
docker build -t dr-kishan-medical-services:latest .

echo "✅ Docker image built successfully!"

# Ask if user wants to run the container
read -p "Do you want to run the container now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🚀 Starting container..."
    
    # Stop any existing container
    docker stop dr-kishan-medical 2>/dev/null || true
    docker rm dr-kishan-medical 2>/dev/null || true
    
    # Run the new container
    docker run -d \
        --name dr-kishan-medical \
        -p 8000:8000 \
        -e SUPABASE_URL=https://cwjsyxxzdwphhlpppxau.supabase.co \
        -e SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN3anN5eHh6ZHdwaGhscHBweGF1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE2MzA2MTUsImV4cCI6MjA3NzIwNjYxNX0.7qmRxFhZr_rHwKRp_YaD3HB4D30feclY3xNPipoJvr0 \
        -e CORS_ORIGINS=* \
        -e HIPAA_ENCRYPTION_KEY=bw7Y9P3w4QJFVJatMqu8+gv8mRlWmlhAB7FHLvR8c8M= \
        -e ENVIRONMENT=production \
        -e ALLOWED_HOSTS=* \
        dr-kishan-medical-services:latest
    
    echo "✅ Container started successfully!"
    echo "🌐 Application available at: http://localhost:8000"
    echo "🏥 Health check: http://localhost:8000/api/health"
    echo "📋 Services API: http://localhost:8000/api/services"
    
    # Show container logs
    echo "📋 Container logs:"
    docker logs -f dr-kishan-medical
else
    echo "ℹ️  To run the container later, use:"
    echo "   docker run -d --name dr-kishan-medical -p 8000:8000 dr-kishan-medical-services:latest"
fi