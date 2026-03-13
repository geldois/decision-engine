from app.application.dto.register_rule_dto_request import RegisterRuleDtoRequest
from app.application.dto.register_rule_dto_response import RegisterRuleDtoResponse
from app.application.mappers.decision_result_mapper import map_outcome_to_result, map_result_to_outcome
from app.application.mappers.event_field_mapper import map_event_field_to_domain
from app.application.mappers.rule_operator_mapper import map_rule_operator_to_domain
from app.application.repositories.rule_repository_contract import RuleRepositoryContract
from app.domain.entities.rules.rule import Rule

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
            condition_field = map_event_field_to_domain(register_rule_dto_request.condition_field), 
            condition_operator = map_rule_operator_to_domain(register_rule_dto_request.condition_operator), 
            condition_value = register_rule_dto_request.condition_value, 
            outcome = map_result_to_outcome(register_rule_dto_request.outcome)
        )
        saved_rule = self.rule_repository.save(rule)

        return RegisterRuleDtoResponse(
            name = saved_rule.name, 
            outcome = map_outcome_to_result(saved_rule.outcome), 
            rule_id = saved_rule._id
        )
        