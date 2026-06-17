from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import select

from decision_engine.application.contracts.repository import RuleRepository
from decision_engine.infrastructure.persistence.sqlalchemy.mappers.sqlalchemy_rule_mapper import (  # noqa: E501
    domain_to_model,
    model_to_domain,
)
from decision_engine.infrastructure.persistence.sqlalchemy.models.rule_model import (
    RuleModel,
)

if TYPE_CHECKING:
    from uuid import UUID

    from sqlalchemy.orm import Session

    from decision_engine.domain.entities.rule import Rule


class SQLAlchemyRuleRepository(RuleRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, rule: Rule) -> Rule:
        rule_model = domain_to_model(rule=rule)
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
            return model_to_domain(rule_model=rule_model)

        return None

    def list_all(self) -> list[Rule]:
        rule_models = self.session.query(RuleModel).all()
        rules: list[Rule] = []

        for rule_model in rule_models:
            rule = model_to_domain(rule_model=rule_model)
            rules.append(rule)

        return rules
