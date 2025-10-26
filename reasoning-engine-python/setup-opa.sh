#!/bin/bash
# Phase 4 Task 2: Implement OPA authorization policies
echo "Setting up OPA (Open Policy Agent) authorization..."

# Create OPA policies directory
mkdir -p ./opa-policies

# Create service authorization policy
cat > ./opa-policies/service-authz.rego << 'POLICY'
package services.authz

default allow = false

# Allow authenticated inter-service communication
allow {
    input.service_authenticated == true
    input.service_cert_valid == true
    valid_service_name
}

valid_service_name {
    input.service_name == "agent-core"
}

valid_service_name {
    input.service_name == "inference-kernel"
}

valid_service_name {
    input.service_name == "reasoning-engine"
}
POLICY

# Create workflow authorization policy
cat > ./opa-policies/workflow-authz.rego << 'POLICY'
package workflows.authz

default allow = false

# Allow workflow execution for authorized services
allow {
    input.action == "execute"
    input.resource_type == "workflow"
    input.service_role in ["executor", "admin"]
}

# Allow workflow monitoring
allow {
    input.action == "read"
    input.resource_type == "workflow"
    input.service_role in ["executor", "admin", "monitor"]
}
POLICY

echo "OPA policies created successfully!"
