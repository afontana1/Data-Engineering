# telemetry/sink.py
from __future__ import annotations

from typing import Protocol, Any, Dict
import asyncio
import json


class UsageSink(Protocol):
    async def write(self, record: Dict[str, Any]) -> None: ...


class StdoutSink:
    async def write(self, record: Dict[str, Any]) -> None:
        print(json.dumps(record, default=str))


class AsyncQueueSink:
    """
    Use this if you don't want DB writes on the hot path.
    Start `worker()` once on app startup.
    """
    def __init__(self, inner: UsageSink, maxsize: int = 10_000):
        self.inner = inner
        self.q: asyncio.Queue[dict] = asyncio.Queue(maxsize=maxsize)

    async def write(self, record: dict) -> None:
        # drop-on-full policy; swap to "await put" if you prefer backpressure
        try:
            self.q.put_nowait(record)
        except asyncio.QueueFull:
            pass

    async def worker(self) -> None:
        while True:
            rec = await self.q.get()
            try:
                await self.inner.write(rec)
            finally:
                self.q.task_done()
