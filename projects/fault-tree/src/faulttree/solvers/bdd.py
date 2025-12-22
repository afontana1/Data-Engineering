from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Dict, Iterable, List, Mapping, Tuple

from faulttree.core.expr import And, Const, Expr, Or, Var
from faulttree.core.graph import FaultTree
from faulttree.solvers.interfaces import SolveMethod, SolveRequest, SolveResult


# -------------------------
# ROBDD representation
# -------------------------

@dataclass(frozen=True)
class BDDNode:
    var: str
    low: int   # node index
    high: int  # node index


class ROBDD:
    """
    Terminal nodes:
      0 => False
      1 => True
    Non-terminals are stored in `nodes` with integer ids >= 2.
    """
    def __init__(self, var_order: List[str]) -> None:
        self.var_order = var_order
        self.var_index = {v: i for i, v in enumerate(var_order)}
        self.nodes: Dict[int, BDDNode] = {}
        self.unique_table: Dict[Tuple[str, int, int], int] = {}
        self._next_id = 2

    def mk(self, var: str, low: int, high: int) -> int:
        if low == high:
            return low
        key = (var, low, high)
        if key in self.unique_table:
            return self.unique_table[key]
        nid = self._next_id
        self._next_id += 1
        self.nodes[nid] = BDDNode(var=var, low=low, high=high)
        self.unique_table[key] = nid
        return nid

    def is_terminal(self, nid: int) -> bool:
        return nid in (0, 1)

    def top_var(self, nid: int) -> str:
        return self.nodes[nid].var

    def children(self, nid: int) -> Tuple[int, int]:
        n = self.nodes[nid]
        return n.low, n.high


def _vars_in_expr(e: Expr, out: set[str]) -> None:
    if isinstance(e, Var):
        out.add(e.name)
    elif isinstance(e, Const):
        return
    elif isinstance(e, And) or isinstance(e, Or):
        for x in e.xs:
            _vars_in_expr(x, out)
    else:
        # Not used in this baseline (we didn't build Not in graph translation)
        raise TypeError(f"Unsupported expr node: {type(e)}")


def _restrict(e: Expr, var: str, value: bool) -> Expr:
    if isinstance(e, Const):
        return e
    if isinstance(e, Var):
        if e.name == var:
            return Const(value)
        return e
    if isinstance(e, And):
        xs = [_restrict(x, var, value) for x in e.xs]
        # simplify
        if any(isinstance(x, Const) and x.value is False for x in xs):
            return Const(False)
        xs2 = [x for x in xs if not (isinstance(x, Const) and x.value is True)]
        if not xs2:
            return Const(True)
        if len(xs2) == 1:
            return xs2[0]
        return And(xs2)
    if isinstance(e, Or):
        xs = [_restrict(x, var, value) for x in e.xs]
        if any(isinstance(x, Const) and x.value is True for x in xs):
            return Const(True)
        xs2 = [x for x in xs if not (isinstance(x, Const) and x.value is False)]
        if not xs2:
            return Const(False)
        if len(xs2) == 1:
            return xs2[0]
        return Or(xs2)
    raise TypeError(f"Unsupported expr node: {type(e)}")


def build_robdd(expr: Expr, var_order: List[str]) -> tuple[ROBDD, int]:
    bdd = ROBDD(var_order)

    @lru_cache(maxsize=None)
    def build(e_repr: str, i: int) -> int:
        # e_repr is a stable string key for caching; we rebuild expr from repr not needed; we use closure with map.
        raise RuntimeError("internal")

    # Instead of stringifying expr, use Python's repr + cache by id via tuple key; simplest: manual cache dict
    memo: Dict[tuple[int, int], int] = {}

    def rec(e: Expr, idx: int) -> int:
        key = (id(e), idx)
        if key in memo:
            return memo[key]

        if isinstance(e, Const):
            memo[key] = 1 if e.value else 0
            return memo[key]
        if idx >= len(var_order):
            # no vars left; should be constant if fully simplified
            # treat non-constant as unknown -> conservative False
            memo[key] = 0
            return 0

        # If expression doesn't contain remaining vars, reduce quickly
        # (cheap check by collecting vars once would be better; OK baseline)
        v = var_order[idx]
        e0 = _restrict(e, v, False)
        e1 = _restrict(e, v, True)
        low = rec(e0, idx + 1)
        high = rec(e1, idx + 1)
        nid = bdd.mk(v, low, high)
        memo[key] = nid
        return nid

    root = rec(expr, 0)
    return bdd, root


def bdd_probability(bdd: ROBDD, root: int, p: Mapping[str, float]) -> float:
    @lru_cache(maxsize=None)
    def prob(nid: int) -> float:
        if nid == 0:
            return 0.0
        if nid == 1:
            return 1.0
        node = bdd.nodes[nid]
        pv = float(p[node.var])
        return (1.0 - pv) * prob(node.low) + pv * prob(node.high)

    return prob(root)


@dataclass
class BDDSolver:
    """
    Exact under:
      - independence of boolean variables
      - dependencies represented via explicit latent vars (CCF expansion) and boolean rewrites
    """

    def solve(self, ft: FaultTree, req: SolveRequest) -> SolveResult:
        expr, base_probs, house_vals = ft.to_boolean_expr()

        # Build probability map with overrides & house events
        probs: Dict[str, float] = dict(base_probs)
        if req.prob_overrides:
            probs.update({k: float(v) for k, v in req.prob_overrides.items()})

        # House events become deterministic vars with p in {0,1}
        hv = dict(house_vals)
        if req.house_overrides:
            hv.update({k: bool(v) for k, v in req.house_overrides.items()})
        for k, v in hv.items():
            probs[k] = 1.0 if v else 0.0

        # Ensure every var in expr has a probability
        vars_set: set[str] = set()
        _vars_in_expr(expr, vars_set)

        missing = [v for v in sorted(vars_set) if v not in probs]
        if missing:
            raise ValueError(f"Missing probabilities/values for vars: {missing}")

        # Variable order: stable alphabetical (baseline). Later: heuristics.
        order = sorted(vars_set)

        bdd, root = build_robdd(expr, order)
        p_top = bdd_probability(bdd, root, probs)

        return SolveResult(
            method=SolveMethod.BDD_EXACT,
            top_event_probability=float(p_top),
            details={
                "var_count": len(order),
                "bdd_node_count": len(bdd.nodes) + 2,
                "assumptions": ["independence_of_vars", "static_boolean"],
                "var_order": order,
            },
        )
