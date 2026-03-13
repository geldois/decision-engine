from app.domain.entities.decisions.decision_outcome import DecisionOutcome
from app.domain.entities.events.event import Event, ExposibleEventField
from app.domain.entities.rules.rule import Rule, RuleOperator
from app.domain.services.decision_engine import DecisionEngine
from app.infrastructure.persistence.in_memory.repositories.in_memory_decision_repository import (
    InMemoryDecisionRepository,
)
from app.infrastructure.persistence.in_memory.repositories.in_memory_event_repository import (
    InMemoryEventRepository,
)
from app.infrastructure.persistence.in_memory.repositories.in_memory_rule_repository import (
    InMemoryRuleRepository,
)
from app.infrastructure.persistence.in_memory.storage.in_memory_storage import (
    InMemoryStorage,
)
from app.infrastructure.persistence.in_memory.unit_of_work.in_memory_unit_of_work import (
    InMemoryUnitOfWork,
)


# ==========
# valid
# ==========
def test_in_memory_unit_of_work_commits():
    event = Event(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        timestamp=1700000000,
    )
    rule = Rule(
        name="ALWAYS_APPLIES",
        condition_field=ExposibleEventField.EVENT_TYPE,
        condition_operator=RuleOperator.EQUALS,
        condition_value="USER_CREATED",
        outcome=DecisionOutcome.APPROVED,
    )
    decision_engine = DecisionEngine()
    decision = decision_engine.decide(event=event, rules=[rule])
    in_memory_storage = InMemoryStorage()
    in_memory_unit_of_work = InMemoryUnitOfWork(
        in_memory_storage=in_memory_storage,
        decision_repository_factory=InMemoryDecisionRepository,
        event_repository_factory=InMemoryEventRepository,
        rule_repository_factory=InMemoryRuleRepository,
    )

    assert not in_memory_storage.events

    assert not in_memory_storage.rules

    assert not in_memory_storage.decisions

    try:
        with in_memory_unit_of_work:
            in_memory_unit_of_work.events.save(event=event)
            in_memory_unit_of_work.rules.save(rule=rule)
            in_memory_unit_of_work.decisions.save(decision=decision)
    except Exception:
        pass

    assert event.id in in_memory_storage.events

    assert rule.id in in_memory_storage.rules

    assert decision.id in in_memory_storage.decisions


# ==========
# invalid
# ==========
def test_in_memory_unit_of_work_rolls_back():
    event = Event(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        timestamp=1700000000,
    )
    rule = Rule(
        name="ALWAYS_APPLIES",
        condition_field=ExposibleEventField.EVENT_TYPE,
        condition_operator=RuleOperator.EQUALS,
        condition_value="USER_CREATED",
        outcome=DecisionOutcome.APPROVED,
    )
    decision_engine = DecisionEngine()
    decision = decision_engine.decide(event=event, rules=[rule])
    in_memory_storage = InMemoryStorage()
    in_memory_unit_of_work = InMemoryUnitOfWork(
        in_memory_storage=in_memory_storage,
        decision_repository_factory=InMemoryDecisionRepository,
        event_repository_factory=InMemoryEventRepository,
        rule_repository_factory=InMemoryRuleRepository,
    )

    assert not in_memory_storage.events

    assert not in_memory_storage.rules

    assert not in_memory_storage.decisions

    try:
        with in_memory_unit_of_work:
            in_memory_unit_of_work.events.save(event=event)
            in_memory_unit_of_work.rules.save(rule=rule)
            in_memory_unit_of_work.decisions.save(decision=decision)

            raise Exception
    except Exception:
        pass

    assert not in_memory_storage.events

    assert not in_memory_storage.rules

    assert not in_memory_storage.decisions
