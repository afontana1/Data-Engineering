from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping, Protocol

from faulttree.core.graph import FaultTree


class SolveMethod(str, Enum):
    CLOSED_FORM = "closed_form"
    CUT_SETS = "cut_sets"
    RARE_EVENT = "rare_event"
    BDD_EXACT = "bdd_exact"
    MONTE_CARLO = "monte_carlo"


@dataclass(frozen=True)
class SolveRequest:
    method: SolveMethod
    mission_time_hours: float | None = None

    # Optional evidence overrides:
    # - house event fixed values
    # - basic event fixed probabilities (for scenarios)
    house_overrides: Mapping[str, bool] | None = None
    prob_overrides: Mapping[str, float] | None = None

    # cut set controls
    max_cut_sets: int = 50_000
    max_cut_set_order: int = 20

    # monte carlo controls
    mc_samples: int = 50_000
    mc_seed: int | None = None


@dataclass(frozen=True)
class SolveResult:
    method: SolveMethod
    top_event_probability: float
    details: dict


class Solver(Protocol):
    def solve(self, ft: FaultTree, req: SolveRequest) -> SolveResult: ...
