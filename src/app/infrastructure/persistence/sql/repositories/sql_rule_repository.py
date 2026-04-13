from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

import app.infrastructure.persistence.sql.mappers.sql_rule_mapper as SQLRuleMapper
from app.application.contracts.repositories.rule_repository_contract import (
    RuleRepositoryContract,
)
from app.domain.entities.rule import Rule
from app.infrastructure.database.models.rule_model import RuleModel


class SQLRuleRepository(RuleRepositoryContract):
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, rule: Rule) -> Rule:
        rule_model = SQLRuleMapper.domain_to_model(rule=rule)
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
            return SQLRuleMapper.model_to_domain(rule_model=rule_model)

        return None

    def list_all(self) -> list[Rule]:
        rule_models = self.session.query(RuleModel).all()
        rules: list[Rule] = []

        for rule_model in rule_models:
            rule = SQLRuleMapper.model_to_domain(rule_model=rule_model)
            rules.append(rule)

        return rules
