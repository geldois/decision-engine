from collections.abc import Callable

import pytest

from decision_engine.domain.entities.event import Event
from decision_engine.domain.value_objects.condition import CompositeCondition, SimpleCondition
from decision_engine.domain.value_objects.operators.logical_operator import LogicalOperator
from decision_engine.infrastructure.persistence.sqlalchemy.codecs.condition_codec import (
    ConditionDeserializer,
    ConditionSerializer,
)


@pytest.fixture(scope="function")
def composite_condition(
    make_simple_condition: Callable[..., SimpleCondition],
) -> CompositeCondition:
    return CompositeCondition(
        operator=LogicalOperator.AND,
        conditions=[
            make_simple_condition(),
            CompositeCondition(
                operator=LogicalOperator.AND,
                conditions=[
                    make_simple_condition(),
                    make_simple_condition(),
                ],
            ),
        ],
    )


# VALID CASES


def test_condition_codec_roundtrip_preserves_structure(
    composite_condition: CompositeCondition,
) -> None:
    encoded = ConditionSerializer.serialize(condition=composite_condition)
    decoded = ConditionDeserializer.deserialize(data=encoded)

    assert decoded == composite_condition


def test_condition_codec_roundtrip_preserves_semantics(
    make_event: Callable[..., Event],
    composite_condition: CompositeCondition,
) -> None:
    event = make_event()

    encoded = ConditionSerializer.serialize(condition=composite_condition)
    decoded = ConditionDeserializer.deserialize(data=encoded)

    result_original = composite_condition.evaluate_result(event=event)
    result_decoded = decoded.evaluate_result(event=event)

    assert result_decoded == result_original
