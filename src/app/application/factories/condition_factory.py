from collections.abc import Callable
from typing import Literal

import app.application.mappers.comparison_operator_mapper as ComparisonOperatorMapper
import app.application.mappers.event_field_mapper as EventFieldMapper
import app.application.mappers.logical_operator_mapper as LogicalOperatorMapper
from app.application.dto.dto_condition import (
    DTOCompositeCondition,
    DTOCondition,
    DTOSimpleCondition,
)
from app.domain.exceptions.condition_exception import ConditionException
from app.domain.value_objects.condition import (
    CompositeCondition,
    Condition,
    SimpleCondition,
)


def _build_composite(dto: DTOCompositeCondition) -> CompositeCondition:
    _validate_composite(dto=dto)

    return CompositeCondition(
        operator=LogicalOperatorMapper.parse_logical_operator(value=dto["operator"]),
        conditions=[build(dto=c) for c in dto["conditions"]],
    )


def _build_simple(dto: DTOSimpleCondition) -> SimpleCondition:
    _validate_simple(dto=dto)

    return SimpleCondition(
        operator=ComparisonOperatorMapper.parse_comparison_operator(
            value=dto["operator"]
        ),
        field=EventFieldMapper.parse_event_field(value=dto["field"]),
        value=dto["value"],
    )


_builders: dict[Literal["composite", "simple"], Callable[..., Condition]] = {
    "composite": _build_composite,
    "simple": _build_simple,
}


def _validate(dto: DTOCondition) -> None:
    if dto["type"] not in _builders:
        raise ConditionException.condition_type_is_invalid(
            details={"type": dto["type"]}
        )


def _validate_composite(dto: DTOCompositeCondition) -> None:
    if len(dto["conditions"]) < 2:
        raise ConditionException.condition_is_invalid(
            details={"conditions": dto["conditions"]}
        )


def _validate_simple(dto: DTOSimpleCondition) -> None:
    if isinstance(dto["value"], str) and not dto["value"].strip():
        raise ConditionException.condition_value_cannot_be_empty(
            details={"value": dto["value"]}
        )


def build(dto: DTOCondition) -> Condition:
    _validate(dto=dto)

    return _builders[dto["type"]](dto)
