from collections.abc import Callable

import pytest

from app.domain.entities.event import Event
from app.domain.value_objects.condition import CompositeCondition, SimpleCondition
from app.domain.value_objects.operators.logical_operator import LogicalOperator
from app.infrastructure.persistence.sqlalchemy.codecs.condition_codec import (
    ConditionDeserializer,
    ConditionSerializer,
)


@pytest.fixture(scope="function")
def composite_condition(
    simple_condition_factory: Callable[..., SimpleCondition],
) -> CompositeCondition:
    return CompositeCondition(
        operator=LogicalOperator.AND,
        conditions=[
            simple_condition_factory(),
            CompositeCondition(
                operator=LogicalOperator.AND,
                conditions=[
                    simple_condition_factory(),
                    simple_condition_factory(),
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
    event_factory: Callable[..., Event],
    composite_condition: CompositeCondition,
) -> None:
    event = event_factory()

    encoded = ConditionSerializer.serialize(condition=composite_condition)
    decoded = ConditionDeserializer.deserialize(data=encoded)

    result_original = composite_condition.evaluate_result(event=event)
    result_decoded = decoded.evaluate_result(event=event)

    assert result_decoded == result_original
