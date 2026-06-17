from collections.abc import Callable

from decision_engine.domain.entities.event import Event
from decision_engine.domain.entities.rule import Rule
from decision_engine.domain.services.decision_engine import DecisionEngine
from decision_engine.domain.value_objects.condition import CompositeCondition, SimpleCondition
from decision_engine.domain.value_objects.decision_outcome import DecisionOutcome
from decision_engine.domain.value_objects.decision_trace import (
    CompositeDecisionTrace,
    SimpleDecisionTrace,
)
from decision_engine.domain.value_objects.event_field import EventField
from decision_engine.domain.value_objects.operators.comparison_operator import ComparisonOperator
from decision_engine.domain.value_objects.operators.logical_operator import LogicalOperator

# VALID CASES


def test_decision_engine_returns_sorted_list_of_rules_by_priority(
    rule_factory: Callable[..., Rule],
) -> None:
    third_priority_rule = rule_factory(priority=0)
    second_priority_rule = rule_factory(priority=1)
    first_priority_rule = rule_factory(priority=2)

    sorted_rules = DecisionEngine.sort_by_priority(
        rules=[third_priority_rule, second_priority_rule, first_priority_rule]
    )

    assert (
        sorted_rules[0] == first_priority_rule
        and sorted_rules[1] == second_priority_rule
        and sorted_rules[2] == third_priority_rule
    )


def test_decision_engine_returns_valid_decision_when_rule_applies() -> None:
    event = Event(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        occurred_at=1700000000,
    )
    composite_rule = Rule(
        name="NEVER_APPLIES",
        condition=CompositeCondition(
            operator=LogicalOperator.AND,
            conditions=[
                SimpleCondition(
                    operator=ComparisonOperator.EQUALS,
                    field=EventField.EVENT_TYPE,
                    value="TEST",
                ),
                SimpleCondition(
                    operator=ComparisonOperator.EQUALS,
                    field=EventField.PAYLOAD,
                    value={"user_id": 123, "email": "user@email.com"},
                ),
            ],
        ),
        outcome=DecisionOutcome.APPROVED,
        priority=1,
    )
    simple_rule = Rule(
        name="ALWAYS_APPLIES",
        condition=SimpleCondition(
            operator=ComparisonOperator.EQUALS,
            field=EventField.EVENT_TYPE,
            value="USER_CREATED",
        ),
        outcome=DecisionOutcome.APPROVED,
        priority=0,
    )

    decision = DecisionEngine.decide(event=event, rules=[composite_rule, simple_rule])

    assert decision.event_id == event.id

    assert decision.rule_id == simple_rule.id

    assert decision.outcome is simple_rule.outcome

    assert decision.traces == (
        CompositeDecisionTrace(
            result=False,
            operator=LogicalOperator.AND,
            traces=(
                SimpleDecisionTrace(
                    result=False,
                    operator=ComparisonOperator.EQUALS,
                    field=EventField.EVENT_TYPE,
                    expected_value="TEST",
                    actual_value="USER_CREATED",
                ),
                SimpleDecisionTrace(
                    result=True,
                    operator=ComparisonOperator.EQUALS,
                    field=EventField.PAYLOAD,
                    expected_value={"user_id": 123, "email": "user@email.com"},
                    actual_value={"user_id": 123, "email": "user@email.com"},
                ),
            ),
        ),
        SimpleDecisionTrace(
            result=True,
            operator=ComparisonOperator.EQUALS,
            field=EventField.EVENT_TYPE,
            expected_value="USER_CREATED",
            actual_value="USER_CREATED",
        ),
    )


def test_decision_engine_returns_valid_decision_when_no_rule_applies() -> None:
    event = Event(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        occurred_at=1700000000,
    )
    composite_rule = Rule(
        name="NEVER_APPLIES",
        condition=CompositeCondition(
            operator=LogicalOperator.AND,
            conditions=[
                SimpleCondition(
                    operator=ComparisonOperator.EQUALS,
                    field=EventField.EVENT_TYPE,
                    value="TEST",
                ),
                SimpleCondition(
                    operator=ComparisonOperator.EQUALS,
                    field=EventField.PAYLOAD,
                    value={"user_id": 123, "email": "user@email.com"},
                ),
            ],
        ),
        outcome=DecisionOutcome.APPROVED,
        priority=1,
    )
    simple_rule = Rule(
        name="ALWAYS_APPLIES",
        condition=SimpleCondition(
            operator=ComparisonOperator.EQUALS,
            field=EventField.EVENT_TYPE,
            value="TEST",
        ),
        outcome=DecisionOutcome.APPROVED,
        priority=0,
    )

    decision = DecisionEngine.decide(event=event, rules=[composite_rule, simple_rule])

    assert decision.event_id == event.id

    assert decision.rule_id is None

    assert decision.outcome is DecisionOutcome.NO_MATCH

    assert decision.traces == (
        CompositeDecisionTrace(
            result=False,
            operator=LogicalOperator.AND,
            traces=(
                SimpleDecisionTrace(
                    result=False,
                    operator=ComparisonOperator.EQUALS,
                    field=EventField.EVENT_TYPE,
                    expected_value="TEST",
                    actual_value="USER_CREATED",
                ),
                SimpleDecisionTrace(
                    result=True,
                    operator=ComparisonOperator.EQUALS,
                    field=EventField.PAYLOAD,
                    expected_value={"user_id": 123, "email": "user@email.com"},
                    actual_value={"user_id": 123, "email": "user@email.com"},
                ),
            ),
        ),
        SimpleDecisionTrace(
            result=False,
            operator=ComparisonOperator.EQUALS,
            field=EventField.EVENT_TYPE,
            expected_value="TEST",
            actual_value="USER_CREATED",
        ),
    )


def test_decision_engine_returns_valid_decision_when_list_of_rules_is_empty(
    event_factory: Callable[..., Event],
) -> None:
    event = event_factory()
    decision = DecisionEngine.decide(event=event, rules=[])

    assert decision.event_id == event.id

    assert not decision.rule_id

    assert decision.outcome is DecisionOutcome.NO_MATCH

    assert not decision.traces
