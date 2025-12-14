from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

import numpy as np


@dataclass
class Record:
    id: str
    vector: np.ndarray
    payload: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TableMetadata:
    name: str
    version: int = 1
    schema: Dict[str, type] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
