import pytest

from collatz.core import (
    collatz_scan_range,
    collatz_sequence,
    collatz_step,
)


def test_collatz_step_even_and_odd():
    assert collatz_step(6) == 3
    assert collatz_step(7) == 22


def test_collatz_sequence_reaches_one():
    result = collatz_sequence(7)
    assert result.reached_one is True
    assert result.iterations == 16
    assert result.sequence[0] == 7
    assert result.sequence[-1] == 1


def test_collatz_sequence_max_steps_limits_iterations():
    result = collatz_sequence(7, max_steps=5)
    assert result.iterations == 5
    assert result.reached_one is False
    assert len(result.sequence) == 6  # start + 5 steps


def test_collatz_scan_range_multiple_numbers():
    results = collatz_scan_range(1, count=3)
    assert [r.start for r in results] == [1, 2, 3]
    assert results[0].reached_one is True
    assert results[1].iterations > 0
    assert results[2].last_value == 1


def test_collatz_step_rejects_non_positive():
    with pytest.raises(ValueError):
        collatz_step(0)
