from __future__ import annotations

import sys
import types
from typing import Any, Callable, Dict, Iterable, List, Optional, Type, TypeVar

T = TypeVar("T")


class PrivateAttributeError(AttributeError):
    """Raised when a private attribute is accessed from an unauthorized caller."""
    pass


def check_caller(obj: Any, level: int) -> None:
    """
    Verify that the caller at the given stack level is:
    1. A function that has the instance `obj` in its local variables, and
    2. That function is one of the original methods defined on the instance's class.

    This is the core of the "privacy" mechanism: only real methods of the class
    (not dynamically added ones, not outside code) may touch private attributes.

    Parameters
    ----------
    obj:
        The instance whose private data is being accessed.
    level:
        How many frames to go up from here to find the caller.
        This depends on who calls `check_caller` (descriptor, dict, etc.).
    """
    frame = sys._getframe(level)
    cls = type(obj)

    # 1) The instance must appear in the caller's local variables
    if obj not in frame.f_locals.values():
        raise PrivateAttributeError("Instance not found in caller's locals.")

    # 2) The caller's code object must match one of the class's function code objects
    caller_code = frame.f_code

    for attr_name, maybe_func in cls.__dict__.items():
        if isinstance(maybe_func, types.FunctionType):
            if maybe_func.__code__ is caller_code:
                # Found a class method that matches the caller
                break
    else:
        # If we didn't break, no method matched
        raise PrivateAttributeError("Caller is not an original method of the class.")


class PrivateAttribute:
    """
    Descriptor that represents a truly private attribute.

    The actual value is stored in the instance's `__privdict__`, and every access
    is guarded by a frame check to ensure it is being used from an authorized method.
    """

    def __init__(self, name: str) -> None:
        self.name = name

    def __get__(self, obj: Any, owner: Optional[Type[Any]] = None) -> Any:
        if obj is None:
            # Accessed through the class, return the descriptor itself
            return self
        # Caller should be 2 frames up: user-code -> descriptor -> check
        check_caller(obj, 2)
        try:
            return obj.__privdict__[self.name]
        except KeyError as exc:
            raise AttributeError(f"Private attribute '{self.name}' not set") from exc

    def __set__(self, obj: Any, value: Any) -> None:
        # Caller should be 2 frames up
        check_caller(obj, 2)
        obj.__privdict__[self.name] = value

    def __delete__(self, obj: Any) -> None:
        # Caller should be 2 frames up
        check_caller(obj, 2)
        try:
            del obj.__privdict__[self.name]
        except KeyError as exc:
            raise AttributeError(f"Private attribute '{self.name}' not set") from exc


class PrivateDict:
    """
    A dictionary-like object used to store private attributes.

    Every access to this storage is also guarded. Even if someone discovers
    `instance.__privdict__`, they still can’t easily read or write it without
    coming from the right frame.
    """

    __slots__ = ["owner", "dic"]

    def __init__(self, owner: Any) -> None:
        # We must bypass our own __setattr__ guard to set these two
        object.__setattr__(self, "owner", owner)
        object.__setattr__(self, "dic", {})  # type: ignore[call-arg]

    def __setitem__(self, key: str, value: Any) -> None:
        # Caller is farther up the stack: caller -> descriptor -> privdict -> here
        check_caller(self.owner, 3)
        self.dic[key] = value  # type: ignore[attr-defined]

    def __getitem__(self, key: str) -> Any:
        check_caller(self.owner, 3)
        return self.dic[key]  # type: ignore[attr-defined]

    def __getattribute__(self, name: str) -> Any:
        """
        Even attribute access on the storage is guarded.

        We allow access only if the caller is legitimate. Then we delegate
        to the normal object attribute access.
        """
        # Caller: user -> privdict attr -> here
        # We want to protect *some* attribute reads too.
        check_caller(object.__getattribute__(self, "owner"), 2)
        return object.__getattribute__(self, name)

    def __setattr__(self, name: str, value: Any) -> None:
        """
        Guard setting attributes on the storage object itself.

        We still allow internal setup via object.__setattr__ in __init__.
        """
        check_caller(object.__getattribute__(self, "owner"), 2)
        object.__setattr__(self, name, value)


class EnablePrivate(type):
    """
    Metaclass that injects a guarded private storage (`__privdict__`) into
    every instance created from a class that uses this metaclass.
    """

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        # Standard instance creation dance
        new_obj = cls.__new__(cls, *args, **kwargs)
        # Attach the guarded private dict
        new_obj.__privdict__ = PrivateDict(new_obj)  # type: ignore[attr-defined]
        # Run the instance initializer
        cls.__init__(new_obj, *args, **kwargs)
        return new_obj


def private(*attr_names: str) -> Callable[[str, tuple[type, ...], dict[str, Any]], type]:
    """
    Convenience factory for declaring private attributes on a class.

    Usage
    -----
    class MyClass(metaclass=private("foo", "bar")):
        ...

    The returned callable acts like a metaclass factory: it injects the
    private descriptors into the class dict, then creates the class using
    `EnablePrivate`.
    """
    # Build the descriptors for the given private attribute names
    private_attrs: Dict[str, PrivateAttribute] = {
        name: PrivateAttribute(name) for name in attr_names
    }

    def metaclass_factory(
        name: str,
        bases: tuple[type, ...],
        ns: dict[str, Any],
    ) -> type:
        # Add our private descriptors to the class namespace
        ns.update(private_attrs)

        # Optionally record original methods (like the original code did)
        methods: List[str] = [
            key for key, value in ns.items() if isinstance(value, types.FunctionType)
        ]
        ns["__original_methods__"] = methods

        # Now actually create the class with our metaclass
        return EnablePrivate(name, bases, ns)

    return metaclass_factory


# ---------------------------------------------------------------------------
# Example / test usage
# ---------------------------------------------------------------------------

class Test(metaclass=private("foo", "bar")):
    """
    Example class that declares two private attributes: 'foo' and 'bar'.

    These attributes can only be accessed from methods defined on this class
    at class-definition time.
    """

    def __init__(self) -> None:
        # This is allowed, we're inside a real method
        self.foo = None
        self.bar = None
        # This one is normal
        self.wow = None

    def set_foo(self, value: str) -> None:
        """Set the private attribute 'foo', and also update 'bar'."""
        self.foo = value
        self.bar = "and I am bar"

    def get_foo(self) -> str:
        """Return the private attribute 'foo'."""
        return self.foo  # type: ignore[return-value]


def testit() -> None:
    """
    Run a sequence of checks to show what is allowed and what is blocked.
    This mirrors the original Python 2 example, updated for Python 3.
    """
    o = Test()
    a = Test()

    # allowed: internal methods
    o.set_foo("I am foo in o")
    a.set_foo("I am foo in a")

    # getter works
    try:
        print("Testing getter: ", end="")
        assert o.get_foo() == "I am foo in o"
        assert a.get_foo() == "I am foo in a"
        print("OK")
    except PrivateAttributeError as exc:
        print("FAIL", exc)

    # direct access should fail
    try:
        print("Testing direct access to get: ", end="")
        _ = o.foo  # type: ignore[attr-defined]
        _ = a.foo  # type: ignore[attr-defined]
        print("ERROR (should have failed)")
    except PrivateAttributeError:
        print("OK")

    # direct set should fail
    try:
        print("Testing direct access to set: ", end="")
        o.foo = "nope"  # type: ignore[attr-defined]
        a.foo = "nope"  # type: ignore[attr-defined]
        print("ERROR (should have failed)")
    except PrivateAttributeError:
        print("OK")

    # accessing via object.__getattribute__ should also fail
    try:
        print("Testing with object.__getattribute__: ", end="")
        _ = object.__getattribute__(o, "foo")
        _ = object.__getattribute__(a, "foo")
        print("ERROR (should have failed)")
    except PrivateAttributeError:
        print("OK")

    # same for object.__setattr__
    try:
        print("Testing with object.__setattr__: ", end="")
        object.__setattr__(o, "foo", "nope")
        object.__setattr__(a, "foo", "nope")
        print("ERROR (should have failed)")
    except PrivateAttributeError:
        print("OK")

    # __dict__ should not contain 'foo' because it's a descriptor on the class
    try:
        print("Testing with __dict__: ", end="")
        _ = o.__dict__["foo"]
        print("ERROR (should have failed)")
    except KeyError:
        print("OK")

    # dynamically added method should fail
    def getfoo(self: Test) -> str:
        return self.foo  # type: ignore[attr-defined]

    try:
        print("Testing with dynamically added getter: ", end="")
        Test.getfoo = getfoo  # type: ignore[method-assign]
        _ = o.getfoo()
        print("ERROR (should have failed)")
    except PrivateAttributeError:
        print("OK")

    # try to reach __privdict__ directly
    try:
        print("Testing with __privdict__: ", end="")
        _ = o.__privdict__["foo"]
        _ = a.__privdict__["foo"]
        print("ERROR (should have failed)")
    except PrivateAttributeError:
        print("OK")

    # even object.__getattribute__ on __privdict__.dic should fail
    try:
        print("Testing with object.__getattribute__ and __privdict__: ", end="")
        _ = object.__getattribute__(o.__privdict__, "dic")["foo"]
        _ = object.__getattribute__(a.__privdict__, "dic")["foo"]
        print("ERROR (should have failed)")
    except PrivateAttributeError:
        print("OK")


if __name__ == "__main__":
    testit()
