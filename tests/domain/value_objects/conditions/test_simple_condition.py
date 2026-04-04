from uuid import uuid4

import pytest

from app.domain.entities.event import Event
from app.domain.exceptions.condition_exception import ConditionException
from app.domain.value_objects.conditions.simple_condition import SimpleCondition
from app.domain.value_objects.event_field import EventField
from app.domain.value_objects.operators.comparison_operator import ComparisonOperator


# ==========
# valid cases
# ==========
def test_simple_condition_returns_valid_bool() -> None:
    event_id = uuid4()
    event = Event(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        occurred_at=1700000000,
        event_id=event_id,
    )

    assert SimpleCondition(
        operator=ComparisonOperator.EQUALS,
        field=EventField.EVENT_TYPE,
        value=event.event_type,
    ).evaluate(event=event)

    assert SimpleCondition(
        operator=ComparisonOperator.EQUALS,
        field=EventField.PAYLOAD,
        value=event.payload,
    ).evaluate(event=event)

    assert SimpleCondition(
        operator=ComparisonOperator.EQUALS,
        field=EventField.OCCURRED_AT,
        value=event.occurred_at,
    ).evaluate(event=event)

    assert SimpleCondition(
        operator=ComparisonOperator.EQUALS,
        field=EventField.EVENT_ID,
        value=event.id,
    ).evaluate(event=event)


# ==========
# valid cases
# ==========
def test_simple_condition_raises_on_invalid_value_type_for_field() -> None:
    with pytest.raises(ConditionException):
        SimpleCondition(
            operator=ComparisonOperator.EQUALS, field=EventField.PAYLOAD, value="TEST"
        )


def test_simple_condition_raises_on_invalid_field_or_value_type_for_operator() -> None:
    event = Event(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        occurred_at=1700000000,
    )

    with pytest.raises(ConditionException):
        SimpleCondition(
            operator=ComparisonOperator.GREATER_THAN,
            field=EventField.PAYLOAD,
            value={"user_id": 123, "email": "user@email.com"},
        ).evaluate(event=event)
