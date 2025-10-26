"""
Shared pytest fixtures for all test suites
"""
import pytest
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent / "reasoning-engine-python"))

@pytest.fixture
def temp_spec_file(tmp_path):
    """Create a temporary .spec.md file for testing"""
    spec_file = tmp_path / "test.spec.md"
    spec_file.write_text("""# Agent Specification

## Identity
- name: test-agent
- version: 1.0.0

## Capabilities
- browse: true
- search: true

## Constraints
- max_tokens: 4096
- timeout: 30s
""")
    return spec_file

@pytest.fixture
def temp_memory_file(tmp_path):
    """Create a temporary .memory.md file for testing"""
    memory_file = tmp_path / "test.memory.md"
    memory_file.write_text("""# Agent Memory

## Short-term Memory
- Last action: test
- Context: testing

## Long-term Memory
- Pattern: test pattern
""")
    return memory_file

@pytest.fixture
def mock_duckdb_connection(tmp_path):
    """Create a temporary DuckDB connection for testing"""
    import duckdb
    db_path = tmp_path / "test.db"
    conn = duckdb.connect(str(db_path))
    yield conn
    conn.close()
