from __future__ import annotations

from typing import TYPE_CHECKING

from decision_engine.application.mappers.comparison_operator_mapper import (
    parse_comparison_operator,
)
from decision_engine.application.mappers.event_field_mapper import parse_event_field
from decision_engine.application.mappers.logical_operator_mapper import (
    parse_logical_operator,
)
from decision_engine.domain.errors.condition_error import (
    EmptyConditionValueError,
    InvalidConditionError,
    InvalidConditionTypeError,
)
from decision_engine.domain.value_objects.condition import (
    CompositeCondition,
    Condition,
    SimpleCondition,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    from decision_engine.application.dto.condition import (
        CompositeConditionDTO,
        ConditionDTO,
        SimpleConditionDTO,
    )


def _build_composite(dto: CompositeConditionDTO) -> CompositeCondition:
    _validate_composite(dto=dto)

    return CompositeCondition(
        operator=parse_logical_operator(value=dto["operator"]),
        conditions=[build_condition(dto=c) for c in dto["conditions"]],
    )


def _build_simple(dto: SimpleConditionDTO) -> SimpleCondition:
    _validate_simple(dto=dto)

    return SimpleCondition(
        operator=parse_comparison_operator(value=dto["operator"]),
        field=parse_event_field(value=dto["field"]),
        value=dto["value"],
    )


_builders: dict[str, Callable[..., Condition]] = {
    "composite": _build_composite,
    "simple": _build_simple,
}


def _validate(dto: ConditionDTO) -> None:
    if dto["type"] not in _builders:
        raise InvalidConditionTypeError(condition_type=dto["type"])


def _validate_composite(dto: CompositeConditionDTO) -> None:
    min_length = 2

    if len(dto["conditions"]) < min_length:
        raise InvalidConditionError


def _validate_simple(dto: SimpleConditionDTO) -> None:
    if isinstance(dto["value"], str) and not dto["value"].strip():
        raise EmptyConditionValueError


def build_condition(dto: ConditionDTO) -> Condition:
    _validate(dto=dto)

    return _builders[dto["type"]](dto)
