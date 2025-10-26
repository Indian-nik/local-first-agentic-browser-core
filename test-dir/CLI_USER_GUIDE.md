# CyberCore v5.0 - CLI User Guide

## Overview

CyberCore CLI provides a comprehensive command-line interface for ethical hacking, penetration testing, and security assessment operations.

## Installation

### From Source
```bash
git clone https://github.com/cybercore/cybercore.git
cd cybercore
pip install -e .
```

### Using pip
```bash
pip install cybercore
```

### Docker
```bash
docker pull cybercore/cybercore:5.0
docker run -it cybercore/cybercore:5.0 cybercore --help
```

## Quick Start

### Display Help
```bash
cybercore --help
```

### Check Version
```bash
cybercore --version
```

## Command Structure

CyberCore CLI follows this structure:
```
cybercore [COMMAND] [SUBCOMMAND] [OPTIONS] [ARGUMENTS]
```

## Core Commands

### 1. Scan Command

Perform vulnerability scanning and reconnaissance.

#### Network Scanning
```bash
# Basic network scan
cybercore scan network 192.168.1.0/24

# Scan specific ports
cybercore scan network target.com --ports 80,443,8080

# Aggressive scan mode
cybercore scan network 10.0.0.1 --aggressive

# Stealth scan
cybercore scan network target.com --stealth

# Save results
cybercore scan network target.com -o results.json
```

#### Web Application Scanning
```bash
# Basic web scan
cybercore scan web https://example.com

# Deep crawl with authentication
cybercore scan web https://app.com --depth 5 --auth token123
```

#### API Scanning
```bash
# Scan REST API
cybercore scan api https://api.example.com
```

### 2. Exploit Command

Execute exploit modules (requires authorization).

```bash
# Run specific exploit
cybercore exploit run 192.168.1.100 --module ms17-010

# List available exploits
cybercore exploit list

# Search for exploits
cybercore exploit search smb
```

**⚠️ WARNING**: All exploit operations require:
- Written authorization from target owner
- Valid scope definition
- Approved testing window

### 3. Report Command

Generate professional security reports.

```bash
# Generate PDF report
cybercore report generate scan_results.json --format pdf

# Generate HTML report
cybercore report generate scan_results.json --format html -o report.html

# Generate JSON report
cybercore report generate scan_results.json --format json

# Executive summary
cybercore report executive scan_results.json
```

### 4. Quantum Command

Quantum-enhanced security operations.

```bash
# Quantum cryptanalysis
cybercore quantum crack encrypted_data.bin

# Quantum key distribution
cybercore quantum qkd --server target.com

# Post-quantum crypto analysis
cybercore quantum pqc-test target.com
```

### 5. Autonomous Command

AI-powered autonomous operations.

```bash
# Autonomous threat hunting
cybercore autonomous hunt 192.168.1.0/24

# Auto-remediation
cybercore autonomous remediate --findings findings.json

# Continuous monitoring
cybercore autonomous monitor --scope scope.yaml
```

### 6. Threat Intelligence Command

Threat intelligence operations.

```bash
# Lookup IOC
cybercore threat-intel lookup 1.2.3.4

# Domain reputation
cybercore threat-intel domain evil.com

# File hash analysis
cybercore threat-intel hash abc123...

# Feed updates
cybercore threat-intel update
```

### 7. Authorization Command

Manage authorization and scope.

```bash
# Verify authorization
cybercore auth verify scope.yaml

# Create scope file
cybercore auth create-scope

# Check current scope
cybercore auth status

# Validate engagement
cybercore auth validate engagement_letter.pdf
```

### 8. Configuration Command

Framework configuration.

```bash
# Show configuration
cybercore config show

# Set API key
cybercore config set api_key YOUR_KEY

# Configure proxy
cybercore config set proxy http://proxy:8080

# Reset configuration
cybercore config reset
```

## Global Options

Available for all commands:

```bash
--verbose, -v          Verbose output
--quiet, -q            Quiet mode
--output, -o FILE      Output file
--format, -f FORMAT    Output format (json, yaml, xml)
--config FILE          Config file path
--log-level LEVEL      Logging level (debug, info, warn, error)
```

## Environment Variables

```bash
# API Keys
export CYBERCORE_API_KEY=your_api_key

# Proxy Settings
export CYBERCORE_PROXY=http://proxy:8080

# Configuration Path
export CYBERCORE_CONFIG=/path/to/config.yaml

# Output Directory
export CYBERCORE_OUTPUT_DIR=/path/to/output
```

## Configuration File

Create `~/.cybercore/config.yaml`:

```yaml
api:
  key: YOUR_API_KEY
  endpoint: https://api.cybercore.dev

scanning:
  default_threads: 50
  timeout: 30
  rate_limit: 1000

reporting:
  template: professional
  include_screenshots: true
  watermark: true

ethics:
  require_authorization: true
  audit_logging: true
  scope_validation: strict
```

## Best Practices

### 1. Authorization First
ALWAYS verify authorization before testing:
```bash
cybercore auth verify scope.yaml
```

### 2. Scope Definition
Create detailed scope file:
```yaml
target:
  name: "Client Name"
  domains:
    - example.com
    - app.example.com
  ip_ranges:
    - 192.168.1.0/24
  excluded:
    - 192.168.1.100

authorization:
  letter: engagement_letter.pdf
  contact: security@example.com
  start_date: 2025-01-01
  end_date: 2025-01-31
```

### 3. Safe Testing
```bash
# Start with passive reconnaissance
cybercore scan network target.com --passive

# Progress to active scanning
cybercore scan network target.com --stealth

# Only exploit with explicit approval
cybercore exploit run target.com --module safe_module
```

### 4. Comprehensive Logging
```bash
# Enable detailed logging
cybercore --verbose --log-level debug scan network target.com
```

## Examples

### Complete Penetration Test Workflow

```bash
# 1. Verify authorization
cybercore auth verify engagement_scope.yaml

# 2. Reconnaissance
cybercore scan network 192.168.1.0/24 -o recon.json

# 3. Web application scanning
cybercore scan web https://target.com --depth 5 -o webapp.json

# 4. Vulnerability analysis
cybercore autonomous hunt 192.168.1.0/24 -o vulns.json

# 5. Threat intelligence
cybercore threat-intel lookup target.com -o intel.json

# 6. Generate report
cybercore report generate combined_results.json --format pdf -o final_report.pdf
```

### Bug Bounty Workflow

```bash
# Quick recon
cybercore scan web https://target.com --quick

# Deep scan on interesting targets
cybercore scan web https://app.target.com --aggressive --depth 10

# API testing
cybercore scan api https://api.target.com

# Generate findings
cybercore report generate results.json --format json
```

## Troubleshooting

### Command Not Found
```bash
# Add to PATH
export PATH=$PATH:~/.local/bin

# Or use full path
python3 -m cybercore_v5.cli.main --help
```

### Permission Denied
```bash
# Install with user flag
pip install --user cybercore

# Or use virtual environment
python3 -m venv venv
source venv/bin/activate
pip install cybercore
```

### Import Errors
```bash
# Install dependencies
pip install -r requirements.txt

# Or reinstall
pip install --force-reinstall cybercore
```

## Support

- **Documentation**: https://docs.cybercore.dev
- **GitHub**: https://github.com/cybercore/cybercore
- **Discord**: https://discord.gg/cybercore
- **Email**: support@cybercore.dev

## Legal & Ethics

### Requirements
1. ✅ **Authorization**: Written permission required
2. ✅ **Scope**: Defined and approved testing scope
3. ✅ **Compliance**: CFAA, GDPR, local laws
4. ✅ **Disclosure**: Responsible vulnerability disclosure

### Prohibited
1. ❌ Unauthorized testing
2. ❌ Out-of-scope targets
3. ❌ Destructive operations without approval
4. ❌ Data exfiltration

---

**Built with ❤️ by the CyberCore Security Team**

*Empowering ethical hackers worldwide since 2020*
