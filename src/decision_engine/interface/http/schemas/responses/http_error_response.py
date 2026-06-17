from collections.abc import Mapping, Sequence

from pydantic import BaseModel


class HTTPErrorResponse(BaseModel):
    error: str
    message: str
    details: Mapping[str, object] | Sequence[object] | None = None
