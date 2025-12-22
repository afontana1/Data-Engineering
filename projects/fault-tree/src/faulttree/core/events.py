from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from faulttree.core.types import NodeId


@runtime_checkable
class Event(Protocol):
    id: NodeId
    name: str

    def is_leaf(self) -> bool: ...


@dataclass(frozen=True)
class BasicEvent:
    """
    Leaf event with a probability model.

    Exactly one of:
      - p: direct probability in [0,1]
      - lambda_rate + mission_time: exponential failure model P=1-exp(-lambda*t)
    may be used at solve-time. If both are given, p wins.
    """
    id: NodeId
    name: str
    p: float | None = None
    lambda_rate_per_hour: float | None = None

    def is_leaf(self) -> bool:
        return True


@dataclass(frozen=True)
class HouseEvent:
    """
    Scenario/condition flag (not random by default).
    If value is None, caller must provide it via evidence or defaults.
    """
    id: NodeId
    name: str
    value: bool | None = None

    def is_leaf(self) -> bool:
        return True
