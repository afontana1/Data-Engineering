from typing import Any, Callable, Dict, Iterable, List, Mapping, Optional, Protocol


Row = Dict[str, Any]


def coerce_to_dict(item: Any) -> Row:
    """Coerce input objects to dict rows."""
    if isinstance(item, Mapping):
        return dict(item)
    if hasattr(item, "__dict__"):
        return dict(vars(item))
    raise TypeError(f"Cannot coerce object of type {type(item)} to dict")


class Predicate(Protocol):
    def matches(self, row: Row) -> bool:
        ...

class Condition:
    """
    Represents a single field lookup, like:
    - "age"       -> equality
    - "age__lt"   -> less-than
    """

    _OPERATORS: Dict[str, Callable[[Any, Any], bool]] = {
        "eq": lambda a, b: a == b,
        "lt": lambda a, b: a is not None and a < b,
        "lte": lambda a, b: a is not None and a <= b,
        "gt": lambda a, b: a is not None and a > b,
        "gte": lambda a, b: a is not None and a >= b,
        "contains": lambda a, b: a is not None and b in a,
        "icontains": lambda a, b: (
            isinstance(a, str) and isinstance(b, str) and b.lower() in a.lower()
        ),
    }

    def __init__(self, lookup: str, value: Any):
        self.field, self.operator = self._parse_lookup(lookup)
        self.value = value

    @staticmethod
    def _parse_lookup(lookup: str) -> (str, str):
        if "__" in lookup:
            field, op = lookup.split("__", 1)
            return field, op
        return lookup, "eq"

    def matches(self, row: Row) -> bool:
        op_func = self._OPERATORS.get(self.operator)
        if op_func is None:
            raise ValueError(f"Unsupported lookup operator: {self.operator}")
        return op_func(row.get(self.field), self.value)


class Q(Predicate):
    """
    Basic container for AND-ed conditions.

    Example:
        Q(username="alice")
        Q(age__lt=30, is_active=True)

    Use `|` to OR two Q-like predicates:
        expr = Q(username="alice") | Q(owner="PUBLIC")
    """

    def __init__(self, **lookups: Any):
        self._conditions: List[Condition] = [
            Condition(lookup, value) for lookup, value in lookups.items()
        ]

    def matches(self, row: Row) -> bool:
        # AND all conditions by default
        return all(cond.matches(row) for cond in self._conditions)

    def __or__(self, other: Predicate) -> "QOr":
        return QOr(self, other)


class QOr(Predicate):
    """Representation of an OR between two predicates (usually Qs)."""

    def __init__(self, left: Predicate, right: Predicate):
        self.left = left
        self.right = right

    def matches(self, row: Row) -> bool:
        return self.left.matches(row) or self.right.matches(row)


class AndPredicate(Predicate):
    """Composable AND of multiple predicates."""

    def __init__(self, predicates: Iterable[Predicate]):
        self._predicates = list(predicates)

    def matches(self, row: Row) -> bool:
        return all(p.matches(row) for p in self._predicates)

class QuerySet:
    """
    In-memory, SQL-like querying inspired by Django.

    Example:
        qs = QuerySet(data=list_of_dicts)

        # kwargs filtering
        qs2 = qs.filter(is_active=True).order_by("-created_at").limit(10)

        # Q-based filtering
        expr = Q(username=user) | Q(owner="PUBLIC")
        first_match = qs.filter(expr).first()
    """

    def __init__(self, data: Iterable[Any]):
        # Coerce all items to dict rows once
        self._data: List[Row] = [coerce_to_dict(item) for item in data]

        # Query "plan"
        self._predicates: List[Predicate] = []
        self._order_by_fields: List[tuple[str, bool]] = []  # (field, reverse)
        self._limit: Optional[int] = None
        self._offset: int = 0

    def _clone(
        self,
        *,
        predicates: Optional[List[Predicate]] = None,
        order_by_fields: Optional[List[tuple[str, bool]]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> "QuerySet":
        """Return a new QuerySet with updated query plan (immutability for chaining)."""
        new = QuerySet(self._data)
        new._predicates = list(predicates if predicates is not None else self._predicates)
        new._order_by_fields = list(
            order_by_fields if order_by_fields is not None else self._order_by_fields
        )
        new._limit = self._limit if limit is None else limit
        new._offset = self._offset if offset is None else offset
        return new

    def _apply_filters(self, rows: Iterable[Row]) -> Iterable[Row]:
        if not self._predicates:
            return rows

        combined = AndPredicate(self._predicates)

        def generator():
            for row in rows:
                if combined.matches(row):
                    yield row

        return generator()

    def _apply_ordering(self, rows: Iterable[Row]) -> List[Row]:
        if not self._order_by_fields:
            return list(rows)

        items = list(rows)
        # Stable sort: apply from last to first
        for field, reverse in reversed(self._order_by_fields):
            items.sort(key=lambda row: row.get(field), reverse=reverse)
        return items

    def _apply_slice(self, rows: List[Row]) -> List[Row]:
        start = self._offset
        end = None if self._limit is None else start + self._limit
        return rows[start:end]

    def _evaluate(self) -> List[Row]:
        rows = self._apply_filters(self._data)
        rows = self._apply_ordering(rows)
        rows = self._apply_slice(rows)
        return rows

    def filter(self, *expressions: Predicate, **lookups: Any) -> "QuerySet":
        """
        Add filtering conditions.

        Usage:
            qs.filter(is_active=True)
            qs.filter(Q(username="alice") | Q(owner="PUBLIC"))
            qs.filter(Q(is_active=True), username="alice")
        """
        new_predicates = list(self._predicates)

        if lookups:
            new_predicates.append(Q(**lookups))

        for expr in expressions:
            new_predicates.append(expr)

        return self._clone(predicates=new_predicates)

    def order_by(self, *fields: str) -> "QuerySet":
        """
        Define ordering.

        Each field can be:
            "field_name"  -> ascending
            "-field_name" -> descending
        """
        order_spec: List[tuple[str, bool]] = []
        for f in fields:
            if f.startswith("-"):
                order_spec.append((f[1:], True))
            elif f.startswith("+"):
                order_spec.append((f[1:], False))
            else:
                order_spec.append((f, False))
        return self._clone(order_by_fields=order_spec)

    def limit(self, n: int) -> "QuerySet":
        """Limit the number of results."""
        if n is not None and n < 0:
            raise ValueError("limit() expects a non-negative integer or None")
        return self._clone(limit=n)

    def offset(self, n: int) -> "QuerySet":
        """Skip the first n results."""
        if n < 0:
            raise ValueError("offset() expects a non-negative integer")
        return self._clone(offset=n)

    def all(self) -> "QuerySet":
        """
        Return a (shallow) copy of this QuerySet.
        Kept chainable, similar to Django.
        """
        return self._clone()

    def first(self) -> Optional[Row]:
        """Return the first row matching the query, or None if empty."""
        for row in self:
            return row
        return None

    def __iter__(self):
        """Iterate over the evaluated result set."""
        return iter(self._evaluate())

    def __len__(self) -> int:
        return len(self._evaluate())

    def __repr__(self) -> str:
        return f"<QuerySet size={len(self)}>"


if __name__ == "__main__":
    data = [
        {"id": 1, "username": "alice", "age": 30, "owner": "PRIVATE"},
        {"id": 2, "username": "bob", "age": 25, "owner": "PUBLIC"},
        {"id": 3, "username": "alice", "age": 20, "owner": "PUBLIC"},
    ]

    qs = QuerySet(data)

    # Simple kwargs filter + ordering + limit
    young_public = (
        qs.filter(owner="PUBLIC", age__lt=30)
        .order_by("-age")
        .limit(1)
        .first()
    )

    # Q-based OR logic
    expr = Q(username="alice") | Q(owner="PUBLIC")
    results = qs.filter(expr).order_by("id")

    for row in results:
        print(row)
