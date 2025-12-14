import asyncio

from app.life.engine import run_simulation
from app.life.patterns import get_pattern
from app.life.schemas import SimulationConfig


def _collect_states(config: SimulationConfig):
    pattern = get_pattern(name=config.pattern, size_hint=max(config.width, config.height))
    states = []

    async def _collect():
        async for state in run_simulation(config, pattern):
            states.append(set(tuple(cell) for cell in state.alive))

    asyncio.run(_collect())
    return states


def test_block_stays_stable():
    config = SimulationConfig(
        width=4,
        height=4,
        generations=3,
        delay_ms=0,
        pattern="Block",
        wrap=False,
    )
    seen = _collect_states(config)

    assert len(seen) == 4  # initial + 3 generations
    # All generations should match the stable block
    assert all(gen == seen[0] for gen in seen)


def test_blinker_oscillates():
    config = SimulationConfig(
        width=5,
        height=5,
        generations=2,
        delay_ms=0,
        pattern="Blinker",
        wrap=False,
    )
    states = _collect_states(config)

    assert len(states) == 3  # initial + 2 generations
    gen0, gen1, gen2 = states

    expected_gen0 = {(2, 1), (2, 2), (2, 3)}  # centered horizontally
    expected_gen1 = {(1, 2), (2, 2), (3, 2)}  # vertical after one step

    assert gen0 == expected_gen0
    assert gen1 == expected_gen1
    assert gen2 == expected_gen0  # oscillates back
