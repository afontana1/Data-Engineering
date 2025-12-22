from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Mapping, Sequence, Set, Union

from faulttree.core.dependencies import CCFGroup, FunctionalDependency
from faulttree.core.events import BasicEvent, HouseEvent
from faulttree.core.gates import Gate, InhibitGate, KofNGate
from faulttree.core.types import GateType, NodeId, ValidationIssue
from faulttree.core.expr import And, Const, Or, Var, Expr


Node = Union[BasicEvent, HouseEvent, Gate, KofNGate, InhibitGate, CCFGroup, FunctionalDependency]


@dataclass
class FaultTree:
    """
    Immutable-ish container for all nodes + a designated top_event_id.

    The actual "network" is defined by Gate.inputs and dependency constructs.
    """
    nodes: Dict[NodeId, Node]
    top_event_id: NodeId

    def get(self, node_id: NodeId) -> Node:
        return self.nodes[node_id]

    def validate(self) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        if self.top_event_id not in self.nodes:
            issues.append(ValidationIssue("missing_top", "top_event_id not found", str(self.top_event_id)))
            return issues

        # Validate references
        for nid, node in self.nodes.items():
            if isinstance(node, Gate):
                for ch in node.inputs:
                    if ch not in self.nodes:
                        issues.append(
                            ValidationIssue("missing_ref", f"Gate input {ch} not found", str(nid))
                        )
            if isinstance(node, CCFGroup):
                if not (0.0 <= node.beta <= 1.0):
                    issues.append(ValidationIssue("bad_beta", "beta must be in [0,1]", str(nid)))
                for m in node.members:
                    if m not in self.nodes:
                        issues.append(ValidationIssue("missing_ref", f"CCF member {m} not found", str(nid)))
            if isinstance(node, FunctionalDependency):
                if node.trigger not in self.nodes:
                    issues.append(ValidationIssue("missing_ref", "trigger not found", str(nid)))
                if node.dependent not in self.nodes:
                    issues.append(ValidationIssue("missing_ref", "dependent not found", str(nid)))

        return issues

    def referenced_children(self, node_id: NodeId) -> Sequence[NodeId]:
        node = self.nodes[node_id]
        if isinstance(node, Gate):
            return list(node.inputs)
        if isinstance(node, CCFGroup):
            return list(node.members)
        if isinstance(node, FunctionalDependency):
            return [node.trigger, node.dependent]
        return []

    def detect_shared_events(self) -> set[NodeId]:
        """
        Returns node ids that are referenced more than once as a child across the graph.
        (Useful to decide whether closed-form bottom-up evaluation is valid.)
        """
        counts: Dict[NodeId, int] = {}
        for node in self.nodes.values():
            if isinstance(node, Gate):
                for ch in node.inputs:
                    counts[ch] = counts.get(ch, 0) + 1
        return {nid for nid, c in counts.items() if c > 1}

    # -------------------------
    # Expansion layer: dependencies => pure gate/event network => boolean Expr
    # -------------------------

    def to_boolean_expr(self) -> tuple[Expr, dict[str, float], dict[str, bool]]:
        """
        Produces:
          - Expr for the top event
          - variable probabilities for stochastic leaf vars (BasicEvent + latent CCF vars)
          - fixed booleans for house events (if provided)

        Dependency constructs are expanded into additional latent vars and OR injections.
        After expansion, variables are assumed independent (beta model achieves this via latent vars).
        """
        expanded_nodes: Dict[NodeId, Node] = dict(self.nodes)

        # 1) Expand CCF groups into latent + per-member independent vars and member rewrites
        #    member = OR(common, ind_member)
        var_probs: dict[str, float] = {}
        house_values: dict[str, bool] = {}

        def basic_p(be: BasicEvent, mission_time_hours: float | None = None) -> float | None:
            if be.p is not None:
                return be.p
            if be.lambda_rate_per_hour is not None and mission_time_hours is not None:
                # P(fail by t) = 1 - exp(-lambda*t) approximated elsewhere; solvers can compute too.
                # Here we leave None and let solvers compute if they pass mission time into prob map builder.
                return None
            return None

        # We'll build probs later in a solver-aware way; here we only set direct p if present.
        for nid, node in expanded_nodes.items():
            if isinstance(node, BasicEvent) and node.p is not None:
                var_probs[str(nid)] = float(node.p)
            if isinstance(node, HouseEvent) and node.value is not None:
                house_values[str(nid)] = bool(node.value)

        # Helper to compute representative channel prob for beta split
        def member_prob(member_id: NodeId) -> float | None:
            n = expanded_nodes[member_id]
            if isinstance(n, BasicEvent):
                return n.p
            return None

        to_add: Dict[NodeId, Node] = {}
        to_replace: Dict[NodeId, Gate] = {}

        for nid, node in list(expanded_nodes.items()):
            if not isinstance(node, CCFGroup):
                continue

            probs = [p for p in (member_prob(m) for m in node.members) if p is not None]
            q = (sum(probs) / len(probs)) if probs else None  # mean if available

            common_id = NodeId(f"{nid}__ccf_common")
            common_be = BasicEvent(
                id=common_id,
                name=f"{node.name} common cause",
                p=(node.beta * q) if q is not None else None,
            )
            to_add[common_id] = common_be
            if common_be.p is not None:
                var_probs[str(common_id)] = float(common_be.p)

            for m in node.members:
                ind_id = NodeId(f"{nid}__ccf_ind__{m}")
                ind_be = BasicEvent(
                    id=ind_id,
                    name=f"{node.name} independent part for {m}",
                    p=((1.0 - node.beta) * q) if q is not None else None,
                )
                to_add[ind_id] = ind_be
                if ind_be.p is not None:
                    var_probs[str(ind_id)] = float(ind_be.p)

                # Rewrite member as OR(common, ind_member, original_member_if_not_basic?)
                # If the member is a BasicEvent, we replace it with an OR gate producing the member id.
                # If member is not a BasicEvent, we still OR-in the common/ind vars (approximate modeling).
                rewritten = Gate(
                    id=m,
                    name=f"{expanded_nodes[m].__class__.__name__} {m} with CCF({node.name})",
                    gate_type=GateType.OR,
                    inputs=[common_id, ind_id, m],
                )
                # NOTE: This creates a self-reference if we include m itself. So for BasicEvent, replace fully;
                # for non-basic, we OR-in at the *parents* would be better. Keep it simple: only rewrite basics.
                if isinstance(expanded_nodes[m], BasicEvent):
                    rewritten = Gate(
                        id=m,
                        name=f"{expanded_nodes[m].__class__.__name__} {m} with CCF({node.name})",
                        gate_type=GateType.OR,
                        inputs=[common_id, ind_id],
                    )
                    to_replace[m] = rewritten

        expanded_nodes.update(to_add)
        expanded_nodes.update(to_replace)

        # 2) Apply functional dependencies: dependent' = OR(dependent, trigger)
        for nid, node in list(expanded_nodes.items()):
            if not isinstance(node, FunctionalDependency):
                continue
            dep = node.dependent
            trig = node.trigger
            dep_node = expanded_nodes.get(dep)
            # Replace dependent with OR gate if dependent is leaf; if it's a gate already, wrap it.
            if isinstance(dep_node, Gate):
                wrapped = Gate(
                    id=dep,
                    name=f"{dep_node.name} with FDEP({node.name})",
                    gate_type=GateType.OR,
                    inputs=[trig, dep],
                )
                # This would self-reference; instead wrap by cloning original under a new id.
                orig_id = NodeId(f"{dep}__orig_before_fdep__{nid}")
                expanded_nodes[orig_id] = dep_node
                wrapped = Gate(
                    id=dep,
                    name=f"{dep_node.name} with FDEP({node.name})",
                    gate_type=GateType.OR,
                    inputs=[trig, orig_id],
                )
                expanded_nodes[dep] = wrapped
            else:
                expanded_nodes[dep] = Gate(
                    id=dep,
                    name=f"{getattr(dep_node, 'name', str(dep))} with FDEP({node.name})",
                    gate_type=GateType.OR,
                    inputs=[trig, dep],
                )
                # self-ref again; fix by renaming original leaf
                orig_id = NodeId(f"{dep}__orig_before_fdep__{nid}")
                if dep_node is not None:
                    expanded_nodes[orig_id] = dep_node
                expanded_nodes[dep] = Gate(
                    id=dep,
                    name=f"{getattr(dep_node, 'name', str(dep))} with FDEP({node.name})",
                    gate_type=GateType.OR,
                    inputs=[trig, orig_id],
                )

        # 3) Build a Boolean Expr for the top event by recursively translating gates.
        #    Leaves become Vars (BasicEvent/HouseEvent).
        memo: dict[NodeId, Expr] = {}

        def to_expr(nid: NodeId) -> Expr:
            if nid in memo:
                return memo[nid]
            node = expanded_nodes[nid]

            if isinstance(node, BasicEvent) or isinstance(node, HouseEvent):
                e = Var(str(nid))
                memo[nid] = e
                return e

            if isinstance(node, InhibitGate):
                e = And([to_expr(x) for x in node.primary_inputs] + [to_expr(node.condition)])
                memo[nid] = e
                return e

            if isinstance(node, KofNGate):
                # K-of-N not represented directly in Expr. We expand to OR of ANDs.
                # (May explode; OK for baseline.)
                from itertools import combinations

                terms: list[Expr] = []
                for combo in combinations(node.inputs, node.k):
                    terms.append(And([to_expr(x) for x in combo]))
                e = Or(terms) if terms else Const(False)
                memo[nid] = e
                return e

            if isinstance(node, Gate):
                xs = [to_expr(x) for x in node.inputs]
                if node.gate_type == GateType.AND:
                    e = And(xs)
                elif node.gate_type == GateType.OR:
                    e = Or(xs)
                elif node.gate_type == GateType.KOFN:
                    raise ValueError("Use KofNGate class for kofn gates")
                elif node.gate_type == GateType.INHIBIT:
                    raise ValueError("Use InhibitGate class for inhibit gates")
                else:
                    raise ValueError(f"Unknown gate type: {node.gate_type}")
                memo[nid] = e
                return e

            if isinstance(node, CCFGroup) or isinstance(node, FunctionalDependency):
                # Constructs should not be directly referenced as signal nodes.
                # If they are, treat as False.
                e = Const(False)
                memo[nid] = e
                return e

            raise TypeError(f"Unknown node type: {type(node)}")

        top_expr = to_expr(self.top_event_id)
        return top_expr, var_probs, house_values
