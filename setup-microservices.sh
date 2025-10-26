#!/bin/bash
set -e

echo "Setting up microservices architecture..."

# Create necessary directories
mkdir -p security/vault security/opa logs

# Setup Vault (secrets management)
if [ -f "./setup-vault.sh" ]; then
    echo "Setting up Vault..."
    chmod +x ./setup-vault.sh
    ./setup-vault.sh
fi

# Setup OPA (policy management)
if [ -f "./setup-opa.sh" ]; then
    echo "Setting up OPA..."
    chmod +x ./setup-opa.sh
    ./setup-opa.sh
fi

# Setup mTLS (mutual TLS)
if [ -f "./setup-mtls.sh" ]; then
    echo "Setting up mTLS..."
    chmod +x ./setup-mtls.sh
    ./setup-mtls.sh
fi

# Setup audit logging
if [ -f "./setup-audit-logging.sh" ]; then
    echo "Setting up audit logging..."
    chmod +x ./setup-audit-logging.sh
    ./setup-audit-logging.sh
fi

# Start microservices with docker-compose
if [ -f "docker-compose.yml" ]; then
    echo "Starting microservices with Docker Compose..."
    docker-compose up -d
    echo "Waiting for services to be ready..."
    sleep 10
fi

echo "Microservices setup complete!"
echo "Services are running and configured with:"
echo "  - Vault for secrets management"
echo "  - OPA for policy enforcement"
echo "  - mTLS for secure communication"
echo "  - Audit logging enabled"
