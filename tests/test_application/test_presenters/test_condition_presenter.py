from app.application.presenters.condition_presenter import ConditionPresenter
from app.domain.value_objects.condition import CompositeCondition, SimpleCondition
from app.domain.value_objects.event_field import EventField
from app.domain.value_objects.operators.comparison_operator import ComparisonOperator
from app.domain.value_objects.operators.logical_operator import LogicalOperator

# VALID CASES


def test_condition_presenter_presents_simple_condition() -> None:
    condition = SimpleCondition(
        operator=ComparisonOperator.EQUALS,
        field=EventField.PAYLOAD,
        value={"test": True},
    )

    data = ConditionPresenter.present(element=condition)

    assert data == {
        "type": "simple",
        "field": "payload",
        "operator": "==",
        "value": {"test": True},
    }


def test_condition_presenter_presents_composite_condition() -> None:
    condition = CompositeCondition(
        operator=LogicalOperator.AND,
        conditions=[
            SimpleCondition(
                operator=ComparisonOperator.EQUALS,
                field=EventField.EVENT_TYPE,
                value="TEST",
            ),
            SimpleCondition(
                operator=ComparisonOperator.EQUALS,
                field=EventField.PAYLOAD,
                value={"test": True},
            ),
        ],
    )

    data = data = ConditionPresenter.present(element=condition)

    assert data == {
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
                "field": "payload",
                "operator": "==",
                "value": {"test": True},
            },
        ],
    }


def test_condition_presenter_presents_nested_composite_condition() -> None:
    condition = CompositeCondition(
        operator=LogicalOperator.AND,
        conditions=[
            SimpleCondition(
                operator=ComparisonOperator.EQUALS,
                field=EventField.EVENT_TYPE,
                value="TEST",
            ),
            CompositeCondition(
                operator=LogicalOperator.AND,
                conditions=[
                    SimpleCondition(
                        operator=ComparisonOperator.EQUALS,
                        field=EventField.EVENT_TYPE,
                        value="TEST",
                    ),
                    SimpleCondition(
                        operator=ComparisonOperator.EQUALS,
                        field=EventField.PAYLOAD,
                        value={"test": True},
                    ),
                ],
            ),
        ],
    )

    data = data = ConditionPresenter.present(element=condition)

    assert data == {
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
                        "field": "payload",
                        "operator": "==",
                        "value": {"test": True},
                    },
                ],
            },
        ],
    }
