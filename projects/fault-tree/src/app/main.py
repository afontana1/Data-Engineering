from __future__ import annotations

from fastapi import FastAPI, HTTPException

from faulttree.core.config import load_config
from faulttree.core.schema_export import fault_tree_config_json_schema
from faulttree.solvers.interfaces import SolveMethod, SolveRequest
from faulttree.solvers.closed_form import ClosedFormSolver
from faulttree.solvers.cut_sets import CutSetSolver
from faulttree.solvers.bdd import BDDSolver
from faulttree.solvers.monte_carlo import MonteCarloSolver

from app.schemas import SolveBody, SolveResponse

app = FastAPI(title="Fault Tree Solver", version="0.1.0")


@app.get("/health")
def health() -> dict:
    return {"ok": True}


@app.get("/schema/faulttree")
def schema_faulttree() -> dict:
    """
    JSON Schema for the fault tree DSL config.
    """
    return fault_tree_config_json_schema()


@app.post("/solve", response_model=SolveResponse)
def solve(body: SolveBody) -> SolveResponse:
    ft = load_config(body.config.model_dump())

    issues = ft.validate()
    if issues:
        raise HTTPException(
            status_code=422,
            detail={"validation_issues": [i.__dict__ for i in issues]},
        )

    req = SolveRequest(
        method=body.method,
        mission_time_hours=body.mission_time_hours,
        house_overrides=body.house_overrides,
        prob_overrides=body.prob_overrides,
        max_cut_sets=body.max_cut_sets,
        max_cut_set_order=body.max_cut_set_order,
        mc_samples=body.mc_samples,
        mc_seed=body.mc_seed,
    )

    solver_map = {
        SolveMethod.CLOSED_FORM: ClosedFormSolver(),
        SolveMethod.CUT_SETS: CutSetSolver(),
        SolveMethod.RARE_EVENT: CutSetSolver(),  # alias; uses rare-event sum in details
        SolveMethod.BDD_EXACT: BDDSolver(),
        SolveMethod.MONTE_CARLO: MonteCarloSolver(),
    }
    solver = solver_map[req.method]

    try:
        result = solver.solve(ft, req)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    return SolveResponse(
        method=result.method,
        top_event_probability=result.top_event_probability,
        details=result.details,
    )
