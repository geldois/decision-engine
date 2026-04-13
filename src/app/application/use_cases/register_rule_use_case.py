import app.application.factories.condition_factory as ConditionFactory
import app.application.mappers.decision_outcome_mapper as DecisionOutcomeMapper
from app.application.contracts.use_case_contract import UseCaseContract
from app.application.dto.dto_register_rule_request import DTORegisterRuleRequest
from app.application.dto.dto_register_rule_response import DTORegisterRuleResponse
from app.application.presenters.condition_presenter import ConditionPresenter
from app.domain.entities.rule import Rule


class RegisterRuleUseCase(
    UseCaseContract[DTORegisterRuleRequest, DTORegisterRuleResponse]
):
    def execute(self, dto: DTORegisterRuleRequest) -> DTORegisterRuleResponse:
        with self.unit_of_work_factory() as unit_of_work:
            rule = Rule(
                name=dto.name,
                condition=ConditionFactory.build(dto=dto.condition),
                outcome=DecisionOutcomeMapper.parse_decision_outcome(dto.outcome),
                priority=dto.priority,
            )
            saved_rule = unit_of_work.rules.save(rule=rule)

            return DTORegisterRuleResponse(
                name=saved_rule.name,
                condition=ConditionPresenter().present(element=saved_rule.condition),
                outcome=saved_rule.outcome.value,
                priority=saved_rule.priority,
                rule_id=saved_rule.id,
            )
