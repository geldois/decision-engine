from typing import Any

from app.domain.exceptions.error_code import ErrorCode


class DomainException(Exception):
    def __init__(
        self, message: str, error_code: ErrorCode, details: dict[str, Any] | None
    ) -> None:
        self.error_code = error_code
        self.details = details or {}
        super().__init__(message)
