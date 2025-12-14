from __future__ import annotations

import re
from typing import Any, Callable, Dict, List, Sequence, Tuple, Type, TypedDict, Optional


class AspectRule(TypedDict, total=False):
    """
    Structure that holds a single aspect rule.
    """
    name_pattern: str
    in_objects: Tuple[Type[Any], ...]
    out_objects: Tuple[Type[Any], ...]
    pre: Callable[..., Any]
    post: Callable[..., Any]


class Aspecter(type):
    """
    Metaclass used by classes that want aspect-oriented method wrapping.

    Every callable defined on the class is wrapped so that, on call, the
    framework can check if there are registered aspect rules that apply
    (by method name and/or argument/return types) and run pre/post functions.
    """

    aspect_rules: List[AspectRule] = []

    def __new__(cls, name: str, bases: Tuple[type, ...], namespace: Dict[str, Any]) -> "Aspecter":
        """
        When a class using this metaclass is created, wrap all its callable
        attributes so we can inject pre/post behavior later.
        """
        new_namespace: Dict[str, Any] = {}
        for key, value in namespace.items():
            if callable(value) and key != "__metaclass__":
                new_namespace[key] = cls.wrap_method(value)
            else:
                new_namespace[key] = value
        return super().__new__(cls, name, bases, new_namespace)

    @classmethod
    def register(
        cls,
        name_pattern: str = "",
        in_objects: Sequence[Type[Any]] = (),
        out_objects: Sequence[Type[Any]] = (),
        pre_function: Optional[Callable[..., Any]] = None,
        post_function: Optional[Callable[..., Any]] = None,
    ) -> None:
        """
        Register a new aspect rule.

        - name_pattern: regex that will be matched against the method name.
                        If empty, matches all methods.
        - in_objects: sequence of types. If any argument is instance of one of these,
                      the rule applies (for pre functions).
        - out_objects: sequence of types. If the return value is instance of one of these,
                       the rule applies (for post functions).
        - pre_function: function to run before the actual method.
        - post_function: function to run after the actual method.

        Rules can be registered at runtime.
        """
        rule: AspectRule = {
            "name_pattern": name_pattern,
            "in_objects": tuple(in_objects),
            "out_objects": tuple(out_objects),
        }
        if pre_function is not None:
            rule["pre"] = pre_function
        if post_function is not None:
            rule["post"] = post_function
        cls.aspect_rules.append(rule)

    @classmethod
    def wrap_method(cls, method: Callable[..., Any]) -> Callable[..., Any]:
        """
        Return a callable that, when invoked, will:
        1. run all matching pre-functions
        2. run the original method
        3. run all matching post-functions
        """
        def call(*args: Any, **kwargs: Any) -> Any:
            pre_functions = cls.matching_pre_functions(method, args, kwargs)
            for function in pre_functions:
                function(*args, **kwargs)

            result = method(*args, **kwargs)

            post_functions = cls.matching_post_functions(method, result)
            for function in post_functions:
                function(result, *args, **kwargs)

            return result

        # Keep method metadata if you like
        call.__name__ = method.__name__
        call.__doc__ = method.__doc__
        return call

    @classmethod
    def matching_names(cls, method: Callable[..., Any]) -> List[AspectRule]:
        """
        Return all rules whose name_pattern matches this method's name,
        or where the pattern is empty.
        """
        method_name = method.__name__
        return [
            rule
            for rule in cls.aspect_rules
            if rule.get("name_pattern") == "" or re.match(rule["name_pattern"], method_name)
        ]

    @classmethod
    def matching_pre_functions(
        cls,
        method: Callable[..., Any],
        args: Tuple[Any, ...],
        kwargs: Dict[str, Any],
    ) -> List[Callable[..., Any]]:
        """
        From all matching-by-name rules, return the pre-functions whose
        in_objects constraint (if any) is satisfied by the current arguments.
        """
        all_args = args + tuple(kwargs.values())
        functions: List[Callable[..., Any]] = []
        for rule in cls.matching_names(method):
            pre = rule.get("pre")
            in_objects = rule.get("in_objects", ())
            if pre is None:
                continue
            if not in_objects:
                # no type constraint, always applies
                functions.append(pre)
            else:
                if any(isinstance(arg, in_objects) for arg in all_args):
                    functions.append(pre)
        return functions

    @classmethod
    def matching_post_functions(
        cls,
        method: Callable[..., Any],
        result: Any,
    ) -> List[Callable[..., Any]]:
        """
        From all matching-by-name rules, return the post-functions whose
        out_objects constraint (if any) is satisfied by the result.
        """
        results: Tuple[Any, ...]
        if isinstance(result, tuple):
            results = result
        else:
            results = (result,)

        functions: List[Callable[..., Any]] = []
        for rule in cls.matching_names(method):
            post = rule.get("post")
            out_objects = rule.get("out_objects", ())
            if post is None:
                continue
            if not out_objects:
                # no type constraint, always applies
                functions.append(post)
            else:
                if any(isinstance(r, out_objects) for r in results):
                    functions.append(post)
        return functions


if __name__ == "__main__":
    # Demo / testing

    class Address:
        def __repr__(self) -> str:
            return "Address(...)"

    class Person(metaclass=Aspecter):
        def update_address(self, address: Address) -> None:
            # pretend to update some state
            pass

        def __str__(self) -> str:
            return "person object"

    def log_update(*args: Any, **kwargs: Any) -> None:
        print(f"Updating object {args[0]}")

    def log_address(*args: Any, **kwargs: Any) -> None:
        all_args = list(args) + list(kwargs.values())
        addresses = [arg for arg in all_args if isinstance(arg, Address)]
        print(addresses)

    # 1) any method whose name starts with "update" → run log_update before
    Aspecter.register(name_pattern=r"^update.*", pre_function=log_update)

    # 2) any method that receives an Address instance → run log_address before
    Aspecter.register(in_objects=(Address,), pre_function=log_address)

    p = Person()
    p.update_address(Address())