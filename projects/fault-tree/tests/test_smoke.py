from faulttree.core.config import load_config
from faulttree.solvers.interfaces import SolveMethod, SolveRequest
from faulttree.solvers.bdd import BDDSolver


def test_smoke_bdd_or_gate():
    cfg = {
        "top_event_id": "T",
        "nodes": [
            {"kind": "basic_event", "id": "A", "name": "A", "p": 0.1},
            {"kind": "basic_event", "id": "B", "name": "B", "p": 0.2},
            {"kind": "gate", "id": "T", "name": "Top", "gate_type": "or", "inputs": ["A", "B"]},
        ],
    }
    ft = load_config(cfg)
    res = BDDSolver().solve(ft, SolveRequest(method=SolveMethod.BDD_EXACT))
    # P(A or B) = 0.1 + 0.2 - 0.02 = 0.28
    assert abs(res.top_event_probability - 0.28) < 1e-9
