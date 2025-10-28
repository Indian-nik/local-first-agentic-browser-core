"""
CyberCore Advanced Red Teaming Module
Sophisticated adversary simulation and red team operations
"""

from .apt_simulator import APTSimulator
from .attack_chain import AttackChainBuilder
from .persistence_engine import PersistenceEngine
from .c2_framework import C2Framework
from .evasion_engine import EvasionEngine
from .social_engineering import SocialEngineeringFramework

__all__ = [
    'APTSimulator',
    'AttackChainBuilder', 
    'PersistenceEngine',
    'C2Framework',
    'EvasionEngine',
    'SocialEngineeringFramework'
]
