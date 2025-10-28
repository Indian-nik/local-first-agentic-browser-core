# Tutorial 1: Your First Security Scan

## Overview

This tutorial will guide you through performing your first security scan using CyberCore v5.0. You'll learn the basics of target authorization, scan configuration, and result analysis.

## Prerequisites

- CyberCore v5.0 installed (Docker or local)
- Written authorization from target owner
- Basic understanding of network security concepts

## Step 1: Obtain Written Authorization

⚠️ **CRITICAL**: Never scan systems without explicit written permission.

```python
from cybercore_v5 import AuthorizationManager

# Initialize authorization manager
auth_mgr = AuthorizationManager()

# Load authorization document
authorization = auth_mgr.load_authorization(
    file_path="path/to/authorization.pdf",
    target_domain="example.com",
    scope=["192.168.1.0/24", "*.example.com"],
    expiry_date="2024-12-31"
)

# Verify authorization is valid
if not auth_mgr.verify_authorization(authorization):
    raise Exception("Invalid or expired authorization")
```

## Step 2: Configure Your First Scan

```python
from cybercore_v5 import CyberCore

# Initialize CyberCore engine
engine = CyberCore(
    authorization=authorization,
    mode="safe",  # Start with safe mode
    logging_level="INFO"
)

# Configure scan parameters
scan_config = {
    "target": "192.168.1.100",
    "scan_type": "comprehensive",
    "intensity": "low",  # Start with low intensity
    "techniques": [
        "port_scanning",
        "service_detection",
        "vulnerability_assessment"
    ],
    "exclusions": [],  # Add any out-of-scope systems
    "rate_limit": 100,  # Requests per second
    "timeout": 3600  # 1 hour max
}
```

## Step 3: Run the Scan

```python
# Start the scan
print("Starting security scan...")
scan_results = engine.run_scan(scan_config)

# Monitor progress
for update in engine.get_scan_progress():
    print(f"Progress: {update['percentage']}% - {update['status']}")
```

## Step 4: Analyze Results

```python
# Get scan summary
summary = scan_results.get_summary()
print(f"\nScan Summary:")
print(f"  Duration: {summary['duration']} seconds")
print(f"  Vulnerabilities Found: {summary['vuln_count']}")
print(f"  Critical: {summary['critical_count']}")
print(f"  High: {summary['high_count']}")
print(f"  Medium: {summary['medium_count']}")
print(f"  Low: {summary['low_count']}")

# Review critical vulnerabilities
for vuln in scan_results.get_vulnerabilities(severity="critical"):
    print(f"\n[CRITICAL] {vuln['title']}")
    print(f"  CVE: {vuln['cve_id']}")
    print(f"  CVSS Score: {vuln['cvss_score']}")
    print(f"  Description: {vuln['description']}")
    print(f"  Remediation: {vuln['remediation']}")
```

## Step 5: Generate Report

```python
# Generate comprehensive report
report = engine.generate_report(
    results=scan_results,
    format="pdf",
    include_sections=[
        "executive_summary",
        "vulnerability_details",
        "remediation_guidance",
        "compliance_mapping"
    ],
    output_path="reports/first_scan_report.pdf"
)

print(f"\nReport generated: {report['path']}")
```

## Step 6: Review Audit Log

```python
# Retrieve audit log for this scan
audit_log = engine.get_audit_log(
    scan_id=scan_results.scan_id,
    include_details=True
)

print(f"\nAudit Log:")
for entry in audit_log:
    print(f"  [{entry['timestamp']}] {entry['action']} - {entry['status']}")
```

## Best Practices

1. **Always Start Safe**: Begin with low-intensity scans and increase gradually
2. **Monitor Impact**: Watch target system performance during scans
3. **Document Everything**: Keep detailed records of all testing activities
4. **Communicate**: Inform stakeholders before starting scans
5. **Respect Scope**: Never test systems outside authorized scope
6. **Handle Data Carefully**: Encrypt and protect all scan results

## Common Issues

### Issue: "Authorization Verification Failed"
**Solution**: Ensure authorization document is valid, signed, and not expired

### Issue: "Target Unreachable"
**Solution**: Verify network connectivity and firewall rules

### Issue: "Rate Limit Exceeded"
**Solution**: Reduce scan intensity or increase timeout values

## Next Steps

- [Tutorial 2: Quantum Cryptography Testing](02-quantum-crypto.md)
- [Tutorial 3: Autonomous Operations](03-autonomous-ops.md)
- [Advanced Scanning Techniques](../guides/advanced-scanning.md)

## Additional Resources

- [API Reference](../api/README.md)
- [Troubleshooting Guide](../guides/troubleshooting.md)
- [Community Forum](https://community.cybercore.security)

---

⚠️ **Ethical Reminder**: This tutorial is for authorized security testing only. Unauthorized scanning is illegal and unethical.
