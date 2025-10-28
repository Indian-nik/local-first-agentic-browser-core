# Local-First Agentic Browser Core

## 🚀 Project Overview

The Local-First Agentic Browser Core is an innovative multi-agent system that combines the power of local-first architecture with intelligent autonomous agents. This project implements a comprehensive ecosystem featuring AI-powered reasoning engines, inference kernels, and seamless desktop integration.

### Main Features

- **🤖 Multi-Agent Architecture**: Distributed agent system with specialized reasoning engines
- **💾 Local-First Design**: Prioritizes offline functionality and data ownership
- **🔄 Real-time Synchronization**: Efficient data sync across multiple nodes
- **🖥️ Desktop Integration**: Native desktop application with system-level interactions
- **🧠 AI-Powered Inference**: Advanced machine learning capabilities for intelligent decision-making
- **📊 Comprehensive Monitoring**: Full observability with metrics, logging, and distributed tracing
- **🔒 Security-First**: Built-in security measures and access controls
- **🌐 Microservices Architecture**: Scalable and maintainable service-oriented design



## 📁 Project Structure

This project follows a modern, modular directory structure designed for scalability and maintainability:

### Core Directories

#### `/docs` - Documentation Hub
Comprehensive project documentation including:
- Architecture guides and design decisions
- API documentation and specifications
- Installation and deployment guides  
- Development workflows and best practices
- Consolidated from root-level documentation files

#### `/deploy` - Deployment Configurations
Production-ready deployment assets:
- Docker Compose configurations for multi-container setups
- Kubernetes manifests and Helm charts
- Environment-specific configuration templates
- CI/CD pipeline definitions
- Deployment scripts and automation tools

#### `/src` - Source Code
Organized by functional domain:

- **`/src/backend`** - Python Backend Services
  - REST API endpoints and business logic
  - Database models and migrations
  - Authentication and authorization
  - Background task processors
  - **Dependencies**: `requirements.txt` now located here
  
- **`/src/frontend`** (`/src/renderer`) - React/TypeScript Frontend
  - UI components and pages
  - State management and routing
  - API client integrations
  - **Dependencies**: `package.json` located here
  
- **`/src/agent`** - Intelligent Agent Core
  - Agent reasoning engine
  - Task orchestration and workflow management
  - Plugin system architecture
  - Multi-modal processing capabilities

#### `/infra` - Infrastructure as Code
Infrastructure provisioning and management:
- Terraform/OpenTofu configurations
- Kubernetes cluster definitions
- Networking and security policies
- Monitoring and observability setup (Prometheus, Grafana)
- Infrastructure automation scripts

#### `/scripts` - Utility Scripts
Automation and helper scripts:
- Build and compilation scripts
- Setup and initialization utilities
- Database migration runners
- Development environment bootstrapping
- Testing and QA automation

#### `/examples` - Usage Examples
Demonstration code and tutorials:
- Sample configurations
- Integration examples
- Quick-start guides
- Best practice implementations

#### `/.github` - GitHub Integration
GitHub-specific configurations:
- CI/CD workflows (GitHub Actions)
- Issue and PR templates
- Dependabot configuration
- Security policies and workflows

#### `/tests` - Test Suite
Comprehensive testing framework:
- Unit tests
- Integration tests
- End-to-end tests
- Test fixtures and mocks
- Performance benchmarks

### Dependency Management

Language-specific dependency files are now located within their respective source directories:

- **Python (Backend)**: `src/backend/requirements.txt`
- **Node.js (Frontend)**: `src/renderer/package.json`
- **Go (if applicable)**: `agent-core-golang/go.mod`

This organization ensures clear dependency isolation and simplifies containerization.

## 📋 Prerequisites

- **Docker** 20.10+ and Docker Compose
- **Python** 3.9+
- **Node.js** 16+ (for desktop components)
- **Git** for version control
- At least **8GB RAM** and **20GB disk space**

## 🛠️ Installation

### Option 1: Docker Deployment (Recommended)

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd local-first-agentic-browser-core
   ```

2. **Start the full stack:**
   ```bash
   docker-compose up -d
   ```

3. **Initialize microservices:**
   ```bash
   ./setup-microservices.sh
   ```

### Option 2: Desktop Launcher

1. **Make the launcher executable:**
   ```bash
   chmod +x run-backend-and-desktop.sh
   ```

2. **Launch the complete system:**
   ```bash
   ./run-backend-and-desktop.sh
   ```

## 🎯 Usage Guide

### Running the System

**Backend Services:**
```bash
# Start all microservices
docker-compose up -d

# Check service health
docker-compose ps

# View logs
docker-compose logs -f [service-name]
```

**Desktop Application:**
```bash
# Launch desktop interface
./run-backend-and-desktop.sh

# Or run components separately
cd src/desktop
npm start
```

### Desktop Interaction

- **Agent Dashboard**: Monitor active agents and their tasks
- **Knowledge Graph**: Visualize data relationships and agent reasoning
- **System Controls**: Manage services, view logs, and configure settings
- **Real-time Updates**: Live monitoring of agent activities and system metrics

### Key Endpoints

- **Main Application**: `http://localhost:3000`
- **API Gateway**: `http://localhost:8000`
- **Monitoring Dashboard**: `http://localhost:9090`
- **Observability**: `http://localhost:5601`

## 🏗️ Architecture Diagram

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Desktop App   │    │   Web Browser   │    │   Mobile App    │
│   (React/Electron)   │    │   (React SPA)   │    │   (React Native)│
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────┴─────────────┐
                    │     API Gateway           │
                    │   (Kong/Express.js)       │
                    └─────────────┬─────────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                       │                        │
┌───────┴────────┐   ┌─────────┴────────┐   ┌──────────┴─────────┐
│ Reasoning      │   │ Inference        │   │ Customization     │
│ Engine         │   │ Kernel           │   │ Control           │
│ (Python)       │   │ (C++)           │   │ (Node.js)         │
└───────┬────────┘   └─────────┬────────┘   └──────────┬─────────┘
        │                      │                       │
        └──────────────────────┼───────────────────────┘
                               │
                  ┌─────────────┴─────────────┐
                  │     Message Bus           │
                  │   (Redis/RabbitMQ)        │
                  └─────────────┬─────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
┌───────┴────────┐   ┌────────┴────────┐   ┌────────┴────────┐
│   PostgreSQL   │   │    MongoDB      │   │    Vector DB    │
│   (Relational) │   │   (Documents)   │   │   (Embeddings)  │
└────────────────┘   └─────────────────┘   └─────────────────┘
```

## 🔧 API Documentation

### Core Services

**Reasoning Engine API** (`/api/reasoning`)
- `POST /analyze` - Submit data for agent analysis
- `GET /agents` - List active reasoning agents
- `POST /agents/{id}/task` - Assign task to specific agent

**Inference Kernel API** (`/api/inference`)
- `POST /predict` - Run ML inference on data
- `GET /models` - List available ML models
- `POST /models/{id}/train` - Trigger model training

**Customization Control API** (`/api/customize`)
- `GET /config` - Retrieve system configuration
- `PUT /config` - Update system settings
- `POST /plugins` - Install new plugins

## 🚀 Microservices & Deployment

### Service Architecture

| Service | Port | Language | Purpose |
|---------|------|----------|----------|
| API Gateway | 8000 | Node.js | Request routing, authentication |
| Reasoning Engine | 3000 | Python | AI agent coordination |
| Inference Kernel | 5000 | C++ | High-performance ML inference |
| Customization Control | 4000 | Node.js | Configuration management |
| Monitoring | 9090 | Go | Metrics collection |
| Observability | 5601 | JavaScript | Log aggregation, visualization |

### Deployment Options

**Local Development:**
```bash
# Development mode with hot reload
docker-compose -f docker-compose.dev.yml up
```

**Production Deployment:**
```bash
# Production-ready configuration
docker-compose -f docker-compose.prod.yml up -d

# With Kubernetes
kubectl apply -f k8s/
```

**Scaling Services:**
```bash
# Scale reasoning engines
docker-compose up -d --scale reasoning-engine=3

# Scale inference kernels
docker-compose up -d --scale inference-kernel=2
```

## 🔍 Troubleshooting

### Common Issues

**Docker Services Won't Start:**
```bash
# Check system resources
docker system df
docker system prune -f

# Restart Docker daemon
sudo systemctl restart docker
```

**Port Conflicts:**
```bash
# Find processes using ports
sudo netstat -tlnp | grep :8000
sudo lsof -i :3000

# Kill conflicting processes
sudo kill -9 <PID>
```

**Memory Issues:**
- Ensure at least 8GB RAM available
- Reduce concurrent agents in config
- Use `docker-compose down` to free resources

**Desktop App Issues:**
```bash
# Clear cache and reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# Reset desktop app data
rm -rf ~/.local/share/local-first-browser
```

### Logs and Monitoring

```bash
# View service logs
docker-compose logs -f reasoning-engine
docker-compose logs -f inference-kernel

# Monitor system resources
docker stats

# Check service health
curl http://localhost:8000/health
```

## 📈 Development Phases

### Phase 1-3: Foundation
- ✅ Core architecture establishment
- ✅ Basic agent framework
- ✅ Initial desktop integration

### Phase 4-6: Enhancement
- ✅ Advanced reasoning capabilities
- ✅ Multi-modal data processing
- ✅ Enhanced security measures

### Phase 7-8: Intelligence
- ✅ Multimodal AI integration
- ✅ Advanced inference optimization
- ✅ Real-time adaptation systems

### Phase 9: Learning & Adaptation
- ✅ Machine learning integration
- ✅ Adaptive behavior systems
- ✅ Self-improving agent capabilities

### Current Status: **Phase 9 Complete**

All major development phases have been completed. The system now features:
- Full multimodal capabilities
- Advanced learning and adaptation
- Comprehensive monitoring and observability
- Production-ready deployment configuration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt
npm install --dev

# Run tests
pytest tests/
npm test

# Run linting
flake8 .
eslint src/
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- 📧 Email: support@local-first-browser.dev
- 💬 Discord: [Community Server](https://discord.gg/local-first-browser)
- 🐛 Issues: [GitHub Issues](https://github.com/local-first-browser/core/issues)
- 📖 Documentation: [Full Docs](https://docs.local-first-browser.dev)

---

**Built with ❤️ by the Local-First Agentic Browser Team**