"""Skill Acquisition and Improvement Engine.

Implements:
- Skill gap identification
- Adaptive learning path generation
- Difficulty adjustment
- Progress tracking
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)

class SkillLevel(Enum):
    NOVICE = 0
    BEGINNER = 1
    INTERMEDIATE = 2
    ADVANCED = 3
    EXPERT = 4

@dataclass
class Skill:
    name: str
    mastery: float = 0.0  # 0-1 scale
    attempts: int = 0
    successes: int = 0
    last_practiced: Optional[datetime] = None

@dataclass
class SkillGap:
    skill_name: str
    current_level: float
    target_level: float
    severity: float  # 0-1 scale
    priority: int = 0

@dataclass
class LearningModule:
    id: str
    skill: str
    difficulty: float  # 0-1 scale
    content: Any
    prerequisites: List[str] = field(default_factory=list)

class SkillAcquisitionEngine:
    """Engine for identifying gaps and creating learning paths."""
    
    def __init__(self):
        self.user_skills: Dict[str, Dict[str, Skill]] = {}
        self.learning_modules: List[LearningModule] = []
        self._ready = True
        logger.info("SkillAcquisitionEngine initialized")
    
    def is_ready(self) -> bool:
        return self._ready
    
    def analyze_gaps(self, user_id: str, target_skills: Dict[str, float]) -> List[SkillGap]:
        """Identify skill gaps."""
        gaps = []
        user_profile = self.user_skills.get(user_id, {})
        
        for skill_name, target_level in target_skills.items():
            current_skill = user_profile.get(skill_name)
            current_level = current_skill.mastery if current_skill else 0.0
            
            if current_level < target_level:
                gap = SkillGap(
                    skill_name=skill_name,
                    current_level=current_level,
                    target_level=target_level,
                    severity=(target_level - current_level) / target_level
                )
                gaps.append(gap)
        
        # Sort by severity (descending)
        gaps.sort(key=lambda x: x.severity, reverse=True)
        logger.info(f"Identified {len(gaps)} skill gaps for user {user_id}")
        return gaps
    
    def create_learning_path(self, gaps: List[SkillGap], learning_style: str = "adaptive") -> List[LearningModule]:
        """Generate ordered learning path."""
        path = []
        
        for gap in gaps:
            # Find modules for this skill
            matching_modules = [
                m for m in self.learning_modules 
                if m.skill == gap.skill_name
            ]
            
            # Sort by difficulty
            matching_modules.sort(key=lambda x: x.difficulty)
            
            # Add modules progressively
            for module in matching_modules:
                if module.difficulty <= gap.target_level:
                    path.append(module)
        
        logger.info(f"Created learning path with {len(path)} modules")
        return path
    
    def get_adaptive_content(self, user_id: str, skill_name: str) -> Optional[LearningModule]:
        """Get next adaptive content based on progress."""
        user_profile = self.user_skills.get(user_id, {})
        skill = user_profile.get(skill_name)
        
        if not skill:
            # Start with easiest module
            modules = [m for m in self.learning_modules if m.skill == skill_name]
            if modules:
                modules.sort(key=lambda x: x.difficulty)
                return modules[0]
            return None
        
        # Find module matching current mastery level
        target_difficulty = min(skill.mastery + 0.1, 1.0)
        matching = [
            m for m in self.learning_modules
            if m.skill == skill_name and abs(m.difficulty - target_difficulty) < 0.2
        ]
        
        if matching:
            matching.sort(key=lambda x: abs(x.difficulty - target_difficulty))
            return matching[0]
        
        return None
    
    def track_progress(self, user_id: str, skill_name: str, success: bool) -> None:
        """Track learning progress."""
        if user_id not in self.user_skills:
            self.user_skills[user_id] = {}
        
        if skill_name not in self.user_skills[user_id]:
            self.user_skills[user_id][skill_name] = Skill(name=skill_name)
        
        skill = self.user_skills[user_id][skill_name]
        skill.attempts += 1
        if success:
            skill.successes += 1
        
        # Update mastery using exponential moving average
        success_rate = skill.successes / skill.attempts
        skill.mastery = 0.7 * skill.mastery + 0.3 * success_rate
        skill.last_practiced = datetime.now()
        
        logger.debug(f"Updated skill {skill_name} for user {user_id}: mastery={skill.mastery:.2f}")
