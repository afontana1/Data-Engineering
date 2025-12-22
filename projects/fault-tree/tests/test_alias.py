from faulttree.core.config import load_config
from faulttree.solvers.bdd import BDDSolver
from faulttree.solvers.interfaces import SolveMethod, SolveRequest


def test_alias_resolution():
    cfg = {
        "version": "1.0",
        "metadata": {"example": True},
        "top_event_id": "TOP",
        "nodes": [
            {"kind": "basic_event", "id": "A", "name": "A", "p": 0.1},
            {"kind": "basic_event", "id": "B", "name": "B", "p": 0.2},
            {"kind": "alias", "id": "A_LOCAL", "target": "A"},
            {"kind": "gate", "id": "TOP", "name": "Top", "gate_type": "or", "inputs": ["A_LOCAL", "B"]},
        ],
    }
    ft = load_config(cfg)
    res = BDDSolver().solve(ft, SolveRequest(method=SolveMethod.BDD_EXACT))
    # P(A or B) = 0.28
    assert abs(res.top_event_probability - 0.28) < 1e-9
