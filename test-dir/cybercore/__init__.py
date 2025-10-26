"""
CyberCore Assistant - Security Professional Edition
Ethical AI Framework for Cybersecurity Professionals
"""

__version__ = "1.0.0"
__author__ = "CyberCore Security Team"
__license__ = "MIT"

from .security.cybercore_assistant import CyberCoreAssistant
from .security.ethical_framework import EthicalSecurityFramework
from .security.authorization import AuthorizationValidator
from .security.audit_logger import SecurityAuditLogger

__all__ = [
    'CyberCoreAssistant',
    'EthicalSecurityFramework',
    'AuthorizationValidator',
    'SecurityAuditLogger'
]
