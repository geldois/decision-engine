from app.application.dto.register_rule_dto_request import RegisterRuleDtoRequest
from app.application.use_cases.register_rule_use_case import RegisterRuleUseCase
from app.domain.entities.decisions.decision_outcome import DecisionOutcome
from app.infrastructure.repositories.in_memory_rule_repository import InMemoryRuleRepository

# tests
def test_register_rule_use_case_returns_correct_dto_response():
    register_rule_use_case = RegisterRuleUseCase(rule_repository = InMemoryRuleRepository())
    register_rule_dto_request = RegisterRuleDtoRequest(
        name = "ALWAYS_APPLIES", 
        condition_field = "event_type", 
        condition_operator = "==", 
        condition_value = "USER_CREATED", 
        outcome = "approved"
    )

    register_rule_dto_response = register_rule_use_case.register_rule(register_rule_dto_request = register_rule_dto_request)

    assert register_rule_dto_response.rule_id

    assert register_rule_dto_response.name == register_rule_dto_request.name

    assert DecisionOutcome(register_rule_dto_response.outcome)
