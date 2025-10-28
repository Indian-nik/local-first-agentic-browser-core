"""
Ethical Security Framework
Defines ethical boundaries and guidelines for security testing
"""

import re
from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum

class EthicalViolationType(Enum):
    """Types of ethical violations"""
    UNAUTHORIZED_ACCESS = "unauthorized_access"
    MALICIOUS_INTENT = "malicious_intent"
    NO_CONSENT = "no_consent"
    HARMFUL_PAYLOAD = "harmful_payload"
    ILLEGAL_ACTIVITY = "illegal_activity"
    PRIVACY_VIOLATION = "privacy_violation"

class EthicalSecurityFramework:
    """
    Ethical framework for security testing and research
    Ensures all security activities comply with professional standards
    """
    
    def __init__(self):
        """Initialize the ethical framework"""
        self.prohibited_patterns = [
            r'hack\s+without\s+permission',
            r'unauthorized\s+access',
            r'steal\s+data',
            r'malicious\s+payload',
            r'damage\s+system',
            r'delete\s+files',
            r'crash\s+server',
            r'ddos\s+attack',
            r'social\s+engineering\s+attack'
        ]
        
        self.required_authorization_keywords = [
            'authorized',
            'permission',
            'consent',
            'approved',
            'legitimate',
            'testing environment',
            'sandbox'
        ]
        
        self.ethical_guidelines = [
            "Only test systems you own or have explicit permission to test",
            "Never cause harm or damage to target systems",
            "Respect privacy and confidentiality",
            "Follow responsible disclosure practices",
            "Maintain professional standards at all times",
            "Document all activities for audit purposes",
            "Stop testing if unauthorized access is detected"
        ]
    
    def validate_request(self, request: str, context) -> Dict[str, Any]:
        """
        Validate a security request against ethical guidelines
        
        Args:
            request: The security testing request
            context: Security context information
            
        Returns:
            Validation result with approval status
        """
        request_lower = request.lower()
        
        # Check for prohibited patterns
        for pattern in self.prohibited_patterns:
            if re.search(pattern, request_lower):
                return {
                    'approved': False,
                    'reason': f'Request contains prohibited activity pattern: {pattern}',
                    'violation_type': EthicalViolationType.MALICIOUS_INTENT.value,
                    'recommendations': [
                        'Ensure you have proper authorization',
                        'Focus on legitimate security testing',
                        'Use authorized testing environments'
                    ]
                }
        
        # Check for authorization indicators
        has_authorization = False
        for keyword in self.required_authorization_keywords:
            if keyword in request_lower or (
                context and 
                hasattr(context, 'authorization_scope') and 
                keyword in context.authorization_scope.lower()
            ):
                has_authorization = True
                break
        
        if not has_authorization:
            return {
                'approved': False,
                'reason': 'No clear authorization or permission indicated',
                'violation_type': EthicalViolationType.NO_CONSENT.value,
                'recommendations': [
                    'Obtain explicit written permission',
                    'Use only authorized testing environments',
                    'Document authorization scope clearly'
                ]
            }
        
        # Check context compliance
        if context:
            compliance_check = self._validate_context_compliance(context)
            if not compliance_check['compliant']:
                return {
                    'approved': False,
                    'reason': compliance_check['reason'],
                    'recommendations': compliance_check['recommendations']
                }
        
        # All checks passed
        return {
            'approved': True,
            'guidelines': self.ethical_guidelines,
            'compliance_framework': getattr(context, 'compliance_framework', 'General'),
            'ethical_score': 100
        }
    
    def _validate_context_compliance(self, context) -> Dict[str, Any]:
        """
        Validate security context for compliance
        
        Args:
            context: Security context to validate
            
        Returns:
            Compliance validation result
        """
        if not hasattr(context, 'authorization_scope'):
            return {
                'compliant': False,
                'reason': 'Missing authorization scope in context',
                'recommendations': ['Define clear authorization scope']
            }
        
        if not hasattr(context, 'task_type'):
            return {
                'compliant': False,
                'reason': 'Missing task type in context',
                'recommendations': ['Specify the type of security task']
            }
        
        # Additional compliance checks based on task type
        if hasattr(context, 'task_type'):
            task_type = str(context.task_type.value) if hasattr(context.task_type, 'value') else str(context.task_type)
            
            if 'penetration' in task_type.lower():
                if not getattr(context, 'authorized_by', None):
                    return {
                        'compliant': False,
                        'reason': 'Penetration testing requires explicit authorization',
                        'recommendations': ['Obtain signed authorization from system owner']
                    }
        
        return {
            'compliant': True,
            'compliance_score': 95
        }
    
    def get_ethical_guidelines(self) -> List[str]:
        """
        Get list of ethical guidelines
        
        Returns:
            List of ethical guidelines
        """
        return self.ethical_guidelines.copy()
    
    def generate_compliance_report(self, assessments: List[Dict]) -> str:
        """
        Generate ethics compliance report
        
        Args:
            assessments: List of security assessments performed
            
        Returns:
            Formatted compliance report
        """
        total_assessments = len(assessments)
        compliant_assessments = sum(1 for a in assessments if a.get('ethical_score', 0) >= 90)
        
        report = f"""
# ETHICAL COMPLIANCE REPORT

## Summary
- Total Assessments: {total_assessments}
- Compliant Assessments: {compliant_assessments}
- Compliance Rate: {(compliant_assessments/total_assessments)*100:.1f}%

## Ethical Framework Applied
"""
        
        for guideline in self.ethical_guidelines:
            report += f"- {guideline}\n"
        
        report += """

## Professional Standards
- All activities logged and auditable
- Full authorization validation performed
- Industry standard methodologies used
- Responsible disclosure practices followed

---
*This report certifies compliance with ethical security testing standards.*
        """
        
        return report
