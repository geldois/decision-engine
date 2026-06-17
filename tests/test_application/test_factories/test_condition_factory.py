import pytest

from decision_engine.application.dto.condition import CompositeConditionDTO, SimpleConditionDTO
from decision_engine.application.factories.condition_factory import build_condition
from decision_engine.domain.errors.condition_error import ConditionError
from decision_engine.domain.value_objects.condition import CompositeCondition, SimpleCondition
from decision_engine.domain.value_objects.event_field import EventField
from decision_engine.domain.value_objects.operators.comparison_operator import ComparisonOperator
from decision_engine.domain.value_objects.operators.logical_operator import LogicalOperator

# VALID CASES


def test_condition_factory_builds_simple_condition() -> None:
    dto = SimpleConditionDTO(
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
    dto = CompositeConditionDTO(
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
    with pytest.raises(ConditionError):
        build_condition(
            dto=SimpleConditionDTO(
                {
                    "type": "TEST",
                    "field": "event_type",
                    "operator": "==",
                    "value": "TEST",
                }
            )
        )


def test_condition_factory_raises_on_invalid_conditions_length() -> None:
    with pytest.raises(ConditionError):
        build_condition(
            dto=CompositeConditionDTO(
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
    with pytest.raises(ConditionError):
        build_condition(
            dto=SimpleConditionDTO(
                {
                    "type": "simple",
                    "field": "event_type",
                    "operator": "==",
                    "value": " ",
                }
            )
        )
