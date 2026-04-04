from app.application.contracts.use_case_contract import UseCaseContract
from app.application.dto.dto_register_rule_request import DTORegisterRuleRequest
from app.application.dto.dto_register_rule_response import DTORegisterRuleResponse
from app.application.factories.condition_factory import ConditionFactory
from app.application.mappers.condition_mapper import ConditionMapper
from app.application.mappers.decision_outcome_mapper import (
    map_outcome_by_value,
)
from app.domain.entities.rule import Rule


class RegisterRuleUseCase(UseCaseContract):
    def execute(self, dto_request: DTORegisterRuleRequest) -> DTORegisterRuleResponse:
        with self.unit_of_work_factory() as unit_of_work:
            rule = Rule(
                name=dto_request.name,
                condition=ConditionFactory.build(dto_condition=dto_request.condition),
                outcome=map_outcome_by_value(dto_request.outcome),
                priority=dto_request.priority,
            )
            saved_rule = unit_of_work.rules.save(rule)

            return DTORegisterRuleResponse(
                name=saved_rule.name,
                condition=ConditionMapper.map_to_dict(condition=saved_rule.condition),
                outcome=saved_rule.outcome.value,
                priority=saved_rule.priority,
                rule_id=saved_rule.id,
            )
