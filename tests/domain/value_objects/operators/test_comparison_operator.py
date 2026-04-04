from uuid import uuid4

from app.domain.entities.event import Event
from app.domain.value_objects.operators.comparison_operator import ComparisonOperator


# ==========
# valid cases
# ==========
def test_comparison_operator_equals_returns_valid_bool() -> None:
    event_id = uuid4()
    event = Event(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        occurred_at=1700000000,
        event_id=event_id,
    )
    operator = ComparisonOperator.EQUALS

    assert operator.evaluate(left=event.event_type, right="USER_CREATED")

    assert operator.evaluate(
        left=event.payload, right={"user_id": 123, "email": "user@email.com"}
    )

    assert operator.evaluate(left=event.occurred_at, right=1700000000)

    assert operator.evaluate(left=event.id, right=event_id)

    assert not operator.evaluate(left=event.event_type, right=True)

    assert not operator.evaluate(left=event.payload, right=True)

    assert not operator.evaluate(left=event.occurred_at, right=True)

    assert not operator.evaluate(left=event.id, right=True)


def test_comparison_operator_greater_than_returns_valid_bool() -> None:
    operator = ComparisonOperator.GREATER_THAN

    assert operator.evaluate(left=0, right=-1)

    assert operator.evaluate(left=1, right=0)

    assert not operator.evaluate(left=0, right=0)

    assert not operator.evaluate(left=0, right=1)

    assert not operator.evaluate(left=-1, right=0)


def test_comparison_operator_less_than_returns_valid_bool() -> None:
    operator = ComparisonOperator.LESS_THAN

    assert operator.evaluate(left=0, right=1)

    assert operator.evaluate(left=-1, right=0)

    assert not operator.evaluate(left=0, right=0)

    assert not operator.evaluate(left=0, right=-1)

    assert not operator.evaluate(left=1, right=0)


def test_comparison_operator_not_equals_returns_valid_bool() -> None:
    event_id = uuid4()
    event = Event(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        occurred_at=1700000000,
        event_id=event_id,
    )
    operator = ComparisonOperator.NOT_EQUALS

    assert operator.evaluate(left=event.event_type, right=True)

    assert operator.evaluate(left=event.payload, right=True)

    assert operator.evaluate(left=event.occurred_at, right=True)

    assert operator.evaluate(left=event.id, right=True)

    assert not operator.evaluate(left=event.event_type, right="USER_CREATED")

    assert not operator.evaluate(
        left=event.payload, right={"user_id": 123, "email": "user@email.com"}
    )

    assert not operator.evaluate(left=event.occurred_at, right=1700000000)

    assert not operator.evaluate(left=event.id, right=event_id)
