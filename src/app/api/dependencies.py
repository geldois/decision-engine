from app.infrastructure.repositories.in_memory_event_repository import InMemoryEventRepository
from app.infrastructure.repositories.in_memory_rule_repository import InMemoryRuleRepository
from app.domain.services.decision_engine import DecisionEngine
from app.application.use_cases.register_event_use_case import RegisterEventUseCase
from app.infrastructure.repositories.sql_event_repository import SqlEventRepository

def get_register_event_use_case() -> RegisterEventUseCase:
    event_repository = SqlEventRepository()
    rule_repository = InMemoryRuleRepository()
    decision_engine = DecisionEngine()

    return RegisterEventUseCase(
        event_repository = event_repository,
        rule_repository = rule_repository,
        decision_engine = decision_engine
    )
