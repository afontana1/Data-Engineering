#!/bin/bash

# Ensure the script stops on first error
set -e

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Print colorful messages
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting RAG Gateway Service...${NC}"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker and try again."
    exit 1
fi

# Build and start the services
echo -e "${BLUE}Building and starting services...${NC}"
docker-compose up --build -d

# Wait for services to be ready
echo -e "${BLUE}Waiting for services to be ready...${NC}"
sleep 5

# Check if services are running
if docker-compose ps | grep -q "Exit"; then
    echo "Error: One or more services failed to start. Check logs with 'docker-compose logs'"
    exit 1
fi

echo -e "${GREEN}RAG Gateway Service is running!${NC}"
echo -e "${GREEN}Gateway API: http://localhost:${GATEWAY_PORT:-8000}${NC}"
echo -e "${GREEN}API Documentation: http://localhost:${GATEWAY_PORT:-8000}/docs${NC}"
echo -e "${BLUE}To view logs: docker-compose logs -f${NC}"
echo -e "${BLUE}To stop services: docker-compose down${NC}" 