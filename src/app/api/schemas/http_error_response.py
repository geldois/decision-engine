from typing import Any

from pydantic import BaseModel

from app.domain.exceptions.domain_exception import DomainException


class HttpErrorResponse(BaseModel):
    error: DomainException
    message: str
    details: dict[str, Any] | None = None
