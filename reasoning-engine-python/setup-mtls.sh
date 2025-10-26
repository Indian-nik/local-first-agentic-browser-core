#!/bin/bash
# Phase 4 Task 1: Enforce mTLS for all inter-service communication
echo "Setting up mTLS for inter-service communication..."

# Create certificates directory
mkdir -p ./certs

# Generate CA certificate
openssl req -x509 -newkey rsa:4096 -days 365 -nodes \
  -keyout ./certs/ca-key.pem \
  -out ./certs/ca-cert.pem \
  -subj "/CN=Service CA"

# Generate service certificates for each microservice
for service in agent-core inference-kernel reasoning-engine; do
  echo "Generating certificate for $service..."
  openssl req -newkey rsa:4096 -nodes \
    -keyout ./certs/${service}-key.pem \
    -out ./certs/${service}-req.pem \
    -subj "/CN=${service}"
  
  openssl x509 -req -in ./certs/${service}-req.pem \
    -days 365 -CA ./certs/ca-cert.pem -CAkey ./certs/ca-key.pem \
    -CAcreateserial -out ./certs/${service}-cert.pem
done

echo "mTLS certificates generated successfully!"
