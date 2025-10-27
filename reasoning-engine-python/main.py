from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import duckdb, os, uuid, datetime, json

app = FastAPI(title="Reasoning Engine")

DUCKDB_PATH = os.getenv("DUCKDB_PATH", "/data/memory.duckdb")
DUCKDB_ENCRYPTION = os.getenv("DUCKDB_ENCRYPTION", "disabled")

# Initialize DB and tables
con = duckdb.connect(DUCKDB_PATH, read_only=False)
con.execute("PRAGMA enable_object_cache");
# Note: encryption would require DuckDB extension/pragma; left configurable
con.execute(
    """
    CREATE TABLE IF NOT EXISTS memories (
        id VARCHAR PRIMARY KEY,
        user_id VARCHAR,
        ts TIMESTAMP,
        type VARCHAR,
        content TEXT,
        embedding BLOB,
        meta JSON
    );
    CREATE INDEX IF NOT EXISTS idx_mem_user ON memories(user_id);
    CREATE INDEX IF NOT EXISTS idx_mem_ts ON memories(ts);
    """
)

class MemoryIn(BaseModel):
    user_id: str
    type: str
    content: str
    meta: dict | None = None
    embedding: bytes | None = None

class MemoryOut(MemoryIn):
    id: str
    ts: datetime.datetime

@app.post("/memory", response_model=MemoryOut)
def create_memory(m: MemoryIn):
    mem_id = str(uuid.uuid4())
    ts = datetime.datetime.utcnow()
    con.execute(
        "INSERT INTO memories VALUES (?, ?, ?, ?, ?, ?, ?)",
        [mem_id, m.user_id, ts, m.type, m.content, m.embedding, json.dumps(m.meta or {})],
    )
    return MemoryOut(id=mem_id, ts=ts, **m.dict())

@app.get("/memory")
def list_memories(user_id: str = Query(...), q: str | None = None, limit: int = 50):
    if q:
        res = con.execute(
            "SELECT id, user_id, ts, type, content, embedding, meta FROM memories WHERE user_id=? AND lower(content) LIKE ? ORDER BY ts DESC LIMIT ?",
            [user_id, f"%{q.lower()}%", limit],
        ).fetchall()
    else:
        res = con.execute(
            "SELECT id, user_id, ts, type, content, embedding, meta FROM memories WHERE user_id=? ORDER BY ts DESC LIMIT ?",
            [user_id, limit],
        ).fetchall()
    out = []
    for row in res:
        rid, uid, ts, typ, content, emb, meta = row
        out.append({
            "id": rid,
            "user_id": uid,
            "ts": ts,
            "type": typ,
            "content": content,
            "embedding": emb,
            "meta": json.loads(meta) if isinstance(meta, str) else meta,
        })
    return out

@app.put("/memory/{mem_id}", response_model=MemoryOut)
def update_memory(mem_id: str, m: MemoryIn):
    ts = datetime.datetime.utcnow()
    cur = con.execute(
        "UPDATE memories SET user_id=?, ts=?, type=?, content=?, embedding=?, meta=? WHERE id=?",
        [m.user_id, ts, m.type, m.content, m.embedding, json.dumps(m.meta or {}), mem_id],
    )
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Memory not found")
    return MemoryOut(id=mem_id, ts=ts, **m.dict())

@app.delete("/memory/{mem_id}")
def delete_memory(mem_id: str):
    cur = con.execute("DELETE FROM memories WHERE id=?", [mem_id])
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Memory not found")
    return {"ok": True}

# Simple RAG query endpoint returning recent relevant memories
@app.get("/rag/context")
def rag_context(user_id: str, q: str, limit: int = 5):
    res = con.execute(
        "SELECT id, content, ts FROM memories WHERE user_id=? AND lower(content) LIKE ? ORDER BY ts DESC LIMIT ?",
        [user_id, f"%{q.lower()}%", limit],
    ).fetchall()
    return [{"id": r[0], "content": r[1], "ts": r[2]} for r in res]
