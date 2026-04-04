from collections.abc import Callable
from typing import Any

from app.domain.value_objects.conditions.composite_condition import CompositeCondition
from app.domain.value_objects.conditions.condition import Condition
from app.domain.value_objects.conditions.simple_condition import SimpleCondition


class ConditionMapper:
    _mappers: dict[str, Callable[..., dict[str, Any]]] = {}

    @classmethod
    def _identify_type(cls, condition: Condition) -> str:
        if isinstance(condition, CompositeCondition):
            return "composite"
        else:
            return "simple"

    @classmethod
    def _init_mappers(cls) -> None:
        if cls._mappers:
            return

        cls._mappers = {
            "composite": cls._map_composite_to_dict,
            "simple": cls._map_simple_to_dict,
        }

    @classmethod
    def _map_composite_to_dict(
        cls,
        condition: CompositeCondition,
    ) -> dict[str, Any]:
        conditions = [cls.map_to_dict(condition=c) for c in condition.conditions]

        return {
            "type": "composite",
            "operator": condition.operator.value,
            "conditions": conditions,
        }

    @classmethod
    def _map_simple_to_dict(cls, condition: SimpleCondition) -> dict[str, Any]:
        return {
            "type": "simple",
            "field": condition.field.value,
            "operator": condition.operator.value,
            "value": condition.value,
        }

    @classmethod
    def map_to_dict(cls, condition: Condition) -> dict[str, Any]:
        cls._init_mappers()

        return cls._mappers[cls._identify_type(condition=condition)](condition)
