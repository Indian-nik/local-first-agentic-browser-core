# CyberCore Installation Guide

Comprehensive installation instructions for CyberCore v6.0 across all supported platforms.

## Table of Contents

- [Quick Start](#quick-start)
- [Prerequisites](#prerequisites)
- [Installation Methods](#installation-methods)
  - [Method 1: From Source (Recommended)](#method-1-from-source-recommended)
  - [Method 2: Using pip](#method-2-using-pip)
  - [Method 3: Using Docker](#method-3-using-docker)
  - [Method 4: Using Docker Compose](#method-4-using-docker-compose)
- [Platform-Specific Instructions](#platform-specific-instructions)
  - [Linux](#linux)
  - [macOS](#macos)
  - [Windows](#windows)
- [Verification](#verification)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Upgrading](#upgrading)
- [Uninstallation](#uninstallation)

## Quick Start

### Linux / macOS

```bash
# Clone or extract the repository
cd cybercore

# Run the installer
./install.sh
```

### Windows

```cmd
REM Open Command Prompt or PowerShell
cd cybercore

REM Run the installer
install.bat
```

## Prerequisites

### Required

- **Python**: 3.11 or higher
- **pip**: Latest version (comes with Python)
- **Virtual Environment**: Recommended (venv)

### Recommended

- **Git**: For cloning the repository
- **Docker**: For containerized deployments
- **Docker Compose**: For multi-service deployments

### System Requirements

- **Memory**: Minimum 4GB RAM (8GB recommended)
- **Disk Space**: Minimum 1GB free space
- **Network**: Internet connection for package downloads

## Installation Methods

### Method 1: From Source (Recommended)

This method gives you the most control and is recommended for development.

#### Linux / macOS

```bash
# Navigate to project directory
cd cybercore

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install CyberCore
pip install -e .

# Verify installation
cybercore --version
```

#### Windows

```cmd
REM Navigate to project directory
cd cybercore

REM Create virtual environment
python -m venv venv

REM Activate virtual environment
venv\Scripts\activate.bat

REM Upgrade pip
python -m pip install --upgrade pip setuptools wheel

REM Install CyberCore
pip install -e .

REM Verify installation
cybercore --version
```

### Method 2: Using pip

```bash
# Install from source directory
pip install .

# Or install with all extras
pip install .[full]

# Or install development dependencies
pip install .[dev]
```

### Method 3: Using Docker

```bash
# Build Docker image
docker build -t cybercore:6.0 .

# Run container
docker run -it --rm cybercore:6.0 cybercore --help

# Run with mounted config
docker run -it --rm -v $(pwd)/config:/app/config cybercore:6.0
```

### Method 4: Using Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Platform-Specific Instructions

### Linux

#### Ubuntu / Debian

```bash
# Install Python 3.11+
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip

# Install system dependencies
sudo apt install build-essential libssl-dev libffi-dev

# Run installation
./install.sh
```

#### Fedora / RHEL

```bash
# Install Python 3.11+
sudo dnf install python3.11 python3-pip

# Install system dependencies
sudo dnf groupinstall "Development Tools"
sudo dnf install openssl-devel libffi-devel

# Run installation
./install.sh
```

### macOS

#### Using Homebrew (Recommended)

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.11+
brew install python@3.11

# Verify Python installation
python3 --version

# Run installation
./install.sh
```

#### Using Official Python Installer

1. Download Python 3.11+ from [python.org](https://www.python.org/downloads/macos/)
2. Install the package
3. Open Terminal and navigate to CyberCore directory
4. Run `./install.sh`

### Windows

#### Using Official Installer

1. Download Python 3.11+ from [python.org](https://www.python.org/downloads/windows/)
2. Run the installer
   - **Important**: Check "Add Python to PATH"
3. Open Command Prompt or PowerShell
4. Navigate to CyberCore directory
5. Run `install.bat`

#### Using Microsoft Store

1. Open Microsoft Store
2. Search for "Python 3.11"
3. Install Python
4. Open Command Prompt or PowerShell
5. Navigate to CyberCore directory
6. Run `install.bat`

## Verification

After installation, verify that CyberCore is working correctly:

```bash
# Check version
cybercore --version

# Run help
cybercore --help

# Run a simple scan (example)
cybercore scan --target localhost --type basic

# Start API server
cybercore-api
# API will be available at http://localhost:8000

# Test DSPY optimizer
cybercore-optimize --help
```

### Running Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run with coverage
pytest --cov=cybercore --cov-report=html

# Run specific test module
pytest tests/unit/test_core.py
```

## Configuration

### Configuration File

CyberCore uses YAML configuration files located in `config/` directory.

```bash
# Copy example configuration
cp config/config.example.yaml config/config.yaml

# Edit configuration
nano config/config.yaml  # or vim, code, etc.
```

### Environment Variables

```bash
# Set CyberCore home directory
export CYBERCORE_HOME=/path/to/cybercore

# Set log level
export CYBERCORE_LOG_LEVEL=INFO

# Set API port
export CYBERCORE_API_PORT=8000
```

### Database Setup

```bash
# Initialize database
cybercore db init

# Run migrations
cybercore db migrate

# Create admin user
cybercore user create --admin
```

## Troubleshooting

### Common Issues

#### Python Version Error

**Error**: `Python 3.11+ required (found 3.9)`

**Solution**:
- Install Python 3.11 or higher
- Make sure it's in your PATH
- Use `python3.11` explicitly if you have multiple versions

#### Permission Denied

**Error**: `Permission denied: './install.sh'`

**Solution**:
```bash
chmod +x install.sh
./install.sh
```

#### Module Not Found

**Error**: `ModuleNotFoundError: No module named 'cybercore'`

**Solution**:
- Make sure virtual environment is activated
- Reinstall: `pip install -e .`
- Check Python path: `python -c "import sys; print(sys.path)"`

#### Port Already in Use

**Error**: `Port 8000 is already in use`

**Solution**:
```bash
# Find process using port
lsof -i :8000  # Linux/macOS
netstat -ano | findstr :8000  # Windows

# Kill the process or use different port
export CYBERCORE_API_PORT=8080
cybercore-api
```

#### SSL Certificate Errors

**Error**: `SSL: CERTIFICATE_VERIFY_FAILED`

**Solution**:
```bash
# Install certificates (macOS)
/Applications/Python\ 3.11/Install\ Certificates.command

# Or use pip with trusted host
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -e .
```

### Getting Help

- Check the [Documentation](docs/README.md)
- View [Examples](docs/examples/)
- Report issues on [GitHub Issues](https://github.com/cybercore/cybercore/issues)
- Join our [Discord Community](https://discord.gg/cybercore)

## Upgrading

### From Source

```bash
# Pull latest changes
git pull origin main

# Upgrade dependencies
pip install --upgrade -e .

# Run database migrations
cybercore db migrate

# Restart services
sudo systemctl restart cybercore-api
```

### Using pip

```bash
# Upgrade to latest version
pip install --upgrade cybercore

# Or upgrade with extras
pip install --upgrade cybercore[full]
```

## Uninstallation

### Remove Package

```bash
# Deactivate virtual environment if active
deactivate

# Uninstall CyberCore
pip uninstall cybercore

# Remove virtual environment
rm -rf venv

# Remove configuration (optional)
rm -rf config

# Remove data (optional)
rm -rf data
```

### Clean Docker

```bash
# Stop and remove containers
docker-compose down -v

# Remove images
docker rmi cybercore:6.0

# Clean up volumes
docker volume prune
```

---

## Additional Resources

- **Quick Start Guide**: [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md)
- **User Guide**: [docs/guides/USER_GUIDE.md](docs/guides/USER_GUIDE.md)
- **API Documentation**: [docs/api/API_REFERENCE.md](docs/api/API_REFERENCE.md)
- **Developer Guide**: [docs/guides/DEVELOPER_GUIDE.md](docs/guides/DEVELOPER_GUIDE.md)
- **Architecture**: [docs/architecture/ARCHITECTURE.md](docs/architecture/ARCHITECTURE.md)

## Support

For commercial support and enterprise deployments:
- Email: enterprise@cybercore.dev
- Website: https://cybercore.dev

---

**CyberCore v6.0** | Autonomous Security Testing Framework
