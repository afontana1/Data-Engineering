from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import NewType

NodeId = NewType("NodeId", str)


class NodeKind(str, Enum):
    BASIC_EVENT = "basic_event"
    HOUSE_EVENT = "house_event"
    GATE = "gate"
    CCF_GROUP = "ccf_group"
    FDEP = "fdep"  # functional dependency (static)


class GateType(str, Enum):
    OR = "or"
    AND = "and"
    KOFN = "kofn"
    INHIBIT = "inhibit"


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    message: str
    node_id: str | None = None
