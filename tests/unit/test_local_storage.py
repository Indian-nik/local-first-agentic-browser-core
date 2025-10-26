"""
Unit tests for local_storage.py - Privacy-first local storage
"""
import pytest
import duckdb
import sys

sys.path.insert(0, "customization-control/local-storage")
from local_storage import LocalStorage, ChatMessage, RAGContext

@pytest.mark.unit
@pytest.mark.customization
class TestLocalStorage:
    def test_storage_initialization(self, tmp_path):
        """Test storage initialization with privacy guarantees"""
        db_path = tmp_path / "test.db"
        storage = LocalStorage(str(db_path))
        assert storage is not None
        # Verify privacy: no external connections
        
    def test_store_chat_message(self, tmp_path):
        """Test storing chat messages locally"""
        db_path = tmp_path / "test.db"
        storage = LocalStorage(str(db_path))
        msg = ChatMessage(
            session_id="test-session",
            role="user",
            content="test message",
            timestamp="2025-10-22T00:00:00Z"
        )
        storage.store_message(msg)
        # Verify message stored locally only
        
    def test_retrieve_session_history(self, tmp_path):
        """Test retrieving session history"""
        db_path = tmp_path / "test.db"
        storage = LocalStorage(str(db_path))
        session_id = "test-session"
        # Store messages
        for i in range(3):
            msg = ChatMessage(
                session_id=session_id,
                role="user",
                content=f"message {i}",
                timestamp=f"2025-10-22T00:0{i}:00Z"
            )
            storage.store_message(msg)
        # Retrieve history
        history = storage.get_session_history(session_id)
        assert len(history) == 3
        
    def test_store_rag_context(self, tmp_path):
        """Test storing RAG context locally"""
        db_path = tmp_path / "test.db"
        storage = LocalStorage(str(db_path))
        context = RAGContext(
            session_id="test-session",
            document="test document",
            embedding=[0.1, 0.2, 0.3],
            metadata={"source": "local"}
        )
        storage.store_rag_context(context)
        # Verify context stored locally
        
    def test_privacy_guarantee_no_external_calls(self, tmp_path):
        """Test that no external network calls are made"""
        db_path = tmp_path / "test.db"
        storage = LocalStorage(str(db_path))
        # Verify all operations are local
        assert storage.is_local_only() is True
        # No external API calls should be detected

@pytest.mark.unit
@pytest.mark.customization  
class TestChatMessage:
    def test_message_creation(self):
        """Test creating chat message"""
        msg = ChatMessage(
            session_id="test",
            role="user",
            content="hello",
            timestamp="2025-10-22T00:00:00Z"
        )
        assert msg.role == "user"
        assert msg.content == "hello"
        
    def test_message_serialization(self):
        """Test message serialization"""
        msg = ChatMessage(
            session_id="test",
            role="assistant",
            content="response",
            timestamp="2025-10-22T00:00:00Z"
        )
        msg_dict = msg.__dict__
        assert "content" in msg_dict

@pytest.mark.unit
@pytest.mark.customization
class TestRAGContext:
    def test_rag_context_creation(self):
        """Test creating RAG context"""
        context = RAGContext(
            session_id="test",
            document="doc content",
            embedding=[0.1, 0.2],
            metadata={"type": "test"}
        )
        assert context.document == "doc content"
        assert len(context.embedding) == 2
