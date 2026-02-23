from app.domain.events.event import Event
from app.application.repositories.event_repository_contract import EventRepositoryContract
from app.application.repositories.rule_repository_contract import RuleRepositoryContract
from app.services.decision_service import DecisionService
from app.application.dto.decision_status import DecisionStatus
from app.application.dto.register_event_request import RegisterEventRequest
from app.application.dto.register_event_response import RegisterEventResponse

class RegisterEvent:
    # constructor
    def __init__(
        self, event_repository: EventRepositoryContract, 
        rule_repository: RuleRepositoryContract, 
        decision_service: DecisionService
    ):
        self.event_repository = event_repository
        self.rule_repository = rule_repository
        self.decision_service = decision_service
    
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
        decision = self.decision_service.decide(
            event = event, 
            rules = rules
        )
        decision_status = DecisionStatus(decision.outcome)
        register_event_response = RegisterEventResponse(
            event_id = saved_event.event_id, 
            status = decision_status
        )

        return register_event_response
    