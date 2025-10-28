"""
Memory Manager - Agent Memory Management
Manages .memory.md files with short-term and long-term memory
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from pathlib import Path
import time
import json
from datetime import datetime, timedelta


@dataclass
class MemoryEntry:
    """Single memory entry"""
    timestamp: float
    content: str
    memory_type: str  # short_term, long_term
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    importance: float = 0.5  # 0.0 to 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "content": self.content,
            "memory_type": self.memory_type,
            "tags": self.tags,
            "metadata": self.metadata,
            "importance": self.importance
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MemoryEntry':
        return cls(**data)
    
    def is_expired(self, ttl_seconds: int) -> bool:
        """Check if memory has expired"""
        age = time.time() - self.timestamp
        return age > ttl_seconds


@dataclass
class AgentMemory:
    """Complete agent memory state"""
    short_term: List[MemoryEntry] = field(default_factory=list)
    long_term: List[MemoryEntry] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "short_term": [e.to_dict() for e in self.short_term],
            "long_term": [e.to_dict() for e in self.long_term],
            "context": self.context
        }


class MemoryManager:
    """
    Memory Manager for .memory.md files
    Handles short-term and long-term memory with consolidation
    """
    
    def __init__(self, memory_path: str, short_term_ttl: int = 3600):
        self.memory_path = Path(memory_path)
        self.short_term_ttl = short_term_ttl  # seconds
        self.memory = AgentMemory()
    
    def add_short_term(self, content: str, tags: List[str] = None, 
                       importance: float = 0.5, metadata: Dict[str, Any] = None):
        """Add short-term memory"""
        entry = MemoryEntry(
            timestamp=time.time(),
            content=content,
            memory_type="short_term",
            tags=tags or [],
            metadata=metadata or {},
            importance=importance
        )
        self.memory.short_term.append(entry)
        
        # Auto-consolidate if important enough
        if importance >= 0.8:
            self._promote_to_long_term(entry)
    
    def add_long_term(self, content: str, tags: List[str] = None,
                      importance: float = 0.7, metadata: Dict[str, Any] = None):
        """Add long-term memory"""
        entry = MemoryEntry(
            timestamp=time.time(),
            content=content,
            memory_type="long_term",
            tags=tags or [],
            metadata=metadata or {},
            importance=importance
        )
        self.memory.long_term.append(entry)
    
    def _promote_to_long_term(self, entry: MemoryEntry):
        """Promote short-term memory to long-term"""
        long_term_entry = MemoryEntry(
            timestamp=entry.timestamp,
            content=entry.content,
            memory_type="long_term",
            tags=entry.tags,
            metadata={**entry.metadata, "promoted_from": "short_term"},
            importance=entry.importance
        )
        self.memory.long_term.append(long_term_entry)
    
    def consolidate(self, importance_threshold: float = 0.7):
        """
        Consolidate memories:
        - Remove expired short-term memories
        - Promote important short-term to long-term
        - Deduplicate long-term memories
        """
        current_time = time.time()
        
        # Filter expired short-term
        valid_short_term = []
        for entry in self.memory.short_term:
            if not entry.is_expired(self.short_term_ttl):
                if entry.importance >= importance_threshold:
                    self._promote_to_long_term(entry)
                else:
                    valid_short_term.append(entry)
        
        self.memory.short_term = valid_short_term
        
        # Deduplicate long-term
        seen_content = set()
        unique_long_term = []
        for entry in sorted(self.memory.long_term, key=lambda e: e.importance, reverse=True):
            if entry.content not in seen_content:
                seen_content.add(entry.content)
                unique_long_term.append(entry)
        
        self.memory.long_term = unique_long_term
    
    def search(self, query: str, memory_type: str = "all") -> List[MemoryEntry]:
        """Search memories by content"""
        results = []
        query_lower = query.lower()
        
        memories_to_search = []
        if memory_type in ["all", "short_term"]:
            memories_to_search.extend(self.memory.short_term)
        if memory_type in ["all", "long_term"]:
            memories_to_search.extend(self.memory.long_term)
        
        for entry in memories_to_search:
            if query_lower in entry.content.lower():
                results.append(entry)
            elif any(query_lower in tag.lower() for tag in entry.tags):
                results.append(entry)
        
        # Sort by importance
        results.sort(key=lambda e: e.importance, reverse=True)
        return results
    
    def get_recent(self, count: int = 10, memory_type: str = "all") -> List[MemoryEntry]:
        """Get recent memories"""
        memories = []
        if memory_type in ["all", "short_term"]:
            memories.extend(self.memory.short_term)
        if memory_type in ["all", "long_term"]:
            memories.extend(self.memory.long_term)
        
        memories.sort(key=lambda e: e.timestamp, reverse=True)
        return memories[:count]
    
    def get_by_tags(self, tags: List[str]) -> List[MemoryEntry]:
        """Get memories by tags"""
        results = []
        tag_set = set(tag.lower() for tag in tags)
        
        all_memories = self.memory.short_term + self.memory.long_term
        for entry in all_memories:
            entry_tags = set(tag.lower() for tag in entry.tags)
            if tag_set & entry_tags:  # Intersection
                results.append(entry)
        
        results.sort(key=lambda e: e.importance, reverse=True)
        return results
    
    def update_context(self, key: str, value: Any):
        """Update context information"""
        self.memory.context[key] = value
    
    def get_context(self, key: str) -> Any:
        """Get context information"""
        return self.memory.context.get(key)
    
    def load(self) -> bool:
        """Load memory from file"""
        if not self.memory_path.exists():
            return False
        
        content = self.memory_path.read_text()
        memory_dict = self._parse_markdown(content)
        
        # Reconstruct memory
        self.memory.short_term = [
            MemoryEntry.from_dict(e) for e in memory_dict.get("short_term", [])
        ]
        self.memory.long_term = [
            MemoryEntry.from_dict(e) for e in memory_dict.get("long_term", [])
        ]
        self.memory.context = memory_dict.get("context", {})
        
        return True
    
    def save(self):
        """Save memory to file"""
        # Consolidate before saving
        self.consolidate()
        
        content = self._to_markdown()
        self.memory_path.parent.mkdir(parents=True, exist_ok=True)
        self.memory_path.write_text(content)
    
    def _parse_markdown(self, content: str) -> Dict[str, Any]:
        """Parse markdown to memory dict"""
        # For simplicity, use JSON blocks in markdown
        memory_dict = {"short_term": [], "long_term": [], "context": {}}
        
        lines = content.split("\n")
        in_json_block = False
        json_content = []
        current_section = None
        
        for line in lines:
            if line.strip().startswith("```json"):
                in_json_block = True
                json_content = []
                continue
            elif line.strip() == "```" and in_json_block:
                in_json_block = False
                if json_content and current_section:
                    try:
                        data = json.loads("\n".join(json_content))
                        memory_dict[current_section] = data
                    except:
                        pass
                continue
            
            if in_json_block:
                json_content.append(line)
            elif line.strip().startswith("## "):
                section = line.strip()[3:].lower().replace(" ", "_").replace("-", "_")
                current_section = section
        
        return memory_dict
    
    def _to_markdown(self) -> str:
        """Convert memory to markdown"""
        lines = ["# Agent Memory", "", f"*Last updated: {datetime.now().isoformat()}*", ""]
        
        # Short-term memory
        lines.append("## Short-Term Memory")
        lines.append(f"*{len(self.memory.short_term)} entries*")
        lines.append("")
        lines.append("```json")
        lines.append(json.dumps([e.to_dict() for e in self.memory.short_term], indent=2))
        lines.append("```")
        lines.append("")
        
        # Long-term memory
        lines.append("## Long-Term Memory")
        lines.append(f"*{len(self.memory.long_term)} entries*")
        lines.append("")
        lines.append("```json")
        lines.append(json.dumps([e.to_dict() for e in self.memory.long_term], indent=2))
        lines.append("```")
        lines.append("")
        
        # Context
        if self.memory.context:
            lines.append("## Context")
            lines.append("```json")
            lines.append(json.dumps(self.memory.context, indent=2))
            lines.append("```")
            lines.append("")
        
        return "\n".join(lines)
    
    def export_json(self) -> str:
        """Export memory as JSON"""
        return json.dumps(self.memory.to_dict(), indent=2)
    
    def import_json(self, json_str: str):
        """Import memory from JSON"""
        data = json.loads(json_str)
        self.memory.short_term = [MemoryEntry.from_dict(e) for e in data.get("short_term", [])]
        self.memory.long_term = [MemoryEntry.from_dict(e) for e in data.get("long_term", [])]
        self.memory.context = data.get("context", {})
    
    def clear(self, memory_type: str = "all"):
        """Clear memories"""
        if memory_type in ["all", "short_term"]:
            self.memory.short_term = []
        if memory_type in ["all", "long_term"]:
            self.memory.long_term = []
        if memory_type == "all":
            self.memory.context = {}
    
    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        return {
            "short_term_count": len(self.memory.short_term),
            "long_term_count": len(self.memory.long_term),
            "total_count": len(self.memory.short_term) + len(self.memory.long_term),
            "context_keys": list(self.memory.context.keys()),
            "avg_importance": sum(e.importance for e in self.memory.short_term + self.memory.long_term) / 
                            max(1, len(self.memory.short_term) + len(self.memory.long_term))
        }


# Example usage
if __name__ == "__main__":
    manager = MemoryManager("agent.memory.md")
    
    # Add memories
    manager.add_short_term("User prefers dark mode", tags=["preference", "ui"], importance=0.9)
    manager.add_short_term("Current task: search for documentation", tags=["task"], importance=0.6)
    manager.add_long_term("User is a software engineer", tags=["profile"], importance=0.95)
    
    # Update context
    manager.update_context("session_id", "session-123")
    manager.update_context("last_action", "search")
    
    # Save
    manager.save()
    
    # Statistics
    stats = manager.get_stats()
    print(f"Memory stats: {stats}")
