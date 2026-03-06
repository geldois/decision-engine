from app.application.dto.register_rule_request import RegisterRuleRequest
from app.application.use_cases.register_rule_use_case import RegisterRuleUseCase
from app.domain.decisions.decision_outcome import DecisionOutcome
from app.infrastructure.repositories.in_memory_rule_repository import InMemoryRuleRepository

# tests
def test_register_rule_use_case_returns_response_with_outcome():
    name = "ALWAYS_APPLIES"
    condition_field = "event_type"
    condition_operator = "=="
    condition_value = "USER_CREATED"
    outcome = "approved"
    rule_repository = InMemoryRuleRepository()
    register_rule_use_case = RegisterRuleUseCase(rule_repository)
    register_rule_request = RegisterRuleRequest(
        name = name, 
        condition_field = condition_field, 
        condition_operator = condition_operator, 
        condition_value = condition_value, 
        outcome = outcome
    )

    register_rule_response = register_rule_use_case.register_rule(register_rule_request)

    assert register_rule_response.rule_id is not None

    assert DecisionOutcome(register_rule_response.outcome)
