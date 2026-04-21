from uuid import uuid4

import pytest

from app.domain.entities.event import Event
from app.domain.exceptions.condition_exception import ConditionException
from app.domain.value_objects.condition import CompositeCondition, SimpleCondition
from app.domain.value_objects.event_field import EventField
from app.domain.value_objects.operators.comparison_operator import ComparisonOperator
from app.domain.value_objects.operators.logical_operator import LogicalOperator

# VALID CASES


def test_composite_condition_returns_valid_bool() -> None:
    event_id = uuid4()
    event = Event(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        occurred_at=1700000000,
        event_id=event_id,
    )
    conditions = [
        SimpleCondition(
            operator=ComparisonOperator.EQUALS,
            field=EventField.EVENT_TYPE,
            value="USER_CREATED",
        ),
        SimpleCondition(
            operator=ComparisonOperator.EQUALS,
            field=EventField.PAYLOAD,
            value={"user_id": 123, "email": "user@email.com"},
        ),
        SimpleCondition(
            operator=ComparisonOperator.EQUALS,
            field=EventField.OCCURRED_AT,
            value=1700000000,
        ),
        SimpleCondition(
            operator=ComparisonOperator.EQUALS,
            field=EventField.EVENT_ID,
            value=event_id,
        ),
        CompositeCondition(
            operator=LogicalOperator.OR,
            conditions=[
                SimpleCondition(
                    operator=ComparisonOperator.EQUALS,
                    field=EventField.EVENT_TYPE,
                    value="USER_CREATED",
                ),
                SimpleCondition(
                    operator=ComparisonOperator.EQUALS,
                    field=EventField.PAYLOAD,
                    value={"user_id": 123},
                ),
                SimpleCondition(
                    operator=ComparisonOperator.EQUALS,
                    field=EventField.OCCURRED_AT,
                    value=1800000000,
                ),
                SimpleCondition(
                    operator=ComparisonOperator.EQUALS,
                    field=EventField.EVENT_ID,
                    value=uuid4(),
                ),
            ],
        ),
    ]

    assert (
        CompositeCondition(operator=LogicalOperator.AND, conditions=conditions)
        .evaluate(event=event)
        .result
    )

    conditions = [
        SimpleCondition(
            operator=ComparisonOperator.EQUALS,
            field=EventField.EVENT_TYPE,
            value="USER_CREATED",
        ),
        SimpleCondition(
            operator=ComparisonOperator.EQUALS,
            field=EventField.PAYLOAD,
            value={"user_id": 123, "email": "user@email.com"},
        ),
        SimpleCondition(
            operator=ComparisonOperator.EQUALS,
            field=EventField.OCCURRED_AT,
            value=1700000000,
        ),
        SimpleCondition(
            operator=ComparisonOperator.EQUALS,
            field=EventField.EVENT_ID,
            value=event_id,
        ),
        CompositeCondition(
            operator=LogicalOperator.OR,
            conditions=[
                SimpleCondition(
                    operator=ComparisonOperator.EQUALS,
                    field=EventField.EVENT_TYPE,
                    value="TEST",
                ),
                SimpleCondition(
                    operator=ComparisonOperator.EQUALS,
                    field=EventField.PAYLOAD,
                    value={"user_id": 123},
                ),
                SimpleCondition(
                    operator=ComparisonOperator.EQUALS,
                    field=EventField.OCCURRED_AT,
                    value=1800000000,
                ),
                SimpleCondition(
                    operator=ComparisonOperator.EQUALS,
                    field=EventField.EVENT_ID,
                    value=uuid4(),
                ),
            ],
        ),
    ]

    assert (
        not CompositeCondition(operator=LogicalOperator.AND, conditions=conditions)
        .evaluate(event=event)
        .result
    )


def test_simple_condition_returns_valid_bool() -> None:
    event_id = uuid4()
    event = Event(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        occurred_at=1700000000,
        event_id=event_id,
    )

    assert (
        SimpleCondition(
            operator=ComparisonOperator.EQUALS,
            field=EventField.EVENT_TYPE,
            value=event.event_type,
        )
        .evaluate(event=event)
        .result
    )

    assert (
        SimpleCondition(
            operator=ComparisonOperator.EQUALS,
            field=EventField.PAYLOAD,
            value=event.payload,
        )
        .evaluate(event=event)
        .result
    )

    assert (
        SimpleCondition(
            operator=ComparisonOperator.EQUALS,
            field=EventField.OCCURRED_AT,
            value=event.occurred_at,
        )
        .evaluate(event=event)
        .result
    )

    assert (
        SimpleCondition(
            operator=ComparisonOperator.EQUALS,
            field=EventField.EVENT_ID,
            value=event.id,
        )
        .evaluate(event=event)
        .result
    )


# INVALID CASES


def test_composite_condition_raises_on_invalid_conditions_length() -> None:
    with pytest.raises(ConditionException):
        CompositeCondition(
            operator=LogicalOperator.AND,
            conditions=[
                SimpleCondition(
                    operator=ComparisonOperator.EQUALS,
                    field=EventField.EVENT_TYPE,
                    value="USER_CREATED",
                )
            ],
        )


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
