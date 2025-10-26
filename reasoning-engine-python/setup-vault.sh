#!/bin/bash
# Phase 4 Task 3: Set up secrets management with Vault
echo "Setting up HashiCorp Vault for secrets management..."

# Create Vault configuration
mkdir -p ./vault-config

cat > ./vault-config/vault.hcl << 'CONFIG'
storage "file" {
  path = "./vault-data"
}

listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_cert_file = "./certs/vault-cert.pem"
  tls_key_file  = "./certs/vault-key.pem"
}

api_addr = "https://127.0.0.1:8200"
ui = true
CONFIG

# Create secrets structure
mkdir -p ./vault-secrets

cat > ./vault-secrets/init-secrets.sh << 'INIT'
#!/bin/bash
# Initialize Vault with service secrets

export VAULT_ADDR='https://127.0.0.1:8200'
export VAULT_SKIP_VERIFY=1

# Enable KV secrets engine
vault secrets enable -version=2 -path=services kv

# Store service API keys
vault kv put services/agent-core \
  api_key="$(openssl rand -base64 32)" \
  db_password="$(openssl rand -base64 32)"

vault kv put services/inference-kernel \
  api_key="$(openssl rand -base64 32)" \
  model_key="$(openssl rand -base64 32)"

vault kv put services/reasoning-engine \
  api_key="$(openssl rand -base64 32)" \
  compute_key="$(openssl rand -base64 32)"

echo "Secrets stored in Vault successfully!"
INIT

chmod +x ./vault-secrets/init-secrets.sh

echo "Vault configuration created successfully!"
