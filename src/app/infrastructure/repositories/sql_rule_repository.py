from sqlalchemy import select
from sqlalchemy.orm import Session

from app.application.repositories.rule_repository_contract import RuleRepositoryContract
from app.domain.decisions.decision_outcome import DecisionOutcome
from app.domain.events.event import EventField
from app.domain.rules.rule import Rule, RuleOperator
from app.infrastructure.database.models import RuleModel

class SqlRuleRepository(RuleRepositoryContract):
    # initializer
    def __init__(
        self, 
        session: Session
    ):
        self.session = session
    
    # methods
    def convert_rule_model_to_rule(
        self, 
        rule_model: RuleModel
    ) -> Rule:
        rule = Rule(
                name = rule_model.name, 
                condition_field = EventField(rule_model.condition_field), 
                condition_operator = RuleOperator(rule_model.condition_operator), 
                condition_value = rule_model.condition_value_int if rule_model.condition_value_int else rule_model.condition_value_str, 
                outcome = DecisionOutcome(rule_model.outcome), 
                rule_id = rule_model.rule_id
            )
        
        return rule
    
    def convert_rule_to_rule_model(
        self, 
        rule: Rule
    ) -> RuleModel:
        rule_model = RuleModel(
            name = rule.name, 
            condition_field = rule.condition_field.value, 
            condition_operator = rule.condition_operator.value, 
            condition_value_int = rule.condition_value if isinstance(rule.condition_value, int) else None, 
            condition_value_str = rule.condition_value if isinstance(rule.condition_value, str) else None, 
            outcome = rule.outcome.value
        )

        return rule_model
    
    # interface methods
    def save(
        self, 
        rule: Rule
    ) -> Rule:
        rule_model = self.convert_rule_to_rule_model(rule)
        self.session.add(rule_model)
        self.session.flush()
        self.session.refresh(rule_model)
        rule.rule_id = rule_model.rule_id

        return rule

    def delete(
        self, 
        rule: Rule
    ) -> bool:
        rule_model = (
            self.session.execute(
                select(RuleModel).where(RuleModel.rule_id == rule.rule_id)
            )
            .scalars()
            .first()
        )
        
        if rule_model:
            self.session.delete(rule_model)

            return True
        
        return False

    def get_by_id(
        self, 
        rule_id: int
    ) -> Rule | None:
        rule_model = (
            self.session.execute(
                select(RuleModel).where(RuleModel.rule_id == rule_id)
            )
            .scalars()
            .first()
        )

        if rule_model:
            return self.convert_rule_model_to_rule(rule_model)
        
        return None

    def list_all(self) -> list[Rule]:
        rule_models = self.session.query(RuleModel).all()
        rules = []

        for rule_model in rule_models:
            rule = self.convert_rule_model_to_rule(rule_model)
            rules.append(rule)
        
        return []
    