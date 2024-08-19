from dataclasses import dataclass
import random
from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib

PATTERNS_FILE = Path(__file__).parent / "patterns.toml"


def get_pattern(name, size, filename=PATTERNS_FILE):
    if name == "Random":
        return Pattern.generate_random("Random", size)
    data = tomllib.loads(filename.read_text(encoding="utf-8"))
    return Pattern.from_toml(name, toml_data=data[name])


def get_all_patterns(filename=PATTERNS_FILE):
    data = tomllib.loads(filename.read_text(encoding="utf-8"))
    return [Pattern.from_toml(name, toml_data) for name, toml_data in data.items()]


@dataclass
class Pattern:
    name: str
    alive_cells: set[tuple[int, int]]

    @classmethod
    def from_toml(cls, name, toml_data):
        return cls(
            name,
            alive_cells={tuple(cell) for cell in toml_data["alive_cells"]},
        )

    @classmethod
    def generate_random(cls, name, size):
        return cls(
            name,
            alive_cells={
                tuple([random.randint(0, 10), random.randint(0, 10)])
                for i in range(size)
            },
        )
