from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SequenceResult:
    start: int
    sequence: List[int]
    iterations: int
    reached_one: bool

    @property
    def last_value(self) -> int:
        return self.sequence[-1]

    def as_dict(self) -> dict:
        return {
            "start": self.start,
            "sequence": self.sequence,
            "iterations": self.iterations,
            "reached_one": self.reached_one,
            "last_value": self.last_value,
        }


@dataclass
class ScanResult:
    start: int
    iterations: int
    reached_one: bool
    last_value: int

    def as_dict(self) -> dict:
        return {
            "start": self.start,
            "iterations": self.iterations,
            "reached_one": self.reached_one,
            "last_value": self.last_value,
        }


def collatz_step(n: int) -> int:
    """
    Compute the next Collatz number.

    Args:
        n: A positive integer.

    Returns:
        The next number in the sequence.

    Raises:
        ValueError: If n is not a positive integer.
    """
    if n < 1:
        raise ValueError("start must be a positive integer")
    return n // 2 if n % 2 == 0 else n * 3 + 1


def collatz_sequence(start: int, max_steps: Optional[int] = None) -> SequenceResult:
    """
    Generate a Collatz sequence starting from `start`.

    Args:
        start: Positive integer starting value.
        max_steps: Optional cap on the number of steps (iterations) to compute.

    Returns:
        SequenceResult containing the sequence and metadata.

    Raises:
        ValueError: If inputs are invalid.
    """
    if start < 1:
        raise ValueError("start must be a positive integer")
    if max_steps is not None and max_steps < 1:
        raise ValueError("max_steps must be a positive integer when provided")

    sequence = [start]
    current = start
    iterations = 0

    while current != 1:
        if max_steps is not None and iterations >= max_steps:
            break

        current = collatz_step(current)
        sequence.append(current)
        iterations += 1

    reached_one = current == 1

    return SequenceResult(
        start=start,
        sequence=sequence,
        iterations=iterations,
        reached_one=reached_one,
    )


def collatz_scan_range(
    start: int, count: int, max_steps: Optional[int] = None
) -> List[ScanResult]:
    """
    Compute Collatz metadata for a range of starting numbers.

    Args:
        start: First starting number (positive integer).
        count: How many consecutive starting numbers to evaluate.
        max_steps: Optional iteration cap per number.

    Returns:
        List of ScanResult objects.

    Raises:
        ValueError: If inputs are invalid.
    """
    if start < 1:
        raise ValueError("start must be a positive integer")
    if count < 1:
        raise ValueError("count must be a positive integer")
    if max_steps is not None and max_steps < 1:
        raise ValueError("max_steps must be a positive integer when provided")

    results: List[ScanResult] = []
    for n in range(start, start + count):
        seq_result = collatz_sequence(n, max_steps=max_steps)
        results.append(
            ScanResult(
                start=n,
                iterations=seq_result.iterations,
                reached_one=seq_result.reached_one,
                last_value=seq_result.last_value,
            )
        )

    return results
