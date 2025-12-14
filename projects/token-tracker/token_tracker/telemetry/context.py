# telemetry/context.py
from __future__ import annotations

from contextvars import ContextVar
from dataclasses import dataclass
import uuid


@dataclass(frozen=True)
class UsageContext:
    user_id: str
    org_id: str
    session_id: str
    trace_id: str  # one per inbound request


usage_ctx_var: ContextVar[UsageContext | None] = ContextVar("usage_ctx_var", default=None)


def set_usage_context(user_id: str, org_id: str, session_id: str) -> UsageContext:
    ctx = UsageContext(
        user_id=user_id,
        org_id=org_id,
        session_id=session_id,
        trace_id=str(uuid.uuid4()),
    )
    usage_ctx_var.set(ctx)
    return ctx
