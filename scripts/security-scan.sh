#!/bin/bash
set -e

echo "🔍 Running security scans..."

# Check if tools are installed
command -v trivy >/dev/null 2>&1 || { echo "❌ trivy not installed"; exit 1; }
command -v bandit >/dev/null 2>&1 || { echo "❌ bandit not installed. Install: pip install bandit"; exit 1; }

# Scan Docker images
echo "Scanning Docker images with Trivy..."
trivy image --severity HIGH,CRITICAL ghcr.io/your-org/agent-core:latest || true
trivy image --severity HIGH,CRITICAL ghcr.io/your-org/reasoning-engine:latest || true

# Scan Python code
echo "Scanning Python code with Bandit..."
bandit -r reasoning-engine-python/ -f json -o bandit-report.json || true

# Check dependencies
echo "Checking Python dependencies..."
safety check --json || true

# Scan filesystem
echo "Scanning filesystem with Trivy..."
trivy fs --severity HIGH,CRITICAL . || true

echo "✅ Security scan complete"
echo "   Review bandit-report.json for Python security issues"
