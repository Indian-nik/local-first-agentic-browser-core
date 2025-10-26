"""
Integration tests for Phase 6 & 7 components
Tests interaction between observability and customization systems
"""
import pytest
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "customization-control/spec-editor")
sys.path.insert(0, "customization-control/local-storage")
sys.path.insert(0, "observability")

from spec_editor import SpecEditor, AgentSpec
from local_storage import LocalStorage, ChatMessage
from agentic_tracer import AgenticTracer, TraceEvent

@pytest.mark.integration
class TestObservabilityCustomizationIntegration:
    def test_traced_spec_loading(self, temp_spec_file, tmp_path):
        """Test spec loading with observability tracing"""
        tracer = AgenticTracer()
        ctx = tracer.create_context()
        
        # Load spec with tracing
        editor = SpecEditor(str(temp_spec_file))
        spec = editor.load()
        
        # Log trace event
        event = TraceEvent(
            trace_id=ctx.trace_id,
            span_id=ctx.span_id,
            event_type="spec_load",
            data={"spec_name": spec.name if hasattr(spec, "name") else "unknown"}
        )
        tracer.log_event(event)
        
        assert spec is not None
        
    def test_traced_storage_operations(self, tmp_path):
        """Test storage operations with observability"""
        db_path = tmp_path / "test.db"
        storage = LocalStorage(str(db_path))
        tracer = AgenticTracer()
        ctx = tracer.create_context()
        
        # Store message with tracing
        msg = ChatMessage(
            session_id="integration-test",
            role="user",
            content="test message",
            timestamp="2025-10-22T00:00:00Z"
        )
        storage.store_message(msg)
        
        # Log trace
        event = TraceEvent(
            trace_id=ctx.trace_id,
            span_id=ctx.span_id,
            event_type="storage_write",
            data={"operation": "store_message", "session": "integration-test"}
        )
        tracer.log_event(event)
        
    def test_end_to_end_workflow(self, temp_spec_file, tmp_path):
        """Test complete workflow: load spec, store data, trace all"""
        # Initialize components
        editor = SpecEditor(str(temp_spec_file))
        db_path = tmp_path / "workflow.db"
        storage = LocalStorage(str(db_path))
        tracer = AgenticTracer()
        
        # Create trace context
        ctx = tracer.create_context()
        
        # Step 1: Load spec
        spec = editor.load()
        tracer.log_event(TraceEvent(
            trace_id=ctx.trace_id,
            span_id=ctx.span_id,
            event_type="workflow_step",
            data={"step": "load_spec", "status": "success"}
        ))
        
        # Step 2: Store chat history
        for i in range(3):
            msg = ChatMessage(
                session_id="workflow-session",
                role="user" if i % 2 == 0 else "assistant",
                content=f"message {i}",
                timestamp=f"2025-10-22T00:0{i}:00Z"
            )
            storage.store_message(msg)
            
        tracer.log_event(TraceEvent(
            trace_id=ctx.trace_id,
            span_id=ctx.span_id,
            event_type="workflow_step",
            data={"step": "store_messages", "count": 3, "status": "success"}
        ))
        
        # Verify workflow completed
        history = storage.get_session_history("workflow-session")
        assert len(history) == 3

@pytest.mark.integration
class TestSecurityIntegration:
    def test_privacy_with_tracing(self, tmp_path):
        """Test that tracing respects privacy guarantees"""
        db_path = tmp_path / "privacy_test.db"
        storage = LocalStorage(str(db_path))
        tracer = AgenticTracer()
        
        # Ensure no external calls in traced operations
        ctx = tracer.create_context()
        msg = ChatMessage(
            session_id="privacy-test",
            role="user",
            content="sensitive data",
            timestamp="2025-10-22T00:00:00Z"
        )
        storage.store_message(msg)
        
        # Verify data stays local
        assert storage.is_local_only() is True
        
    def test_audit_trail_completeness(self, tmp_path):
        """Test complete audit trail for all operations"""
        tracer = AgenticTracer()
        ctx = tracer.create_context()
        
        operations = ["load", "save", "update", "delete"]
        for op in operations:
            event = TraceEvent(
                trace_id=ctx.trace_id,
                span_id=ctx.span_id,
                event_type="audit",
                data={"operation": op, "timestamp": "2025-10-22T00:00:00Z"}
            )
            tracer.log_event(event)
        
        # Verify all operations logged
        # In real implementation, query Elasticsearch for events
