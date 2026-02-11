#!/bin/bash

# Ensure the script stops on first error
set -e

# Print colorful messages
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}Running RAG Gateway Service tests...${NC}"

# Check if Python virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${BLUE}Creating Python virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies if needed
if [ ! -f "venv/.dependencies_installed" ]; then
    echo -e "${BLUE}Installing dependencies...${NC}"
    pip install -r requirements.txt
    touch venv/.dependencies_installed
fi

# Run tests with coverage
echo -e "${BLUE}Running test suite...${NC}"
pytest tests/ -v --cov=app --cov-report=term-missing

# Check if tests passed
if [ $? -eq 0 ]; then
    echo -e "${GREEN}All tests passed successfully!${NC}"
else
    echo -e "${RED}Some tests failed. Please check the output above.${NC}"
    exit 1
fi

# Deactivate virtual environment
deactivate 