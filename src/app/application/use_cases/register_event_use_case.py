from app.domain.events.event import Event
from app.domain.services.decision_engine import DecisionEngine
from app.application.repositories.event_repository_contract import EventRepositoryContract
from app.application.repositories.rule_repository_contract import RuleRepositoryContract
from app.application.dto.register_event_request import RegisterEventRequest
from app.application.dto.register_event_response import RegisterEventResponse
from app.application.mappers.decision_outcome_to_status_mapper import map_outcome_to_status

class RegisterEventUseCase:
    # initializer
    def __init__(
        self, event_repository: EventRepositoryContract, 
        rule_repository: RuleRepositoryContract, 
        decision_engine: DecisionEngine
    ):
        self.event_repository = event_repository
        self.rule_repository = rule_repository
        self.decision_engine = decision_engine
    
    # methods
    def register_event(
        self, 
        register_event_request: RegisterEventRequest
    ) -> RegisterEventResponse:
        event = Event(
            event_type = register_event_request.event_type, 
            payload = register_event_request.payload, 
            timestamp = register_event_request.timestamp
        )
        saved_event = self.event_repository.save(event)
        rules = self.rule_repository.list_all()
        decision = self.decision_engine.decide(
            event = event, 
            rules = rules
        )
        decision_status = map_outcome_to_status(decision.outcome)
        register_event_response = RegisterEventResponse(
            event_id = saved_event.event_id, 
            status = decision_status
        )

        return register_event_response
    