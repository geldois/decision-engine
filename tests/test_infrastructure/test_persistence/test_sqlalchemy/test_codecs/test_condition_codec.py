from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from decision_engine.domain.value_objects.condition import CompositeCondition
from decision_engine.domain.value_objects.operators.logical_operator import (
    LogicalOperator,
)
from decision_engine.infrastructure.persistence.sqlalchemy.codecs.condition_codec import (  # noqa: E501
    ConditionDeserializer,
    ConditionSerializer,
)

if TYPE_CHECKING:
    from tests.conftest import MakeEvent, MakeSimpleCondition


@pytest.fixture
def composite_condition(
    make_simple_condition: MakeSimpleCondition,
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
    make_event: MakeEvent,
    composite_condition: CompositeCondition,
) -> None:
    event = make_event()

    encoded = ConditionSerializer.serialize(condition=composite_condition)
    decoded = ConditionDeserializer.deserialize(data=encoded)

    result_original = composite_condition.evaluate_result(event=event)
    result_decoded = decoded.evaluate_result(event=event)

    assert result_decoded == result_original
