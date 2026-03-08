from app.application.dto.produce_decision_dto_request import ProduceDecisionDtoRequest
from app.application.dto.produce_decision_dto_response import ProduceDecisionDtoResponse
from app.application.mappers.decision_outcome_to_status_mapper import map_outcome_to_status
from app.application.repositories.event_repository_contract import EventRepositoryContract
from app.application.repositories.rule_repository_contract import RuleRepositoryContract
from app.domain.events.event import Event
from app.domain.services.decision_engine import DecisionEngine

class ProduceDecisionUseCase:
    # initializer
    def __init__(
        self, 
        event_repository: EventRepositoryContract, 
        rule_repository: RuleRepositoryContract, 
        decision_engine: DecisionEngine,
    ):
        self.event_repository = event_repository
        self.rule_repository = rule_repository
        self.decision_engine = decision_engine
    
    # methods
    def produce_decision(
        self, 
        produce_decision_dto_request: ProduceDecisionDtoRequest
    ) -> ProduceDecisionDtoResponse:
        event = Event(
            event_type = produce_decision_dto_request.event_type, 
            payload = produce_decision_dto_request.payload, 
            timestamp = produce_decision_dto_request.timestamp
        )
        saved_event = self.event_repository.save(event)
        rules = self.rule_repository.list_all()
        decision = self.decision_engine.decide(
            event = event, 
            rules = rules
        )
        decision_status = map_outcome_to_status(decision.outcome)
        produce_decision_dto_response = ProduceDecisionDtoResponse(
            event_id = saved_event._id, 
            status = decision_status
        )

        return produce_decision_dto_response
        