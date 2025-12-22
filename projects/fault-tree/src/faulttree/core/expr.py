from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence


class Expr:
    pass


@dataclass(frozen=True)
class Var(Expr):
    name: str


@dataclass(frozen=True)
class Not(Expr):
    x: Expr


@dataclass(frozen=True)
class And(Expr):
    xs: Sequence[Expr]


@dataclass(frozen=True)
class Or(Expr):
    xs: Sequence[Expr]


@dataclass(frozen=True)
class Const(Expr):
    value: bool


def eval_expr(expr: Expr, env: Mapping[str, bool]) -> bool:
    if isinstance(expr, Const):
        return expr.value
    if isinstance(expr, Var):
        return bool(env[expr.name])
    if isinstance(expr, Not):
        return not eval_expr(expr.x, env)
    if isinstance(expr, And):
        return all(eval_expr(x, env) for x in expr.xs)
    if isinstance(expr, Or):
        return any(eval_expr(x, env) for x in expr.xs)
    raise TypeError(f"Unknown expr type: {type(expr)}")
