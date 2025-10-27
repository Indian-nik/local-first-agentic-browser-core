# INSTALLATION_GUIDE

Comprehensive, step-by-step installation, usage, and uninstallation guide for local-first-agentic-browser-core. Sections are organized by OS where steps differ: Windows, macOS, and Linux.

- Covered: prerequisites, cloning, Docker, Node.js, Git, backend (docker-compose), desktop app (Electron), usage, testing, interaction, full cleanup, and troubleshooting.

## Prerequisites

- Hardware
  - 8 GB RAM minimum (16 GB recommended)
  - 10+ GB free disk space
  - Internet access
- Supported OS
  - Windows 10/11 (x64) with WSL2 recommended for Docker
  - macOS 12+ (Monterey or later) on Intel or Apple Silicon
  - Linux: Ubuntu 20.04+/22.04+, Debian 11+, Fedora 38+, Arch (latest)
- Software
  - Git (latest stable)
  - Node.js LTS (>= 18.x) + npm
  - Docker Engine + Docker Compose plugin (v2) or Docker Desktop
  - Make (optional, if using provided scripts)

## 1. Install Git

- Windows
  - Download: https://git-scm.com/download/win
  - During setup, keep defaults. Ensure "Git from the command line" is enabled.
- macOS
  - Option A (Homebrew): `brew install git`
  - Option B (Xcode CLI): `xcode-select --install`
- Linux
  - Ubuntu/Debian: `sudo apt update && sudo apt install -y git`
  - Fedora: `sudo dnf install -y git`
  - Arch: `sudo pacman -S --noconfirm git`

Verify: `git --version`

## 2. Install Node.js (LTS >= 18)

- Windows
  - Download installer: https://nodejs.org/en/download
  - Choose LTS. After install, verify in a new terminal.
- macOS
  - With Homebrew: `brew install node@18` then `brew link --force --overwrite node@18`
- Linux (use NodeSource or nvm)
  - NodeSource (Ubuntu/Debian):
    - `curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -`
    - `sudo apt install -y nodejs`
  - nvm (any distro):
    - `curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash`
    - `source ~/.nvm/nvm.sh && nvm install --lts`

Verify: `node -v` and `npm -v`

## 3. Install Docker + Docker Compose v2

- Windows
  - Install Docker Desktop: https://www.docker.com/products/docker-desktop/
  - Enable WSL2 backend in Docker Desktop settings.
  - Ensure "Use the WSL 2 based engine" is checked. Restart if prompted.
- macOS
  - Install Docker Desktop for Mac (Intel/Apple Silicon): https://www.docker.com/products/docker-desktop/
- Linux
  - Ubuntu/Debian:
    - `sudo apt update`
    - `sudo apt install -y ca-certificates curl gnupg lsb-release`
    - `sudo install -m 0755 -d /etc/apt/keyrings`
    - `curl -fsSL https://download.docker.com/linux/$(. /etc/os-release; echo $ID)/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg`
    - `echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/$(. /etc/os-release; echo $ID) $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null`
    - `sudo apt update`
    - `sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin`
    - Add user to docker group: `sudo usermod -aG docker $USER && newgrp docker`
  - Fedora: `sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin && sudo systemctl enable --now docker`
  - Arch: `sudo pacman -S --noconfirm docker docker-compose && sudo systemctl enable --now docker`

Verify: `docker --version` and `docker compose version`

## 4. Clone the repository

- Choose a directory and run:

```
git clone https://github.com/<YOUR_ORG_OR_USER>/local-first-agentic-browser-core.git
cd local-first-agentic-browser-core
```

If you are in GitHub Codespaces, the repo is already cloned.

## 5. Backend setup (docker-compose)

- Environment configuration
  - Copy any example envs if present (skip if not applicable):
    - `cp .env.example .env` and adjust values
  - Open `docker-compose.yml` to review services and ports
- Start services
  - Dev up (foreground): `docker compose up`
  - Detached: `docker compose up -d`
- Verify services
  - List containers: `docker ps`
  - Check logs: `docker compose logs -f`
- Stop services
  - `docker compose down` (keeps volumes)
  - `docker compose down -v` (removes volumes)

## 6. Desktop app setup (Electron)

- Install dependencies
  - In project root: `npm install`
  - If the Electron app is in a subfolder (for example `desktop`), then:
    - `cd desktop && npm install && cd -`
- Development run
  - If package.json scripts are defined: `npm run electron:dev` or `npm run start`
  - Alternative typical commands:
    - `npx electron .` (from the app folder)
- Build distributables (optional)
  - `npm run electron:build` (or `npm run build` depending on scripts)

Note: Exact script names may vary. Check package.json for available scripts.

## 7. Usage instructions

- Run backend with Docker
  - `docker compose up -d`
  - Confirm health by checking logs and exposed ports
- Run desktop app
  - `npm run electron:dev` (or start command per package.json)
- Testing
  - Python tests (if applicable): `pytest`
  - Node tests: `npm test`
  - End-to-end (if provided): see `tests/` or scripts
- Interact
  - Use the desktop UI to connect to the backend
  - Typical local URLs: http://localhost:3000, http://localhost:8000 (adjust per docker-compose.yml)

## 8. Uninstallation and deletion (full cleanup)

- Stop and remove containers
  - `docker compose down`
- Remove volumes and networks created by compose
  - `docker compose down -v --remove-orphans`
- Remove images (careful: shared images may be used elsewhere)
  - `docker images | awk '/local-first-agentic-browser-core|<your-image-prefix>/{print $3}' | xargs -r docker rmi`
  - Or prune all unused: `docker image prune -a`
- Remove leftover volumes and networks globally (optional)
  - `docker volume prune`
  - `docker network prune`
- Remove repo folder
  - From one directory above the repo: `rm -rf local-first-agentic-browser-core`
  - Windows PowerShell: `Remove-Item -Recurse -Force .\local-first-agentic-browser-core`
- Uninstall dependencies (optional)
  - Windows
    - Docker Desktop: Apps & Features > Uninstall
    - Node.js: Apps & Features > Uninstall
    - Git: Apps & Features > Uninstall
  - macOS
    - Docker Desktop: Drag to Trash or `brew uninstall --cask docker`
    - Node.js (brew): `brew uninstall node` (or remove nvm-managed versions via `nvm uninstall`)
    - Git (brew): `brew uninstall git`
  - Linux
    - Docker Engine: `sudo apt remove -y docker-ce docker-ce-cli containerd.io` (Ubuntu/Debian)
    - Node.js: if NodeSource: `sudo apt remove -y nodejs`; if nvm: `nvm uninstall --lts`
    - Git: `sudo apt remove -y git` (adjust per distro)

## 9. OS-specific notes and differences

- Windows
  - Prefer WSL2 for best Docker performance. Ensure `wsl --install` and a default distro.
  - Run commands inside WSL Ubuntu terminal when possible.
  - File watchers may require `CHOKIDAR_USEPOLLING=1` for large repos.
- macOS
  - For Apple Silicon, prefer ARM64 images or use Docker Desktop emulation.
  - You may need to allow the app in System Settings > Privacy & Security on first run.
- Linux
  - Ensure your user is in the `docker` group to avoid sudo.
  - Open ports may be blocked by firewalld/ufw; allow as needed.

## 10. Troubleshooting

- Docker compose command not found
  - Ensure Docker Desktop is installed (Win/macOS) or compose-plugin (Linux)
  - Check: `docker compose version` (v2)
- Permission denied (EACCES) on npm install
  - Avoid `sudo npm install` globally
  - Use nvm-managed Node; clear cache: `npm cache clean --force`
- Ports already in use
  - Identify: `lsof -i :PORT` (macOS/Linux) or `netstat -ab` (Windows PowerShell)
  - Change port mappings in `docker-compose.yml`
- Containers exit immediately
  - Check logs: `docker compose logs SERVICE -f`
  - Verify environment variables (.env) and required files
- Electron app fails to start
  - Delete node_modules and reinstall: `rm -rf node_modules && npm install`
  - Ensure compatible Node/Electron versions
- WSL2 networking or file system issues (Windows)
  - Restart WSL: `wsl --shutdown` then reopen
  - Reset Docker Desktop if needed
- Slow builds or installs
  - Enable BuildKit: `export DOCKER_BUILDKIT=1`
  - Use a closer registry mirror or corporate proxy settings
- Proxy environments
  - Configure Docker daemon and npm proxy:
    - Docker: `/etc/systemd/system/docker.service.d/proxy.conf`
    - npm: `npm config set proxy http://user:pass@host:port`

## 11. Quick start ( TL;DR )

```
# Prereqs: Git, Node 18+, Docker + Compose v2 installed

# Clone
git clone https://github.com/<YOUR_ORG_OR_USER>/local-first-agentic-browser-core.git
cd local-first-agentic-browser-core

# Backend up
docker compose up -d

# App deps
npm install

# Run desktop app (adjust to your scripts)
npm run electron:dev
```
