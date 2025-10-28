#!/usr/bin/env python3
"""Example VAPT Usage - Vulnerability Assessment and Penetration Testing"""

from cybercore_v5.vapt import (
    VulnerabilityScanner,
    PenetrationTester,
    VAPTReporter
)

def main():
    print("=" * 60)
    print("CyberCore v5.0 - VAPT Example")
    print("=" * 60)
    
    # Example 1: Vulnerability Scanning
    print("\n[1] Vulnerability Scanning")
    print("-" * 60)
    
    scanner = VulnerabilityScanner(
        target="example.com",
        scope={"domains": ["example.com", "*.example.com"]}
    )
    
    # Network scan
    print("\nRunning network scan...")
    network_results = scanner.scan_network(port_range="1-1000")
    print(f"  Open ports found: {len(network_results.get('open_ports', []))}")
    print(f"  Vulnerabilities: {len(network_results.get('vulnerabilities', []))}")
    
    # Web application scan
    print("\nRunning web application scan...")
    web_results = scanner.scan_web(depth=3)
    print(f"  Findings: {len(web_results.get('findings', []))}")
    
    # API scan
    print("\nRunning API scan...")
    api_results = scanner.scan_api()
    print(f"  Security issues: {len(api_results.get('security_issues', []))}")
    
    # Example 2: Penetration Testing (requires authorization)
    print("\n[2] Penetration Testing")
    print("-" * 60)
    
    authorization = {
        "authorized_by": "Security Director",
        "scope": ["example.com"],
        "date": "2025-10-24",
        "signature": "digital_signature_hash_123"
    }
    
    try:
        pentester = PenetrationTester(
            target="example.com",
            authorization=authorization
        )
        
        print("\nAuthorization verified!")
        print("Running exploit modules (test mode)...")
        
        # Run test exploit
        exploit_result = pentester.run_exploit(
            module="test_module",
            options={"mode": "test"}
        )
        print(f"  Exploit status: {exploit_result.get('success')}")
        
        # Test privilege escalation
        priv_esc = pentester.privilege_escalation()
        print(f"  Privilege escalation tests: {len(priv_esc.get('methods_tested', []))}")
        
    except PermissionError as e:
        print(f"  Error: {e}")
    
    # Example 3: Report Generation
    print("\n[3] Report Generation")
    print("-" * 60)
    
    reporter = VAPTReporter(findings=scanner.findings)
    
    # Executive summary
    exec_summary = reporter.generate_executive_summary()
    print(exec_summary)
    
    # Export report
    reporter.export_json("vapt_report.json")
    print("\n  Report exported to: vapt_report.json")
    
    print("\n" + "=" * 60)
    print("VAPT Assessment Complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
