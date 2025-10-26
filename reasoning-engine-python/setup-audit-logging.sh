#!/bin/bash
# Phase 4 Task 4: Add audit logging for security events
echo "Setting up audit logging infrastructure..."

# Create audit logs directory
mkdir -p ./audit-logs ./audit-config

# Create audit logging configuration
cat > ./audit-config/audit-logger.yaml << 'YAML'
audit:
  enabled: true
  log_level: INFO
  output:
    file:
      path: ./audit-logs/security-events.log
      max_size: 100MB
      max_age: 90
      rotation: daily
    syslog:
      enabled: true
      facility: local0
      protocol: tcp
      endpoint: localhost:514
  events:
    authentication:
      - login_success
      - login_failure
      - token_issued
      - token_revoked
    authorization:
      - access_granted
      - access_denied
      - policy_violation
    data_access:
      - read_sensitive
      - write_sensitive
      - delete_operation
    system:
      - service_started
      - service_stopped
      - configuration_changed
      - certificate_renewed
YAML

# Create audit event collector script
cat > ./audit-config/audit-collector.sh << 'SCRIPT'
#!/bin/bash
# Audit event collector service

AUDIT_LOG="./audit-logs/security-events.log"
ALERT_LOG="./audit-logs/security-alerts.log"

log_event() {
    local event_type="$1"
    local service="$2"
    local details="$3"
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    
    echo "{\"timestamp\":\"$timestamp\",\"type\":\"$event_type\",\"service\":\"$service\",\"details\":\"$details\"}" >> "$AUDIT_LOG"
    
    # Trigger alerts for critical events
    if [[ "$event_type" =~ (access_denied|login_failure|policy_violation) ]]; then
        echo "{\"timestamp\":\"$timestamp\",\"alert\":\"$event_type\",\"service\":\"$service\"}" >> "$ALERT_LOG"
    fi
}

export -f log_event

echo "Audit logging collector ready"
SCRIPT

chmod +x ./audit-config/audit-collector.sh

echo "Audit logging infrastructure created successfully!"
