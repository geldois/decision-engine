from app.infrastructure.repositories.in_memory_event_repository import InMemoryEventRepository
from app.infrastructure.repositories.in_memory_rule_repository import InMemoryRuleRepository
from app.domain.services.decision_engine import DecisionEngine
from app.application.use_cases.register_event import RegisterEvent
from app.infrastructure.repositories.sql_event_repository import SqlEventRepository

def get_register_event_use_case() -> RegisterEvent:
    event_repository = SqlEventRepository()
    rule_repository = InMemoryRuleRepository()
    decision_service = DecisionEngine()

    return RegisterEvent(
        event_repository = event_repository,
        rule_repository = rule_repository,
        decision_service = decision_service
    )
