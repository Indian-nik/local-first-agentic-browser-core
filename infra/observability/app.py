from fastapi import FastAPI, Request
from pydantic import BaseModel
import os

app = FastAPI(title="Observability")

logs = []

class Log(BaseModel):
    type: str
    agent_id: str | None = None
    task_id: str | None = None
    result: str | None = None
    ts: str | None = None

@app.post("/log")
async def ingest(l: Log):
    logs.append(l.dict())
    return {"ok": True}

@app.get("/logs")
async def list_logs():
    return logs[-500:]

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/metrics")
async def get_metrics():
    return {"logs": len(logs)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "9000")))
