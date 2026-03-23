from app.application.contracts.use_case_contract import UseCaseContract
from app.application.dto.dto_register_rule_request import DTORegisterRuleRequest
from app.application.dto.dto_register_rule_response import DTORegisterRuleResponse
from app.application.mappers.decision_outcome_mapper import (
    map_outcome_by_value,
)
from app.application.mappers.event_field_mapper import (
    map_event_field_by_value,
)
from app.application.mappers.rule_operator_mapper import map_rule_operator_by_value
from app.domain.entities.rule import Rule


class RegisterRuleUseCase(UseCaseContract):
    def execute(self, dto_request: DTORegisterRuleRequest) -> DTORegisterRuleResponse:
        with self.unit_of_work_factory() as unit_of_work:
            rule = Rule(
                name=dto_request.name,
                condition_field=map_event_field_by_value(dto_request.condition_field),
                condition_operator=map_rule_operator_by_value(
                    dto_request.condition_operator
                ),
                condition_value=dto_request.condition_value,
                outcome=map_outcome_by_value(dto_request.outcome),
            )
            saved_rule = unit_of_work.rules.save(rule)

            return DTORegisterRuleResponse(
                name=saved_rule.name,
                outcome=saved_rule.outcome,
                rule_id=saved_rule.id,
            )
