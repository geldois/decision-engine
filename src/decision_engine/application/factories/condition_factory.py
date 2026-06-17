from __future__ import annotations

from typing import TYPE_CHECKING

from decision_engine.application.mappers.comparison_operator_mapper import (
    parse_comparison_operator,
)
from decision_engine.application.mappers.event_field_mapper import parse_event_field
from decision_engine.application.mappers.logical_operator_mapper import (
    parse_logical_operator,
)
from decision_engine.domain.exceptions.condition_exception import ConditionException
from decision_engine.domain.value_objects.condition import (
    CompositeCondition,
    Condition,
    SimpleCondition,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    from decision_engine.application.dto.condition import (
        CompositeConditionDTO,
        DTOCondition,
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


def _validate(dto: DTOCondition) -> None:
    if dto["type"] not in _builders:
        raise ConditionException.condition_type_is_invalid(
            details={"type": dto["type"]}
        )


def _validate_composite(dto: CompositeConditionDTO) -> None:
    const = 2

    if len(dto["conditions"]) < const:
        raise ConditionException.condition_is_invalid(
            details={"conditions": dto["conditions"]}
        )


def _validate_simple(dto: SimpleConditionDTO) -> None:
    if isinstance(dto["value"], str) and not dto["value"].strip():
        raise ConditionException.condition_value_cannot_be_empty(
            details={"value": dto["value"]}
        )


def build_condition(dto: DTOCondition) -> Condition:
    _validate(dto=dto)

    return _builders[dto["type"]](dto)
