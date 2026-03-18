from app.infrastructure.database.engine import SessionLocal
from utils.domain_entity_util import assert_domain_entities_equal_structurally

from app.domain.entities.decisions.decision_outcome import DecisionOutcome
from app.domain.entities.events.event import Event, EventField
from app.domain.entities.rules.rule import Rule, RuleOperator
from app.domain.services.decision_engine import DecisionEngine
from app.infrastructure.persistence.sql.repositories.sql_decision_repository import (
    SqlDecisionRepository,
)


def test_sql_decision_repository_assigns_correct_ids_when_decision_is_saved_with_rule():
    event = Event(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        timestamp=1700000000,
    )
    rule = Rule(
        name="ALWAYS_APPLIES",
        condition_field=EventField.EVENT_TYPE,
        condition_operator=RuleOperator.EQUALS,
        condition_value="USER_CREATED",
        outcome=DecisionOutcome.APPROVED,
    )
    decision_engine = DecisionEngine()
    decision = decision_engine.decide(event=event, rules=[rule])
    decision_repository = SqlDecisionRepository(session=SessionLocal())

    saved_decision = decision_repository.save(decision=decision)

    assert saved_decision is decision

    assert saved_decision._id and saved_decision.event_id and saved_decision.rule_id

    assert saved_decision._id == decision._id

    assert saved_decision.event_id == event._id

    assert saved_decision.rule_id == rule._id


def test_sql_decision_repository_assigns_correct_ids_when_decision_is_saved_without_rule():
    event = Event(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        timestamp=1700000000,
    )
    decision_engine = DecisionEngine()
    decision = decision_engine.decide(event=event, rules=[])
    decision_repository = SqlDecisionRepository(session=SessionLocal())

    saved_decision = decision_repository.save(decision=decision)

    assert saved_decision is decision

    assert saved_decision._id and saved_decision.event_id and not saved_decision.rule_id

    assert saved_decision._id == decision._id

    assert saved_decision.event_id == event._id


def test_sql_decision_repository_assigns_correct_outcome_when_decision_is_saved_without_rule():
    event = Event(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        timestamp=1700000000,
    )
    rule = Rule(
        name="ALWAYS_APPLIES",
        condition_field=EventField.EVENT_TYPE,
        condition_operator=RuleOperator.EQUALS,
        condition_value="USER_CREATED",
        outcome=DecisionOutcome.APPROVED,
    )
    decision_engine = DecisionEngine()
    decision = decision_engine.decide(event=event, rules=[rule])
    decision_repository = SqlDecisionRepository(session=SessionLocal())

    saved_decision = decision_repository.save(decision=decision)

    assert saved_decision.outcome is rule.outcome


def test_in_memory_decision_repository_assigns_correct_outcome_when_decision_is_saved_without_rule():
    event = Event(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        timestamp=1700000000,
    )
    decision_engine = DecisionEngine()
    decision = decision_engine.decide(event=event, rules=[])
    decision_repository = SqlDecisionRepository(session=SessionLocal())

    saved_decision = decision_repository.save(decision=decision)

    assert saved_decision.outcome is DecisionOutcome.NO_MATCH


def test_sql_decision_repository_returns_true_when_decision_is_deleted():
    event = Event(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        timestamp=1700000000,
    )
    rule = Rule(
        name="ALWAYS_APPLIES",
        condition_field=EventField.EVENT_TYPE,
        condition_operator=RuleOperator.EQUALS,
        condition_value="USER_CREATED",
        outcome=DecisionOutcome.APPROVED,
    )
    decision_engine = DecisionEngine()
    decision = decision_engine.decide(event=event, rules=[rule])
    decision_repository = SqlDecisionRepository(session=SessionLocal())

    saved_decision = decision_repository.save(decision=decision)

    it_was_deleted = decision_repository.delete(decision=saved_decision)

    returned_decision = decision_repository.get_by_id(decision_id=saved_decision._id)

    assert it_was_deleted

    assert not returned_decision


def test_sql_decision_repository_returns_false_when_decision_is_not_deleted():
    event = Event(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        timestamp=1700000000,
    )
    rule = Rule(
        name="ALWAYS_APPLIES",
        condition_field=EventField.EVENT_TYPE,
        condition_operator=RuleOperator.EQUALS,
        condition_value="USER_CREATED",
        outcome=DecisionOutcome.APPROVED,
    )
    decision_engine = DecisionEngine()
    decision = decision_engine.decide(event=event, rules=[rule])
    decision_repository = SqlDecisionRepository(session=SessionLocal())

    it_was_deleted = decision_repository.delete(decision=decision)

    assert not it_was_deleted


def test_sql_decision_repository_returns_decision_when_id_exists():
    event = Event(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        timestamp=1700000000,
    )
    rule = Rule(
        name="ALWAYS_APPLIES",
        condition_field=EventField.EVENT_TYPE,
        condition_operator=RuleOperator.EQUALS,
        condition_value="USER_CREATED",
        outcome=DecisionOutcome.APPROVED,
    )
    decision_engine = DecisionEngine()
    decision = decision_engine.decide(event=event, rules=[rule])
    decision_repository = SqlDecisionRepository(session=SessionLocal())

    saved_decision = decision_repository.save(decision=decision)

    returned_decision = decision_repository.get_by_id(decision_id=saved_decision._id)

    assert assert_domain_entities_equal_structurally(a=returned_decision, b=decision)


def test_sql_decision_repository_returns_none_when_id_does_not_exist():
    event = Event(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        timestamp=1700000000,
    )
    rule = Rule(
        name="ALWAYS_APPLIES",
        condition_field=EventField.EVENT_TYPE,
        condition_operator=RuleOperator.EQUALS,
        condition_value="USER_CREATED",
        outcome=DecisionOutcome.APPROVED,
    )
    decision_engine = DecisionEngine()
    decision = decision_engine.decide(event=event, rules=[rule])
    decision_repository = SqlDecisionRepository(session=SessionLocal())

    returned_decision = decision_repository.get_by_id(decision_id=decision._id)

    assert not returned_decision


def test_sql_decision_repository_returns_a_valid_list_of_decisions():
    event = Event(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        timestamp=1700000000,
    )
    rule = Rule(
        name="ALWAYS_APPLIES",
        condition_field=EventField.EVENT_TYPE,
        condition_operator=RuleOperator.EQUALS,
        condition_value="USER_CREATED",
        outcome=DecisionOutcome.APPROVED,
    )
    decision_engine = DecisionEngine()
    decision = decision_engine.decide(event=event, rules=[rule])
    decision_repository = SqlDecisionRepository(session=SessionLocal())
    saved_decision = decision_repository.save(decision=decision)

    decisions = decision_repository.list_all()

    assert decisions

    assert isinstance(decisions, list)

    for d in decisions:
        if saved_decision._id == d._id:
            assert assert_domain_entities_equal_structurally(a=saved_decision, b=d)
