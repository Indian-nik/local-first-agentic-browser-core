#!/bin/bash
set -e

echo "======================================"
echo "  CyberCore Installation Script"
echo "  Cross-Platform Security Framework"
echo "======================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check Python version
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    echo "Please install Python 3.11 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓ Python $PYTHON_VERSION detected${NC}"

# Check if version is 3.11+
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 11 ]); then
    echo -e "${RED}Error: Python 3.11+ required (found $PYTHON_VERSION)${NC}"
    exit 1
fi

echo ""
echo "Installation Options:"
echo "  1. Install in virtual environment (recommended)"
echo "  2. Install system-wide (requires sudo)"
echo "  3. Install in development mode"
echo ""
read -p "Choose option [1-3]: " option

case $option in
    1)
        echo -e "${YELLOW}Installing in virtual environment...${NC}"
        python3 -m venv venv
        source venv/bin/activate
        pip install --upgrade pip setuptools wheel
        pip install -e .
        echo ""
        echo -e "${GREEN}✓ Installation complete!${NC}"
        echo ""
        echo "To activate the environment, run:"
        echo "  source venv/bin/activate"
        echo ""
        echo "Then you can use:"
        echo "  cybercore --help"
        echo "  cybercore-api"
        echo "  cybercore-optimize"
        ;;
    2)
        echo -e "${YELLOW}Installing system-wide...${NC}"
        sudo pip3 install -e .
        echo ""
        echo -e "${GREEN}✓ Installation complete!${NC}"
        echo ""
        echo "You can now use:"
        echo "  cybercore --help"
        echo "  cybercore-api"
        echo "  cybercore-optimize"
        ;;
    3)
        echo -e "${YELLOW}Installing in development mode...${NC}"
        python3 -m venv venv
        source venv/bin/activate
        pip install --upgrade pip setuptools wheel
        pip install -e ".[dev,docs]"
        echo ""
        echo -e "${GREEN}✓ Development installation complete!${NC}"
        echo ""
        echo "To activate the environment, run:"
        echo "  source venv/bin/activate"
        echo ""
        echo "Development tools installed:"
        echo "  - pytest, black, flake8, mypy"
        echo "  - sphinx for documentation"
        ;;
    *)
        echo -e "${RED}Invalid option${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}For more information, see INSTALL.md${NC}"
