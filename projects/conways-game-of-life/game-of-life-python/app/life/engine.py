"""Core Game of Life logic and async streaming helpers."""
from __future__ import annotations

import asyncio
from typing import AsyncIterator, Dict, Iterable, Set, Tuple

from .patterns import Pattern
from .schemas import GenerationState, SimulationConfig

Coord = Tuple[int, int]
NeighborCounts = Dict[Coord, int]


def _wrap_coord(value: int, limit: int) -> int:
    return value % limit


def _valid(value: int, limit: int) -> bool:
    return 0 <= value < limit


def _neighbor_positions(y: int, x: int) -> Iterable[Tuple[int, int]]:
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dy == 0 and dx == 0:
                continue
            yield y + dy, x + dx


def _count_neighbors(
    alive: Set[Coord], width: int, height: int, wrap: bool
) -> NeighborCounts:
    counts: NeighborCounts = {}
    for y, x in alive:
        for ny, nx in _neighbor_positions(y, x):
            if wrap:
                ny = _wrap_coord(ny, height)
                nx = _wrap_coord(nx, width)
            elif not (_valid(ny, height) and _valid(nx, width)):
                continue

            counts[(ny, nx)] = counts.get((ny, nx), 0) + 1
    return counts


def _step(alive: Set[Coord], width: int, height: int, wrap: bool) -> Set[Coord]:
    counts = _count_neighbors(alive, width, height, wrap)
    next_alive: Set[Coord] = set()
    for cell, count in counts.items():
        if count == 3 or (count == 2 and cell in alive):
            next_alive.add(cell)
    return next_alive


def _center_pattern(alive: Set[Coord], width: int, height: int) -> Set[Coord]:
    if not alive:
        return set()
    min_y = min(y for y, _ in alive)
    min_x = min(x for _, x in alive)
    max_y = max(y for y, _ in alive)
    max_x = max(x for _, x in alive)

    offset_y = max((height - (max_y - min_y + 1)) // 2, 0) - min_y
    offset_x = max((width - (max_x - min_x + 1)) // 2, 0) - min_x

    centered = {
        (y + offset_y, x + offset_x)
        for y, x in alive
        if 0 <= y + offset_y < height and 0 <= x + offset_x < width
    }
    return centered


async def run_simulation(
    config: SimulationConfig, pattern: Pattern
) -> AsyncIterator[GenerationState]:
    width = config.width
    height = config.height

    alive: Set[Coord] = _center_pattern(set(pattern.alive_cells), width, height)
    generation = 0

    yield GenerationState(
        generation=generation, width=width, height=height, alive=sorted(alive)
    )

    limit = config.generations
    delay = config.delay_ms / 1000

    while limit is None or generation < limit:
        generation += 1
        alive = _step(alive, width, height, config.wrap)
        yield GenerationState(
            generation=generation, width=width, height=height, alive=sorted(alive)
        )
        if delay:
            await asyncio.sleep(delay)
