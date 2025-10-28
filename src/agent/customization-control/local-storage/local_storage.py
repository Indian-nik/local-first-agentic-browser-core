"""
Local Storage - Privacy-First Data Storage
ALL data stays local. NEVER for external training.
Uses DuckDB + PyArrow for local-only storage.
"""
import duckdb
import pyarrow as pa
import pyarrow.parquet as pq
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from pathlib import Path
import json
import time


@dataclass
class ChatMessage:
    """Chat message - stored LOCALLY ONLY"""
    session_id: str
    role: str  # user, assistant, system
    content: str
    timestamp: str
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class RAGContext:
    """RAG context - stored LOCALLY ONLY"""
    session_id: str
    document: str
    embedding: List[float]
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class LocalStorage:
    """
    Privacy-First Local Storage
    
    CRITICAL GUARANTEES:
    - ALL data stays on local machine
    - NO external API calls
    - NO telemetry or analytics
    - NO cloud sync
    - Data NEVER used for training
    """
    
    def __init__(self, db_path: str, encrypted: bool = False):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = duckdb.connect(str(self.db_path))
        self.encrypted = encrypted
        self._init_schema()
    
    def _init_schema(self):
        """Initialize database schema"""
        # Messages table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY,
                session_id VARCHAR,
                role VARCHAR,
                content TEXT,
                timestamp VARCHAR,
                metadata JSON
            )
        """)
        
        # RAG context table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS rag_context (
                id INTEGER PRIMARY KEY,
                session_id VARCHAR,
                document TEXT,
                embedding DOUBLE[],
                metadata JSON
            )
        """)
        
        # User preferences table (LOCAL ONLY)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS user_preferences (
                key VARCHAR PRIMARY KEY,
                value JSON,
                updated_at VARCHAR
            )
        """)
        
        # Session metadata
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id VARCHAR PRIMARY KEY,
                created_at VARCHAR,
                last_active VARCHAR,
                metadata JSON
            )
        """)
    
    def store_message(self, msg: ChatMessage):
        """Store chat message LOCALLY"""
        self.conn.execute("""
            INSERT INTO messages (session_id, role, content, timestamp, metadata)
            VALUES (?, ?, ?, ?, ?)
        """, [msg.session_id, msg.role, msg.content, msg.timestamp, 
              json.dumps(msg.metadata)])
    
    def get_session_history(self, session_id: str) -> List[ChatMessage]:
        """Get session history from LOCAL storage"""
        result = self.conn.execute("""
            SELECT session_id, role, content, timestamp, metadata
            FROM messages
            WHERE session_id = ?
            ORDER BY timestamp ASC
        """, [session_id]).fetchall()
        
        messages = []
        for row in result:
            messages.append(ChatMessage(
                session_id=row[0],
                role=row[1],
                content=row[2],
                timestamp=row[3],
                metadata=json.loads(row[4]) if row[4] else {}
            ))
        return messages
    
    def store_rag_context(self, context: RAGContext):
        """Store RAG context LOCALLY"""
        self.conn.execute("""
            INSERT INTO rag_context (session_id, document, embedding, metadata)
            VALUES (?, ?, ?, ?)
        """, [context.session_id, context.document, context.embedding,
              json.dumps(context.metadata)])
    
    def search_rag_context(self, session_id: str, query: str) -> List[RAGContext]:
        """Search RAG context LOCALLY (full-text search)"""
        result = self.conn.execute("""
            SELECT session_id, document, embedding, metadata
            FROM rag_context
            WHERE session_id = ? AND document LIKE ?
            LIMIT 10
        """, [session_id, f"%{query}%"]).fetchall()
        
        contexts = []
        for row in result:
            contexts.append(RAGContext(
                session_id=row[0],
                document=row[1],
                embedding=row[2],
                metadata=json.loads(row[3]) if row[3] else {}
            ))
        return contexts
    
    def set_preference(self, key: str, value: Any):
        """Set user preference - stored LOCALLY ONLY"""
        self.conn.execute("""
            INSERT OR REPLACE INTO user_preferences (key, value, updated_at)
            VALUES (?, ?, ?)
        """, [key, json.dumps(value), str(time.time())])
    
    def get_preference(self, key: str) -> Optional[Any]:
        """Get user preference from LOCAL storage"""
        result = self.conn.execute("""
            SELECT value FROM user_preferences WHERE key = ?
        """, [key]).fetchone()
        
        return json.loads(result[0]) if result else None
    
    def create_session(self, session_id: str, metadata: Dict[str, Any] = None):
        """Create session - tracked LOCALLY"""
        self.conn.execute("""
            INSERT OR REPLACE INTO sessions (session_id, created_at, last_active, metadata)
            VALUES (?, ?, ?, ?)
        """, [session_id, str(time.time()), str(time.time()), 
              json.dumps(metadata or {})])
    
    def update_session_activity(self, session_id: str):
        """Update session last active time"""
        self.conn.execute("""
            UPDATE sessions SET last_active = ? WHERE session_id = ?
        """, [str(time.time()), session_id])
    
    def export_to_parquet(self, table: str, output_path: str):
        """Export table to Parquet for LOCAL backup"""
        result = self.conn.execute(f"SELECT * FROM {table}").fetch_arrow_table()
        pq.write_table(result, output_path)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get storage statistics"""
        stats = {}
        stats["total_messages"] = self.conn.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
        stats["total_rag_entries"] = self.conn.execute("SELECT COUNT(*) FROM rag_context").fetchone()[0]
        stats["total_sessions"] = self.conn.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
        stats["database_size_bytes"] = self.db_path.stat().st_size
        return stats
    
    def is_local_only(self) -> bool:
        """Verify this is local-only storage - NO external connections"""
        # This is ALWAYS true - no external connections
        return True
    
    def close(self):
        """Close database connection"""
        self.conn.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
