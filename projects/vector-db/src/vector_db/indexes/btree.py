from __future__ import annotations

from typing import Any, Iterable, List

from ..records import Record


class BTreeIndex:
    """
    Very simplified B-tree-like index for scalar metadata:

    Uses sorted lists + bisect for range queries.
    """

    def __init__(self, field: str):
        self.field = field
        self.keys: List[Any] = []
        self.record_ids: List[str] = []

    def build_from(self, records: Iterable[Record]) -> None:
        items = []
        for r in records:
            v = r.payload.get(self.field)
            if v is not None:
                items.append((v, r.id))
        items.sort(key=lambda x: x[0])
        self.keys = [k for k, _ in items]
        self.record_ids = [rid for _, rid in items]

    def add(self, record: Record) -> None:
        v = record.payload.get(self.field)
        if v is None:
            return
        import bisect

        i = bisect.bisect_left(self.keys, v)
        self.keys.insert(i, v)
        self.record_ids.insert(i, record.id)

    def remove(self, record_id: str) -> None:
        if record_id not in self.record_ids:
            return
        i = self.record_ids.index(record_id)
        del self.record_ids[i]
        del self.keys[i]

    def update(self, record: Record) -> None:
        self.remove(record.id)
        self.add(record)

    def range_search(self, low: Any = None, high: Any = None) -> List[str]:
        import bisect

        if low is None:
            start = 0
        else:
            start = bisect.bisect_left(self.keys, low)

        if high is None:
            end = len(self.keys)
        else:
            end = bisect.bisect_right(self.keys, high)

        return self.record_ids[start:end]
