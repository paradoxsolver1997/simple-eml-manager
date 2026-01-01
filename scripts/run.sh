#!/bin/bash

# Set color
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# show title
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}        EML Search Server starts${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Set the working directory to the directory where the script is located
cd "$(dirname "$0")"

# examine Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[Error] Python3. ${NC}"
    echo "Install Python 3.8+ first"
    echo "Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "CentOS/RHEL: sudo yum install python3 python3-pip"
    echo "macOS: brew install python"
    echo "Download address: https://www.python.org"
    read -p "according to Enter key to exit..."
    exit 1
fi

# show Python Version
python_version=$(python3 --version 2>&1)
echo -e "${BLUE}[Info] $python_version${NC}"

# Check virtual environment
if [ -d "../.venv" ]; then
    echo -e "${BLUE}[Info] Activate virtual environment...${NC}"
    source ../.venv/bin/activate
else
    echo -e "${YELLOW}[Warning] Virtual environment not found. Use the systemPython${NC}"
fi

# Check whether the port is occupied
if netstat -tuln 2>/dev/null | grep -q ":8000 "; then
    echo -e "${YELLOW}[Warning] port8000Already occupied. ${NC}"
    echo "Please stop the program occupying the port first. or use another port"
    read -p "according to Enter key to exit..."
    exit 1
fi

echo ""
echo -e "${BLUE}[Info] starting up FastAPI server...${NC}"
echo -e "${GREEN}[Frontend] http://localhost:8000${NC}"
echo ""
echo "Press Ctrl+C to stop the server"
echo -e "${GREEN}========================================${NC}"
echo ""

# Start the server
cd .. && uvicorn backend.main:app --reload --port 8000 --host 0.0.0.0

# Check exit status
if [ $? -eq 0 ]; then
    echo -e "${BLUE}[Info] Server exits normally${NC}"
else
    echo -e "${RED}[Error] Server startup failed${NC}"
fi

read -p "Press Enter key to exit..."