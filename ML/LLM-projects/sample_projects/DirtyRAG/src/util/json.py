import json
from typing import Any, Dict, Optional, cast


def json_to_dict(json_string: str) -> Optional[Dict[str, Any]]:
    try:
        # Cast the result of json.loads() to Dict[str, Any]
        return cast(Dict[str, Any], json.loads(json_string))
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None
