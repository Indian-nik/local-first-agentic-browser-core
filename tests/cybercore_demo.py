#!/usr/bin/env python3
"""
CyberCore Assistant Demonstration
Showcases ethical security testing capabilities
"""

import sys
import os
from datetime import datetime, timedelta

# Add the cybercore module to Python path
sys.path.insert(0, '.')

from cybercore.security.cybercore_assistant import (
    CyberCoreAssistant, SecurityContext, SecurityTaskType
)
from cybercore.security.authorization import AuthorizationScope, AuthorizationLevel

def main():
    print("🛡️  CyberCore Assistant - Security Professional Edition")
    print("    Ethical AI Framework for Cybersecurity Professionals")
    print("=" * 60)
    
    # Initialize CyberCore Assistant
    assistant = CyberCoreAssistant()
    
    # Demo 1: Authorized Vulnerability Assessment
    print("\n📋 DEMO 1: Authorized Vulnerability Assessment")
    print("-" * 50)
    
    # Create authorization scope
    auth_scope = AuthorizationScope(
        target_systems=["testapp.example.com", "dev-server.internal"],
        authorized_activities=["vulnerability_scanning", "web_application_testing"],
        time_window=(
            datetime.now(),
            datetime.now() + timedelta(days=7)
        ),
        authorization_level=AuthorizationLevel.FULL_ASSESSMENT,
        authorized_by="Security Team Lead",
        contact_info="security@company.com",
        restrictions=["No destructive testing", "Business hours only"]
    )
    
    # Add authorization to assistant
    assistant.authorization_checker.add_authorization_scope(auth_scope)
    
    # Create security context
    context = SecurityContext(
        task_type=SecurityTaskType.VULNERABILITY_ASSESSMENT,
        authorization_scope="authorized testing of web applications",
        target_system="testapp.example.com",
        compliance_framework="OWASP",
        authorized_by="Security Team Lead"
    )
    
    # Perform assessment
    target_info = {
        "name": "testapp.example.com",
        "type": "web_application",
        "environment": "development"
    }
    
    result = assistant.perform_vulnerability_assessment(target_info, context)
    print(f"✅ Assessment Status: {result['status']}")
    print(f"📊 Methodology: {result.get('methodology', 'N/A')}")
    print(f"🔍 Session ID: {result.get('session_id', 'N/A')}")
    
    # Demo 2: Code Security Analysis
    print("\n📋 DEMO 2: Security Code Analysis")
    print("-" * 50)
    
    sample_code = """
    def login(username, password):
        # Secure authentication function
        if authenticate_user(username, password):
            session_id = generate_secure_session()
            return {"success": True, "session": session_id}
        return {"success": False}
    """
    
    code_context = SecurityContext(
        task_type=SecurityTaskType.CODE_REVIEW,
        authorization_scope="authorized code security review",
        target_system="internal_application",
        compliance_framework="OWASP",
        authorized_by="Security Team Lead"
    )
    
    code_result = assistant.analyze_security_code(sample_code, "python", code_context)
    print(f"✅ Analysis Status: {code_result['status']}")
    print(f"📊 Lines Analyzed: {code_result.get('lines_analyzed', 0)}")
    print(f"📊 Compliance Score: {code_result.get('compliance_score', 0)}")
    
    # Demo 3: Generate Professional Report
    print("\n📋 DEMO 3: Professional Security Report Generation")
    print("-" * 50)
    
    report = assistant.generate_security_report([result, code_result])
    print("📄 Security Report Generated:")
    print(report[:500] + "..." if len(report) > 500 else report)
    
    # Demo 4: Session Summary and Audit Trail
    print("\n📋 DEMO 4: Session Summary & Audit Trail")
    print("-" * 50)
    
    session_summary = assistant.get_session_summary()
    print(f"🔐 Session ID: {session_summary['session_id']}")
    print(f"📈 Active Contexts: {session_summary['active_contexts']}")
    print(f"✅ Ethical Compliance: {session_summary['ethical_compliance']}")
    print(f"📊 Audit Trail: {session_summary['audit_trail_available']}")
    
    # Demo 5: Authorization Status
    print("\n📋 DEMO 5: Authorization Status")
    print("-" * 50)
    
    auth_status = assistant.authorization_checker.get_authorization_status()
    print(f"🔒 Total Scopes: {auth_status['total_scopes']}")
    print(f"✅ Active Scopes: {auth_status['active_scopes']}")
    
    # Demo 6: Audit Report
    print("\n📋 DEMO 6: Comprehensive Audit Report")
    print("-" * 50)
    
    audit_report = assistant.audit_logger.generate_audit_report()
    print("📄 Audit Report Generated:")
    print(audit_report[:400] + "..." if len(audit_report) > 400 else audit_report)
    
    print("\n🎉 CyberCore Assistant Demonstration Complete!")
    print("\n🔍 Key Features Demonstrated:")
    print("  ✅ Ethical framework validation")
    print("  ✅ Authorization scope management")
    print("  ✅ Professional security assessments")
    print("  ✅ Comprehensive audit logging")
    print("  ✅ Industry-standard reporting")
    print("  ✅ Full compliance verification")
    
    print("\n📋 Industry Acceptance Features:")
    print("  ��️  OWASP methodology compliance")
    print("  🔐 GDPR/CCPA privacy compliance")
    print("  📊 Professional documentation")
    print("  🔍 Complete audit trail")
    print("  ⚖️  Ethical guidelines enforcement")
    print("  🎓 Professional certification support")

if __name__ == "__main__":
    main()
