import app.infrastructure.serialization.condition_codec as ConditionCodec
from app.domain.value_objects.condition import CompositeCondition, SimpleCondition
from app.domain.value_objects.event_field import EventField
from app.domain.value_objects.operators.comparison_operator import ComparisonOperator
from app.domain.value_objects.operators.logical_operator import LogicalOperator


# ==========
# valid cases
# ==========
def test_condition_codec_serializes_simple_condition() -> None:
    condition = SimpleCondition(
        operator=ComparisonOperator.EQUALS,
        field=EventField.PAYLOAD,
        value={"test": True},
    )

    data = ConditionCodec.ConditionSerializer().serialize(condition=condition)

    assert (
        data
        == '{"type": "simple", "field": "payload", "operator": "==", "value": {"test": true}}'
    )


def test_condition_codec_deserializes_simple_condition() -> None:
    condition = SimpleCondition(
        operator=ComparisonOperator.EQUALS,
        field=EventField.PAYLOAD,
        value={"test": True},
    )

    data = ConditionCodec.ConditionSerializer().serialize(condition=condition)

    assert ConditionCodec.deserialize(condition=data) == condition


def test_condition_codec_serializes_composite_condition() -> None:
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

    data = ConditionCodec.ConditionSerializer().serialize(condition=condition)

    assert (
        data
        == '{"type": "composite", "operator": "and", "conditions": [{"type": "simple", "field": "event_type", "operator": "==", "value": "TEST"}, {"type": "simple", "field": "payload", "operator": "==", "value": {"test": true}}]}'
    )


def test_condition_codec_deserializes_composite_condition() -> None:
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

    data = ConditionCodec.ConditionSerializer().serialize(condition=condition)

    assert ConditionCodec.deserialize(condition=data) == condition


def test_condition_codec_serializes_nested_composite_condition() -> None:
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

    data = ConditionCodec.ConditionSerializer().serialize(condition=condition)

    assert (
        data
        == '{"type": "composite", "operator": "and", "conditions": [{"type": "simple", "field": "event_type", "operator": "==", "value": "TEST"}, {"type": "composite", "operator": "and", "conditions": [{"type": "simple", "field": "event_type", "operator": "==", "value": "TEST"}, {"type": "simple", "field": "payload", "operator": "==", "value": {"test": true}}]}]}'
    )


def test_condition_codec_deserializes_nested_composite_condition() -> None:
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

    data = ConditionCodec.ConditionSerializer().serialize(condition=condition)

    assert ConditionCodec.deserialize(condition=data) == condition
