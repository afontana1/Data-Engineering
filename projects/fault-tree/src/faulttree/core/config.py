from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

from faulttree.core.dependencies import CCFGroup, FunctionalDependency
from faulttree.core.events import BasicEvent, HouseEvent
from faulttree.core.gates import Gate, InhibitGate, KofNGate
from faulttree.core.types import GateType, NodeId
from faulttree.core.graph import FaultTree, Node


# -----------------------------
# Pydantic config models (JSON)
# -----------------------------

class BasicEventCfg(BaseModel):
    kind: Literal["basic_event"] = "basic_event"
    id: str
    name: str
    p: float | None = None
    lambda_rate_per_hour: float | None = None


class HouseEventCfg(BaseModel):
    kind: Literal["house_event"] = "house_event"
    id: str
    name: str
    value: bool | None = None


class GateCfg(BaseModel):
    kind: Literal["gate"] = "gate"
    id: str
    name: str
    gate_type: GateType
    inputs: list[str] = Field(default_factory=list)
    k: int | None = None  # only for kofn


class CCFGroupCfg(BaseModel):
    kind: Literal["ccf_group"] = "ccf_group"
    id: str
    name: str
    members: list[str]
    beta: float


class FDepCfg(BaseModel):
    kind: Literal["fdep"] = "fdep"
    id: str
    name: str
    trigger: str
    dependent: str


class AliasCfg(BaseModel):
    """
    Pure DSL convenience: lets the frontend create local names while referencing the same underlying node.

    Example:
      {"kind":"alias","id":"PUMP_A","target":"PUMP_FAIL"}

    Loader behavior:
      - alias nodes are NOT added to the FaultTree nodes dict
      - all references to alias ids are rewritten to the target id (recursively)
    """
    kind: Literal["alias"] = "alias"
    id: str
    target: str
    name: str | None = None


NodeCfg = BasicEventCfg | HouseEventCfg | GateCfg | CCFGroupCfg | FDepCfg | AliasCfg


class FaultTreeConfig(BaseModel):
    """
    Backwards-compatible DSL.

    - version/metadata are optional (future-proofing)
    - nodes is the list of node definitions (including aliases)
    """
    version: str = "1.0"
    metadata: dict[str, Any] = Field(default_factory=dict)

    top_event_id: str
    nodes: list[NodeCfg]


def load_config(data: dict[str, Any]) -> FaultTree:
    cfg = FaultTreeConfig.model_validate(data)

    # 1) Collect aliases
    alias_map: dict[str, str] = {}
    for n in cfg.nodes:
        if isinstance(n, AliasCfg):
            alias_map[n.id] = n.target

    def resolve_id(raw: str) -> str:
        """
        Resolve alias chains. Detect cycles.
        """
        seen: set[str] = set()
        cur = raw
        while cur in alias_map:
            if cur in seen:
                raise ValueError(f"Alias cycle detected at '{cur}' (chain: {sorted(seen)})")
            seen.add(cur)
            cur = alias_map[cur]
        return cur

    # 2) Build internal nodes dict for non-alias nodes
    nodes: dict[NodeId, Node] = {}

    for n in cfg.nodes:
        if isinstance(n, AliasCfg):
            continue

        nid = NodeId(resolve_id(n.id))

        if isinstance(n, BasicEventCfg):
            nodes[nid] = BasicEvent(
                id=nid, name=n.name, p=n.p, lambda_rate_per_hour=n.lambda_rate_per_hour
            )

        elif isinstance(n, HouseEventCfg):
            nodes[nid] = HouseEvent(id=nid, name=n.name, value=n.value)

        elif isinstance(n, GateCfg):
            inputs = [NodeId(resolve_id(x)) for x in n.inputs]
            if n.gate_type == GateType.KOFN:
                if n.k is None:
                    raise ValueError(f"Gate {n.id} is kofn but missing k")
                nodes[nid] = KofNGate(
                    id=nid,
                    name=n.name,
                    gate_type=GateType.KOFN,
                    inputs=inputs,
                    k=n.k,
                )
            elif n.gate_type == GateType.INHIBIT:
                nodes[nid] = InhibitGate(
                    id=nid,
                    name=n.name,
                    gate_type=GateType.INHIBIT,
                    inputs=inputs,
                )
            else:
                nodes[nid] = Gate(
                    id=nid,
                    name=n.name,
                    gate_type=n.gate_type,
                    inputs=inputs,
                )

        elif isinstance(n, CCFGroupCfg):
            nodes[nid] = CCFGroup(
                id=nid,
                name=n.name,
                members=[NodeId(resolve_id(x)) for x in n.members],
                beta=n.beta,
            )

        elif isinstance(n, FDepCfg):
            nodes[nid] = FunctionalDependency(
                id=nid,
                name=n.name,
                trigger=NodeId(resolve_id(n.trigger)),
                dependent=NodeId(resolve_id(n.dependent)),
            )

        else:
            raise TypeError(f"Unknown node config: {type(n)}")

    top = NodeId(resolve_id(cfg.top_event_id))
    return FaultTree(nodes=nodes, top_event_id=top)
