from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, Mapping, Set

from faulttree.core.events import BasicEvent, HouseEvent
from faulttree.core.gates import Gate, InhibitGate, KofNGate
from faulttree.core.graph import FaultTree
from faulttree.core.types import GateType, NodeId
from faulttree.solvers.interfaces import SolveRequest, SolveResult, SolveMethod


def _p_from_basic(be: BasicEvent, mission_time_hours: float | None) -> float:
    if be.p is not None:
        return float(be.p)
    if be.lambda_rate_per_hour is not None and mission_time_hours is not None:
        lam = float(be.lambda_rate_per_hour)
        t = float(mission_time_hours)
        return 1.0 - math.exp(-lam * t)
    raise ValueError(f"BasicEvent {be.id} missing probability model (p or lambda+mission_time)")


@dataclass
class ClosedFormSolver:
    """
    Assumes:
      - no repeated child references (tree structure, not DAG)
      - independence
      - no dynamic gates
    """

    def solve(self, ft: FaultTree, req: SolveRequest) -> SolveResult:
        shared = ft.detect_shared_events()
        if shared:
            raise ValueError(
                f"closed_form requires a tree (no shared events). Shared: {sorted(map(str, shared))}"
            )

        # Evaluate recursively
        memo: Dict[NodeId, float] = {}

        house_over = req.house_overrides or {}
        prob_over = req.prob_overrides or {}

        def p_node(nid: NodeId) -> float:
            if nid in memo:
                return memo[nid]

            node = ft.get(nid)

            # leafs
            if isinstance(node, HouseEvent):
                if str(nid) in house_over:
                    val = bool(house_over[str(nid)])
                elif node.value is not None:
                    val = bool(node.value)
                else:
                    # Default: False unless specified
                    val = False
                memo[nid] = 1.0 if val else 0.0
                return memo[nid]

            if isinstance(node, BasicEvent):
                if str(nid) in prob_over:
                    memo[nid] = float(prob_over[str(nid)])
                else:
                    memo[nid] = _p_from_basic(node, req.mission_time_hours)
                return memo[nid]

            # gates
            if isinstance(node, InhibitGate):
                ps = [p_node(x) for x in node.primary_inputs]
                pc = p_node(node.condition)
                # AND of all primaries and condition
                p = pc
                for x in ps:
                    p *= x
                memo[nid] = p
                return p

            if isinstance(node, KofNGate):
                # compute P(at least k) for independent children with their probabilities
                ps = [p_node(x) for x in node.inputs]
                n = len(ps)
                k = node.k
                # dynamic programming on binomial-like sums for non-identical p
                dp = [0.0] * (n + 1)
                dp[0] = 1.0
                for p in ps:
                    for j in range(n, 0, -1):
                        dp[j] = dp[j] * (1 - p) + dp[j - 1] * p
                    dp[0] *= (1 - p)
                memo[nid] = sum(dp[k:])
                return memo[nid]

            if isinstance(node, Gate):
                ps = [p_node(x) for x in node.inputs]
                if node.gate_type == GateType.AND:
                    p = 1.0
                    for x in ps:
                        p *= x
                    memo[nid] = p
                    return p
                if node.gate_type == GateType.OR:
                    q = 1.0
                    for x in ps:
                        q *= (1.0 - x)
                    memo[nid] = 1.0 - q
                    return memo[nid]

            raise TypeError(f"Unsupported node in closed_form: {type(node)}")

        p_top = p_node(ft.top_event_id)
        return SolveResult(
            method=SolveMethod.CLOSED_FORM,
            top_event_probability=p_top,
            details={"assumptions": ["independence", "tree_only"]},
        )
