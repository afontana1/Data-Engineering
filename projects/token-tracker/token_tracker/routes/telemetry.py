# telemetry query routes
from __future__ import annotations

from typing import Any, List, Optional
import asyncio

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field


router = APIRouter()


class TelemetryQuery(BaseModel):
    sql: str = Field(..., min_length=1)
    params: Optional[List[Any]] = None


def _is_read_only_sql(sql: str) -> bool:
    stripped = sql.lstrip().lower()
    return stripped.startswith("select") or stripped.startswith("with")


@router.post("/telemetry/query")
async def query_telemetry(request: Request, payload: TelemetryQuery):
    sql = payload.sql.strip()
    if sql.endswith(";"):
        sql = sql[:-1]

    if not _is_read_only_sql(sql):
        raise HTTPException(status_code=400, detail="Only SELECT queries are allowed.")

    connector = getattr(request.app.state, "db_connector", None)
    if connector is None:
        raise HTTPException(status_code=500, detail="Database connector not initialized.")

    try:
        columns, rows, truncated = await asyncio.to_thread(
            connector.query, sql, payload.params
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        "columns": columns,
        "rows": [list(r) for r in rows],
        "truncated": truncated,
    }
