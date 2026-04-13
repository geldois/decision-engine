import json
from typing import Any


def deserialize(payload: str) -> dict[str, Any]:
    return json.loads(payload)


def serialize(payload: dict[str, Any]) -> str:
    return json.dumps(payload)
