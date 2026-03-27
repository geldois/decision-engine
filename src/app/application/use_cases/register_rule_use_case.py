from app.application.contracts.use_case_contract import UseCaseContract
from app.application.dto.register_rule_dto_request import RegisterRuleDtoRequest
from app.application.dto.register_rule_dto_response import RegisterRuleDtoResponse
from app.application.mappers.decision_result_mapper import (
    map_outcome_to_result,
    map_result_to_outcome,
)
from app.application.mappers.exponible_event_field_mapper import (
    map_exponible_event_field_to_domain,
)
from app.application.mappers.rule_operator_mapper import map_rule_operator_to_domain
from app.domain.entities.rule import Rule


class RegisterRuleUseCase(UseCaseContract):
    def execute(self, dto_request: RegisterRuleDtoRequest) -> RegisterRuleDtoResponse:
        with self.unit_of_work_factory() as unit_of_work:
            rule = Rule(
                name=dto_request.name,
                condition_field=map_exponible_event_field_to_domain(
                    dto_request.condition_field
                ),
                condition_operator=map_rule_operator_to_domain(
                    dto_request.condition_operator
                ),
                condition_value=dto_request.condition_value,
                outcome=map_result_to_outcome(dto_request.outcome),
            )
            saved_rule = unit_of_work.rules.save(rule)

            return RegisterRuleDtoResponse(
                name=saved_rule.name,
                outcome=map_outcome_to_result(saved_rule.outcome),
                rule_id=saved_rule.id,
            )
