"""Storage backend for learning data."""

import logging
from typing import Dict, List, Any, Optional, Protocol
from abc import abstractmethod

logger = logging.getLogger(__name__)

class LearningStorage(Protocol):
    """Protocol for learning data storage."""
    
    @abstractmethod
    def store(self, key: str, value: Any) -> None:
        """Store a value."""
        ...
    
    @abstractmethod
    def retrieve(self, key: str) -> Optional[Any]:
        """Retrieve a value."""
        ...
    
    @abstractmethod
    def delete(self, key: str) -> bool:
        """Delete a value."""
        ...
    
    @abstractmethod
    def list_keys(self, prefix: str = "") -> List[str]:
        """List keys with optional prefix."""
        ...

class InMemoryStorage:
    """In-memory storage implementation."""
    
    def __init__(self):
        self._storage: Dict[str, Any] = {}
        logger.info("InMemoryStorage initialized")
    
    def store(self, key: str, value: Any) -> None:
        """Store a value."""
        self._storage[key] = value
        logger.debug(f"Stored key: {key}")
    
    def retrieve(self, key: str) -> Optional[Any]:
        """Retrieve a value."""
        return self._storage.get(key)
    
    def delete(self, key: str) -> bool:
        """Delete a value."""
        if key in self._storage:
            del self._storage[key]
            logger.debug(f"Deleted key: {key}")
            return True
        return False
    
    def list_keys(self, prefix: str = "") -> List[str]:
        """List keys with optional prefix."""
        if prefix:
            return [k for k in self._storage.keys() if k.startswith(prefix)]
        return list(self._storage.keys())
    
    def clear(self) -> None:
        """Clear all data."""
        self._storage.clear()
        logger.info("Storage cleared")
