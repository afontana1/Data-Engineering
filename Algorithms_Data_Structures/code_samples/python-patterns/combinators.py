from __future__ import annotations

import asyncio
from typing import Any, Awaitable, Callable, Iterable, List, TypeVar

T = TypeVar("T")
U = TypeVar("U")

# ------------------------
# Basic function combinators
# ------------------------

def identity(x: T) -> T:
    return x

def compose(*fns: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """
    compose(f, g, h)(x) == f(g(h(x)))
    (right-to-left)
    """
    def composed(x: Any) -> Any:
        for f in reversed(fns):
            x = f(x)
        return x
    return composed

def pipe(x: Any, *fns: Callable[[Any], Any]) -> Any:
    """
    pipe(x, f, g, h) == h(g(f(x)))
    (left-to-right)
    """
    for f in fns:
        x = f(x)
    return x

def and_(p: Callable[[T], bool], q: Callable[[T], bool]) -> Callable[[T], bool]:
    """Predicate AND combinator."""
    return lambda x: p(x) and q(x)

def or_(p: Callable[[T], bool], q: Callable[[T], bool]) -> Callable[[T], bool]:
    """Predicate OR combinator."""
    return lambda x: p(x) or q(x)

# ------------------------
# "Monad" combinators for Awaitable (Promise-like)
# ------------------------

async def async_of(value: T) -> T:
    """Monad 'pure' / 'of' for the Awaitable monad."""
    return value

async def async_map(fn: Callable[[T], U], aw: Awaitable[T]) -> U:
    """
    fmap / map :: (a -> b) -> Awaitable a -> Awaitable b
    """
    return fn(await aw)

async def async_chain(fn: Callable[[T], Awaitable[U]], aw: Awaitable[T]) -> U:
    """
    chain / bind :: (a -> Awaitable b) -> Awaitable a -> Awaitable b
    """
    return await fn(await aw)

# For naming similar to many FP libs:
chain = async_chain

# ------------------------
# Monoid helper
# ------------------------

def fold_monoid(
    identity_value: T,
    op: Callable[[T, U], T],
    values: Iterable[U],
) -> T:
    """
    Generic monoid fold:
    - identity_value is mempty
    - op is mappend
    """
    acc = identity_value
    for v in values:
        acc = op(acc, v)
    return acc

# ------------------------
# Monadic sequence (Awaitable[T]^n -> Awaitable[List[T]])
# Shows monad + list-monoid pattern
# ------------------------

async def sequence(awaitables: Iterable[Awaitable[T]]) -> List[T]:
    """
    Sequential version of Promise.all, just to show the shape:

    - monad: Awaitable
    - monoid: list (mempty = [], mappend = +)
    """
    results: List[T] = []

    async def step(acc: List[T], nxt: Awaitable[T]) -> List[T]:
        v = await nxt
        # List is a monoid: [] is identity, + is associative
        return acc + [v]

    for aw in awaitables:
        results = await step(results, aw)
    return results

# ------------------------
# Promise.all-ish using combinators
# ------------------------

async def promise_all(awaitables: Iterable[Awaitable[T]]) -> List[T]:
    """
    Parallel version, close to JS Promise.all:

    - starts all awaitables at once
    - fails fast if any awaitable raises
    - returns a list of results in original order
    """
    tasks = [asyncio.create_task(a) for a in awaitables]

    try:
        # Same *shape* as sequence (Awaitable^n -> Awaitable[List]),
        # but implemented via asyncio.gather for parallelism.
        results = await asyncio.gather(*tasks)
        return list(results)
    finally:
        # Best-effort cleanup if we exited with an error
        for t in tasks:
            if not t.done():
                t.cancel()

# ------------------------
# Promise.race-ish using combinators
# ------------------------

async def promise_race(awaitables: Iterable[Awaitable[T]]) -> T:
    """
    Rough Promise.race equivalent:

    - returns / raises with the first awaitable to complete
    - cancels the others

    (Conceptually: this is a 'first to settle' combinator;
     in FP land you can think of it as a 'First' monoid over
     completion times.)
    """
    tasks = [asyncio.create_task(a) for a in awaitables]

    done, pending = await asyncio.wait(
        tasks,
        return_when=asyncio.FIRST_COMPLETED,
    )

    # There will be at least one in 'done'
    winner = next(iter(done))

    # Cancel everything else
    for t in pending:
        t.cancel()

    # Propagate result or exception
    return await winner

# ------------------------
# Tiny demo
# ------------------------

async def delay(value: T, ms: int) -> T:
    await asyncio.sleep(ms / 1000)
    return value

async def demo():
    # --- basic combinators ---
    inc = lambda x: x + 1
    double = lambda x: x * 2
    is_even = lambda x: x % 2 == 0
    is_positive = lambda x: x > 0

    f = compose(inc, double)   # inc(double(x))
    g = pipe(3, double, inc)   # passes value through the pipeline

    print("compose(3):", f(3))    # 7
    print("pipe(3, double, inc):", g)  # 7

    is_pos_even = and_(is_even, is_positive)
    print("is_pos_even(4):", is_pos_even(4))     # True
    print("is_pos_even(-2):", is_pos_even(-2))   # False

    # --- monad combinators on Awaitable ---
    async_value = async_of(10)
    mapped = await async_map(lambda x: x * 3, async_value)
    print("async_map *3:", mapped)  # 30

    chained = await chain(lambda x: async_of(x * 5), async_value)
    print("async_chain *5:", chained)  # 50

    # --- Promise.all-style ---
    all_results = await promise_all([
        delay("A", 100),
        delay("B", 50),
        delay("C", 10),
    ])
    print("promise_all:", all_results)  # ['A', 'B', 'C'] (order preserved)

    # --- Promise.race-style ---
    winner = await promise_race([
        delay("slow", 200),
        delay("fast", 50),
    ])
    print("promise_race winner:", winner)  # 'fast'

if __name__ == "__main__":
    asyncio.run(demo())
