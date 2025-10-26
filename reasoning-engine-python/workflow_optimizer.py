#!/usr/bin/env python3
"""
AI-Powered Workflow Optimization Module
Phase 6: Advanced Features - Cross-Service Workflow Automation

Implements ML-driven workflow scheduling, prediction, and auto-tuning.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
import json
import time
from dataclasses import dataclass, asdict
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import pickle
import os

@dataclass
class WorkflowMetrics:
    """Metrics collected from workflow execution"""
    workflow_id: str
    execution_time: float
    memory_usage: float
    cpu_utilization: float
    ipc_buffer_size: int
    batch_size: int
    success_rate: float
    throughput: float
    timestamp: float

@dataclass
class OptimizationSuggestion:
    """Workflow optimization suggestion"""
    suggestion_type: str
    parameter: str
    current_value: any
    suggested_value: any
    expected_improvement: float
    confidence: float
    reasoning: str

class WorkflowOptimizer:
    """ML-driven workflow optimization engine"""
    
    def __init__(self, model_path: str = 'models/workflow_optimizer.pkl'):
        self.model_path = model_path
        self.execution_model = None
        self.memory_model = None
        self.scaler = StandardScaler()
        self.metrics_history: List[WorkflowMetrics] = []
        self.load_or_init_models()
        
    def load_or_init_models(self):
        """Load existing models or initialize new ones"""
        if os.path.exists(self.model_path):
            with open(self.model_path, 'rb') as f:
                data = pickle.load(f)
                self.execution_model = data['execution_model']
                self.memory_model = data['memory_model']
                self.scaler = data['scaler']
                print(f"[WorkflowOptimizer] Models loaded from {self.model_path}")
        else:
            self.execution_model = RandomForestRegressor(n_estimators=100, random_state=42)
            self.memory_model = RandomForestRegressor(n_estimators=100, random_state=42)
            print("[WorkflowOptimizer] Initialized new models")
    
    def save_models(self):
        """Save trained models to disk"""
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        with open(self.model_path, 'wb') as f:
            pickle.dump({
                'execution_model': self.execution_model,
                'memory_model': self.memory_model,
                'scaler': self.scaler
            }, f)
        print(f"[WorkflowOptimizer] Models saved to {self.model_path}")
    
    def record_metrics(self, metrics: WorkflowMetrics):
        """Record workflow execution metrics"""
        self.metrics_history.append(metrics)
        print(f"[WorkflowOptimizer] Recorded metrics for {metrics.workflow_id}")
        
        # Retrain models periodically
        if len(self.metrics_history) >= 50 and len(self.metrics_history) % 50 == 0:
            self.train_models()
    
    def extract_features(self, metrics: WorkflowMetrics) -> np.ndarray:
        """Extract features from workflow metrics"""
        return np.array([
            metrics.ipc_buffer_size,
            metrics.batch_size,
            metrics.memory_usage,
            metrics.cpu_utilization,
            metrics.throughput
        ])
    
    def train_models(self):
        """Train ML models on collected metrics"""
        if len(self.metrics_history) < 10:
            print("[WorkflowOptimizer] Not enough data to train models")
            return
        
        X = np.array([self.extract_features(m) for m in self.metrics_history])
        y_time = np.array([m.execution_time for m in self.metrics_history])
        y_memory = np.array([m.memory_usage for m in self.metrics_history])
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train models
        self.execution_model.fit(X_scaled, y_time)
        self.memory_model.fit(X_scaled, y_memory)
        
        print(f"[WorkflowOptimizer] Models trained on {len(self.metrics_history)} samples")
        self.save_models()
    
    def predict_performance(self, ipc_buffer_size: int, batch_size: int,
                          memory_usage: float, cpu_util: float, 
                          throughput: float) -> Tuple[float, float]:
        """Predict execution time and memory usage"""
        features = np.array([[ipc_buffer_size, batch_size, memory_usage, 
                            cpu_util, throughput]])
        
        if len(self.metrics_history) < 10:
            # Return heuristic estimates if not enough training data
            estimated_time = (batch_size * 0.01) / (cpu_util + 0.1)
            estimated_memory = memory_usage * (1 + batch_size / 1000)
            return estimated_time, estimated_memory
        
        features_scaled = self.scaler.transform(features)
        predicted_time = self.execution_model.predict(features_scaled)[0]
        predicted_memory = self.memory_model.predict(features_scaled)[0]
        
        return predicted_time, predicted_memory
    
    def suggest_optimizations(self, current_metrics: WorkflowMetrics) -> List[OptimizationSuggestion]:
        """Generate optimization suggestions based on current metrics"""
        suggestions = []
        
        # Analyze buffer size
        if current_metrics.ipc_buffer_size < 4096:
            suggestions.append(OptimizationSuggestion(
                suggestion_type='buffer_resize',
                parameter='ipc_buffer_size',
                current_value=current_metrics.ipc_buffer_size,
                suggested_value=8192,
                expected_improvement=0.15,
                confidence=0.85,
                reasoning='Increasing buffer size will reduce IPC overhead'
            ))
        
        # Analyze batch size
        if current_metrics.batch_size < 50 and current_metrics.throughput < 100:
            suggestions.append(OptimizationSuggestion(
                suggestion_type='batch_resize',
                parameter='batch_size',
                current_value=current_metrics.batch_size,
                suggested_value=min(current_metrics.batch_size * 2, 100),
                expected_improvement=0.20,
                confidence=0.78,
                reasoning='Larger batch size will improve throughput'
            ))
        
        # Memory optimization
        if current_metrics.memory_usage > 1024 * 1024 * 512:  # >512MB
            suggestions.append(OptimizationSuggestion(
                suggestion_type='memory_optimization',
                parameter='memory_usage',
                current_value=current_metrics.memory_usage,
                suggested_value=current_metrics.memory_usage * 0.7,
                expected_improvement=0.25,
                confidence=0.70,
                reasoning='Enable memory pooling and reduce cache size'
            ))
        
        # CPU utilization
        if current_metrics.cpu_utilization < 0.3:
            suggestions.append(OptimizationSuggestion(
                suggestion_type='parallelization',
                parameter='worker_threads',
                current_value='auto',
                suggested_value='increased',
                expected_improvement=0.30,
                confidence=0.82,
                reasoning='Low CPU utilization suggests opportunity for more parallelism'
            ))
        
        return suggestions
    
    def auto_tune_parameters(self, workflow_id: str) -> Dict[str, any]:
        """Automatically tune workflow parameters"""
        if len(self.metrics_history) < 5:
            return {
                'status': 'insufficient_data',
                'message': 'Not enough historical data for auto-tuning'
            }
        
        # Get recent metrics for this workflow
        workflow_metrics = [m for m in self.metrics_history[-20:] 
                          if m.workflow_id == workflow_id]
        
        if not workflow_metrics:
            return {
                'status': 'no_workflow_data',
                'message': f'No historical data for workflow {workflow_id}'
            }
        
        # Calculate optimal parameters
        avg_metrics = self._calculate_average_metrics(workflow_metrics)
        
        # Test different parameter combinations
        best_config = self._grid_search_optimal_config(avg_metrics)
        
        return {
            'status': 'success',
            'workflow_id': workflow_id,
            'optimized_parameters': best_config,
            'estimated_improvement': best_config.get('improvement', 0)
        }
    
    def _calculate_average_metrics(self, metrics: List[WorkflowMetrics]) -> WorkflowMetrics:
        """Calculate average metrics from a list"""
        if not metrics:
            return None
        
        return WorkflowMetrics(
            workflow_id=metrics[0].workflow_id,
            execution_time=np.mean([m.execution_time for m in metrics]),
            memory_usage=np.mean([m.memory_usage for m in metrics]),
            cpu_utilization=np.mean([m.cpu_utilization for m in metrics]),
            ipc_buffer_size=int(np.mean([m.ipc_buffer_size for m in metrics])),
            batch_size=int(np.mean([m.batch_size for m in metrics])),
            success_rate=np.mean([m.success_rate for m in metrics]),
            throughput=np.mean([m.throughput for m in metrics]),
            timestamp=time.time()
        )
    
    def _grid_search_optimal_config(self, baseline: WorkflowMetrics) -> Dict[str, any]:
        """Search for optimal configuration using grid search"""
        buffer_sizes = [2048, 4096, 8192, 16384]
        batch_sizes = [32, 64, 128, 256]
        
        best_config = None
        best_score = float('inf')
        
        for buffer_size in buffer_sizes:
            for batch_size in batch_sizes:
                pred_time, pred_memory = self.predict_performance(
                    buffer_size, batch_size,
                    baseline.memory_usage, baseline.cpu_utilization,
                    baseline.throughput
                )
                
                # Score based on time and memory (weighted)
                score = pred_time + (pred_memory / 1024 / 1024 / 100)  # normalize memory
                
                if score < best_score:
                    best_score = score
                    best_config = {
                        'ipc_buffer_size': buffer_size,
                        'batch_size': batch_size,
                        'predicted_time': pred_time,
                        'predicted_memory': pred_memory,
                        'improvement': (baseline.execution_time - pred_time) / baseline.execution_time
                    }
        
        return best_config or {}

if __name__ == '__main__':
    print("[WorkflowOptimizer] Module loaded successfully")
    print("Phase 6: AI-Powered Workflow Optimization - STARTED")
    
    # Example usage
    optimizer = WorkflowOptimizer()
    
    # Simulate some metrics
    for i in range(15):
        metrics = WorkflowMetrics(
            workflow_id=f"workflow_{i % 3}",
            execution_time=np.random.uniform(0.5, 2.0),
            memory_usage=np.random.uniform(100*1024*1024, 500*1024*1024),
            cpu_utilization=np.random.uniform(0.2, 0.8),
            ipc_buffer_size=4096,
            batch_size=64,
            success_rate=0.95,
            throughput=np.random.uniform(50, 150),
            timestamp=time.time()
        )
        optimizer.record_metrics(metrics)
    
    # Get suggestions
    suggestions = optimizer.suggest_optimizations(metrics)
    print(f"\n[WorkflowOptimizer] Generated {len(suggestions)} suggestions")
    for i, sugg in enumerate(suggestions, 1):
        print(f"  {i}. {sugg.suggestion_type}: {sugg.reasoning}")
    
    # Auto-tune
    result = optimizer.auto_tune_parameters('workflow_0')
    print(f"\n[WorkflowOptimizer] Auto-tune result: {result['status']}")
    if result['status'] == 'success':
        print(f"  Optimized parameters: {result['optimized_parameters']}")
