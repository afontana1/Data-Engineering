from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Dict

from faulttree.core.expr import eval_expr
from faulttree.core.graph import FaultTree
from faulttree.solvers.interfaces import SolveMethod, SolveRequest, SolveResult


@dataclass
class MonteCarloSolver:
    def solve(self, ft: FaultTree, req: SolveRequest) -> SolveResult:
        expr, base_probs, house_vals = ft.to_boolean_expr()

        probs: Dict[str, float] = dict(base_probs)
        if req.prob_overrides:
            probs.update({k: float(v) for k, v in req.prob_overrides.items()})

        hv = dict(house_vals)
        if req.house_overrides:
            hv.update({k: bool(v) for k, v in req.house_overrides.items()})
        for k, v in hv.items():
            probs[k] = 1.0 if v else 0.0

        rng = random.Random(req.mc_seed)

        vars_list = sorted(probs.keys())

        n = int(req.mc_samples)
        hits = 0
        for _ in range(n):
            env = {v: (rng.random() < probs[v]) for v in vars_list}
            if eval_expr(expr, env):
                hits += 1

        phat = hits / n
        # Normal approx CI (ok baseline; Wilson is better)
        z = 1.96
        se = math.sqrt(max(phat * (1 - phat), 1e-18) / n)
        lo = max(0.0, phat - z * se)
        hi = min(1.0, phat + z * se)

        return SolveResult(
            method=SolveMethod.MONTE_CARLO,
            top_event_probability=float(phat),
            details={
                "samples": n,
                "hits": hits,
                "ci95": [lo, hi],
                "seed": req.mc_seed,
            },
        )
