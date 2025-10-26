"""User profile data model."""

from dataclasses import dataclass, field
from typing import Dict, List, Any
from datetime import datetime

@dataclass
class UserProfile:
    """Complete user profile with preferences and skills."""
    user_id: str
    preferences: Dict[str, Any] = field(default_factory=dict)
    skill_mastery: Dict[str, float] = field(default_factory=dict)
    constraints: Dict[str, Any] = field(default_factory=dict)
    privacy_opts: Dict[str, bool] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def update_preference(self, key: str, value: Any) -> None:
        """Update a user preference."""
        self.preferences[key] = value
        self.updated_at = datetime.now()
    
    def update_skill(self, skill: str, mastery: float) -> None:
        """Update skill mastery level."""
        self.skill_mastery[skill] = max(0.0, min(1.0, mastery))
        self.updated_at = datetime.now()
    
    def get_skill_level(self, skill: str) -> float:
        """Get mastery level for a skill."""
        return self.skill_mastery.get(skill, 0.0)
