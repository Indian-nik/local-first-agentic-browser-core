"""Learning and Adaptation Module for Agentic Browser.

Provides:
- Online learning from user interactions (RLAIF)
- Preference learning and personalization
- Skill acquisition and improvement
- Context-aware behavior adaptation
"""

from .online_learner import OnlineLearner
from .preference_engine import PreferenceEngine
from .skill_acquisition import SkillAcquisitionEngine
from .context_adapter import ContextAdapter

__all__ = [
    'OnlineLearner',
    'PreferenceEngine',
    'SkillAcquisitionEngine',
    'ContextAdapter',
]

__version__ = '1.0.0'
