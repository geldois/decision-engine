from __future__ import annotations

from uuid import uuid4

import pytest
from pydantic import BaseModel, ValidationError

from decision_engine.domain.errors.event_error import NotFoundEventError
from decision_engine.interface.http.mappers.http_error_code_mapper import (
    map_http_error_code,
    map_http_exception,
)


class ValidationModel(BaseModel):
    x: int


# VALID CASES


def test_map_http_error_code_returns_mapped_status_for_known_code() -> None:
    assert map_http_error_code(error_code="EVENT_NOT_FOUND") == 404
    assert map_http_error_code(error_code="CONDITION_INVALID") == 422


def test_map_http_error_code_returns_500_for_unknown_code() -> None:
    assert map_http_error_code(error_code="UNKNOWN_CODE") == 500


def test_map_http_exception_returns_404_or_422_when_receives_domain_error() -> None:
    http_exception = map_http_exception(exception=NotFoundEventError(event_id=uuid4()))

    assert http_exception.status_code in (404, 422)


def test_map_http_exception_returns_422_when_receives_validation_error() -> None:
    with pytest.raises(ValidationError) as exception:
        ValidationModel.model_validate({"x": "not-an-int"})

    http_exception = map_http_exception(exception=exception.value)

    assert http_exception.status_code == 422


def test_map_http_exception_returns_500_on_internal_server_error() -> None:
    http_exception = map_http_exception(exception=RuntimeError())

    assert http_exception.status_code == 500
