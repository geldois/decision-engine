from uuid import uuid4

import pytest

from app.domain.entities.event import Event
from app.domain.exceptions.condition_exception import ConditionException
from app.domain.value_objects.conditions.composite_condition import CompositeCondition
from app.domain.value_objects.conditions.simple_condition import SimpleCondition
from app.domain.value_objects.event_field import EventField
from app.domain.value_objects.operators.comparison_operator import ComparisonOperator
from app.domain.value_objects.operators.logical_operator import LogicalOperator


# ==========
# valid cases
# ==========
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

    assert CompositeCondition(
        operator=LogicalOperator.AND, conditions=conditions
    ).evaluate(event=event)

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

    assert not CompositeCondition(
        operator=LogicalOperator.AND, conditions=conditions
    ).evaluate(event=event)


# ==========
# valid cases
# ==========
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
