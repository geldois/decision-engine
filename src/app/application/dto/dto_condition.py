from __future__ import annotations

from typing import Literal, TypedDict


class DTOSimpleCondition(TypedDict):
    type: Literal["simple"]
    field: Literal["id", "event_type", "occurred_at", "payload"]
    operator: Literal["==", ">", "<", "!="]
    value: object


class DTOCompositeCondition(TypedDict):
    type: Literal["composite"]
    operator: Literal["and", "or"]
    conditions: list[DTOCondition]


DTOCondition = DTOSimpleCondition | DTOCompositeCondition
