"""Learning state data model."""

from dataclasses import dataclass, field
from typing import Dict, Any
from datetime import datetime

@dataclass
class LearningStateModel:
    """Persistable learning state."""
    action_type: str
    success_rate: float = 0.0
    total_attempts: int = 0
    successful_attempts: int = 0
    average_rating: float = 0.0
    learned_parameters: Dict[str, Any] = field(default_factory=dict)
    last_updated: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'action_type': self.action_type,
            'success_rate': self.success_rate,
            'total_attempts': self.total_attempts,
            'successful_attempts': self.successful_attempts,
            'average_rating': self.average_rating,
            'learned_parameters': self.learned_parameters,
            'last_updated': self.last_updated.isoformat(),
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LearningStateModel':
        """Create from dictionary."""
        data = data.copy()
        data['last_updated'] = datetime.fromisoformat(data['last_updated'])
        return cls(**data)
