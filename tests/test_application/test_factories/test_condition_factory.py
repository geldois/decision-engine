import pytest

from app.application.dto.dto_condition import DTOCompositeCondition, DTOSimpleCondition
from app.application.factories.condition_factory import build_condition
from app.domain.exceptions.condition_exception import ConditionException
from app.domain.value_objects.condition import CompositeCondition, SimpleCondition
from app.domain.value_objects.event_field import EventField
from app.domain.value_objects.operators.comparison_operator import ComparisonOperator
from app.domain.value_objects.operators.logical_operator import LogicalOperator

# VALID CASES


def test_condition_factory_builds_simple_condition() -> None:
    dto = DTOSimpleCondition(
        {
            "type": "simple",
            "field": "event_type",
            "operator": "==",
            "value": "TEST",
        }
    )

    condition = build_condition(dto=dto)

    assert condition == SimpleCondition(
        operator=ComparisonOperator.EQUALS, field=EventField.EVENT_TYPE, value="TEST"
    )


def test_condition_factory_builds_composite_condition() -> None:
    dto = DTOCompositeCondition(
        {
            "type": "composite",
            "operator": "and",
            "conditions": [
                {
                    "type": "simple",
                    "field": "event_type",
                    "operator": "==",
                    "value": "TEST",
                },
                {
                    "type": "simple",
                    "field": "event_type",
                    "operator": "==",
                    "value": "TEST",
                },
            ],
        }
    )
    simple_condition = SimpleCondition(
        operator=ComparisonOperator.EQUALS,
        field=EventField.EVENT_TYPE,
        value="TEST",
    )
    composite_condition = CompositeCondition(
        operator=LogicalOperator.AND,
        conditions=[simple_condition, simple_condition],
    )

    condition = build_condition(dto=dto)

    assert condition == composite_condition


# INVALID CASES


def test_condition_factory_raises_on_invalid_dto_type() -> None:
    with pytest.raises(ConditionException):
        build_condition(
            dto=DTOSimpleCondition(
                {
                    "type": "TEST",
                    "field": "event_type",
                    "operator": "==",
                    "value": "TEST",
                }
            )
        )


def test_condition_factory_raises_on_invalid_conditions_length() -> None:
    with pytest.raises(ConditionException):
        build_condition(
            dto=DTOCompositeCondition(
                {
                    "type": "composite",
                    "operator": "and",
                    "conditions": [
                        {
                            "type": "simple",
                            "field": "event_type",
                            "operator": "==",
                            "value": "TEST",
                        }
                    ],
                }
            )
        )


def test_condition_factory_raises_on_empty_string_value() -> None:
    with pytest.raises(ConditionException):
        build_condition(
            dto=DTOSimpleCondition(
                {
                    "type": "simple",
                    "field": "event_type",
                    "operator": "==",
                    "value": " ",
                }
            )
        )
