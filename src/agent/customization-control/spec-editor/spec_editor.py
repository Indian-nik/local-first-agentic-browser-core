"""
Spec Editor - Agent Specification Management
Allows full editability of .spec.md files for advanced users
"""
from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Optional, Callable
from pathlib import Path
import yaml
import hashlib
import time
import json
import re


@dataclass
class AgentSpec:
    """Agent specification data model"""
    name: str
    version: str
    capabilities: Dict[str, bool] = field(default_factory=dict)
    constraints: Dict[str, Any] = field(default_factory=dict)
    tools: List[str] = field(default_factory=list)
    behaviors: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AgentSpec':
        """Create from dictionary"""
        return cls(**data)


@dataclass
class ValidationRule:
    """Validation rule for spec files"""
    name: str
    description: str
    validator: Callable[[Dict[str, Any]], bool]
    severity: str = "error"  # error, warning, info
    
    def validate(self, spec: Dict[str, Any]) -> bool:
        """Execute validation"""
        try:
            return self.validator(spec)
        except Exception as e:
            print(f"Validation error in {self.name}: {e}")
            return False


class SpecEditor:
    """
    Spec Editor for .spec.md files
    Provides hot-reload, validation, versioning, and diff capabilities
    """
    
    def __init__(self, spec_path: str):
        self.spec_path = Path(spec_path)
        self.validation_rules: List[ValidationRule] = []
        self._last_mtime = 0
        self._last_hash = ""
        self._setup_default_validation()
    
    def _setup_default_validation(self):
        """Setup default validation rules"""
        self.add_validation_rule(ValidationRule(
            name="has_name",
            description="Spec must have a name",
            validator=lambda s: "name" in s and len(s["name"]) > 0
        ))
        
        self.add_validation_rule(ValidationRule(
            name="has_version",
            description="Spec must have a version",
            validator=lambda s: "version" in s
        ))
        
        self.add_validation_rule(ValidationRule(
            name="valid_capabilities",
            description="Capabilities must be boolean values",
            validator=lambda s: all(isinstance(v, bool) for v in s.get("capabilities", {}).values())
        ))
        
        self.add_validation_rule(ValidationRule(
            name="reasonable_token_limit",
            description="Max tokens should be reasonable (< 1M)",
            validator=lambda s: s.get("constraints", {}).get("max_tokens", 0) < 1000000,
            severity="warning"
        ))
    
    def add_validation_rule(self, rule: ValidationRule):
        """Add a custom validation rule"""
        self.validation_rules.append(rule)
    
    def load(self) -> Optional[AgentSpec]:
        """Load spec from file"""
        if not self.spec_path.exists():
            print(f"Spec file not found: {self.spec_path}")
            return None
        
        content = self.spec_path.read_text()
        spec_dict = self._parse_markdown(content)
        
        # Validate
        errors = self.validate(spec_dict)
        if errors:
            print(f"Validation errors: {errors}")
        
        return AgentSpec.from_dict(spec_dict)
    
    def save(self, spec: AgentSpec):
        """Save spec to file"""
        # Validate before saving
        errors = self.validate(spec.to_dict())
        if any(e["severity"] == "error" for e in errors):
            raise ValueError(f"Cannot save invalid spec: {errors}")
        
        content = self._to_markdown(spec)
        self.spec_path.parent.mkdir(parents=True, exist_ok=True)
        self.spec_path.write_text(content)
        self._update_tracking()
    
    def validate(self, spec_dict: Dict[str, Any]) -> List[Dict[str, str]]:
        """Validate spec against rules"""
        errors = []
        for rule in self.validation_rules:
            if not rule.validate(spec_dict):
                errors.append({
                    "rule": rule.name,
                    "description": rule.description,
                    "severity": rule.severity
                })
        return errors
    
    def has_changed(self) -> bool:
        """Check if file has changed (hot-reload detection)"""
        if not self.spec_path.exists():
            return False
        
        current_mtime = self.spec_path.stat().st_mtime
        return current_mtime > self._last_mtime
    
    def get_diff(self, other_spec: AgentSpec) -> Dict[str, Any]:
        """Compare with another spec"""
        current = self.load()
        if not current:
            return {"error": "Current spec not found"}
        
        current_dict = current.to_dict()
        other_dict = other_spec.to_dict()
        
        diff = {
            "added": {},
            "removed": {},
            "modified": {}
        }
        
        # Check all keys
        all_keys = set(current_dict.keys()) | set(other_dict.keys())
        for key in all_keys:
            if key not in current_dict:
                diff["added"][key] = other_dict[key]
            elif key not in other_dict:
                diff["removed"][key] = current_dict[key]
            elif current_dict[key] != other_dict[key]:
                diff["modified"][key] = {
                    "old": current_dict[key],
                    "new": other_dict[key]
                }
        
        return diff
    
    def _parse_markdown(self, content: str) -> Dict[str, Any]:
        """Parse markdown content to spec dict"""
        spec = {}
        current_section = None
        
        for line in content.split("\n"):
            line = line.strip()
            
            # Section headers
            if line.startswith("## "):
                current_section = line[3:].lower().replace(" ", "_")
                continue
            
            # Key-value pairs
            if line.startswith("- ") and ":" in line:
                key_value = line[2:].split(":", 1)
                key = key_value[0].strip()
                value = key_value[1].strip()
                
                # Try to parse as YAML
                try:
                    parsed_value = yaml.safe_load(value)
                except:
                    parsed_value = value
                
                if current_section:
                    if current_section not in spec:
                        spec[current_section] = {}
                    spec[current_section][key] = parsed_value
                else:
                    spec[key] = parsed_value
        
        # Flatten identity section to top level
        if "identity" in spec:
            spec.update(spec.pop("identity"))
        
        return spec
    
    def _to_markdown(self, spec: AgentSpec) -> str:
        """Convert spec to markdown format"""
        lines = ["# Agent Specification", ""]
        
        # Identity
        lines.extend([
            "## Identity",
            f"- name: {spec.name}",
            f"- version: {spec.version}",
            ""
        ])
        
        # Capabilities
        if spec.capabilities:
            lines.append("## Capabilities")
            for key, value in spec.capabilities.items():
                lines.append(f"- {key}: {str(value).lower()}")
            lines.append("")
        
        # Constraints
        if spec.constraints:
            lines.append("## Constraints")
            for key, value in spec.constraints.items():
                lines.append(f"- {key}: {value}")
            lines.append("")
        
        # Tools
        if spec.tools:
            lines.append("## Tools")
            for tool in spec.tools:
                lines.append(f"- {tool}")
            lines.append("")
        
        # Behaviors
        if spec.behaviors:
            lines.append("## Behaviors")
            for key, value in spec.behaviors.items():
                lines.append(f"- {key}: {value}")
            lines.append("")
        
        return "\n".join(lines)
    
    def _update_tracking(self):
        """Update file tracking for hot-reload"""
        if self.spec_path.exists():
            self._last_mtime = self.spec_path.stat().st_mtime
            content = self.spec_path.read_text()
            self._last_hash = hashlib.sha256(content.encode()).hexdigest()
    
    def export_json(self) -> str:
        """Export spec as JSON"""
        spec = self.load()
        if spec:
            return json.dumps(spec.to_dict(), indent=2)
        return "{}"
    
    def import_json(self, json_str: str):
        """Import spec from JSON"""
        spec_dict = json.loads(json_str)
        spec = AgentSpec.from_dict(spec_dict)
        self.save(spec)
    
    def create_template(self, name: str) -> AgentSpec:
        """Create a template spec"""
        return AgentSpec(
            name=name,
            version="1.0.0",
            capabilities={
                "browse": True,
                "search": True,
                "reason": True
            },
            constraints={
                "max_tokens": 4096,
                "timeout": 30
            },
            tools=["browser", "search", "calculator"],
            behaviors={
                "autonomous": False,
                "requires_confirmation": True
            },
            metadata={
                "created": time.time(),
                "author": "system"
            }
        )


# Example usage
if __name__ == "__main__":
    editor = SpecEditor("example.spec.md")
    
    # Create template
    spec = editor.create_template("example-agent")
    editor.save(spec)
    
    # Load and validate
    loaded = editor.load()
    if loaded:
        print(f"Loaded spec: {loaded.name} v{loaded.version}")
    
    # Export to JSON
    json_export = editor.export_json()
    print(f"JSON export: {json_export}")
