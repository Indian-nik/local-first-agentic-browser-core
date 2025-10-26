"""
Unit tests for agentic_tracer.py - Phase 6 observability
"""
import pytest
import sys

sys.path.insert(0, "observability")
from agentic_tracer import AgenticTracer, TraceContext, TraceEvent

@pytest.mark.unit
@pytest.mark.observability
class TestAgenticTracer:
    def test_tracer_initialization(self):
        """Test tracer initialization"""
        tracer = AgenticTracer(buffer_size=1000)
        assert tracer is not None
        
    def test_create_trace_context(self):
        """Test creating trace context"""
        tracer = AgenticTracer()
        ctx = tracer.create_context()
        assert ctx.trace_id is not None
        assert ctx.span_id is not None
        
    def test_log_reasoning_step(self):
        """Test logging reasoning step"""
        tracer = AgenticTracer()
        ctx = tracer.create_context()
        event = TraceEvent(
            trace_id=ctx.trace_id,
            span_id=ctx.span_id,
            event_type="reasoning",
            data={"step": "analyze query"}
        )
        tracer.log_event(event)
        # Verify event logged
        
    def test_log_tool_call(self):
        """Test logging tool call"""
        tracer = AgenticTracer()
        ctx = tracer.create_context()
        event = TraceEvent(
            trace_id=ctx.trace_id,
            span_id=ctx.span_id,
            event_type="tool_call",
            data={"tool": "browser", "action": "navigate"}
        )
        tracer.log_event(event)
        
    def test_log_cot_process(self):
        """Test logging chain-of-thought process"""
        tracer = AgenticTracer()
        ctx = tracer.create_context()
        event = TraceEvent(
            trace_id=ctx.trace_id,
            span_id=ctx.span_id,
            event_type="cot",
            data={"thought": "user wants to search", "confidence": 0.95}
        )
        tracer.log_event(event)
        
    def test_distributed_tracing(self):
        """Test distributed tracing with parent-child spans"""
        tracer = AgenticTracer()
        parent_ctx = tracer.create_context()
        child_ctx = tracer.create_context(parent_span_id=parent_ctx.span_id)
        assert child_ctx.parent_span_id == parent_ctx.span_id

@pytest.mark.unit
@pytest.mark.observability
class TestTraceContext:
    def test_context_creation(self):
        """Test trace context creation"""
        ctx = TraceContext(
            trace_id="trace-123",
            span_id="span-456",
            parent_span_id=None
        )
        assert ctx.trace_id == "trace-123"
        assert ctx.span_id == "span-456"

@pytest.mark.unit
@pytest.mark.observability
class TestTraceEvent:
    def test_event_creation(self):
        """Test trace event creation"""
        event = TraceEvent(
            trace_id="trace-123",
            span_id="span-456",
            event_type="reasoning",
            data={"step": "test"}
        )
        assert event.event_type == "reasoning"
        assert event.data["step"] == "test"
