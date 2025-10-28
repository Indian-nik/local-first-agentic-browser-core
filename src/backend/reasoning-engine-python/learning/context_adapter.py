"""Context-Aware Behavior Adaptation.

Implements:
- Environmental context detection
- Strategy selection based on context
- Dynamic behavior adaptation
- Fallback mechanisms
"""

import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)

class ContextType(Enum):
    DEVICE = "device"
    TIME = "time"
    LOCATION = "location"
    TASK = "task"
    SENTIMENT = "sentiment"

class AdaptationStrategy(Enum):
    VERBOSE = "verbose"
    CONCISE = "concise"
    PROACTIVE = "proactive"
    REACTIVE = "reactive"
    CAUTIOUS = "cautious"
    CONFIDENT = "confident"

@dataclass
class Context:
    device_type: Optional[str] = None
    time_of_day: Optional[str] = None
    task_complexity: Optional[str] = None
    user_sentiment: Optional[str] = None
    network_quality: Optional[str] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

class ContextAdapter:
    """Adapts agent behavior based on context."""
    
    def __init__(self):
        self._ready = True
        self.context_history = []
        logger.info("ContextAdapter initialized")
    
    def is_ready(self) -> bool:
        return self._ready
    
    def detect_context(self, environment: Optional[Dict[str, Any]] = None,
                      user_state: Optional[Dict[str, Any]] = None) -> Context:
        """Detect current context."""
        env = environment or {}
        state = user_state or {}
        
        context = Context(
            device_type=env.get('device', 'desktop'),
            time_of_day=self._get_time_category(),
            task_complexity=state.get('task_complexity', 'medium'),
            user_sentiment=state.get('sentiment', 'neutral'),
            network_quality=env.get('network', 'good')
        )
        
        self.context_history.append(context)
        logger.debug(f"Detected context: device={context.device_type}, time={context.time_of_day}")
        return context
    
    def _get_time_category(self) -> str:
        """Categorize current time."""
        hour = datetime.now().hour
        if 6 <= hour < 12:
            return "morning"
        elif 12 <= hour < 17:
            return "afternoon"
        elif 17 <= hour < 22:
            return "evening"
        else:
            return "night"
    
    def select_strategy(self, task: str, context: Context) -> AdaptationStrategy:
        """Select adaptation strategy based on context."""
        # Mobile devices: be concise
        if context.device_type in ['mobile', 'tablet']:
            return AdaptationStrategy.CONCISE
        
        # Late hours: be cautious
        if context.time_of_day == "night":
            return AdaptationStrategy.CAUTIOUS
        
        # Negative sentiment: be reactive and careful
        if context.user_sentiment in ['negative', 'frustrated']:
            return AdaptationStrategy.REACTIVE
        
        # Complex tasks: be verbose and proactive
        if context.task_complexity == "high":
            return AdaptationStrategy.VERBOSE
        
        # Default: confident
        return AdaptationStrategy.CONFIDENT
    
    def apply_adaptation(self, action: Dict[str, Any], 
                        strategy: AdaptationStrategy) -> Dict[str, Any]:
        """Apply strategy to action."""
        adapted = action.copy()
        
        if strategy == AdaptationStrategy.CONCISE:
            adapted['max_tokens'] = adapted.get('max_tokens', 500) // 2
            adapted['verbosity'] = 'low'
        
        elif strategy == AdaptationStrategy.VERBOSE:
            adapted['max_tokens'] = adapted.get('max_tokens', 500) * 2
            adapted['verbosity'] = 'high'
            adapted['include_explanations'] = True
        
        elif strategy == AdaptationStrategy.CAUTIOUS:
            adapted['require_confirmation'] = True
            adapted['confidence_threshold'] = 0.8
        
        elif strategy == AdaptationStrategy.PROACTIVE:
            adapted['suggest_alternatives'] = True
            adapted['anticipate_needs'] = True
        
        logger.debug(f"Applied {strategy.value} strategy to action")
        return adapted
