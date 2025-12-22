from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from faulttree.core.types import NodeId


@dataclass(frozen=True)
class CCFGroup:
    """
    Common-Cause Failure group using a beta-factor style decomposition.

    This is implemented as a *modeling construct* that expands into:
      - one latent common-cause basic event (independent)
      - independent-basic-events for each member
      - each member becomes: member = common OR independent_member

    Notes:
      - Best practice is identical channels. If you provide different member probabilities,
        this implementation uses their mean as the "total channel failure probability" for beta split.
    """
    id: NodeId
    name: str
    members: Sequence[NodeId]
    beta: float  # in [0,1]


@dataclass(frozen=True)
class FunctionalDependency:
    """
    Static functional dependency: if trigger occurs, dependent is forced to occur.

    Implemented as: dependent' = dependent OR trigger
    (dependent is usually a basic event or intermediate event id)
    """
    id: NodeId
    name: str
    trigger: NodeId
    dependent: NodeId
