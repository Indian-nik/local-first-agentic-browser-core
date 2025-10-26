# 🐳 CyberCore v5.0 - Docker Testing Environment

## 📦 What's Included

This Docker environment includes:

1. **CyberCore Engine** - Main security testing framework
2. **PostgreSQL** - Audit log database
3. **Redis** - Caching and task queue
4. **DVWA** - Damn Vulnerable Web Application (test target)
5. **OWASP Juice Shop** - Modern vulnerable web app (test target)

## 🚀 Quick Start

```bash
# Build and start all services
docker-compose -f docker-compose.cybercore.yml up --build

# Start in detached mode
docker-compose -f docker-compose.cybercore.yml up -d

# View logs
docker-compose -f docker-compose.cybercore.yml logs -f
```

## 🔗 Access Points

- **CyberCore API**: http://localhost:8000
- **CyberCore HTTPS**: https://localhost:8443
- **DVWA**: http://localhost:8080
- **Juice Shop**: http://localhost:3000
- **PostgreSQL**: localhost:5432 (from host)

## ⚖️ IMPORTANT: Ethical Use Only

⚠️ **This environment is for AUTHORIZED TESTING ONLY**

- Only test against included vulnerable applications
- Never test against external targets without authorization
- All actions are logged and audited
