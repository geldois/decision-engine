from __future__ import annotations

from decision_engine.domain.entities.rule import Rule
from decision_engine.domain.value_objects.decision_outcome import DecisionOutcome
from decision_engine.infrastructure.persistence.sqlalchemy.codecs.condition_codec import (
    ConditionDeserializer,
    ConditionSerializer,
)
from decision_engine.infrastructure.persistence.sqlalchemy.models.rule_model import (
    RuleModel,
)


def domain_to_model(rule: Rule) -> RuleModel:
    rule_model = RuleModel(
        id=rule.id,
        name=rule.name,
        condition=ConditionSerializer.serialize(condition=rule.condition),
        outcome=rule.outcome.value,
        priority=rule.priority,
        created_at=rule.created_at,
    )

    return rule_model


def model_to_domain(rule_model: RuleModel) -> Rule:
    rule = Rule(
        name=rule_model.name,
        condition=ConditionDeserializer.deserialize(data=rule_model.condition),
        outcome=DecisionOutcome(rule_model.outcome),
        priority=rule_model.priority,
        created_at=rule_model.created_at,
        rule_id=rule_model.id,
    )

    return rule
