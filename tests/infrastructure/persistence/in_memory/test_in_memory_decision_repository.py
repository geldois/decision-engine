from app.domain.entities.decisions.decision_outcome import DecisionOutcome
from app.domain.entities.events.event import Event, ExposibleEventField
from app.domain.entities.rules.rule import Rule, RuleOperator
from app.domain.services.decision_engine import DecisionEngine
from app.infrastructure.persistence.in_memory.repositories.in_memory_decision_repository import (
    InMemoryDecisionRepository,
)
from app.infrastructure.persistence.in_memory.storage.in_memory_storage import (
    InMemoryStorage,
)


# ==========
# valid
# ==========
def test_in_memory_decision_repository_returns_saved_decision():
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
    decision_repository = InMemoryDecisionRepository(
        in_memory_storage=InMemoryStorage()
    )

    saved_decision = decision_repository.save(decision=decision)

    assert saved_decision is decision


def test_in_memory_decision_repository_returns_decision_when_id_exists():
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
    decision_repository = InMemoryDecisionRepository(
        in_memory_storage=InMemoryStorage()
    )
    decision_repository.save(decision=decision)

    returned_decision = decision_repository.get_by_id(decision_id=decision.id)

    assert returned_decision is decision


def test_in_memory_decision_repository_returns_none_when_id_does_not_exist():
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
    decision_repository = InMemoryDecisionRepository(
        in_memory_storage=InMemoryStorage()
    )

    returned_decision = decision_repository.get_by_id(decision_id=decision.id)

    assert not returned_decision


def test_in_memory_decision_repository_returns_true_when_decision_is_deleted():
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
    decision_repository = InMemoryDecisionRepository(
        in_memory_storage=InMemoryStorage()
    )
    decision_repository.save(decision=decision)

    it_was_deleted = decision_repository.delete(decision=decision)

    returned_decision = decision_repository.get_by_id(decision_id=decision.id)

    assert it_was_deleted

    assert not returned_decision


def test_in_memory_decision_repository_returns_false_when_decision_is_not_deleted():
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
    decision_repository = InMemoryDecisionRepository(
        in_memory_storage=InMemoryStorage()
    )

    it_was_deleted = decision_repository.delete(decision=decision)

    assert not it_was_deleted


def test_in_memory_decision_repository_returns_list_of_decisions():
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
    decision_repository = InMemoryDecisionRepository(
        in_memory_storage=InMemoryStorage()
    )
    decision_repository.save(decision=decision)

    decisions = decision_repository.list_all()

    assert isinstance(decisions, list)

    assert decision in decisions
