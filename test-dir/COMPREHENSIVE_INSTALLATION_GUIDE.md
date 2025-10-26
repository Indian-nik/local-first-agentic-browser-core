
## 4. Installation Steps

### 4.1 Quick Installation Summary

| Platform | Quick Command |
|----------|---------------|
| Windows | `install.bat` or `pip install -e .` |
| macOS | `./install.sh` or `brew install cybercore` |
| Linux | `./install.sh` or `snap install cybercore` |
| All | `conda install -c conda-forge cybercore` |

### 4.2 Windows Installation

#### Method 1: Automated Installer (Recommended)

**Step 1: Download CyberCore**
```powershell
# Option A: Download from GitHub Releases
# Visit: https://github.com/cybercore/cybercore/releases/latest
# Download: cybercore-6.0.0.zip

# Option B: Clone from Git
git clone https://github.com/cybercore/cybercore.git
cd cybercore
```

**Step 2: Run the Installer**
```cmd
REM Right-click install.bat and select "Run as Administrator" (optional)
REM Or open Command Prompt and run:
install.bat
```

**Step 3: Choose Installation Option**
- **Option 1**: Virtual environment (recommended for most users)
- **Option 2**: System-wide (requires administrator privileges)
- **Option 3**: Development mode (for contributors)

**Step 4: Wait for Installation**
The installer will:
1. Check Python version
2. Create virtual environment (if selected)
3. Install all dependencies
4. Configure entry points
5. Verify installation

**Step 5: Verify Installation**
```cmd
REM If virtual environment was used:
venv\Scripts\activate.bat

REM Test the installation:
cybercore --version
cybercore --help
```

#### Method 2: Using Chocolatey

**Step 1: Install Chocolatey** (if not already installed)
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

**Step 2: Install CyberCore**
```powershell
choco install cybercore -y
```

**Step 3: Verify Installation**
```powershell
cybercore --version
```

#### Method 3: Using pip (Manual)

**Step 1: Download Source**
```powershell
git clone https://github.com/cybercore/cybercore.git
cd cybercore
```

**Step 2: Create Virtual Environment**
```powershell
python -m venv venv
venv\Scripts\activate.bat
```

**Step 3: Install**
```powershell
python -m pip install --upgrade pip setuptools wheel
pip install -e .
```

**Step 4: Verify**
```powershell
cybercore --version
```

#### Screenshots for Windows

*[Screenshot 1: Running install.bat]*
- Show Command Prompt with install.bat running
- Display installation progress

*[Screenshot 2: Installation Options Menu]*
- Show the three installation options

*[Screenshot 3: Successful Installation]*
- Show "Installation complete!" message
- Display cybercore --version output

### 4.3 macOS Installation

#### Method 1: Using Homebrew (Recommended)

**Step 1: Install Homebrew** (if not already installed)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Step 2: Install CyberCore**
```bash
brew install cybercore
```

**Step 3: Verify Installation**
```bash
cybercore --version
cybercore --help
```

#### Method 2: Automated Installer

**Step 1: Download CyberCore**
```bash
# Option A: Download from GitHub
curl -LO https://github.com/cybercore/cybercore/archive/refs/tags/v6.0.0.tar.gz
tar -xzf v6.0.0.tar.gz
cd cybercore-6.0.0

# Option B: Clone repository
git clone https://github.com/cybercore/cybercore.git
cd cybercore
```

**Step 2: Make Installer Executable**
```bash
chmod +x install.sh
```

**Step 3: Run Installer**
```bash
./install.sh
```

**Step 4: Select Installation Type**
- **Option 1**: Virtual environment (recommended)
- **Option 2**: System-wide (requires sudo)
- **Option 3**: Development mode

**Step 5: Activate Environment** (if using virtual environment)
```bash
source venv/bin/activate
```

**Step 6: Verify Installation**
```bash
cybercore --version
```

#### Method 3: Using pip (Manual)

**Step 1: Install Python 3.11+**
```bash
# Using Homebrew:
brew install python@3.11

# Or download from python.org
```

**Step 2: Clone Repository**
```bash
git clone https://github.com/cybercore/cybercore.git
cd cybercore
```

**Step 3: Create Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Step 4: Install Dependencies**
```bash
pip install --upgrade pip setuptools wheel
pip install -e .
```

**Step 5: Verify**
```bash
cybercore --version
cybercore scan --help
```

#### Screenshots for macOS

*[Screenshot 1: Terminal with install.sh]*
- Show installation script running
- Colorful output with progress indicators

*[Screenshot 2: Installation Menu]*
- Display three installation options

*[Screenshot 3: Successful Installation]*
- Green checkmark and success message
- Version verification output

### 4.4 Linux Installation

#### Method 1: Using Snap (Ubuntu/Debian)

**Step 1: Install Snap** (if not already installed)
```bash
sudo apt update
sudo apt install snapd
```

**Step 2: Install CyberCore**
```bash
sudo snap install cybercore
```

**Step 3: Verify Installation**
```bash
cybercore --version
```

#### Method 2: Automated Installer

**Ubuntu/Debian:**

**Step 1: Install Prerequisites**
```bash
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3-pip git
sudo apt install -y build-essential libssl-dev libffi-dev python3-dev
```

**Step 2: Download CyberCore**
```bash
git clone https://github.com/cybercore/cybercore.git
cd cybercore
```

**Step 3: Run Installer**
```bash
chmod +x install.sh
./install.sh
```

**Step 4: Follow Prompts**
- Choose installation type (1, 2, or 3)
- Wait for installation to complete

**Step 5: Activate Environment** (if virtual environment)
```bash
source venv/bin/activate
```

**Step 6: Verify**
```bash
cybercore --version
```

**Fedora/RHEL:**

**Step 1: Install Prerequisites**
```bash
sudo dnf install -y python3.11 python3-pip git
sudo dnf groupinstall -y "Development Tools"
sudo dnf install -y openssl-devel libffi-devel python3-devel
```

**Step 2-6**: Same as Ubuntu/Debian steps above

#### Method 3: Using Package Manager (Distribution-Specific)

**Ubuntu/Debian (APT):**
```bash
# Add CyberCore PPA (if available)
sudo add-apt-repository ppa:cybercore/stable
sudo apt update
sudo apt install cybercore
```

**Fedora/RHEL (DNF):**
```bash
# Add CyberCore repository (if available)
sudo dnf config-manager --add-repo https://repo.cybercore.dev/fedora
sudo dnf install cybercore
```

**Arch Linux (AUR):**
```bash
git clone https://aur.archlinux.org/cybercore.git
cd cybercore
makepkg -si
```

#### Screenshots for Linux

*[Screenshot 1: Terminal Installation Process]*
- Show color-coded installation output
- Progress indicators

*[Screenshot 2: Installation Options]*
- Three-option menu

*[Screenshot 3: Success Message]*
- Green success indicators
- Version information

### 4.5 Docker Installation (All Platforms)

**Step 1: Install Docker**
- Windows: Docker Desktop from https://www.docker.com/
- macOS: Docker Desktop from https://www.docker.com/
- Linux: `sudo apt install docker.io` or equivalent

**Step 2: Pull CyberCore Image**
```bash
docker pull cybercore/cybercore:6.0
```

**Step 3: Run Container**
```bash
# Interactive mode:
docker run -it --rm cybercore/cybercore:6.0 cybercore --help

# With mounted config:
docker run -it --rm -v $(pwd)/config:/app/config cybercore/cybercore:6.0

# Run API server:
docker run -d -p 8000:8000 --name cybercore-api cybercore/cybercore:6.0 cybercore-api
```

**Step 4: Verify**
```bash
docker run --rm cybercore/cybercore:6.0 cybercore --version
```

### 4.6 Using Docker Compose

**Step 1: Create docker-compose.yml**
```yaml
version: '3.8'

services:
  cybercore-api:
    image: cybercore/cybercore:6.0
    command: cybercore-api
    ports:
      - "8000:8000"
    volumes:
      - ./config:/app/config
      - ./data:/app/data
    environment:
      - CYBERCORE_LOG_LEVEL=INFO
    restart: unless-stopped

  cybercore-optimizer:
    image: cybercore/cybercore:6.0
    command: cybercore-optimize --daemon
    volumes:
      - ./data:/app/data
    depends_on:
      - cybercore-api
    restart: unless-stopped
```

**Step 2: Start Services**
```bash
docker-compose up -d
```

**Step 3: Check Status**
```bash
docker-compose ps
docker-compose logs -f
```

**Step 4: Stop Services**
```bash
docker-compose down
```

---

## 5. Post-Installation Configuration

### 5.1 Initial Setup

**Step 1: Verify Installation**
```bash
# Check version
cybercore --version

# Run help
cybercore --help

# List available commands
cybercore --commands
```

**Step 2: Configure Environment Variables** (Optional)

**Windows:**
```powershell
# Add to system PATH (PowerShell as Administrator)
[Environment]::SetEnvironmentVariable("CYBERCORE_HOME", "C:\\cybercore", "Machine")
[Environment]::SetEnvironmentVariable("CYBERCORE_LOG_LEVEL", "INFO", "User")
```

**Linux/macOS:**
```bash
# Add to ~/.bashrc or ~/.zshrc
export CYBERCORE_HOME="$HOME/cybercore"
export CYBERCORE_LOG_LEVEL="INFO"
export CYBERCORE_API_PORT=8000

# Apply changes
source ~/.bashrc  # or source ~/.zshrc
```

### 5.2 Configuration File Setup

**Step 1: Create Configuration Directory**
```bash
mkdir -p ~/.cybercore/config
```

**Step 2: Copy Example Configuration**
```bash
cp config/config.example.yaml ~/.cybercore/config/config.yaml
```

**Step 3: Edit Configuration**
```yaml
# ~/.cybercore/config/config.yaml
general:
  log_level: INFO
  data_dir: ~/.cybercore/data
  cache_dir: ~/.cybercore/cache

api:
  host: 0.0.0.0
  port: 8000
  workers: 4
  reload: false

dspy:
  optimization_interval: 3600  # 1 hour
  metrics_retention: 7  # days
  auto_optimize: true

security:
  scan_timeout: 300  # seconds
  max_concurrent_scans: 5
  report_format: json
```

### 5.3 Database Initialization

```bash
# Initialize database
cybercore db init

# Run migrations
cybercore db migrate

# Create admin user (optional)
cybercore user create --admin --username admin --email admin@example.com
```

### 5.4 API Server Setup

**Start API Server:**
```bash
# Development mode (auto-reload)
cybercore-api --reload

# Production mode
cybercore-api --workers 4

# With custom port
cybercore-api --port 9000
```

**Test API:**
```bash
# Health check
curl http://localhost:8000/health

# API documentation
open http://localhost:8000/docs  # Opens in browser
```

**Create Systemd Service (Linux):**

```bash
# Create service file
sudo nano /etc/systemd/system/cybercore-api.service
```

```ini
[Unit]
Description=CyberCore API Server
After=network.target

[Service]
Type=simple
User=cybercore
WorkingDirectory=/opt/cybercore
Environment="PATH=/opt/cybercore/venv/bin"
ExecStart=/opt/cybercore/venv/bin/cybercore-api --workers 4
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable cybercore-api
sudo systemctl start cybercore-api
sudo systemctl status cybercore-api
```

### 5.5 DSPY Optimizer Configuration

```bash
# Run initial optimization
cybercore-optimize --analyze

# Enable automatic optimization
cybercore-optimize --enable-auto

# Set optimization schedule
cybercore-optimize --schedule "0 */6 * * *"  # Every 6 hours
```

### 5.6 Firewall Configuration

**Windows Firewall:**
```powershell
# Allow CyberCore API through firewall
New-NetFirewallRule -DisplayName "CyberCore API" -Direction Inbound -Protocol TCP -LocalPort 8000 -Action Allow
```

**Linux (UFW):**
```bash
# Allow API port
sudo ufw allow 8000/tcp
sudo ufw reload
```

**Linux (firewalld):**
```bash
# Allow API port
sudo firewall-cmd --permanent --add-port=8000/tcp
sudo firewall-cmd --reload
```

---

## 6. Deletion/Uninstallation

### 6.1 Windows Uninstallation

#### Method 1: Using Chocolatey

```powershell
# Uninstall CyberCore
choco uninstall cybercore -y

# Remove configuration (optional)
Remove-Item -Recurse -Force "$env:USERPROFILE\.cybercore"
```

#### Method 2: Manual Uninstallation

**Step 1: Deactivate Virtual Environment**
```cmd
deactivate
```

**Step 2: Uninstall via pip**
```powershell
pip uninstall cybercore -y
```

**Step 3: Remove Virtual Environment**
```powershell
# If you used virtual environment
Remove-Item -Recurse -Force ".\venv"
```

**Step 4: Remove Configuration Files**
```powershell
# Remove user configuration
Remove-Item -Recurse -Force "$env:USERPROFILE\.cybercore"

# Remove AppData files
Remove-Item -Recurse -Force "$env:LOCALAPPDATA\cybercore"
```

**Step 5: Remove Environment Variables**
```powershell
# Remove user environment variables
[Environment]::SetEnvironmentVariable("CYBERCORE_HOME", $null, "User")
[Environment]::SetEnvironmentVariable("CYBERCORE_LOG_LEVEL", $null, "User")
```

**Step 6: Remove from PATH** (if added manually)
```powershell
# Use System Properties > Environment Variables
# Or via PowerShell (advanced)
```

#### Using Control Panel

1. Open **Control Panel**
2. Go to **Programs and Features**
3. Find **CyberCore** in the list
4. Click **Uninstall**
5. Follow the uninstallation wizard

### 6.2 macOS Uninstallation

#### Method 1: Using Homebrew

```bash
# Uninstall CyberCore
brew uninstall cybercore

# Remove configuration (optional)
rm -rf ~/.cybercore
```

#### Method 2: Manual Uninstallation

**Step 1: Deactivate Virtual Environment**
```bash
deactivate
```

**Step 2: Uninstall via pip**
```bash
pip uninstall cybercore -y
```

**Step 3: Remove Installation Directory**
```bash
# If installed in /usr/local
sudo rm -rf /usr/local/cybercore

# If installed in /opt
sudo rm -rf /opt/cybercore
```

**Step 4: Remove Virtual Environment**
```bash
rm -rf ./venv
```

**Step 5: Remove Configuration Files**
```bash
# User configuration
rm -rf ~/.cybercore

# Application support files
rm -rf ~/Library/Application\ Support/cybercore

# Cache files
rm -rf ~/Library/Caches/cybercore

# Logs
rm -rf ~/Library/Logs/cybercore
```

**Step 6: Remove Environment Variables**
```bash
# Edit ~/.bashrc or ~/.zshrc
nano ~/.bashrc

# Remove lines:
# export CYBERCORE_HOME="..."
# export CYBERCORE_LOG_LEVEL="..."

# Apply changes
source ~/.bashrc
```

**Step 7: Remove Launch Agents** (if configured)
```bash
rm -f ~/Library/LaunchAgents/com.cybercore.api.plist
launchctl unload ~/Library/LaunchAgents/com.cybercore.api.plist
```

### 6.3 Linux Uninstallation

#### Method 1: Using Snap

```bash
# Remove CyberCore
sudo snap remove cybercore

# Snap automatically removes most files
# Remove user configuration (optional)
rm -rf ~/.cybercore
```

#### Method 2: Using Package Manager

**Ubuntu/Debian:**
```bash
# Uninstall package
sudo apt remove cybercore

# Remove configuration files
sudo apt purge cybercore

# Remove dependencies
sudo apt autoremove
```

**Fedora/RHEL:**
```bash
# Uninstall package
sudo dnf remove cybercore

# Remove dependencies
sudo dnf autoremove
```

#### Method 3: Manual Uninstallation

**Step 1: Stop Services**
```bash
# Stop systemd service (if configured)
sudo systemctl stop cybercore-api
sudo systemctl disable cybercore-api
sudo rm /etc/systemd/system/cybercore-api.service
sudo systemctl daemon-reload
```

**Step 2: Deactivate Virtual Environment**
```bash
deactivate
```

**Step 3: Uninstall via pip**
```bash
pip uninstall cybercore -y
# Or if installed system-wide:
sudo pip3 uninstall cybercore -y
```

**Step 4: Remove Installation Directory**
```bash
# If installed in /opt
sudo rm -rf /opt/cybercore

# If installed in /usr/local
sudo rm -rf /usr/local/cybercore
```

**Step 5: Remove Virtual Environment**
```bash
rm -rf ./venv
```

**Step 6: Remove Configuration Files**
```bash
# User configuration
rm -rf ~/.cybercore

# System configuration
sudo rm -rf /etc/cybercore

# Log files
sudo rm -rf /var/log/cybercore

# Data files
sudo rm -rf /var/lib/cybercore
```

**Step 7: Remove Environment Variables**
```bash
# Edit ~/.bashrc, ~/.profile, or /etc/environment
nano ~/.bashrc

# Remove CyberCore-related exports
# Apply changes
source ~/.bashrc
```

**Step 8: Remove Firewall Rules** (if configured)
```bash
# UFW
sudo ufw delete allow 8000/tcp

# firewalld
sudo firewall-cmd --permanent --remove-port=8000/tcp
sudo firewall-cmd --reload
```

### 6.4 Docker Cleanup

```bash
# Stop and remove containers
docker stop cybercore-api
docker rm cybercore-api

# Remove image
docker rmi cybercore/cybercore:6.0

# Remove volumes
docker volume ls | grep cybercore | awk '{print $2}' | xargs docker volume rm

# Docker Compose cleanup
docker-compose down -v --rmi all
```

### 6.5 Verification of Complete Removal

```bash
# Check if command still exists
which cybercore  # Should return nothing

# Check for remaining files
find / -name "*cybercore*" 2>/dev/null

# Check for running processes
ps aux | grep cybercore

# Check for listening ports
netstat -tuln | grep 8000
```

---

## 7. Troubleshooting

### 7.1 Installation Issues

#### Issue 1: Python Version Not Supported

**Error Message:**
```
ERROR: Python 3.11+ required (found 3.9)
```

**Solution:**
```bash
# Check current Python version
python --version

# Install Python 3.11+ from:
# - Windows: https://www.python.org/downloads/
# - macOS: brew install python@3.11
# - Linux: sudo apt install python3.11

# Use specific Python version
python3.11 -m venv venv
```

#### Issue 2: Permission Denied

**Error Message:**
```
Permission denied: './install.sh'
```

**Solution:**
```bash
# Make script executable
chmod +x install.sh

# Then run again
./install.sh
```

#### Issue 3: Module Not Found

**Error Message:**
```
ModuleNotFoundError: No module named 'cybercore'
```

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate.bat  # Windows

# Reinstall
pip install -e .

# Check Python path
python -c "import sys; print(sys.path)"
```

#### Issue 4: SSL Certificate Error

**Error Message:**
```
SSL: CERTIFICATE_VERIFY_FAILED
```

**Solution:**

**macOS:**
```bash
# Install certificates
/Applications/Python\ 3.11/Install\ Certificates.command
```

**All Platforms:**
```bash
# Use trusted host
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -e .

# Or upgrade certifi
pip install --upgrade certifi
```

#### Issue 5: Build Dependencies Missing

**Error Message:**
```
error: Microsoft Visual C++ 14.0 or greater is required
```

**Solution:**

**Windows:**
- Install Visual Studio Build Tools from:
  https://visualstudio.microsoft.com/downloads/
- Select "Desktop development with C++"

**Linux:**
```bash
# Ubuntu/Debian
sudo apt install build-essential python3-dev

# Fedora/RHEL
sudo dnf groupinstall "Development Tools"
sudo dnf install python3-devel
```

**macOS:**
```bash
xcode-select --install
```

### 7.2 Runtime Issues

#### Issue 6: Port Already in Use

**Error Message:**
```
Error: Port 8000 is already in use
```

**Solution:**

**Linux/macOS:**
```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
cybercore-api --port 8080
```

**Windows:**
```powershell
# Find process
netstat -ano | findstr :8000

# Kill process
taskkill /PID <PID> /F

# Or use different port
cybercore-api --port 8080
```

#### Issue 7: Configuration File Not Found

**Error Message:**
```
ERROR: Configuration file not found
```

**Solution:**
```bash
# Create config directory
mkdir -p ~/.cybercore/config

# Copy example config
cp config/config.example.yaml ~/.cybercore/config/config.yaml

# Or specify config location
cybercore --config /path/to/config.yaml
```

#### Issue 8: Database Connection Error

**Error Message:**
```
Could not connect to database
```

**Solution:**
```bash
# Initialize database
cybercore db init

# Check database file permissions
ls -la ~/.cybercore/data/

# Reset database (caution: deletes all data)
cybercore db reset --force
```

#### Issue 9: Import Error After Installation

**Error Message:**
```
ImportError: cannot import name 'X' from 'cybercore'
```

**Solution:**
```bash
# Clear Python cache
find . -type d -name "__pycache__" -exec rm -r {} +
find . -type f -name "*.pyc" -delete

# Reinstall in development mode
pip uninstall cybercore -y
pip install -e .

# Or clear pip cache
pip cache purge
pip install -e .
```

### 7.3 Uninstallation Issues

#### Issue 10: Cannot Uninstall Package

**Error Message:**
```
ERROR: Cannot uninstall 'cybercore'
```

**Solution:**
```bash
# Force uninstall
pip uninstall cybercore -y

# If still fails, remove manually
find $(python -c "import sys; print(sys.prefix)") -name "*cybercore*" -delete

# Remove from site-packages
rm -rf $(python -c "import site; print(site.getsitepackages()[0])")/cybercore*
```

#### Issue 11: Residual Files Remain

**Problem**: Files remain after uninstallation

**Solution:**
```bash
# Find all CyberCore files
find / -name "*cybercore*" 2>/dev/null

# Remove specific directories
rm -rf ~/.cybercore
rm -rf ~/.local/share/cybercore
rm -rf ~/.cache/cybercore

# Windows
Remove-Item -Recurse -Force "$env:USERPROFILE\.cybercore"
Remove-Item -Recurse -Force "$env:LOCALAPPDATA\cybercore"
```

### 7.4 Performance Issues

#### Issue 12: Slow Performance

**Solution:**

```bash
# Enable optimization
cybercore-optimize --analyze
cybercore-optimize --apply

# Increase worker count
cybercore-api --workers 8

# Check system resources
top  # Linux/macOS
Resmon.exe  # Windows

# Clear cache
cybercore cache clear
```

#### Issue 13: High Memory Usage

**Solution:**

```bash
# Reduce concurrent scans
export CYBERCORE_MAX_CONCURRENT=3

# Configure in config file
cat >> ~/.cybercore/config/config.yaml << EOF
resources:
  max_memory: 2G
  max_workers: 4
EOF

# Restart service
sudo systemctl restart cybercore-api
```

### 7.5 Getting Help

**Check Logs:**
```bash
# View logs
cybercore logs --tail 100

# Specific component
cybercore logs --component api

# Debug mode
cybercore --debug --verbose scan --target example.com
```

**Diagnostic Information:**
```bash
# Generate diagnostic report
cybercore diagnose

# System information
cybercore system-info

# Check dependencies
cybercore check-deps
```

**Community Support:**
- **GitHub Issues**: https://github.com/cybercore/cybercore/issues
- **Discord**: https://discord.gg/cybercore
- **Stack Overflow**: Tag `cybercore`
- **Documentation**: https://docs.cybercore.dev
- **Email**: support@cybercore.dev

---

## 8. Conclusion

### Summary

This comprehensive guide has covered:

✅ **Introduction**: Understanding CyberCore and its capabilities
✅ **Prerequisites**: System requirements across all platforms
✅ **System Requirements**: Detailed specifications for Windows, macOS, and Linux
✅ **Installation Steps**: Multiple installation methods for each platform
✅ **Post-Installation**: Configuration and setup procedures
✅ **Uninstallation**: Complete removal instructions for all platforms
✅ **Troubleshooting**: Solutions to common issues

### Quick Reference

| Platform | Install Command | Uninstall Command |
|----------|----------------|-------------------|
| Windows | `install.bat` | `pip uninstall cybercore -y` |
| macOS | `./install.sh` | `brew uninstall cybercore` |
| Linux | `./install.sh` | `pip uninstall cybercore -y` |
| Docker | `docker pull cybercore/cybercore:6.0` | `docker rmi cybercore/cybercore:6.0` |

### Key Takeaways

1. **Python 3.11+** is required for all installations
2. **Virtual environments** are recommended for isolated installations
3. **Multiple installation methods** are available for flexibility
4. **Configuration** is stored in `~/.cybercore/config/`
5. **Thorough uninstallation** requires removing configuration files
6. **Community support** is available for troubleshooting

### Next Steps

After successful installation:

1. **Explore Documentation**
   ```bash
   cybercore docs --open
   ```

2. **Run First Scan**
   ```bash
   cybercore scan --target example.com --type basic
   ```

3. **Start API Server**
   ```bash
   cybercore-api
   # Visit: http://localhost:8000/docs
   ```

4. **Enable DSPY Optimization**
   ```bash
   cybercore-optimize --enable-auto
   ```

5. **Join Community**
   - GitHub: https://github.com/cybercore/cybercore
   - Discord: https://discord.gg/cybercore
   - Twitter: @cybercoredev

### Need Help?

If you encounter issues not covered in this guide:

1. **Search Documentation**: https://docs.cybercore.dev
2. **Check GitHub Issues**: https://github.com/cybercore/cybercore/issues
3. **Ask on Discord**: https://discord.gg/cybercore
4. **Email Support**: support@cybercore.dev

**Include in your support request:**
- Operating system and version
- Python version (`python --version`)
- CyberCore version (`cybercore --version`)
- Installation method used
- Complete error message
- Steps to reproduce the issue
- Diagnostic report (`cybercore diagnose`)

### Contributing

CyberCore is open-source and welcomes contributions!

```bash
# Fork the repository
gh repo fork cybercore/cybercore

# Clone your fork
git clone https://github.com/YOUR_USERNAME/cybercore.git

# Install in development mode
cd cybercore
pip install -e ".[dev]"

# Run tests
pytest

# Submit pull request
gh pr create
```

See [CONTRIBUTING.md](https://github.com/cybercore/cybercore/blob/main/CONTRIBUTING.md) for guidelines.

### License

CyberCore is released under the MIT License. See [LICENSE](LICENSE) for details.

### Acknowledgments

Thank you for choosing CyberCore! We're committed to providing the best autonomous security testing framework.

**Happy Testing! 🔒🚀**

---

**Document Version**: 1.0  
**Last Updated**: October 25, 2025  
**CyberCore Version**: 6.0.0  
**License**: MIT  

**CyberCore** | Autonomous Security Testing Framework  
https://cybercore.dev

