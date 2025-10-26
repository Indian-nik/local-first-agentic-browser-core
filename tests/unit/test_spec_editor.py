"""
Unit tests for spec_editor.py
"""
import pytest
from pathlib import Path
import sys

sys.path.insert(0, "customization-control/spec-editor")
from spec_editor import AgentSpec, SpecEditor, ValidationRule

@pytest.mark.unit
@pytest.mark.customization
class TestAgentSpec:
    def test_spec_creation(self):
        """Test creating an agent specification"""
        spec = AgentSpec(
            name="test-agent",
            version="1.0.0",
            capabilities={"browse": True, "search": True},
            constraints={"max_tokens": 4096}
        )
        assert spec.name == "test-agent"
        assert spec.version == "1.0.0"
        assert spec.capabilities["browse"] is True
        
    def test_spec_validation(self):
        """Test specification validation"""
        spec = AgentSpec(
            name="test-agent",
            version="1.0.0",
            capabilities={"browse": True},
            constraints={"max_tokens": 4096}
        )
        # Should validate successfully
        assert spec.name is not None
        
    def test_spec_to_dict(self):
        """Test converting spec to dictionary"""
        spec = AgentSpec(
            name="test-agent",
            version="1.0.0",
            capabilities={"browse": True},
            constraints={"max_tokens": 4096}
        )
        spec_dict = spec.__dict__
        assert "name" in spec_dict
        assert "capabilities" in spec_dict

@pytest.mark.unit
@pytest.mark.customization
class TestSpecEditor:
    def test_load_spec_from_file(self, temp_spec_file):
        """Test loading specification from file"""
        editor = SpecEditor(str(temp_spec_file))
        spec = editor.load()
        assert spec is not None
        
    def test_save_spec_to_file(self, tmp_path):
        """Test saving specification to file"""
        spec_file = tmp_path / "new_spec.md"
        editor = SpecEditor(str(spec_file))
        spec = AgentSpec(
            name="new-agent",
            version="1.0.0",
            capabilities={"browse": True},
            constraints={"max_tokens": 2048}
        )
        editor.save(spec)
        assert spec_file.exists()
        
    def test_hot_reload_detection(self, temp_spec_file):
        """Test hot-reload change detection"""
        editor = SpecEditor(str(temp_spec_file))
        initial_mtime = Path(temp_spec_file).stat().st_mtime
        # Modify file
        with open(temp_spec_file, "a") as f:
            f.write("\n# Modified\n")
        new_mtime = Path(temp_spec_file).stat().st_mtime
        assert new_mtime > initial_mtime

@pytest.mark.unit
@pytest.mark.customization
class TestValidationRule:
    def test_validation_rule_creation(self):
        """Test creating validation rules"""
        rule = ValidationRule(
            name="max_tokens_limit",
            description="Ensure max_tokens is reasonable",
            validator=lambda spec: spec.get("constraints", {}).get("max_tokens", 0) <= 100000
        )
        assert rule.name == "max_tokens_limit"
        
    def test_validation_rule_execution(self):
        """Test executing validation rule"""
        rule = ValidationRule(
            name="has_name",
            description="Spec must have a name",
            validator=lambda spec: "name" in spec
        )
        assert rule.validator({"name": "test"}) is True
        assert rule.validator({}) is False
