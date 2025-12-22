from __future__ import annotations

from typing import Any

from faulttree.core.config import FaultTreeConfig


def fault_tree_config_json_schema() -> dict[str, Any]:
    """
    JSON Schema for the FaultTreeConfig DSL.

    Useful for frontend validation + editor tooling (autocomplete, etc.).
    """
    return FaultTreeConfig.model_json_schema()
