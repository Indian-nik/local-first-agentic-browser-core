#!/bin/bash
set -e

echo "🔐 Setting up HashiCorp Vault"

# Start Vault in dev mode
docker run -d --name vault \
  -p 8200:8200 \
  -e 'VAULT_DEV_ROOT_TOKEN_ID=root' \
  -e 'VAULT_DEV_LISTEN_ADDRESS=0.0.0.0:8200' \
  --cap-add=IPC_LOCK \
  hashicorp/vault:1.15

echo "Waiting for Vault to start..."
sleep 3

# Set Vault address
export VAULT_ADDR='http://localhost:8200'
export VAULT_TOKEN='root'

# Initialize secrets
echo "Initializing secrets..."
docker exec vault vault kv put secret/agentic-browser \
  db_password="local-only-password" \
  api_key="not-used-locally"

echo "✅ Vault setup complete"
echo "   Address: $VAULT_ADDR"
echo "   Token: $VAULT_TOKEN"
echo "   UI: http://localhost:8200/ui"
