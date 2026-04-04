from collections.abc import Callable

from app.application.dto.dto_condition import (
    DTOCompositeCondition,
    DTOCondition,
    DTOSimpleCondition,
)
from app.application.mappers.comparison_operator_mapper import (
    map_comparison_operator_by_value,
)
from app.application.mappers.event_field_mapper import (
    map_event_field_by_value,
)
from app.application.mappers.logical_operator_mapper import (
    map_logical_operator_by_value,
)
from app.domain.exceptions.condition_exception import ConditionException
from app.domain.value_objects.conditions.composite_condition import CompositeCondition
from app.domain.value_objects.conditions.condition import Condition
from app.domain.value_objects.conditions.simple_condition import SimpleCondition


class ConditionFactory:
    _builders: dict[str, Callable[..., Condition]] = {}

    @classmethod
    def _build_composite(
        cls, dto_condition: DTOCompositeCondition
    ) -> CompositeCondition:
        cls._validate_composite(dto_condition=dto_condition)

        conditions = [cls.build(dto_condition=c) for c in dto_condition["conditions"]]

        return CompositeCondition(
            operator=map_logical_operator_by_value(
                logical_operator_value=dto_condition["operator"]
            ),
            conditions=conditions,
        )

    @classmethod
    def _build_simple(cls, dto_condition: DTOSimpleCondition) -> SimpleCondition:
        cls._validate_simple(dto_condition=dto_condition)

        return SimpleCondition(
            operator=map_comparison_operator_by_value(
                comparison_operator_value=dto_condition["operator"]
            ),
            field=map_event_field_by_value(event_field_value=dto_condition["field"]),
            value=dto_condition["value"],
        )

    @classmethod
    def _init_builders(cls):
        if cls._builders:
            return

        cls._builders = {"composite": cls._build_composite, "simple": cls._build_simple}

    @classmethod
    def _validate(cls, dto_condition: DTOCondition) -> None:
        if dto_condition["type"] not in cls._builders:
            raise ConditionException.condition_type_is_invalid(
                details={"type": dto_condition["type"]}
            )

    @classmethod
    def _validate_composite(cls, dto_condition: DTOCompositeCondition) -> None:
        if len(dto_condition["conditions"]) < 2:
            raise ConditionException.condition_list_is_invalid(
                details={"conditions": dto_condition["conditions"]}
            )

    @classmethod
    def _validate_simple(cls, dto_condition: DTOSimpleCondition) -> None:
        if isinstance(dto_condition["value"], str) and not dto_condition["value"]:
            raise ConditionException.condition_value_cannot_be_empty(
                details={"value": dto_condition["value"]}
            )

    @classmethod
    def build(cls, dto_condition: DTOCondition) -> Condition:
        cls._init_builders()
        cls._validate(dto_condition=dto_condition)

        return cls._builders[dto_condition["type"]](dto_condition)
