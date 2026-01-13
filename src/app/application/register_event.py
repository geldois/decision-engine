from app.domain.events.event import Event
from app.infrastructure.repositories.event_repository import EventRepository
from app.infrastructure.repositories.rule_repository import RuleRepository
from app.services.decision_service import DecisionService

class RegisterEvent:
    # constructor
    def __init__(self, event_repository: EventRepository, rule_repository: RuleRepository, decision_service: DecisionService):
        self.event_repository = event_repository
        self.rule_repository = rule_repository
        self.decision_service = decision_service
    # methods
    def register_event(self, event_type: str, payload: dict, timestamp: int):
        event = Event(event_type, payload, timestamp)
        saved_event = self.event_repository.save(event)
        rules = self.rule_repository.list_all()
        decision = self.decision_service.decide(event, rules)
        return decision
    