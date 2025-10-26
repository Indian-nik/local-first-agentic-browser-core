"""Online Learning from User Interactions with RLAIF.

Implements:
- Real-time feedback processing
- Reinforcement Learning from AI/User Feedback (RLAIF)
- Automatic retry and error recovery
- Multi-modal interaction learning
- Dynamic goal adaptation
"""

import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import numpy as np

logger = logging.getLogger(__name__)

class FeedbackType(Enum):
    """Types of feedback that can be received."""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    CORRECTION = "correction"
    ENHANCEMENT = "enhancement"

@dataclass
class ActionResult:
    """Represents the result of an action taken by the agent."""
    action_id: str
    action_type: str
    parameters: Dict[str, Any]
    outcome: Any
    success: bool
    timestamp: datetime = field(default_factory=datetime.now)
    context: Dict[str, Any] = field(default_factory=dict)
    
@dataclass
class UserFeedback:
    """User feedback on an action result."""
    action_id: str
    feedback_type: FeedbackType
    rating: Optional[float] = None  # 0-1 scale
    correction: Optional[Dict[str, Any]] = None
    comment: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class LearningState:
    """Current learning state for an action type."""
    action_type: str
    success_rate: float = 0.0
    total_attempts: int = 0
    successful_attempts: int = 0
    average_rating: float = 0.0
    learned_parameters: Dict[str, Any] = field(default_factory=dict)
    last_updated: datetime = field(default_factory=datetime.now)

class OnlineLearner:
    """Online learning engine with RLAIF capabilities."""
    
    def __init__(self, learning_rate: float = 0.1, memory_size: int = 1000):
        """Initialize the online learner.
        
        Args:
            learning_rate: Rate at which to incorporate new feedback
            memory_size: Maximum number of interactions to remember
        """
        self.learning_rate = learning_rate
        self.memory_size = memory_size
        self.learning_states: Dict[str, LearningState] = {}
        self.interaction_history: List[Tuple[ActionResult, Optional[UserFeedback]]] = []
        self.retry_strategies: Dict[str, List[Dict[str, Any]]] = {}
        self._ready = True
        logger.info(f"OnlineLearner initialized with lr={learning_rate}, memory={memory_size}")
    
    def is_ready(self) -> bool:
        """Check if the learner is ready."""
        return self._ready
    
    def update_from_feedback(self, action_result: ActionResult, 
                           feedback: UserFeedback) -> None:
        """Update learning state from user feedback.
        
        Args:
            action_result: The action that was taken
            feedback: User feedback on the action
        """
        action_type = action_result.action_type
        
        # Initialize learning state if needed
        if action_type not in self.learning_states:
            self.learning_states[action_type] = LearningState(action_type=action_type)
        
        state = self.learning_states[action_type]
        
        # Update statistics
        state.total_attempts += 1
        if feedback.feedback_type == FeedbackType.POSITIVE:
            state.successful_attempts += 1
        
        state.success_rate = state.successful_attempts / state.total_attempts
        
        # Update average rating
        if feedback.rating is not None:
            old_avg = state.average_rating
            state.average_rating = (old_avg * (state.total_attempts - 1) + 
                                   feedback.rating) / state.total_attempts
        
        # Learn from corrections
        if feedback.correction:
            self._incorporate_correction(state, action_result, feedback.correction)
        
        # Store interaction
        self.interaction_history.append((action_result, feedback))
        if len(self.interaction_history) > self.memory_size:
            self.interaction_history.pop(0)
        
        state.last_updated = datetime.now()
        
        logger.info(f"Updated learning state for {action_type}: "
                   f"success_rate={state.success_rate:.2f}, "
                   f"avg_rating={state.average_rating:.2f}")
    
    def _incorporate_correction(self, state: LearningState, 
                               action_result: ActionResult,
                               correction: Dict[str, Any]) -> None:
        """Incorporate a correction into learned parameters."""
        for param, corrected_value in correction.items():
            if param in state.learned_parameters:
                # Blend old and new values
                old_value = state.learned_parameters[param]
                if isinstance(old_value, (int, float)) and isinstance(corrected_value, (int, float)):
                    state.learned_parameters[param] = (
                        (1 - self.learning_rate) * old_value + 
                        self.learning_rate * corrected_value
                    )
                else:
                    state.learned_parameters[param] = corrected_value
            else:
                state.learned_parameters[param] = corrected_value
    
    def optimize_action(self, action_type: str, 
                       base_parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Optimize action parameters based on learned experience.
        
        Args:
            action_type: Type of action to optimize
            base_parameters: Base parameters to start with
            
        Returns:
            Optimized parameters
        """
        if action_type not in self.learning_states:
            return base_parameters or {}
        
        state = self.learning_states[action_type]
        optimized = (base_parameters or {}).copy()
        
        # Apply learned parameters
        optimized.update(state.learned_parameters)
        
        logger.info(f"Optimized parameters for {action_type}: {optimized}")
        return optimized
    
    def should_retry(self, action_result: ActionResult) -> bool:
        """Determine if an action should be retried based on learned patterns.
        
        Args:
            action_result: The failed action result
            
        Returns:
            Whether to retry the action
        """
        action_type = action_result.action_type
        
        if action_type not in self.learning_states:
            return True  # Retry unknown actions
        
        state = self.learning_states[action_type]
        
        # Retry if success rate is reasonable
        return state.success_rate > 0.3 or state.total_attempts < 5
    
    def get_retry_strategy(self, action_result: ActionResult) -> Optional[Dict[str, Any]]:
        """Get a retry strategy for a failed action.
        
        Args:
            action_result: The failed action result
            
        Returns:
            Retry strategy with modified parameters, or None
        """
        action_type = action_result.action_type
        
        if action_type not in self.retry_strategies:
            self.retry_strategies[action_type] = []
        
        # Try learned parameters first
        if action_type in self.learning_states:
            state = self.learning_states[action_type]
            if state.learned_parameters:
                return {
                    'strategy': 'learned_parameters',
                    'parameters': state.learned_parameters
                }
        
        # Fall back to exploration
        return {
            'strategy': 'exploration',
            'parameters': self._explore_parameters(action_result.parameters)
        }
    
    def _explore_parameters(self, base_parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Explore parameter space for better solutions."""
        explored = base_parameters.copy()
        
        for key, value in explored.items():
            if isinstance(value, (int, float)):
                # Add small random variation
                variation = np.random.normal(0, 0.1) * value
                explored[key] = value + variation
        
        return explored
    
    def get_statistics(self, action_type: Optional[str] = None) -> Dict[str, Any]:
        """Get learning statistics.
        
        Args:
            action_type: Specific action type, or None for all
            
        Returns:
            Statistics dictionary
        """
        if action_type:
            if action_type in self.learning_states:
                state = self.learning_states[action_type]
                return {
                    'action_type': action_type,
                    'success_rate': state.success_rate,
                    'total_attempts': state.total_attempts,
                    'average_rating': state.average_rating,
                    'learned_parameters': state.learned_parameters
                }
            return {}
        
        return {
            'total_action_types': len(self.learning_states),
            'total_interactions': len(self.interaction_history),
            'action_types': {
                action_type: {
                    'success_rate': state.success_rate,
                    'total_attempts': state.total_attempts,
                    'average_rating': state.average_rating
                }
                for action_type, state in self.learning_states.items()
            }
        }
    
    def export_learning_state(self) -> str:
        """Export learning state as JSON."""
        state_dict = {
            'learning_states': {
                action_type: {
                    'action_type': state.action_type,
                    'success_rate': state.success_rate,
                    'total_attempts': state.total_attempts,
                    'successful_attempts': state.successful_attempts,
                    'average_rating': state.average_rating,
                    'learned_parameters': state.learned_parameters,
                    'last_updated': state.last_updated.isoformat()
                }
                for action_type, state in self.learning_states.items()
            },
            'meta': {
                'learning_rate': self.learning_rate,
                'memory_size': self.memory_size,
                'total_interactions': len(self.interaction_history)
            }
        }
        return json.dumps(state_dict, indent=2)
    
    def import_learning_state(self, state_json: str) -> None:
        """Import learning state from JSON."""
        state_dict = json.loads(state_json)
        
        self.learning_rate = state_dict['meta']['learning_rate']
        self.memory_size = state_dict['meta']['memory_size']
        
        self.learning_states = {}
        for action_type, state_data in state_dict['learning_states'].items():
            self.learning_states[action_type] = LearningState(
                action_type=state_data['action_type'],
                success_rate=state_data['success_rate'],
                total_attempts=state_data['total_attempts'],
                successful_attempts=state_data['successful_attempts'],
                average_rating=state_data['average_rating'],
                learned_parameters=state_data['learned_parameters'],
                last_updated=datetime.fromisoformat(state_data['last_updated'])
            )
        
        logger.info(f"Imported learning state with {len(self.learning_states)} action types")
