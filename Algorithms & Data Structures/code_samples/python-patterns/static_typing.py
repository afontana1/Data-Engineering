from __future__ import annotations

from functools import wraps
from typing import Any, Callable, Tuple, Dict


class Staticator:
    """
    A decorator that enforces runtime type checks on function arguments.

    Usage:
        @Staticator(int, int, name=str)
        def foo(x, y, name="bob"):
            ...

    - Positional types are passed as *args to the decorator.
    - Keyword-argument types are passed as **kwargs to the decorator.
    - At call time, the decorator checks that each provided argument matches
      the declared type and raises TypeError otherwise.
    """

    def __init__(self, *pos_types: type, **kw_types: type) -> None:
        """
        Initialize the Staticator with expected types.

        :param pos_types: Expected types for positional arguments, in order.
        :param kw_types: Expected types for keyword arguments, by name.
        """
        self.pos_types: Tuple[type, ...] = pos_types
        self.kw_types: Dict[str, type] = kw_types
        self.func_name: str = "<unknown>"

    def __call__(self, function: Callable[..., Any]) -> Callable[..., Any]:
        """
        Wrap the target function so that calls to it are type-checked.
        """
        self.func_name = function.__name__

        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            self._check_args(args, kwargs)
            return function(*args, **kwargs)

        return wrapper

    def _raise_type_error(self, arg: Any, expected: type) -> None:
        """
        Raise a TypeError with a helpful message.
        """
        raise TypeError(
            f"Incorrect argument {arg!r} - should be of type {expected} "
            f"in call to {self.func_name}()"
        )

    def _check_args(self, args: Tuple[Any, ...], kwargs: Dict[str, Any]) -> None:
        """
        Check both positional and keyword arguments against the expected types.
        """
        # Check positional arguments
        for expected_type, actual_arg in zip(self.pos_types, args):
            if not isinstance(actual_arg, expected_type):
                self._raise_type_error(actual_arg, expected_type)

        # Check keyword arguments
        for key, value in kwargs.items():
            if key not in self.kw_types:
                raise TypeError(
                    f"{self.func_name}() got an unexpected keyword argument {key!r}"
                )
            expected_type = self.kw_types[key]
            if not isinstance(value, expected_type):
                self._raise_type_error(value, expected_type)


if __name__ == "__main__":
    @Staticator(int, int)
    def add(a: int, b: int) -> int:
        """Return the sum of two integers."""
        return a + b

    print(add(2, 3))     # OK
    print(add(2.0, 3))   # Raises TypeError
