from __future__ import annotations

from fastapi import HTTPException, status
from pydantic import ValidationError

from decision_engine.domain.errors.domain_error import DomainError
from decision_engine.interface.http.schemas.responses.http_error_response import (
    HTTPErrorResponse,
)

_MAPPING: dict[str, int] = {
    "CONDITION_INVALID": status.HTTP_422_UNPROCESSABLE_CONTENT,
    "CONDITION_MISSING_FIELDS": status.HTTP_422_UNPROCESSABLE_CONTENT,
    "CONDITION_OPERATOR_EMPTY": status.HTTP_422_UNPROCESSABLE_CONTENT,
    "CONDITION_OPERATOR_INVALID": status.HTTP_422_UNPROCESSABLE_CONTENT,
    "CONDITION_TYPE_INVALID": status.HTTP_422_UNPROCESSABLE_CONTENT,
    "CONDITION_VALUE_EMPTY": status.HTTP_422_UNPROCESSABLE_CONTENT,
    "DECISION_NOT_FOUND": status.HTTP_404_NOT_FOUND,
    "DECISION_OUTCOME_INVALID": status.HTTP_422_UNPROCESSABLE_CONTENT,
    "EVENT_FIELD_EMPTY": status.HTTP_422_UNPROCESSABLE_CONTENT,
    "EVENT_FIELD_INVALID": status.HTTP_422_UNPROCESSABLE_CONTENT,
    "EVENT_NOT_FOUND": status.HTTP_404_NOT_FOUND,
    "EVENT_OCCURRED_AT_INVALID": status.HTTP_422_UNPROCESSABLE_CONTENT,
    "EVENT_PAYLOAD_EMPTY": status.HTTP_422_UNPROCESSABLE_CONTENT,
    "EVENT_TYPE_EMPTY": status.HTTP_422_UNPROCESSABLE_CONTENT,
    "RULE_NAME_EMPTY": status.HTTP_422_UNPROCESSABLE_CONTENT,
    "RULE_NOT_FOUND": status.HTTP_404_NOT_FOUND,
    "RULE_OUTCOME_EMPTY": status.HTTP_422_UNPROCESSABLE_CONTENT,
    "RULE_PRIORITY_INVALID": status.HTTP_422_UNPROCESSABLE_CONTENT,
}


def map_http_error_code(*, error_code: str) -> int:
    return _MAPPING.get(error_code, status.HTTP_500_INTERNAL_SERVER_ERROR)


def map_http_exception(*, exception: Exception) -> HTTPException:
    if isinstance(exception, DomainError):
        error_code = exception.error_code or "INTERNAL_SERVER_ERROR"

        return HTTPException(
            status_code=map_http_error_code(error_code=error_code),
            detail=HTTPErrorResponse(
                error=error_code, message=str(exception)
            ).model_dump(),
        )

    if isinstance(exception, ValidationError):
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=HTTPErrorResponse(
                error="VALIDATION_ERROR",
                message="Invalid request data",
                details=exception.errors(),
            ).model_dump(),
        )

    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=HTTPErrorResponse(
            error="INTERNAL_SERVER_ERROR", message="Internal server error"
        ).model_dump(),
    )
