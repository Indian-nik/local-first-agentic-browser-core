"""STQA (Software Testing and Quality Assurance) Module

Comprehensive quality assurance framework for software testing,
automation, performance testing, and quality metrics.
"""

__version__ = "5.0.0"
__author__ = "CyberCore Security Team"

from .tester import SoftwareTester
from .automation import TestAutomation
from .quality_analyzer import QualityAnalyzer

__all__ = [
    'SoftwareTester',
    'TestAutomation',
    'QualityAnalyzer'
]
