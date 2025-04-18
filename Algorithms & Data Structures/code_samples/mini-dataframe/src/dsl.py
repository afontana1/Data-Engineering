# my_dataframe/dsl.py

import ast
import operator


class QueryDSL:
    ops = {
        ast.Eq: operator.eq,
        ast.NotEq: operator.ne,
        ast.Gt: operator.gt,
        ast.Lt: operator.lt,
        ast.GtE: operator.ge,
        ast.LtE: operator.le,
        ast.And: operator.and_,
        ast.Or: operator.or_,
    }

    @classmethod
    def build_filter(cls, expr):
        tree = ast.parse(expr, mode="eval")
        return cls._compile_expr(tree.body)

    @classmethod
    def _compile_expr(cls, node):
        if isinstance(node, ast.BoolOp):
            op = cls.ops[type(node.op)]
            values = [cls._compile_expr(v) for v in node.values]
            return lambda row: cls._fold(op, values, row)
        elif isinstance(node, ast.Compare):
            left = cls._compile_operand(node.left)
            right = cls._compile_operand(node.comparators[0])
            op = cls.ops[type(node.ops[0])]
            return lambda row: op(left(row), right(row))
        else:
            raise ValueError(f"Unsupported expression: {ast.dump(node)}")

    @classmethod
    def _compile_operand(cls, node):
        if isinstance(node, ast.Name):
            return lambda row: row[node.id]
        elif isinstance(node, ast.Constant):
            return lambda row: node.value
        elif isinstance(node, ast.Str):  # For Python < 3.8
            return lambda row: node.s
        else:
            raise ValueError(f"Unsupported operand: {ast.dump(node)}")

    @classmethod
    def _fold(cls, op, funcs, row):
        result = funcs[0](row)
        for func in funcs[1:]:
            result = op(result, func(row))
        return result
