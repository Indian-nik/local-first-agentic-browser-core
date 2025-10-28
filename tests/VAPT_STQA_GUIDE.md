# CyberCore v5.0 - VAPT & STQA Complete Guide

## Table of Contents
1. [VAPT Module](#vapt-module)
2. [STQA Module](#stqa-module)
3. [Integration Examples](#integration-examples)
4. [Best Practices](#best-practices)

---

# VAPT Module

## Vulnerability Assessment and Penetration Testing

### Overview
The VAPT module provides comprehensive security testing capabilities including:
- Network vulnerability scanning
- Web application security assessment
- API security testing
- Penetration testing frameworks
- Professional security reporting

### Components

#### 1. VulnerabilityScanner
Advanced scanning engine for identifying security vulnerabilities.

```python
from cybercore_v5.vapt import VulnerabilityScanner

# Initialize scanner
scanner = VulnerabilityScanner(
    target="example.com",
    scope={"domains": ["example.com", "*.example.com"]}
)

# Network scan
network_results = scanner.scan_network(port_range="1-1000")
print(f"Open ports found: {len(network_results['open_ports'])}")

# Web application scan
web_results = scanner.scan_web(depth=3)
print(f"Vulnerabilities found: {len(web_results['findings'])}")

# API scan
api_results = scanner.scan_api()

# Export findings
report_json = scanner.export_findings(format="json")
```

**Features:**
- Network port scanning
- Service identification
- Vulnerability detection
- OWASP Top 10 testing
- API security assessment
- Multiple output formats

#### 2. PenetrationTester
Ethical exploitation framework for authorized testing.

```python
from cybercore_v5.vapt import PenetrationTester

# Authorization required!
authorization = {
    "authorized_by": "Client Security Team",
    "scope": ["192.168.1.0/24", "example.com"],
    "date": "2025-10-24",
    "signature": "digital_signature_hash"
}

# Initialize penetration tester
pentester = PenetrationTester(
    target="example.com",
    authorization=authorization
)

# Run specific exploit
result = pentester.run_exploit(
    module="ms17-010",
    options={"payload": "test"}
)

# Test privilege escalation
priv_esc = pentester.privilege_escalation()

# Test lateral movement
lateral = pentester.lateral_movement()
```

**⚠️ Authorization Requirements:**
- Written authorization from target owner
- Defined scope of testing
- Valid engagement dates
- Digital signature/approval

#### 3. VAPTReporter
Professional security report generation.

```python
from cybercore_v5.vapt import VAPTReporter

# Generate reports
reporter = VAPTReporter(findings=scanner.findings)

# Executive summary
exec_summary = reporter.generate_executive_summary()
print(exec_summary)

# Technical report
tech_report = reporter.generate_technical_report()

# Export as JSON
reporter.export_json("vapt_report.json")
```

**Report Types:**
- Executive summary
- Technical findings report
- JSON export for integration
- Customizable templates

### VAPT Workflow Example

```python
from cybercore_v5.vapt import (
    VulnerabilityScanner,
    PenetrationTester,
    VAPTReporter
)

# Step 1: Vulnerability Assessment
scanner = VulnerabilityScanner(target="target.com")
network_scan = scanner.scan_network()
web_scan = scanner.scan_web(depth=5)
api_scan = scanner.scan_api()

# Step 2: Penetration Testing (authorized only)
authorization = {
    "authorized_by": "Security Director",
    "scope": ["target.com"],
    "date": "2025-10-24",
    "signature": "abc123"
}

pentester = PenetrationTester("target.com", authorization)
exploit_result = pentester.run_exploit("test_module")

# Step 3: Report Generation
all_findings = scanner.findings
reporter = VAPTReporter(all_findings)
exec_report = reporter.generate_executive_summary()
tech_report = reporter.generate_technical_report()
reporter.export_json("final_vapt_report.json")
```

---

# STQA Module

## Software Testing and Quality Assurance

### Overview
The STQA module provides comprehensive software quality assurance including:
- Functional testing
- Integration testing
- Performance testing
- Security testing
- Test automation
- Code quality analysis

### Components

#### 1. SoftwareTester
Comprehensive testing framework.

```python
from cybercore_v5.stqa import SoftwareTester

# Initialize tester
tester = SoftwareTester(application="MyApp v1.0")

# Functional testing
test_cases = [
    {"name": "Login Test", "type": "functional"},
    {"name": "Checkout Test", "type": "functional"},
    {"name": "Search Test", "type": "functional"}
]

functional_results = tester.functional_testing(test_cases)
print(f"Passed: {functional_results['passed']}")
print(f"Failed: {functional_results['failed']}")

# Integration testing
components = ["Database", "API", "Frontend", "Cache"]
integration_results = tester.integration_testing(components)

# Performance testing
load_config = {"users": 1000, "duration": 300}
perf_results = tester.performance_testing(load_config)
print(f"Response time: {perf_results['metrics']['response_time_ms']}ms")

# Security testing
security_results = tester.security_testing()
```

**Testing Types:**
- Functional testing
- Integration testing  
- Performance testing
- Security testing
- Regression testing
- Smoke testing

#### 2. TestAutomation
Automated testing framework.

```python
from cybercore_v5.stqa import TestAutomation

# Initialize automation
automation = TestAutomation(project_name="MyProject")

# Add tests
def test_login():
    assert True  # Your test logic

def test_registration():
    assert True  # Your test logic

automation.add_test("Login Test", test_login)
automation.add_test("Registration Test", test_registration)

# Run all tests
results = automation.run_all_tests()
print(f"Total: {results['total_tests']}")
print(f"Passed: {results['passed']}")
print(f"Duration: {results['duration_seconds']}s")

# CI/CD integration
ci_config = {"pipeline": "github-actions", "build": 42}
ci_results = automation.continuous_integration(ci_config)

# Regression testing
regression_results = automation.regression_testing()
```

**Automation Features:**
- Test suite management
- Automated test execution
- CI/CD integration
- Regression testing
- Results tracking

#### 3. QualityAnalyzer
Code quality and metrics analysis.

```python
from cybercore_v5.stqa import QualityAnalyzer

# Initialize analyzer
analyzer = QualityAnalyzer(project_path="/path/to/project")

# Analyze code quality
metrics = analyzer.analyze_code_quality()

print(f"Maintainability Index: {metrics['maintainability']['maintainability_index']}")
print(f"Test Coverage: {metrics['test_coverage']['line_coverage']}%")
print(f"Technical Debt: {metrics['technical_debt']['debt_hours']} hours")

# Generate quality report
quality_report = analyzer.generate_quality_report()
print(quality_report)
```

**Quality Metrics:**
- Cyclomatic complexity
- Maintainability index
- Test coverage (line, branch, function)
- Code smells detection
- Technical debt calculation
- SQALE rating

### STQA Workflow Example

```python
from cybercore_v5.stqa import (
    SoftwareTester,
    TestAutomation,
    QualityAnalyzer
)

# Step 1: Manual Testing
tester = SoftwareTester("MyApp v2.0")

test_cases = [
    {"name": "Feature A", "type": "functional"},
    {"name": "Feature B", "type": "functional"}
]

functional = tester.functional_testing(test_cases)
integration = tester.integration_testing(["DB", "API", "UI"])
performance = tester.performance_testing({"users": 500})

# Step 2: Test Automation
automation = TestAutomation("MyApp")

def test_critical_path():
    assert True

automation.add_test("Critical Path", test_critical_path)
test_results = automation.run_all_tests()

# Step 3: Quality Analysis
analyzer = QualityAnalyzer("/path/to/project")
quality_metrics = analyzer.analyze_code_quality()
quality_report = analyzer.generate_quality_report()

print(quality_report)
```

---

# Integration Examples

## Combined VAPT + STQA Pipeline

```python
from cybercore_v5.vapt import VulnerabilityScanner
from cybercore_v5.stqa import SoftwareTester, QualityAnalyzer

# Complete security and quality pipeline
def full_assessment(application_url, project_path):
    # Security Assessment
    scanner = VulnerabilityScanner(application_url)
    security_scan = scanner.scan_web(depth=5)
    
    # Quality Testing
    tester = SoftwareTester("Application")
    security_tests = tester.security_testing()
    
    # Code Quality
    analyzer = QualityAnalyzer(project_path)
    quality_metrics = analyzer.analyze_code_quality()
    
    # Combined report
    return {
        "security": security_scan,
        "testing": security_tests,
        "quality": quality_metrics
    }

# Run complete assessment
results = full_assessment("https://myapp.com", "/path/to/code")
```

## CI/CD Integration

```yaml
# GitHub Actions example
name: Security and Quality Check

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run VAPT
        run: |
          python -m cybercore_v5.vapt.scanner
      - name: Run STQA
        run: |
          python -m cybercore_v5.stqa.tester
      - name: Quality Analysis
        run: |
          python -m cybercore_v5.stqa.quality_analyzer
```

---

# Best Practices

## VAPT Best Practices

### 1. Authorization First
```python
# ALWAYS verify authorization before testing
if not authorization_valid:
    raise PermissionError("Authorization required")
```

### 2. Scope Compliance
```python
# Stay within authorized scope
if target not in authorized_scope:
    raise PermissionError("Target out of scope")
```

### 3. Rate Limiting
```python
# Don't overwhelm target systems
scanner = VulnerabilityScanner(target, rate_limit=10)  # 10 req/sec
```

### 4. Comprehensive Reporting
```python
# Document everything
reporter.export_json("report.json")
reporter.generate_executive_summary()
reporter.generate_technical_report()
```

## STQA Best Practices

### 1. Test Early and Often
```python
# Run tests on every commit
automation.continuous_integration(ci_config)
```

### 2. Maintain High Coverage
```python
# Aim for >80% code coverage
if metrics['test_coverage']['line_coverage'] < 80:
    print("Warning: Low test coverage")
```

### 3. Monitor Quality Metrics
```python
# Track quality over time
analyzer = QualityAnalyzer(project_path)
metrics = analyzer.analyze_code_quality()

if metrics['maintainability']['maintainability_index'] < 60:
    print("Alert: Maintainability declining")
```

### 4. Automate Everything
```python
# Automate repetitive tests
automation = TestAutomation("Project")
automation.add_test("Test 1", test_func_1)
automation.add_test("Test 2", test_func_2)
automation.run_all_tests()
```

---

## Support

- **Documentation**: https://docs.cybercore.dev
- **GitHub**: https://github.com/cybercore/cybercore
- **Discord**: https://discord.gg/cybercore
- **Email**: support@cybercore.dev

---

**Built with ❤️ by the CyberCore Security Team**

*Empowering security professionals and QA teams worldwide*
