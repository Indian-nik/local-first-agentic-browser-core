#!/bin/bash
set -e

echo "🔄 Renewing SPIFFE certificates..."

# Check SPIRE server health
if ! docker exec spire-server /opt/spire/bin/spire-server healthcheck; then
    echo "❌ SPIRE server not healthy"
    exit 1
fi

# Rotate agent certificates
docker exec spire-agent /opt/spire/bin/spire-agent api fetch x509 \
  -socketPath /opt/spire/agent.sock \
  -write /tmp/

echo "✅ Certificate renewal complete"
