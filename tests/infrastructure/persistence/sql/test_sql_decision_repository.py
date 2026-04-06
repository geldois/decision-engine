from utils.domain_entity_util import compare_domain_entities

from app.bootstrap.bootstrap import build_dev_session_factory
from app.domain.entities.event import Event
from app.domain.entities.rule import Rule
from app.domain.services.decision_engine import DecisionEngine
from app.domain.value_objects.decision_outcome import DecisionOutcome
from app.domain.value_objects.event_field import EventField
from app.domain.value_objects.operators.comparison_operator import ComparisonOperator
from app.infrastructure.persistence.sql.repositories.sql_decision_repository import (
    SqlDecisionRepository,
)


# ==========
# valid cases
# ==========
def test_sql_decision_repository_returns_saved_decision() -> None:
    event = Event(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        occurred_at=1700000000,
    )
    rule = Rule(
        name="ALWAYS_APPLIES",
        condition_field=EventField.EVENT_TYPE,
        condition_operator=ComparisonOperator.EQUALS,
        condition_value="USER_CREATED",
        outcome=DecisionOutcome.APPROVED,
        priority=0,
    )
    decision_engine = DecisionEngine()
    decision = decision_engine.decide(event=event, rules=[rule])
    session_factory = build_dev_session_factory()
    decision_repository = SqlDecisionRepository(session=session_factory())

    saved_decision = decision_repository.save(decision=decision)

    assert saved_decision is decision


def test_sql_decision_repository_returns_decision_when_id_exists() -> None:
    event = Event(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        occurred_at=1700000000,
    )
    rule = Rule(
        name="ALWAYS_APPLIES",
        condition_field=EventField.EVENT_TYPE,
        condition_operator=ComparisonOperator.EQUALS,
        condition_value="USER_CREATED",
        outcome=DecisionOutcome.APPROVED,
        priority=0,
    )
    decision_engine = DecisionEngine()
    decision = decision_engine.decide(event=event, rules=[rule])
    session_factory = build_dev_session_factory()
    decision_repository = SqlDecisionRepository(session=session_factory())
    decision_repository.save(decision=decision)

    returned_decision = decision_repository.get_by_id(decision_id=decision.id)

    assert compare_domain_entities(a=returned_decision, b=decision)


def test_sql_decision_repository_returns_none_when_id_does_not_exist() -> None:
    event = Event(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        occurred_at=1700000000,
    )
    rule = Rule(
        name="ALWAYS_APPLIES",
        condition_field=EventField.EVENT_TYPE,
        condition_operator=ComparisonOperator.EQUALS,
        condition_value="USER_CREATED",
        outcome=DecisionOutcome.APPROVED,
        priority=0,
    )
    decision_engine = DecisionEngine()
    decision = decision_engine.decide(event=event, rules=[rule])
    session_factory = build_dev_session_factory()
    decision_repository = SqlDecisionRepository(session=session_factory())

    returned_decision = decision_repository.get_by_id(decision_id=decision.id)

    assert not returned_decision


def test_sql_decision_repository_returns_true_when_decision_is_deleted() -> None:
    event = Event(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        occurred_at=1700000000,
    )
    rule = Rule(
        name="ALWAYS_APPLIES",
        condition_field=EventField.EVENT_TYPE,
        condition_operator=ComparisonOperator.EQUALS,
        condition_value="USER_CREATED",
        outcome=DecisionOutcome.APPROVED,
        priority=0,
    )
    decision_engine = DecisionEngine()
    decision = decision_engine.decide(event=event, rules=[rule])
    session_factory = build_dev_session_factory()
    decision_repository = SqlDecisionRepository(session=session_factory())
    decision_repository.save(decision=decision)

    it_was_deleted = decision_repository.delete(decision=decision)

    returned_decision = decision_repository.get_by_id(decision_id=decision.id)

    assert it_was_deleted

    assert not returned_decision


def test_sql_decision_repository_returns_false_when_decision_is_not_deleted() -> None:
    event = Event(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        occurred_at=1700000000,
    )
    rule = Rule(
        name="ALWAYS_APPLIES",
        condition_field=EventField.EVENT_TYPE,
        condition_operator=ComparisonOperator.EQUALS,
        condition_value="USER_CREATED",
        outcome=DecisionOutcome.APPROVED,
        priority=0,
    )
    decision_engine = DecisionEngine()
    decision = decision_engine.decide(event=event, rules=[rule])
    session_factory = build_dev_session_factory()
    decision_repository = SqlDecisionRepository(session=session_factory())

    it_was_deleted = decision_repository.delete(decision=decision)

    assert not it_was_deleted


def test_sql_decision_repository_returns_list_of_decisions() -> None:
    event = Event(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        occurred_at=1700000000,
    )
    rule = Rule(
        name="ALWAYS_APPLIES",
        condition_field=EventField.EVENT_TYPE,
        condition_operator=ComparisonOperator.EQUALS,
        condition_value="USER_CREATED",
        outcome=DecisionOutcome.APPROVED,
        priority=0,
    )
    decision_engine = DecisionEngine()
    decision = decision_engine.decide(event=event, rules=[rule])
    session_factory = build_dev_session_factory()
    decision_repository = SqlDecisionRepository(session=session_factory())
    decision_repository.save(decision=decision)

    decisions = decision_repository.list_all()

    assert isinstance(decisions, list)

    for d in decisions:
        if d.id == decision.id:
            assert compare_domain_entities(a=d, b=decision)
