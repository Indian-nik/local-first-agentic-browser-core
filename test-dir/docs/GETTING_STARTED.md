# 🚀 CyberCore v5.0 - Getting Started Guide

## 🎯 Welcome to CyberCore Ultimate v5.0

CyberCore is the most advanced ethical security testing framework, combining quantum-resistant cryptography, autonomous operations, and AI-powered capabilities.

## 📚 Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Basic Usage](#basic-usage)
4. [Ethical Guidelines](#ethical-guidelines)
5. [Tutorials](#tutorials)

## 📦 Installation

### Option 1: Docker (Recommended)

```bash
# Clone repository
git clone https://github.com/cybercore/v5.0.git
cd v5.0

# Start with Docker
docker-compose -f docker-compose.cybercore.yml up -d
```

### Option 2: Local Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install CyberCore
pip install -e .
```

## ⚡ Quick Start

```python
from cybercore_v5 import CyberCoreEngine

# Initialize engine
engine = CyberCoreEngine()

# Load authorization
engine.load_authorization('authorization.json')

# Run scan
results = engine.scan(target='http://localhost:8080')
```

## ⚖️ Ethical Guidelines

⚠️ **CRITICAL: READ BEFORE USE**

1. **ALWAYS obtain written authorization** before testing
2. **NEVER test** systems you don't own or have permission for
3. **Stay within scope** - Respect boundaries
4. **All actions are logged** - Complete audit trail
5. **Follow responsible disclosure** - 90-day timeline

## 📚 Next Steps

- [Tutorial 1: Your First Scan](tutorials/01-first-scan.md)
- [Tutorial 2: Quantum Cryptography Testing](tutorials/02-quantum-crypto.md)
- [Tutorial 3: Autonomous Operations](tutorials/03-autonomous-ops.md)
- [API Reference](api/README.md)
