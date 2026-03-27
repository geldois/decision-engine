from fastapi import status

from app.application.errors.error_code import ErrorCode

_MAPPING: dict[ErrorCode, int] = {
    ErrorCode.INVALID_DECISION: status.HTTP_422_UNPROCESSABLE_CONTENT,
    ErrorCode.INVALID_EVENT: status.HTTP_422_UNPROCESSABLE_CONTENT,
    ErrorCode.INVALID_RULE: status.HTTP_422_UNPROCESSABLE_CONTENT,
}


def map_error_code_to_http_error_code(error_code: ErrorCode) -> int:
    return _MAPPING[error_code]


def map_http_error_code_to_error_code(
    http_error_code: int,
) -> ErrorCode | None:
    for error_code, http_error in _MAPPING.items():
        if http_error is http_error_code:
            return error_code
