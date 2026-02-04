# telemetry/sink.py
from __future__ import annotations

from typing import Protocol, Any, Dict, Iterable
import asyncio
import json
import logging
import uuid

from token_tracker.telemetry.db_connector import DatabaseConnector

logger = logging.getLogger(__name__)


class UsageSink(Protocol):
    async def write(self, record: Dict[str, Any]) -> None: ...


class DynamoDBTableClient(Protocol):
    def put_item(self, *, Item: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]: ...


class StdoutSink:
    async def write(self, record: Dict[str, Any]) -> None:
        print(json.dumps(record, default=str))


class DatabaseSink:
    def __init__(self, connector: DatabaseConnector):
        self.connector = connector
        self.connector.connect()
        self.connector.init_schema()

    async def write(self, record: Dict[str, Any]) -> None:
        await asyncio.to_thread(self.connector.insert_usage, record)


class DynamoDBSink:
    def __init__(self, table: DynamoDBTableClient):
        self.table = table

    async def write(self, record: Dict[str, Any]) -> None:
        item = dict(record)
        # Table uses `id` as HASH key. Reuse call_id when present.
        item.setdefault("id", item.get("call_id") or str(uuid.uuid4()))
        await asyncio.to_thread(self.table.put_item, Item=item)


class MultiSink:
    def __init__(self, sinks: Iterable[UsageSink]):
        self.sinks = list(sinks)

    async def write(self, record: Dict[str, Any]) -> None:
        results = await asyncio.gather(
            *(sink.write(record) for sink in self.sinks),
            return_exceptions=True,
        )
        for sink, result in zip(self.sinks, results):
            if isinstance(result, Exception):
                logger.exception("Telemetry sink failed (%s): %s", type(sink).__name__, result)


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
