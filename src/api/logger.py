import json
import uuid
from datetime import datetime
from pathlib import Path

from httpcore import request

LOG_FILE = Path("logs/app_logs.jsonl")

# Ensure logs directory exists
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

def log_request(
    query: str,
    response_status: str,
    latency_ms: float,
):
    log_entry = {
        "trace_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "query": query,
        "response_status": response_status,
        "latency_ms": round(latency_ms, 2),
    }

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")