from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class HTTPRegisterRuleRequest(BaseModel):
    name: str
    condition: dict[str, Any]
    outcome: str
    priority: int
