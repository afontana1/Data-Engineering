from __future__ import annotations

from typing import Any, Dict, List, Tuple

from ..records import Record


class FullTextIndex:
    """
    Very simple inverted index over specified string fields of the payload.

    Tokenization: whitespace + lowercasing.
    Ranking: term match count (could be extended to TF-IDF / BM25).
    """

    def __init__(self, fields: List[str] | None = None):
        self.fields = fields or []
        self.inverted: Dict[str, Dict[str, int]] = {}
        self.documents: Dict[str, Dict[str, Any]] = {}

    def _tokenize(self, text: str) -> List[str]:
        return [t.lower() for t in text.split() if t]

    def _extract_text(self, payload: Dict[str, Any]) -> str:
        parts: List[str] = []
        for f in self.fields:
            v = payload.get(f)
            if isinstance(v, str):
                parts.append(v)
        return " ".join(parts)

    def add(self, record: Record) -> None:
        text = self._extract_text(record.payload)
        self.documents[record.id] = record.payload
        tokens = self._tokenize(text)
        for tok in tokens:
            posting = self.inverted.setdefault(tok, {})
            posting[record.id] = posting.get(record.id, 0) + 1

    def remove(self, record_id: str) -> None:
        if record_id in self.documents:
            payload = self.documents.pop(record_id)
            text = self._extract_text(payload)
            tokens = self._tokenize(text)
            for tok in tokens:
                posting = self.inverted.get(tok)
                if posting and record_id in posting:
                    del posting[record_id]
                    if not posting:
                        del self.inverted[tok]

    def update(self, record: Record) -> None:
        self.remove(record.id)
        self.add(record)

    def search(self, query: str, k: int = 10) -> List[Tuple[str, float]]:
        tokens = self._tokenize(query)
        scores: Dict[str, float] = {}
        for tok in tokens:
            posting = self.inverted.get(tok, {})
            for rid, count in posting.items():
                scores[rid] = scores.get(rid, 0.0) + count
        results = [(rid, -score) for rid, score in scores.items()]
        results.sort(key=lambda x: x[1])
        return results[:k]
