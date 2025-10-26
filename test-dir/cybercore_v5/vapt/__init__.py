"""VAPT (Vulnerability Assessment and Penetration Testing) Module

Comprehensive security testing framework for web applications,
networks, APIs, and infrastructure.
"""

__version__ = "5.0.0"
__author__ = "CyberCore Security Team"

from .scanner import VulnerabilityScanner
from .pentester import PenetrationTester
from .reporter import VAPTReporter

__all__ = [
    'VulnerabilityScanner',
    'PenetrationTester',
    'VAPTReporter'
]
