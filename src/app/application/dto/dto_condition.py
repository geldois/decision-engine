from __future__ import annotations

from typing import Literal, TypedDict


class DTOSimpleCondition(TypedDict):
    type: Literal["simple"]
    field: str
    operator: str
    value: object


class DTOCompositeCondition(TypedDict):
    type: Literal["composite"]
    operator: Literal["and", "or"]
    conditions: list[DTOCondition]


DTOCondition = DTOSimpleCondition | DTOCompositeCondition
