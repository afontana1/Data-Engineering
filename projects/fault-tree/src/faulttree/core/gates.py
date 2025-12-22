from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from faulttree.core.types import GateType, NodeId


@dataclass(frozen=True)
class Gate:
    id: NodeId
    name: str
    gate_type: GateType
    inputs: Sequence[NodeId]

    def arity(self) -> int:
        return len(self.inputs)


@dataclass(frozen=True)
class KofNGate(Gate):
    k: int = 1  # must satisfy 1 <= k <= n

    def __post_init__(self) -> None:
        if self.gate_type != GateType.KOFN:
            raise ValueError("KofNGate gate_type must be 'kofn'")
        n = len(self.inputs)
        if not (1 <= self.k <= n):
            raise ValueError(f"Invalid k={self.k} for n={n}")


@dataclass(frozen=True)
class InhibitGate(Gate):
    """
    Output = (all primary inputs) AND condition
    Convention:
      - last input is the condition event (often a HouseEvent)
      - all preceding inputs are primary causes
    """
    def __post_init__(self) -> None:
        if self.gate_type != GateType.INHIBIT:
            raise ValueError("InhibitGate gate_type must be 'inhibit'")
        if len(self.inputs) < 2:
            raise ValueError("InhibitGate requires at least 2 inputs (primary + condition)")

    @property
    def condition(self) -> NodeId:
        return self.inputs[-1]

    @property
    def primary_inputs(self) -> Sequence[NodeId]:
        return self.inputs[:-1]
