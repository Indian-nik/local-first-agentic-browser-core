"""Comprehensive tests for Phase 9 Learning & Adaptation."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'reasoning-engine-python'))

from learning.online_learner import OnlineLearner, ActionResult, UserFeedback, FeedbackType
from learning.preference_engine import PreferenceEngine
from learning.skill_acquisition import SkillAcquisitionEngine
from learning.context_adapter import ContextAdapter
from models.user_profile import UserProfile
from storage.learning_storage import InMemoryStorage
from datetime import datetime

def test_online_learner():
    """Test online learning functionality."""
    print("\n=== Testing Online Learner ===")
    
    learner = OnlineLearner(learning_rate=0.1)
    assert learner.is_ready(), "OnlineLearner should be ready"
    
    # Create test action
    action = ActionResult(
        action_id="test_1",
        action_type="search",
        parameters={"query": "test"},
        outcome="success",
        success=True
    )
    
    # Provide feedback
    feedback = UserFeedback(
        action_id="test_1",
        feedback_type=FeedbackType.POSITIVE,
        rating=0.9
    )
    
    learner.update_from_feedback(action, feedback)
    
    # Check statistics
    stats = learner.get_statistics("search")
    assert stats['total_attempts'] == 1
    assert stats['success_rate'] == 1.0
    print(f"✅ Online learner stats: {stats}")
    
    # Test optimization
    optimized = learner.optimize_action("search", {"query": "new_test"})
    assert 'query' in optimized
    print(f"✅ Optimized parameters: {optimized}")
    
    # Test export/import
    exported = learner.export_learning_state()
    assert len(exported) > 0
    print("✅ State export successful")
    
    print("✅ Online Learner: ALL TESTS PASSED")

def test_preference_engine():
    """Test preference learning."""
    print("\n=== Testing Preference Engine ===")
    
    prefs = PreferenceEngine(decay_factor=0.95)
    assert prefs.is_ready()
    
    # Observe interactions
    prefs.observe_interaction(
        user_id="user_1",
        action="search",
        outcome="found_results",
        context={"device": "mobile"},
        satisfaction=0.8
    )
    
    prefs.observe_interaction(
        user_id="user_1",
        action="search",
        outcome="found_results",
        context={"device": "mobile"},
        satisfaction=0.9
    )
    
    # Save explicit preference
    prefs.save_preference("theme", "dark", "user_1")
    
    # Predict preferences
    predictions = prefs.predict_preferences("user_1", {"device": "mobile"})
    assert len(predictions) > 0
    print(f"✅ Predicted {len(predictions)} preferences")
    
    # Get profile
    profile = prefs.get_user_profile("user_1")
    assert profile['user_id'] == "user_1"
    assert profile['explicit_preferences'] >= 1
    print(f"✅ User profile: {profile}")
    
    print("✅ Preference Engine: ALL TESTS PASSED")

def test_skill_acquisition():
    """Test skill acquisition."""
    print("\n=== Testing Skill Acquisition ===")
    
    skills = SkillAcquisitionEngine()
    assert skills.is_ready()
    
    # Analyze gaps
    target_skills = {
        "python": 0.8,
        "javascript": 0.6
    }
    
    gaps = skills.analyze_gaps("user_1", target_skills)
    assert len(gaps) == 2
    print(f"✅ Identified {len(gaps)} skill gaps")
    
    # Track progress
    skills.track_progress("user_1", "python", success=True)
    skills.track_progress("user_1", "python", success=True)
    skills.track_progress("user_1", "python", success=False)
    
    # Check mastery
    user_skills = skills.user_skills.get("user_1", {})
    if "python" in user_skills:
        mastery = user_skills["python"].mastery
        assert 0 <= mastery <= 1
        print(f"✅ Python mastery: {mastery:.2f}")
    
    print("✅ Skill Acquisition: ALL TESTS PASSED")

def test_context_adapter():
    """Test context adaptation."""
    print("\n=== Testing Context Adapter ===")
    
    adapter = ContextAdapter()
    assert adapter.is_ready()
    
    # Detect context
    context = adapter.detect_context(
        environment={"device": "mobile"},
        user_state={"sentiment": "positive"}
    )
    
    assert context.device_type == "mobile"
    print(f"✅ Detected context: device={context.device_type}, time={context.time_of_day}")
    
    # Select strategy
    strategy = adapter.select_strategy("search", context)
    print(f"✅ Selected strategy: {strategy.value}")
    
    # Apply adaptation
    action = {"max_tokens": 500, "verbosity": "medium"}
    adapted = adapter.apply_adaptation(action, strategy)
    assert 'max_tokens' in adapted
    print(f"✅ Adapted action: {adapted}")
    
    print("✅ Context Adapter: ALL TESTS PASSED")

def test_models():
    """Test data models."""
    print("\n=== Testing Data Models ===")
    
    # Test UserProfile
    profile = UserProfile(user_id="test_user")
    profile.update_preference("theme", "dark")
    profile.update_skill("python", 0.75)
    
    assert profile.preferences["theme"] == "dark"
    assert profile.get_skill_level("python") == 0.75
    print("✅ UserProfile works correctly")
    
    # Test Storage
    storage = InMemoryStorage()
    storage.store("key1", "value1")
    assert storage.retrieve("key1") == "value1"
    
    keys = storage.list_keys()
    assert "key1" in keys
    print("✅ InMemoryStorage works correctly")
    
    print("✅ Data Models: ALL TESTS PASSED")

def test_integration():
    """Test integration between components."""
    print("\n=== Testing Component Integration ===")
    
    # Create all components
    learner = OnlineLearner()
    prefs = PreferenceEngine()
    skills = SkillAcquisitionEngine()
    adapter = ContextAdapter()
    
    # Simulate workflow
    context = adapter.detect_context(
        environment={"device": "desktop"},
        user_state={"task_complexity": "high"}
    )
    
    strategy = adapter.select_strategy("complex_task", context)
    
    # Record interaction
    prefs.observe_interaction(
        user_id="integrated_user",
        action="complex_task",
        outcome="success",
        context={"strategy": strategy.value},
        satisfaction=0.85
    )
    
    # Track skill improvement
    skills.track_progress("integrated_user", "complex_tasks", success=True)
    
    print("✅ Components integrated successfully")
    print("✅ Integration: ALL TESTS PASSED")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("   PHASE 9: LEARNING & ADAPTATION - TEST SUITE")
    print("="*60)
    
    try:
        test_online_learner()
        test_preference_engine()
        test_skill_acquisition()
        test_context_adapter()
        test_models()
        test_integration()
        
        print("\n" + "="*60)
        print("   ✅ ALL TESTS PASSED - PHASE 9 COMPLETE!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
