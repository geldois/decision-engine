from __future__ import annotations

import structlog

from decision_engine.application.contracts.use_case import UseCase
from decision_engine.application.dto.responses.register_rule import (
    RegisterRuleDTOResponse,
)
from decision_engine.application.presenters.condition_presenter import (
    ConditionPresenter,
)

logger = structlog.get_logger()


class ListRulesUseCase(UseCase[None, list[RegisterRuleDTOResponse]]):
    def execute(self, dto: None) -> list[RegisterRuleDTOResponse]:  # noqa: ARG002
        with self.uow_factory() as uow:
            rules = uow.rules.list_all()

            logger.info("rules.listed", count=len(rules))

            return [
                RegisterRuleDTOResponse(
                    name=rule.name,
                    condition=ConditionPresenter.present(element=rule.condition),
                    outcome=rule.outcome.value,
                    priority=rule.priority,
                    rule_id=rule.id,
                )
                for rule in rules
            ]
