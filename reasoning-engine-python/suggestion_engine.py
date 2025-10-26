#!/usr/bin/env python3
"""
User Suggestion Engine for Workflow Improvements
Phase 6: Advanced Features - Cross-Service Workflow Automation
"""

import time
from typing import Dict, List, Tuple, Set
from dataclasses import dataclass, field
import json
from collections import defaultdict

@dataclass
class WorkflowPattern:
    """Detected workflow pattern"""
    pattern_id: str
    workflow_steps: List[str]
    frequency: int
    avg_duration: float
    optimization_potential: float

@dataclass
class ImprovementSuggestion:
    """Suggested workflow improvement"""
    suggestion_id: str
    category: str  # 'performance', 'cost', 'reliability', 'usability'
    title: str
    description: str
    impact: str  # 'high', 'medium', 'low'
    effort: str  # 'high', 'medium', 'low'
    expected_benefit: str
    implementation_steps: List[str]
    related_workflows: List[str] = field(default_factory=list)

class SuggestionEngine:
    """AI-powered suggestion engine for workflow improvements"""
    
    def __init__(self):
        self.workflow_history: List[Dict] = []
        self.patterns: Dict[str, WorkflowPattern] = {}
        self.suggestions: List[ImprovementSuggestion] = []
        self.user_feedback: Dict[str, str] = {}  # suggestion_id -> feedback
        
    def analyze_workflow(self, workflow_data: Dict):
        """Analyze a workflow execution"""
        self.workflow_history.append({
            **workflow_data,
            'timestamp': time.time()
        })
        
        # Detect patterns every 10 workflows
        if len(self.workflow_history) % 10 == 0:
            self._detect_patterns()
            self._generate_suggestions()
    
    def _detect_patterns(self):
        """Detect common workflow patterns"""
        step_sequences = defaultdict(list)
        
        for wf in self.workflow_history[-50:]:
            steps = tuple(wf.get('steps', []))
            if len(steps) > 1:
                step_sequences[steps].append(wf.get('duration', 0))
        
        # Create patterns from frequent sequences
        for steps, durations in step_sequences.items():
            if len(durations) >= 3:
                pattern_id = f"pattern_{hash(steps) % 10000}"
                self.patterns[pattern_id] = WorkflowPattern(
                    pattern_id=pattern_id,
                    workflow_steps=list(steps),
                    frequency=len(durations),
                    avg_duration=sum(durations) / len(durations),
                    optimization_potential=self._calculate_optimization_potential(durations)
                )
        
        print(f"[SuggestionEngine] Detected {len(self.patterns)} patterns")
    
    def _calculate_optimization_potential(self, durations: List[float]) -> float:
        """Calculate optimization potential score"""
        if len(durations) < 2:
            return 0.0
        
        import numpy as np
        avg = np.mean(durations)
        std = np.std(durations)
        
        # Higher variance and longer durations = higher potential
        potential = (std / (avg + 0.001)) * (avg / 10.0)
        return min(potential, 1.0)
    
    def _generate_suggestions(self):
        """Generate improvement suggestions"""
        new_suggestions = []
        
        # Analyze patterns for suggestions
        for pattern in self.patterns.values():
            if pattern.optimization_potential > 0.5:
                new_suggestions.append(ImprovementSuggestion(
                    suggestion_id=f"sugg_{pattern.pattern_id}",
                    category='performance',
                    title=f"Optimize frequent workflow pattern",
                    description=f"This workflow pattern (steps: {' -> '.join(pattern.workflow_steps[:3])}) "
                                f"occurs {pattern.frequency} times with high variance.",
                    impact='high',
                    effort='medium',
                    expected_benefit=f"Reduce average execution time by ~{int(pattern.optimization_potential * 30)}%",
                    implementation_steps=[
                        "1. Enable caching for repeated operations",
                        "2. Parallelize independent steps",
                        "3. Add result memoization"
                    ]
                ))
        
        # Analyze resource usage
        if len(self.workflow_history) >= 20:
            recent = self.workflow_history[-20:]
            avg_memory = sum(wf.get('memory_usage', 0) for wf in recent) / len(recent)
            
            if avg_memory > 500 * 1024 * 1024:  # >500MB
                new_suggestions.append(ImprovementSuggestion(
                    suggestion_id="sugg_memory_opt",
                    category='cost',
                    title="Reduce memory footprint",
                    description="Average memory usage is high across recent workflows",
                    impact='medium',
                    effort='low',
                    expected_benefit="Reduce memory usage by ~30%, lower infrastructure costs",
                    implementation_steps=[
                        "1. Enable memory pooling",
                        "2. Use streaming for large datasets",
                        "3. Clear intermediate results"
                    ]
                ))
        
        # Analyze error patterns
        errors = sum(1 for wf in self.workflow_history[-30:] if wf.get('error', False))
        if errors > 3:
            new_suggestions.append(ImprovementSuggestion(
                suggestion_id="sugg_reliability",
                category='reliability',
                title="Add error handling and retries",
                description=f"Detected {errors} errors in last 30 workflows",
                impact='high',
                effort='medium',
                expected_benefit="Improve success rate by ~50%",
                implementation_steps=[
                    "1. Add exponential backoff retry logic",
                    "2. Implement circuit breakers",
                    "3. Add comprehensive logging"
                ]
            ))
        
        # Analyze complexity
        complex_workflows = [wf for wf in self.workflow_history[-20:] 
                           if len(wf.get('steps', [])) > 5]
        if len(complex_workflows) > 10:
            new_suggestions.append(ImprovementSuggestion(
                suggestion_id="sugg_simplify",
                category='usability',
                title="Simplify complex workflows",
                description=f"Found {len(complex_workflows)} workflows with >5 steps",
                impact='medium',
                effort='high',
                expected_benefit="Improve maintainability and debugging",
                implementation_steps=[
                    "1. Break workflows into sub-workflows",
                    "2. Create reusable workflow templates",
                    "3. Add workflow visualization"
                ]
            ))
        
        self.suggestions.extend(new_suggestions)
        print(f"[SuggestionEngine] Generated {len(new_suggestions)} new suggestions")
    
    def get_suggestions(self, category: str = None, 
                       min_impact: str = None) -> List[ImprovementSuggestion]:
        """Get filtered suggestions"""
        filtered = self.suggestions
        
        if category:
            filtered = [s for s in filtered if s.category == category]
        
        if min_impact:
            impact_order = {'high': 3, 'medium': 2, 'low': 1}
            min_level = impact_order.get(min_impact, 0)
            filtered = [s for s in filtered if impact_order.get(s.impact, 0) >= min_level]
        
        # Sort by impact then effort
        impact_order = {'high': 3, 'medium': 2, 'low': 1}
        effort_order = {'low': 1, 'medium': 2, 'high': 3}
        
        filtered.sort(key=lambda s: (
            -impact_order.get(s.impact, 0),
            effort_order.get(s.effort, 0)
        ))
        
        return filtered
    
    def record_feedback(self, suggestion_id: str, feedback: str):
        """Record user feedback on a suggestion"""
        self.user_feedback[suggestion_id] = feedback
        print(f"[SuggestionEngine] Recorded feedback for {suggestion_id}: {feedback}")
    
    def export_suggestions(self, filepath: str):
        """Export suggestions to JSON file"""
        data = [{
            'id': s.suggestion_id,
            'category': s.category,
            'title': s.title,
            'description': s.description,
            'impact': s.impact,
            'effort': s.effort,
            'expected_benefit': s.expected_benefit,
            'implementation_steps': s.implementation_steps,
            'feedback': self.user_feedback.get(s.suggestion_id, 'none')
        } for s in self.suggestions]
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"[SuggestionEngine] Exported {len(data)} suggestions to {filepath}")

if __name__ == '__main__':
    print("[SuggestionEngine] Module loaded successfully")
    print("Phase 6: User Suggestion Engine - STARTED")
    
    # Example usage
    engine = SuggestionEngine()
    
    # Simulate workflow data
    import numpy as np
    for i in range(25):
        workflow = {
            'workflow_id': f"wf_{i}",
            'steps': ['auth', 'fetch', 'process', 'store'] if i % 2 == 0 else ['auth', 'transform', 'export'],
            'duration': np.random.uniform(1.0, 5.0),
            'memory_usage': np.random.uniform(300*1024*1024, 700*1024*1024),
            'error': np.random.random() < 0.1
        }
        engine.analyze_workflow(workflow)
    
    # Get suggestions
    suggestions = engine.get_suggestions(min_impact='medium')
    print(f"\n[SuggestionEngine] Top suggestions (impact >= medium):")
    for i, sugg in enumerate(suggestions[:3], 1):
        print(f"  {i}. [{sugg.category.upper()}] {sugg.title}")
        print(f"     Impact: {sugg.impact}, Effort: {sugg.effort}")
        print(f"     Benefit: {sugg.expected_benefit}")
