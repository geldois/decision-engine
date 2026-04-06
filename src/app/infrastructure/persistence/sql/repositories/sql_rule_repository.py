from datetime import UTC
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.application.contracts.repositories.rule_repository_contract import (
    RuleRepositoryContract,
)
from app.domain.entities.rule import Rule
from app.domain.value_objects.decision_outcome import DecisionOutcome
from app.domain.value_objects.event_field import EventField
from app.domain.value_objects.operators.comparison_operator import ComparisonOperator
from app.infrastructure.database.models.rule_model import RuleModel


class SqlRuleRepository(RuleRepositoryContract):
    def __init__(self, session: Session) -> None:
        self.session = session

    def convert_rule_model_to_rule(self, rule_model: RuleModel) -> Rule:
        created_at = (
            rule_model.created_at.replace(tzinfo=UTC)
            if rule_model.created_at.tzinfo is None
            else rule_model.created_at
        )

        rule = Rule(
            name=rule_model.name,
            condition=EventField(rule_model.condition_field),
            condition_operator=ComparisonOperator(rule_model.condition_operator),
            condition_value=rule_model.condition_value_int
            if rule_model.condition_value_int
            else rule_model.condition_value_str,
            outcome=DecisionOutcome(rule_model.outcome),
            priority=rule_model.priority,
            created_at=created_at,
            rule_id=rule_model.id,
        )

        return rule

    def convert_rule_to_rule_model(self, rule: Rule) -> RuleModel:
        rule_model = RuleModel(
            id=rule.id,
            name=rule.name,
            condition_field=rule.condition.value,
            condition_operator=rule.condition_operator.value,
            condition_value_int=rule.condition_value
            if isinstance(rule.condition_value, int)
            else None,
            condition_value_str=rule.condition_value
            if isinstance(rule.condition_value, str)
            else None,
            outcome=rule.outcome.value,
            priority=rule.priority,
            created_at=rule.created_at,
        )

        return rule_model

    def save(self, rule: Rule) -> Rule:
        rule_model = self.convert_rule_to_rule_model(rule=rule)
        self.session.add(rule_model)
        self.session.flush()
        self.session.refresh(rule_model)

        return rule

    def delete(self, rule: Rule) -> bool:
        rule_model = (
            self.session.execute(select(RuleModel).where(RuleModel.id == rule.id))
            .scalars()
            .first()
        )

        if rule_model:
            self.session.delete(rule_model)
            self.session.flush()

            return True

        return False

    def get_by_id(self, rule_id: UUID) -> Rule | None:
        rule_model = (
            self.session.execute(select(RuleModel).where(RuleModel.id == rule_id))
            .scalars()
            .first()
        )

        if rule_model:
            return self.convert_rule_model_to_rule(rule_model=rule_model)

        return None

    def list_all(self) -> list[Rule]:
        rule_models = self.session.query(RuleModel).all()
        rules: list[Rule] = []

        for rule_model in rule_models:
            rule = self.convert_rule_model_to_rule(rule_model=rule_model)
            rules.append(rule)

        return rules
