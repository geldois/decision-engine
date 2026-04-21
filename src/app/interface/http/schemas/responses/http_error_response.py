from collections.abc import Mapping, Sequence
from typing import Any

from pydantic import BaseModel


class HTTPErrorResponse(BaseModel):
    error: str
    message: str
    details: Mapping[str, Any] | Sequence[Any] | None
