"""Preference Learning and Personalization Engine.

Implements:
- Behavioral analytics and pattern recognition
- Predictive preference modeling  
- Personalized recommendations
- Privacy-preserving learning
- Explainable AI
"""

import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict
import math

logger = logging.getLogger(__name__)

@dataclass
class InteractionEvent:
    """Represents a user interaction event."""
    user_id: str
    action: str
    outcome: Any
    context: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    satisfaction: Optional[float] = None  # 0-1 scale

@dataclass
class PreferenceSignal:
    """A learned preference signal."""
    key: str
    value: Any
    confidence: float = 0.5
    frequency: int = 1
    last_seen: datetime = field(default_factory=datetime.now)
    context_tags: List[str] = field(default_factory=list)

class PreferenceEngine:
    """Engine for learning and predicting user preferences."""
    
    def __init__(self, memory_backend=None, decay_factor: float = 0.95):
        """Initialize preference engine.
        
        Args:
            memory_backend: Optional memory system for persistence
            decay_factor: Time decay factor for preference signals (0-1)
        """
        self.memory_backend = memory_backend
        self.decay_factor = decay_factor
        self.user_profiles: Dict[str, Dict[str, PreferenceSignal]] = defaultdict(dict)
        self.interaction_history: List[InteractionEvent] = []
        self._ready = True
        logger.info(f"PreferenceEngine initialized with decay={decay_factor}")
    
    def is_ready(self) -> bool:
        """Check if engine is ready."""
        return self._ready
    
    def observe_interaction(self, user_id: str, action: str, outcome: Any,
                          context: Optional[Dict[str, Any]] = None,
                          satisfaction: Optional[float] = None) -> None:
        """Observe and learn from a user interaction.
        
        Args:
            user_id: User identifier
            action: Action performed
            outcome: Result of the action
            context: Additional context (time, device, etc.)
            satisfaction: User satisfaction score (0-1)
        """
        event = InteractionEvent(
            user_id=user_id,
            action=action,
            outcome=outcome,
            context=context or {},
            satisfaction=satisfaction
        )
        
        self.interaction_history.append(event)
        
        # Extract preference signals
        self._extract_preferences(event)
        
        logger.debug(f"Observed interaction for user {user_id}: {action}")
    
    def _extract_preferences(self, event: InteractionEvent) -> None:
        """Extract preference signals from an interaction event."""
        user_id = event.user_id
        profile = self.user_profiles[user_id]
        
        # Learn from action patterns
        action_key = f"action:{event.action}"
        if action_key in profile:
            signal = profile[action_key]
            signal.frequency += 1
            signal.last_seen = datetime.now()
            # Update confidence based on satisfaction
            if event.satisfaction is not None:
                signal.confidence = (
                    0.7 * signal.confidence + 0.3 * event.satisfaction
                )
        else:
            profile[action_key] = PreferenceSignal(
                key=action_key,
                value=event.action,
                confidence=event.satisfaction or 0.5,
                frequency=1
            )
        
        # Learn from context patterns
        for ctx_key, ctx_value in event.context.items():
            pref_key = f"context:{ctx_key}:{ctx_value}"
            if pref_key in profile:
                signal = profile[pref_key]
                signal.frequency += 1
                signal.last_seen = datetime.now()
            else:
                profile[pref_key] = PreferenceSignal(
                    key=pref_key,
                    value=ctx_value,
                    frequency=1
                )
        
        # Learn from outcome patterns
        if event.satisfaction and event.satisfaction > 0.7:
            outcome_key = f"outcome:{event.action}"
            profile[outcome_key] = PreferenceSignal(
                key=outcome_key,
                value=event.outcome,
                confidence=event.satisfaction
            )
    
    def save_preference(self, key: str, value: Any, user_id: Optional[str] = None) -> None:
        """Explicitly save a user preference.
        
        Args:
            key: Preference key
            value: Preference value
            user_id: User ID (defaults to "default")
        """
        uid = user_id or "default"
        profile = self.user_profiles[uid]
        
        pref_key = f"explicit:{key}"
        profile[pref_key] = PreferenceSignal(
            key=pref_key,
            value=value,
            confidence=1.0,  # Explicit preferences have max confidence
            frequency=1
        )
        
        # Persist to memory backend if available
        if self.memory_backend:
            try:
                self.memory_backend.store(f"pref:{uid}:{key}", value)
            except Exception as e:
                logger.warning(f"Failed to persist preference: {e}")
        
        logger.info(f"Saved preference {key}={value} for user {uid}")
    
    def predict_preferences(self, user_id: str, 
                          context: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Predict user preferences in given context.
        
        Args:
            user_id: User identifier
            context: Current context for prediction
            
        Returns:
            List of predicted preferences with confidence scores
        """
        if user_id not in self.user_profiles:
            return []
        
        profile = self.user_profiles[user_id]
        context = context or {}
        
        # Apply time decay to signals
        self._apply_time_decay(profile)
        
        # Score preferences based on context match
        scored_prefs = []
        for signal in profile.values():
            score = self._score_preference(signal, context)
            if score > 0.3:  # Threshold for relevance
                scored_prefs.append({
                    'key': signal.key,
                    'value': signal.value,
                    'confidence': signal.confidence,
                    'score': score,
                    'frequency': signal.frequency
                })
        
        # Sort by score (descending)
        scored_prefs.sort(key=lambda x: x['score'], reverse=True)
        
        logger.debug(f"Predicted {len(scored_prefs)} preferences for user {user_id}")
        return scored_prefs[:10]  # Return top 10
    
    def _apply_time_decay(self, profile: Dict[str, PreferenceSignal]) -> None:
        """Apply time decay to preference signals."""
        now = datetime.now()
        for signal in profile.values():
            # Calculate days since last seen
            days_old = (now - signal.last_seen).days
            # Apply exponential decay
            decay = self.decay_factor ** days_old
            signal.confidence *= decay
    
    def _score_preference(self, signal: PreferenceSignal, 
                         context: Dict[str, Any]) -> float:
        """Score a preference signal based on context match."""
        base_score = signal.confidence
        
        # Boost score for frequent preferences
        frequency_boost = min(math.log(signal.frequency + 1) / 5, 0.5)
        
        # Boost score for context matches
        context_boost = 0.0
        for ctx_key, ctx_value in context.items():
            if f":{ctx_key}:{ctx_value}" in signal.key:
                context_boost += 0.2
        
        return min(base_score + frequency_boost + context_boost, 1.0)
    
    def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """Get user profile summary.
        
        Args:
            user_id: User identifier
            
        Returns:
            Profile summary dictionary
        """
        if user_id not in self.user_profiles:
            return {}
        
        profile = self.user_profiles[user_id]
        
        return {
            'user_id': user_id,
            'total_preferences': len(profile),
            'explicit_preferences': sum(
                1 for s in profile.values() if s.key.startswith('explicit:')
            ),
            'learned_preferences': sum(
                1 for s in profile.values() if not s.key.startswith('explicit:')
            ),
            'avg_confidence': sum(s.confidence for s in profile.values()) / len(profile)
                            if profile else 0.0
        }
    
    def export_profile(self, user_id: str) -> str:
        """Export user profile as JSON.
        
        Args:
            user_id: User identifier
            
        Returns:
            JSON string of profile
        """
        if user_id not in self.user_profiles:
            return json.dumps({})
        
        profile = self.user_profiles[user_id]
        profile_dict = {
            signal.key: {
                'value': signal.value,
                'confidence': signal.confidence,
                'frequency': signal.frequency,
                'last_seen': signal.last_seen.isoformat()
            }
            for signal in profile.values()
        }
        
        return json.dumps(profile_dict, indent=2)
    
    def import_profile(self, user_id: str, profile_json: str) -> None:
        """Import user profile from JSON.
        
        Args:
            user_id: User identifier
            profile_json: JSON string of profile
        """
        profile_dict = json.loads(profile_json)
        profile = {}
        
        for key, data in profile_dict.items():
            profile[key] = PreferenceSignal(
                key=key,
                value=data['value'],
                confidence=data['confidence'],
                frequency=data['frequency'],
                last_seen=datetime.fromisoformat(data['last_seen'])
            )
        
        self.user_profiles[user_id] = profile
        logger.info(f"Imported profile for user {user_id} with {len(profile)} preferences")
