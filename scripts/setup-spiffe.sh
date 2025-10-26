#!/bin/bash
set -e

echo "🔒 Setting up SPIFFE/SPIRE for Zero Trust Architecture"

# Install SPIRE server
echo "Installing SPIRE server..."
docker run -d --name spire-server \
  -p 8081:8081 \
  -v $(pwd)/security/spire/server.conf:/opt/spire/conf/server/server.conf \
  ghcr.io/spiffe/spire-server:1.8.0 \
  -config /opt/spire/conf/server/server.conf

# Wait for server to start
echo "Waiting for SPIRE server to start..."
sleep 5

# Install SPIRE agent
echo "Installing SPIRE agent..."
docker run -d --name spire-agent \
  -v $(pwd)/security/spire/agent.conf:/opt/spire/conf/agent/agent.conf \
  -v /var/run/docker.sock:/var/run/docker.sock \
  ghcr.io/spiffe/spire-agent:1.8.0 \
  -config /opt/spire/conf/agent/agent.conf

echo "✅ SPIFFE/SPIRE setup complete"
echo "   Server: http://localhost:8081"
echo "   Healthcheck: docker exec spire-server /opt/spire/bin/spire-server healthcheck"
