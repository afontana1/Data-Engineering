from __future__ import annotations

from pydantic import BaseModel, Field

from faulttree.core.config import FaultTreeConfig
from faulttree.solvers.interfaces import SolveMethod


class SolveBody(BaseModel):
    config: FaultTreeConfig
    method: SolveMethod = SolveMethod.BDD_EXACT
    mission_time_hours: float | None = None

    house_overrides: dict[str, bool] | None = None
    prob_overrides: dict[str, float] | None = None

    max_cut_sets: int = 50_000
    max_cut_set_order: int = 20

    mc_samples: int = 50_000
    mc_seed: int | None = None


class SolveResponse(BaseModel):
    method: SolveMethod
    top_event_probability: float
    details: dict = Field(default_factory=dict)
