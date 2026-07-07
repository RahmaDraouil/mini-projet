#!/bin/bash

# Deployment script for Employee Management System
# This script is called by GitHub Actions during deployment

set -e  # Exit on error

echo "========================================="
echo "Starting deployment process..."
echo "========================================="

# Configuration
APP_DIR="/path/to/your/app"
BACKUP_DIR="/path/to/backups"
COMPOSE_FILE="docker-compose.yml"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Create backup
backup_database() {
    log_info "Creating database backup..."
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    BACKUP_FILE="${BACKUP_DIR}/db_backup_${TIMESTAMP}.sql"
    
    mkdir -p "${BACKUP_DIR}"
    
    docker-compose exec -T mysql mysqldump -u user -ppassword employee_db > "${BACKUP_FILE}" || {
        log_warn "Database backup failed, continuing anyway..."
    }
    
    log_info "Backup created: ${BACKUP_FILE}"
}

# Navigate to app directory
cd "${APP_DIR}" || {
    log_error "Failed to navigate to ${APP_DIR}"
    exit 1
}

# Backup database before deployment
backup_database

# Pull latest code
log_info "Pulling latest code..."
git fetch origin
git reset --hard origin/main

# Pull latest Docker images
log_info "Pulling Docker images..."
docker-compose pull

# Stop existing containers
log_info "Stopping existing containers..."
docker-compose down

# Start new containers
log_info "Starting new containers..."
docker-compose up -d

# Wait for services to be healthy
log_info "Waiting for services to become healthy..."
sleep 10

# Check if services are running
if docker-compose ps | grep -q "Up"; then
    log_info "Deployment successful!"
    
    # Show running containers
    log_info "Running containers:"
    docker-compose ps
    
    # Show recent logs
    log_info "Recent logs:"
    docker-compose logs --tail=20
    
    # Cleanup old images
    log_info "Cleaning up old Docker images..."
    docker image prune -f
    
    echo "========================================="
    echo -e "${GREEN}Deployment completed successfully!${NC}"
    echo "========================================="
else
    log_error "Deployment failed! Services are not running."
    log_error "Attempting rollback..."
    
    # Show error logs
    docker-compose logs --tail=50
    
    # Rollback to previous version
    git reset --hard HEAD~1
    docker-compose up -d
    
    exit 1
fi
