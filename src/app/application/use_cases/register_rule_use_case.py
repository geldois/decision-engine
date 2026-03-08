from app.application.dto.register_rule_dto_request import RegisterRuleDtoRequest
from app.application.dto.register_rule_dto_response import RegisterRuleDtoResponse
from app.application.repositories.rule_repository_contract import RuleRepositoryContract
from app.domain.decisions.decision_outcome import DecisionOutcome
from app.domain.events.event import EventField
from app.domain.rules.rule import Rule, RuleOperator

class RegisterRuleUseCase:
    # initializer
    def __init__(
        self, 
        rule_repository: RuleRepositoryContract
    ):
        self.rule_repository = rule_repository

    # methods
    def register_rule(
        self, 
        register_rule_dto_request: RegisterRuleDtoRequest
    ) -> RegisterRuleDtoResponse:
        rule = Rule(
            name = register_rule_dto_request.name,
            condition_field = EventField(register_rule_dto_request.condition_field), 
            condition_operator = RuleOperator(register_rule_dto_request.condition_operator),
            condition_value = register_rule_dto_request.condition_value, 
            outcome = DecisionOutcome(register_rule_dto_request.outcome)
        )
        saved_rule = self.rule_repository.save(rule)
        register_rule_dto_response = RegisterRuleDtoResponse(
            rule_id = saved_rule._id, 
            outcome = saved_rule.outcome
        )

        return register_rule_dto_response
        