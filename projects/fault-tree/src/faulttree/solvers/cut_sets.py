from __future__ import annotations

import math
from dataclasses import dataclass
from itertools import combinations
from typing import Dict, FrozenSet, Iterable, List, Mapping, Set, Tuple

from faulttree.core.events import BasicEvent, HouseEvent
from faulttree.core.gates import Gate, InhibitGate, KofNGate
from faulttree.core.graph import FaultTree
from faulttree.core.types import GateType, NodeId
from faulttree.solvers.interfaces import SolveMethod, SolveRequest, SolveResult


CutSet = FrozenSet[str]  # set of leaf var names (node ids as strings)


def _minimize(sets: Iterable[CutSet]) -> list[CutSet]:
    """
    Remove non-minimal cut sets (supersets).
    """
    s_list = sorted(set(sets), key=lambda x: (len(x), sorted(x)))
    minimal: list[CutSet] = []
    for s in s_list:
        if any(m.issubset(s) for m in minimal):
            continue
        minimal.append(s)
    return minimal


def _p_from_basic_id(ft: FaultTree, nid: NodeId, req: SolveRequest) -> float:
    from faulttree.solvers.closed_form import _p_from_basic  # reuse

    prob_over = req.prob_overrides or {}
    house_over = req.house_overrides or {}

    node = ft.get(nid)
    if isinstance(node, BasicEvent):
        if str(nid) in prob_over:
            return float(prob_over[str(nid)])
        return _p_from_basic(node, req.mission_time_hours)
    if isinstance(node, HouseEvent):
        if str(nid) in house_over:
            return 1.0 if bool(house_over[str(nid)]) else 0.0
        if node.value is not None:
            return 1.0 if bool(node.value) else 0.0
        return 0.0
    raise TypeError("Cut sets require leaves to be basic/house events after expansion.")


@dataclass
class CutSetSolver:
    """
    Enumerates minimal cut sets (best-effort) for static trees.

    Assumptions for quantitative use:
      - independence of leaf variables
      - dependency constructs should be expanded before cut set solving (use ft.to_boolean_expr in other solvers)
    """

    def _cut_sets(self, ft: FaultTree, nid: NodeId, req: SolveRequest, memo: Dict[NodeId, list[CutSet]]) -> list[CutSet]:
        if nid in memo:
            return memo[nid]

        node = ft.get(nid)

        # Leaf
        if isinstance(node, (BasicEvent, HouseEvent)):
            cs = [frozenset([str(nid)])]
            memo[nid] = cs
            return cs

        # Inhibit: AND(primary..., condition)
        if isinstance(node, InhibitGate):
            parts = [self._cut_sets(ft, x, req, memo) for x in node.primary_inputs]
            parts.append(self._cut_sets(ft, node.condition, req, memo))
            out = [frozenset()]
            for p in parts:
                out = [a.union(b) for a in out for b in p]
                if len(out) > req.max_cut_sets:
                    raise ValueError("cut set explosion (increase limits or simplify model)")
            memo[nid] = _minimize(out)
            return memo[nid]

        # K-of-N => OR of all k-sized ANDs (combinatorial)
        if isinstance(node, KofNGate):
            term_sets: list[CutSet] = []
            for combo in combinations(node.inputs, node.k):
                # AND combine
                out = [frozenset()]
                for x in combo:
                    out = [a.union(b) for a in out for b in self._cut_sets(ft, x, req, memo)]
                    if len(out) > req.max_cut_sets:
                        raise ValueError("cut set explosion in kofn expansion")
                term_sets.extend(out)
                if len(term_sets) > req.max_cut_sets:
                    raise ValueError("cut set explosion in kofn")
            memo[nid] = _minimize(term_sets)
            return memo[nid]

        if isinstance(node, Gate):
            child_cut_sets = [self._cut_sets(ft, x, req, memo) for x in node.inputs]

            if node.gate_type == GateType.OR:
                # union of child cut sets
                out = [cs for sets in child_cut_sets for cs in sets]
                memo[nid] = _minimize(out)
                return memo[nid]

            if node.gate_type == GateType.AND:
                out = [frozenset()]
                for sets in child_cut_sets:
                    out = [a.union(b) for a in out for b in sets]
                    if len(out) > req.max_cut_sets:
                        raise ValueError("cut set explosion (AND product too large)")
                memo[nid] = _minimize(out)
                return memo[nid]

        raise TypeError(f"Unsupported node for cut sets: {type(node)}")

    def solve(self, ft: FaultTree, req: SolveRequest) -> SolveResult:
        memo: Dict[NodeId, list[CutSet]] = {}
        cut_sets = self._cut_sets(ft, ft.top_event_id, req, memo)
        cut_sets = [cs for cs in cut_sets if len(cs) <= req.max_cut_set_order]
        cut_sets = cut_sets[: req.max_cut_sets]

        # First-order rare event approximation: sum of cut set probs
        # P(cut) = product p_i, assuming independence
        leaf_cache: Dict[str, float] = {}
        def leaf_p(name: str) -> float:
            if name in leaf_cache:
                return leaf_cache[name]
            p = _p_from_basic_id(ft, NodeId(name), req)
            leaf_cache[name] = p
            return p

        cut_ps: list[float] = []
        for cs in cut_sets:
            p = 1.0
            for v in cs:
                p *= leaf_p(v)
            cut_ps.append(p)

        rare = float(sum(cut_ps))
        rare = min(max(rare, 0.0), 1.0)

        return SolveResult(
            method=SolveMethod.CUT_SETS,
            top_event_probability=rare,
            details={
                "cut_sets": [sorted(list(cs)) for cs in cut_sets],
                "cut_set_probabilities": cut_ps,
                "approximation": "rare_event_sum_of_cut_sets",
                "assumptions": ["independence"],
            },
        )
