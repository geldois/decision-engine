from __future__ import annotations

from typing import Literal, TypedDict


class CompositeConditionDTO(TypedDict):
    type: Literal["composite"]
    operator: Literal["and", "or"]
    conditions: list[DTOCondition]


class SimpleConditionDTO(TypedDict):
    type: Literal["simple"]
    field: Literal["id", "event_type", "occurred_at", "payload"]
    operator: Literal["==", ">", "<", "!="]
    value: object

DTOCondition = SimpleConditionDTO | CompositeConditionDTO
