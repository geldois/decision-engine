import pytest
from pydantic import BaseModel, ValidationError

from app.api.mappers.http_error_code_mapper import (
    map_error_code_to_http_error_code,
    map_exception_to_http_exception,
)
from app.domain.exceptions.domain_exception import DomainException
from app.domain.exceptions.error_code import ErrorCode


# ==========
# valid cases
# ==========
def test_map_error_code_to_http_error_code_always_returns_http_error_codes() -> None:
    for member in ErrorCode:
        assert map_error_code_to_http_error_code(error_code=member)


def test_map_exception_to_http_exception_returns_404_or_422_when_receives_domain_exception() -> (
    None
):
    with pytest.raises(DomainException) as exception:
        raise DomainException(
            message="Test",
            error_code=ErrorCode.EVENT_NOT_FOUND,
            details={"test": "test"},
        )

    domain_exception = exception.value

    http_exception = map_exception_to_http_exception(exception=domain_exception)

    assert http_exception.status_code in (404, 422)


class ValidationModel(BaseModel):
    x: int


def test_map_exception_to_http_exception_returns_422_when_receives_validation_error() -> (
    None
):
    with pytest.raises(ValidationError) as exception:
        ValidationModel(x="test")

    validation_error = exception.value

    http_exception = map_exception_to_http_exception(exception=validation_error)

    assert http_exception.status_code == 422


def test_map_exception_to_http_exception_returns_500_on_internal_server_error() -> None:
    with pytest.raises(RuntimeError) as exception:
        raise RuntimeError()

    internal_server_error = exception.value

    http_exception = map_exception_to_http_exception(exception=internal_server_error)

    assert http_exception.status_code == 500
