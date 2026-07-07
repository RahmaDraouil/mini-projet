#!/bin/bash

# Quick setup script for Employee Management System

set -e

echo "========================================="
echo "Employee Management System Setup"
echo "========================================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}Docker is not installed. Please install Docker first.${NC}"
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${YELLOW}Docker Compose is not installed. Please install Docker Compose first.${NC}"
    echo "Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

echo -e "${GREEN}✓ Docker and Docker Compose are installed${NC}"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo -e "${GREEN}✓ Created .env file${NC}"
    echo -e "${YELLOW}⚠ Please edit .env file with your configuration${NC}"
else
    echo -e "${GREEN}✓ .env file already exists${NC}"
fi

# Ask user which mode to run
echo ""
echo "Select deployment mode:"
echo "1) Development (SQLite, debug mode)"
echo "2) Production (MySQL, Docker Compose)"
read -p "Enter choice [1-2]: " choice

case $choice in
    1)
        echo ""
        echo "Setting up for development..."
        
        # Create virtual environment
        if [ ! -d "venv" ]; then
            echo "Creating virtual environment..."
            python3 -m venv venv
            echo -e "${GREEN}✓ Virtual environment created${NC}"
        fi
        
        # Activate virtual environment
        source venv/bin/activate || source venv/Scripts/activate
        
        # Install dependencies
        echo "Installing dependencies..."
        pip install -r requirements.txt
        echo -e "${GREEN}✓ Dependencies installed${NC}"
        
        # Run tests
        echo "Running tests..."
        python -m pytest tests/ -v
        
        echo ""
        echo -e "${GREEN}=========================================${NC}"
        echo -e "${GREEN}Setup complete!${NC}"
        echo -e "${GREEN}=========================================${NC}"
        echo ""
        echo "To start the application:"
        echo "  source venv/bin/activate  # or venv\\Scripts\\activate on Windows"
        echo "  python app.py"
        echo ""
        echo "Access the application at: http://localhost:5000"
        ;;
        
    2)
        echo ""
        echo "Setting up for production with Docker..."
        
        # Build and start containers
        echo "Building Docker images..."
        docker-compose build
        echo -e "${GREEN}✓ Docker images built${NC}"
        
        echo "Starting containers..."
        docker-compose up -d
        echo -e "${GREEN}✓ Containers started${NC}"
        
        # Wait for services
        echo "Waiting for services to start..."
        sleep 10
        
        # Check status
        echo ""
        echo "Container status:"
        docker-compose ps
        
        echo ""
        echo -e "${GREEN}=========================================${NC}"
        echo -e "${GREEN}Setup complete!${NC}"
        echo -e "${GREEN}=========================================${NC}"
        echo ""
        echo "Application is running at: http://localhost:5000"
        echo ""
        echo "Useful commands:"
        echo "  docker-compose logs -f       # View logs"
        echo "  docker-compose down          # Stop containers"
        echo "  docker-compose restart       # Restart containers"
        echo "  docker-compose ps            # Check status"
        ;;
        
    *)
        echo -e "${YELLOW}Invalid choice. Exiting.${NC}"
        exit 1
        ;;
esac
