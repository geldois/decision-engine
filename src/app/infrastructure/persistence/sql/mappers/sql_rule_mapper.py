from datetime import UTC

import app.infrastructure.serialization.condition_codec as ConditionCodec
from app.domain.entities.rule import Rule
from app.domain.value_objects.decision_outcome import DecisionOutcome
from app.infrastructure.database.models.rule_model import RuleModel


def domain_to_model(rule: Rule) -> RuleModel:
    rule_model = RuleModel(
        id=rule.id,
        name=rule.name,
        condition=ConditionCodec.ConditionSerializer().serialize(
            condition=rule.condition
        ),
        outcome=rule.outcome.value,
        priority=rule.priority,
        created_at=rule.created_at,
    )

    return rule_model


def model_to_domain(rule_model: RuleModel) -> Rule:
    created_at = (
        rule_model.created_at.replace(tzinfo=UTC)
        if rule_model.created_at.tzinfo is None
        else rule_model.created_at
    )

    rule = Rule(
        name=rule_model.name,
        condition=ConditionCodec.deserialize(condition=rule_model.condition),
        outcome=DecisionOutcome(rule_model.outcome),
        priority=rule_model.priority,
        created_at=created_at,
        rule_id=rule_model.id,
    )

    return rule
