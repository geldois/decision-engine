from typing import Any


class DomainException(Exception):
    def __init__(
        self, message: str, exception_code: str, details: dict[str, Any] | None
    ) -> None:
        self.message = message
        self.exception_code = exception_code
        self.details = details
        super().__init__(self.message)
