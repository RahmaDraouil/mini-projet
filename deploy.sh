#!/bin/bash

set -e

echo "============================================"
echo "Employee Management System - Deployment"
echo "============================================"

# Build Docker image
echo "Building Docker image..."
docker build -t employee-app:latest .

# Stop and remove existing containers
echo "Stopping existing containers..."
docker-compose down || true

# Start services
echo "Starting services..."
docker-compose up -d

# Wait for services to be healthy
echo "Waiting for services to be ready..."
sleep 10

# Check service status
echo "Checking service status..."
docker-compose ps

echo "============================================"
echo "Deployment completed successfully!"
echo "Application is running at http://localhost:5000"
echo "============================================"
