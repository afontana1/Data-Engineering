from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional, Sequence, Tuple, List
import json
import sqlite3
import threading


@dataclass
class DatabaseConfig:
    db_type: str
    database: str


class DatabaseConnector:
    """
    Simple connector that can be extended to support multiple database types.
    """
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self._conn: Optional[sqlite3.Connection] = None
        self._lock = threading.Lock()

    def connect(self) -> None:
        if self.config.db_type == "sqlite":
            self._conn = sqlite3.connect(self.config.database, check_same_thread=False)
            with self._lock:
                self._conn.execute("PRAGMA journal_mode=WAL;")
                self._conn.execute("PRAGMA synchronous=NORMAL;")
            return
        raise ValueError(f"Unsupported db_type: {self.config.db_type}")

    def close(self) -> None:
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def init_schema(self) -> None:
        conn = self._require_conn()
        with self._lock:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS usage_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ts_ms INTEGER,
                    latency_ms INTEGER,
                    kind TEXT,
                    call_id TEXT,
                    model TEXT,
                    prompt_tokens_est INTEGER,
                    completion_tokens_est INTEGER,
                    total_tokens_est INTEGER,
                    user_id TEXT,
                    org_id TEXT,
                    session_id TEXT,
                    trace_id TEXT,
                    status TEXT,
                    error_type TEXT,
                    error TEXT,
                    record_json TEXT
                )
                """
            )
            conn.commit()

    def insert_usage(self, record: Dict[str, Any]) -> None:
        conn = self._require_conn()
        with self._lock:
            conn.execute(
                """
                INSERT INTO usage_events (
                    ts_ms,
                    latency_ms,
                    kind,
                    call_id,
                    model,
                    prompt_tokens_est,
                    completion_tokens_est,
                    total_tokens_est,
                    user_id,
                    org_id,
                    session_id,
                    trace_id,
                    status,
                    error_type,
                    error,
                    record_json
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record.get("ts_ms"),
                    record.get("latency_ms"),
                    record.get("kind"),
                    record.get("call_id"),
                    record.get("model"),
                    record.get("prompt_tokens_est"),
                    record.get("completion_tokens_est"),
                    record.get("total_tokens_est"),
                    record.get("user_id"),
                    record.get("org_id"),
                    record.get("session_id"),
                    record.get("trace_id"),
                    record.get("status"),
                    record.get("error_type"),
                    record.get("error"),
                    json.dumps(record, default=str),
                ),
            )
            conn.commit()

    def query(self, sql: str, params: Optional[Sequence[Any]] = None,
              *, max_rows: int = 500) -> Tuple[List[str], List[Tuple[Any, ...]], bool]:
        conn = self._require_conn()
        with self._lock:
            cur = conn.execute(sql, params or [])
            columns = [c[0] for c in cur.description] if cur.description else []
            rows = cur.fetchmany(max_rows + 1)
        truncated = len(rows) > max_rows
        if truncated:
            rows = rows[:max_rows]
        return columns, rows, truncated

    def _require_conn(self) -> sqlite3.Connection:
        if self._conn is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self._conn
