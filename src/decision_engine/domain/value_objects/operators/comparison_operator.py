from __future__ import annotations

import operator
from enum import Enum
from numbers import Number
from typing import TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from collections.abc import Callable


class ComparisonOperator(Enum):
    _function: Callable[..., bool]
    accepted_types: tuple[type[object], ...]

    EQUALS = "==", operator.eq, (dict, Number, str, UUID)
    GREATER_THAN = ">", operator.gt, (Number,)
    LESS_THAN = "<", operator.lt, (Number,)
    NOT_EQUALS = "!=", operator.ne, (dict, Number, str, UUID)

    def __new__(
        cls,
        operator: str,
        _function: Callable[..., bool],
        accepted_types: tuple[type[object], ...],
    ) -> ComparisonOperator:
        obj = object.__new__(cls)
        obj._value_ = operator
        obj._function = _function
        obj.accepted_types = accepted_types

        return obj

    def _is_number(self, obj: object) -> bool:
        if isinstance(obj, bool):
            return False

        return isinstance(obj, Number)

    def _is_valid_type(self, obj: object) -> bool:
        return isinstance(obj, self.accepted_types)

    def validate(self, field: object, value: object) -> bool:
        if not self._is_valid_type(obj=field) or not self._is_valid_type(obj=value):
            return False

        if self._is_number(obj=field) and self._is_number(obj=value):
            return True

        if isinstance(field, dict) and isinstance(value, dict):
            return self in {ComparisonOperator.EQUALS, ComparisonOperator.NOT_EQUALS}

        if isinstance(field, str) and isinstance(value, str):
            return self in {ComparisonOperator.EQUALS, ComparisonOperator.NOT_EQUALS}

        if isinstance(field, UUID) and isinstance(value, UUID):
            return self in {ComparisonOperator.EQUALS, ComparisonOperator.NOT_EQUALS}

        return False

    def accepts_type(self, typ: type[object]) -> bool:
        return typ in self.accepted_types

    def evaluate(self, left: object, right: object) -> bool:
        return self._function(left, right)
