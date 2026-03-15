from app.application.dto.produce_decision_dto_request import ProduceDecisionDtoRequest
from app.application.dto.produce_decision_dto_response import ProduceDecisionDtoResponse
from app.application.mappers.decision_result_mapper import map_outcome_to_result
from app.application.repositories.decision_repository_contract import (
    DecisionRepositoryContract,
)
from app.application.repositories.event_repository_contract import (
    EventRepositoryContract,
)
from app.application.repositories.rule_repository_contract import RuleRepositoryContract
from app.domain.services.decision_engine import DecisionEngine


class ProduceDecisionUseCase:
    def __init__(
        self,
        decision_repository: DecisionRepositoryContract,
        event_repository: EventRepositoryContract,
        rule_repository: RuleRepositoryContract,
        decision_engine: DecisionEngine,
    ):
        self.decision_repository = decision_repository
        self.event_repository = event_repository
        self.rule_repository = rule_repository
        self.decision_engine = decision_engine

    def produce_decision(
        self, produce_decision_dto_request: ProduceDecisionDtoRequest
    ) -> ProduceDecisionDtoResponse:
        event = self.event_repository.get_by_id(
            event_id=produce_decision_dto_request.event_id
        )
        rules = self.rule_repository.list_all()
        if not event:
            raise ValueError("Event not found in ProduceDecisionUseCase")
        decision = self.decision_engine.decide(event=event, rules=rules)
        saved_decision = self.decision_repository.save(decision=decision)

        return ProduceDecisionDtoResponse(
            event_id=saved_decision.event_id,
            rule_id=saved_decision.rule_id,
            status=map_outcome_to_result(saved_decision.outcome),
            explanation=saved_decision.explanation,
            decision_id=saved_decision._id,
        )
