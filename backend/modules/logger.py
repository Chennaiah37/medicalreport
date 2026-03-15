"""
backend/modules/logger.py
===========================
Audit logging — every prediction is saved to results/audit_log.json.
"""

import os
import json
import datetime

LOG_DIR  = os.path.join(os.path.dirname(__file__), "..", "results")
LOG_FILE = os.path.join(LOG_DIR, "audit_log.json")


def save_log(snippet: str, disease: str, confidence: float, engine: str) -> None:
    """Append one prediction record to the audit log."""
    os.makedirs(LOG_DIR, exist_ok=True)
    entry = {
        "timestamp":  datetime.datetime.now().isoformat(),
        "snippet":    snippet[:120],
        "prediction": disease,
        "confidence": confidence,
        "engine":     engine,
    }
    logs = load_log()
    logs.append(entry)
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)


def load_log() -> list:
    """Load all log entries. Returns empty list if no log exists."""
    if not os.path.exists(LOG_FILE):
        return []
    try:
        with open(LOG_FILE) as f:
            return json.load(f)
    except Exception:
        return []


def clear_log() -> None:
    """Clear all log entries."""
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump([], f)
