from __future__ import annotations

from functools import wraps
from types import FunctionType
from typing import Any, Callable, Dict, Hashable, Tuple, Type


def para_polymorphator_factory() -> Type["ParaPolymorphator"]:
    """
    Factory that creates a per-class decorator/registry object.

    Each produced class keeps:
    - a class-level `methods` dict: {method_name: {signature: function}}
    - instances act as decorators to register a new overload
    """
    class ParaPolymorphator:
        """
        Per-class polymorphator.

        An instance of this class is used as a decorator like:

            @polymorphator(int, int)
            def foo(self, a, b): ...

        and it will register `foo` for the signature (int, int).
        """

        # class-level registry: method_name -> {signature: function}
        methods: Dict[str, Dict[Tuple[Tuple[type, ...], Tuple[Tuple[str, type], ...]], Callable]] = {}

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            """
            Store the registration signature (the types/values given to the decorator).
            For example, @polymorphator(int, int) → registration signature is ((int, int), ())
            """
            self.methods = {}  # instance-level, but we mostly use the class-level dict
            self.signature = self.get_reg_signature(args, kwargs)

        def get_reg_signature(
            self,
            args: Tuple[Any, ...],
            kwargs: Dict[str, Any],
        ) -> Tuple[Tuple[Any, ...], Tuple[Tuple[str, Any], ...]]:
            """
            Signature used at **registration** time (what the decorator saw).

            We keep it as-is (not types) because the original code did so.
            """
            return (tuple(args), tuple(sorted(kwargs.items())))

        def get_run_signature(
            self,
            args: Tuple[Any, ...],
            kwargs: Dict[str, Any],
        ) -> Tuple[Tuple[type, ...], Tuple[Tuple[str, type], ...]]:
            """
            Signature used at **call** time.

            - we drop args[0] (self) because we don't dispatch on the instance
            - we convert values to their types
            """
            arg_types: Tuple[type, ...] = tuple(type(arg) for arg in args[1:])
            kw_types: Tuple[Tuple[str, type], ...] = tuple(
                sorted((name, type(val)) for name, val in kwargs.items())
            )
            return (arg_types, kw_types)

        def __call__(self, method: Callable) -> Callable:
            """
            Actual decorator body.

            Registers the method under the class-level registry for its name and signature,
            then returns a wrapper that does runtime dispatch.
            """
            name = method.__name__
            cls_methods = self.__class__.methods

            # register the method for this signature
            if name not in cls_methods:
                cls_methods[name] = {self.signature: method}
            else:
                cls_methods[name][self.signature] = method

            @wraps(method)
            def new_function(*args: Any, **kwargs: Any) -> Any:
                signature = self.get_run_signature(args, kwargs)
                try:
                    impl = cls_methods[name][signature]
                except KeyError as exc:
                    raise TypeError(
                        f"No method '{name}' registered for signature {signature}"
                    ) from exc
                return impl(*args, **kwargs)

            # marker so the metaclass knows “this method was polymorphed”
            new_function.polymorphed = True  # type: ignore[attr-defined]
            return new_function

    return ParaPolymorphator


class Polymorphator:
    """
    Front object users decorate with: `@polymorphator(...)`.

    It keeps:
    - a global dict of class-name → polymorphator-for-that-class
    - a “current” polymorphator that is active while we define a class
    """
    polymorphators: Dict[str, Any] = {}

    def __init__(self) -> None:
        # lazily create the first current polymorphator
        if not hasattr(self.__class__, "current_polymorphator"):
            self.__class__.current_polymorphator = para_polymorphator_factory()

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """
        When you write @polymorphator(...), this forwards to the current class's
        para-polymorphator instance.
        """
        return self.__class__.current_polymorphator(*args, **kwargs)

    @classmethod
    def commit_class(cls, class_name: str) -> None:
        """
        Called by the metaclass when a class finishes being defined.

        We “seal” the polymorphator used during that class definition under the class name,
        and create a new one for the next class.
        """
        cls.polymorphators[class_name] = cls.current_polymorphator
        cls.current_polymorphator = para_polymorphator_factory()


class MetaPolymorphator(type):
    """
    Metaclass that:
    1. tells Polymorphator “we just finished class X, save its registry”
    2. merges polymorphed methods from base classes into the new class
    """
    def __new__(
        mcls,
        name: str,
        bases: Tuple[type, ...],
        namespace: Dict[str, Any],
    ):
        # finalize the previous “current” class's polymorphator
        Polymorphator.commit_class(name)

        # create the class first
        cls = super().__new__(mcls, name, bases, namespace)

        function_type = FunctionType

        # for every function defined on this class that is a polymorphed wrapper,
        # copy in the base-class overloads of the same name
        for key, value in namespace.items():
            if isinstance(value, function_type) and hasattr(value, "polymorphed"):
                base_homonymous: Dict[Hashable, Callable] = {}

                # NOTE: original code did not do full MRO recursion; we keep behavior
                for base in reversed(bases):
                    base_name = base.__name__
                    if base_name in Polymorphator.polymorphators:
                        base_methods = Polymorphator.polymorphators[base_name].methods
                        if key in base_methods:
                            # base_methods[key] is: {signature: function}
                            base_homonymous.update(base_methods[key])

                # now merge these into THIS class's registry
                Polymorphator.polymorphators[name].methods.setdefault(key, {})
                Polymorphator.polymorphators[name].methods[key].update(base_homonymous)

        return cls


# this is the decorator users will actually write
polymorphator = Polymorphator()


class PolymorphicBase(metaclass=MetaPolymorphator):
    """
    Base class that activates the metaclass.
    Any class that wants polymorphic methods should inherit from this.
    """
    pass


# ===== Example usage / tests =====

class A(PolymorphicBase):
    @polymorphator(int, int)
    def sum(self, a: int, b: int) -> None:
        """Add two ints and print the result."""
        print(f"The sum of {a} and {b} is: {a + b}")

    @polymorphator(str, str)
    def sum(self, a: str, b: str) -> None:  # type: ignore[no-redef]
        """Concatenate two strings and print the result."""
        print(f"The concatenation of {a} and {b} is: {a} - {b}")


class B(PolymorphicBase):
    @polymorphator(float, float)
    def sum(self, a: float, b: float) -> None:
        """Add two floats and print the result."""
        print(f"The sum of {a} and {b} is: {a + b}")


class C(A):
    @polymorphator(complex, complex)
    def sum(self, a: complex, b: complex) -> None:  # type: ignore[no-redef]
        """Add two complex numbers and print the result."""
        print(f"The sum of complex {a} and {b} is: {a + b}")


if __name__ == "__main__":
    a = A()
    a.sum(2, 3)
    a.sum("apple", "orange")

    b = B()
    b.sum(2.5, 3.1)
    try:
        b.sum(2, 3)  # no (int, int) in B
    except TypeError as error:
        print(f"Properly raised TypeError: {error}")

    c = C()
    c.sum(1 + 1j, -1j)  # complex
    c.sum(4, 8)         # inherited (int, int) from A
    try:
        c.sum(2.1, 3.1)  # no (float, float) in C (and C doesn't inherit from B)
    except TypeError as error:
        print(f"Properly raised TypeError: {error}")
