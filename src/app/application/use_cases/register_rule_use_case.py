import app.application.factories.condition_factory as ConditionFactory
from app.application.contracts.use_case import UseCase
from app.application.dto.dto_register_rule_request import DTORegisterRuleRequest
from app.application.dto.dto_register_rule_response import DTORegisterRuleResponse
from app.application.mappers.decision_outcome_mapper import (
    parse_decision_outcome,
)
from app.application.presenters.condition_presenter import ConditionPresenter
from app.domain.entities.rule import Rule


class RegisterRuleUseCase(UseCase[DTORegisterRuleRequest, DTORegisterRuleResponse]):
    def execute(self, dto: DTORegisterRuleRequest) -> DTORegisterRuleResponse:
        with self.uow_factory() as uow:
            rule = Rule(
                name=dto.name,
                condition=ConditionFactory.build_condition(dto=dto.condition),
                outcome=parse_decision_outcome(dto.outcome),
                priority=dto.priority,
            )
            saved_rule = uow.rules.save(rule=rule)

            return DTORegisterRuleResponse(
                name=saved_rule.name,
                condition=ConditionPresenter.present(element=saved_rule.condition),
                outcome=saved_rule.outcome.value,
                priority=saved_rule.priority,
                rule_id=saved_rule.id,
            )
