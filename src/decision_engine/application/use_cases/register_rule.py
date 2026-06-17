from __future__ import annotations

import decision_engine.application.factories.condition_factory as ConditionFactory
from decision_engine.application.contracts.use_case import UseCase
from decision_engine.application.dto.requests.register_rule import (
    RegisterRuleDTORequest,
)
from decision_engine.application.dto.responses.register_rule import (
    RegisterRuleDTOResponse,
)
from decision_engine.application.mappers.decision_outcome_mapper import (
    parse_decision_outcome,
)
from decision_engine.application.presenters.condition_presenter import (
    ConditionPresenter,
)
from decision_engine.domain.entities.rule import Rule


class RegisterRuleUseCase(UseCase[RegisterRuleDTORequest, RegisterRuleDTOResponse]):
    def execute(self, dto: RegisterRuleDTORequest) -> RegisterRuleDTOResponse:
        with self.uow_factory() as uow:
            rule = Rule(
                name=dto.name,
                condition=ConditionFactory.build_condition(dto=dto.condition),
                outcome=parse_decision_outcome(dto.outcome),
                priority=dto.priority,
            )
            saved_rule = uow.rules.save(rule=rule)

            return RegisterRuleDTOResponse(
                name=saved_rule.name,
                condition=ConditionPresenter.present(element=saved_rule.condition),
                outcome=saved_rule.outcome.value,
                priority=saved_rule.priority,
                rule_id=saved_rule.id,
            )
