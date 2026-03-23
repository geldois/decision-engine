from fastapi import HTTPException, status
from pydantic import ValidationError

from app.api.schemas.http_error_response import HTTPErrorResponse
from app.domain.exceptions.domain_exception import DomainException
from app.domain.exceptions.error_code import ErrorCode

_MAPPING: dict[ErrorCode, int] = {
    ErrorCode.DECISION_EXPLANATION_EMPTY: status.HTTP_422_UNPROCESSABLE_CONTENT,
    ErrorCode.DECISION_NOT_FOUND: status.HTTP_404_NOT_FOUND,
    ErrorCode.DECISION_OUTCOME_INVALID: status.HTTP_422_UNPROCESSABLE_CONTENT,
    ErrorCode.EVENT_FIELD_EMPTY: status.HTTP_422_UNPROCESSABLE_CONTENT,
    ErrorCode.EVENT_FIELD_INVALID: status.HTTP_422_UNPROCESSABLE_CONTENT,
    ErrorCode.EVENT_NOT_FOUND: status.HTTP_404_NOT_FOUND,
    ErrorCode.EVENT_PAYLOAD_EMPTY: status.HTTP_422_UNPROCESSABLE_CONTENT,
    ErrorCode.EVENT_TIMESTAMP_INVALID: status.HTTP_422_UNPROCESSABLE_CONTENT,
    ErrorCode.EVENT_TYPE_EMPTY: status.HTTP_422_UNPROCESSABLE_CONTENT,
    ErrorCode.RULE_CONDITION_INVALID: status.HTTP_422_UNPROCESSABLE_CONTENT,
    ErrorCode.RULE_CONDITION_OPERATOR_EMPTY: status.HTTP_422_UNPROCESSABLE_CONTENT,
    ErrorCode.RULE_CONDITION_OPERATOR_INVALID: status.HTTP_422_UNPROCESSABLE_CONTENT,
    ErrorCode.RULE_CONDITION_VALUE_EMPTY: status.HTTP_422_UNPROCESSABLE_CONTENT,
    ErrorCode.RULE_NAME_EMPTY: status.HTTP_422_UNPROCESSABLE_CONTENT,
    ErrorCode.RULE_OUTCOME_EMPTY: status.HTTP_422_UNPROCESSABLE_CONTENT,
    ErrorCode.RULE_NOT_FOUND: status.HTTP_404_NOT_FOUND,
}


def map_error_code_to_http_error_code(error_code: ErrorCode) -> int:
    try:
        return _MAPPING[error_code]
    except KeyError:
        return status.HTTP_500_INTERNAL_SERVER_ERROR


def map_exception_to_http_exception(
    exception: Exception,
) -> HTTPException:
    if isinstance(exception, DomainException):
        http_error_response = HTTPErrorResponse(
            error=exception.error_code.value,
            message=str(exception),
            details=exception.details,
        )

        return HTTPException(
            status_code=map_error_code_to_http_error_code(
                error_code=exception.error_code
            ),
            detail=http_error_response.model_dump(),
        )

    if isinstance(exception, ValidationError):
        http_error_response = HTTPErrorResponse(
            error="VALIDATION_ERROR",
            message="Invalid request data",
            details=exception.errors(),
        )

        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=http_error_response.model_dump(),
        )

    http_error_response = HTTPErrorResponse(
        error="INTERNAL_SERVER_ERROR", message="Internal server error", details={}
    )

    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=http_error_response.model_dump(),
    )
