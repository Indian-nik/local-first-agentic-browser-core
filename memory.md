# Memory Architecture

## Overview
This document describes the memory management and persistence strategies for the local-first agentic browser core.

## Memory Types

### Short-term Memory
- Session-based context
- In-memory cache for fast access
- Cleared on restart

### Long-term Memory
- Persistent storage using local database
- Indexed for efficient retrieval
- Survives restarts

### Working Memory
- Current task context
- Active reasoning state
- Shared between components

## Storage Strategy

### Local-First Approach
- All data stored locally by default
- Optional cloud sync for backup
- Privacy-preserving design

### Data Structures
- Graph-based relationships
- Vector embeddings for semantic search
- Time-series for temporal queries

## Memory Limits
- Short-term: 100MB per session
- Working memory: 10MB active context
- Long-term: Limited by disk space

## Garbage Collection
- Automatic cleanup of expired sessions
- Manual purge options for users
- Privacy-focused deletion
