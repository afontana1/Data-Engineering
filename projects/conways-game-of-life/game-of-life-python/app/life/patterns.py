"""Pattern loading and generation for Game of Life."""
from dataclasses import dataclass
from pathlib import Path
import random
from typing import Iterable, Set, Tuple

try:
    import tomllib  # Python 3.11+
except ImportError:  # pragma: no cover
    import tomli as tomllib


PATTERNS_FILE = Path(__file__).parent / "patterns.toml"
Coord = Tuple[int, int]


@dataclass
class Pattern:
    name: str
    alive_cells: Set[Coord]


def _load_all(filename: Path = PATTERNS_FILE) -> dict:
    return tomllib.loads(filename.read_text(encoding="utf-8"))


def get_pattern(name: str, random_fill: float = 0.2, size_hint: int = 50) -> Pattern:
    if name.lower() == "random":
        total_cells = max(size_hint * size_hint, 1)
        alive_target = int(total_cells * random_fill)
        max_coord = max(size_hint // 2, 1)
        alive = {
            (random.randint(0, max_coord), random.randint(0, max_coord))
            for _ in range(alive_target)
        }
        return Pattern(name="Random", alive_cells=alive)

    data = _load_all()
    if name not in data:
        raise ValueError(f"Unknown pattern '{name}'. Available: {', '.join(data)}")
    alive_cells = {tuple(cell) for cell in data[name]["alive_cells"]}
    return Pattern(name=name, alive_cells=alive_cells)


def list_patterns(filename: Path = PATTERNS_FILE) -> Iterable[str]:
    return _load_all(filename).keys()
