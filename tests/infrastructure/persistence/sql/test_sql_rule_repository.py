from app.bootstrap.bootstrap import build_dev_session_factory
from app.domain.entities.rule import Rule
from app.domain.value_objects.conditions.simple_condition import SimpleCondition
from app.domain.value_objects.decision_outcome import DecisionOutcome
from app.domain.value_objects.event_field import EventField
from app.domain.value_objects.operators.comparison_operator import ComparisonOperator
from app.infrastructure.persistence.sql.repositories.sql_rule_repository import (
    SqlRuleRepository,
)


# ==========
# valid cases
# ==========
def test_sql_rule_repository_returns_saved_rule() -> None:
    rule = Rule(
        name="ALWAYS_APPLIES",
        condition=SimpleCondition(
            operator=ComparisonOperator.EQUALS,
            field=EventField.EVENT_TYPE,
            value="USER_CREATED",
        ),
        outcome=DecisionOutcome.APPROVED,
        priority=0,
    )
    session_factory = build_dev_session_factory()
    rule_repository = SqlRuleRepository(session=session_factory())

    saved_rule = rule_repository.save(rule=rule)

    assert saved_rule is rule


def test_sql_rule_repository_returns_rule_when_id_exists() -> None:
    rule = Rule(
        name="ALWAYS_APPLIES",
        condition=SimpleCondition(
            operator=ComparisonOperator.EQUALS,
            field=EventField.EVENT_TYPE,
            value="USER_CREATED",
        ),
        outcome=DecisionOutcome.APPROVED,
        priority=0,
    )
    session_factory = build_dev_session_factory()
    rule_repository = SqlRuleRepository(session=session_factory())
    rule_repository.save(rule=rule)

    returned_rule = rule_repository.get_by_id(rule_id=rule.id)

    assert returned_rule

    assert returned_rule.is_structurally_equal(other=rule)


def test_sql_rule_repository_returns_none_when_id_does_not_exist() -> None:
    rule = Rule(
        name="ALWAYS_APPLIES",
        condition=SimpleCondition(
            operator=ComparisonOperator.EQUALS,
            field=EventField.EVENT_TYPE,
            value="USER_CREATED",
        ),
        outcome=DecisionOutcome.APPROVED,
        priority=0,
    )
    session_factory = build_dev_session_factory()
    rule_repository = SqlRuleRepository(session=session_factory())

    returned_rule = rule_repository.get_by_id(rule_id=rule.id)

    assert not returned_rule


def test_sql_rule_repository_returns_true_when_rule_is_deleted() -> None:
    rule = Rule(
        name="ALWAYS_APPLIES",
        condition=SimpleCondition(
            operator=ComparisonOperator.EQUALS,
            field=EventField.EVENT_TYPE,
            value="USER_CREATED",
        ),
        outcome=DecisionOutcome.APPROVED,
        priority=0,
    )
    session_factory = build_dev_session_factory()
    rule_repository = SqlRuleRepository(session=session_factory())
    rule_repository.save(rule=rule)

    it_was_deleted = rule_repository.delete(rule=rule)

    returned_rule = rule_repository.get_by_id(rule_id=rule.id)

    assert it_was_deleted

    assert not returned_rule


def test_sql_rule_repository_returns_false_when_rule_is_not_deleted() -> None:
    rule = Rule(
        name="ALWAYS_APPLIES",
        condition=SimpleCondition(
            operator=ComparisonOperator.EQUALS,
            field=EventField.EVENT_TYPE,
            value="USER_CREATED",
        ),
        outcome=DecisionOutcome.APPROVED,
        priority=0,
    )
    session_factory = build_dev_session_factory()
    rule_repository = SqlRuleRepository(session=session_factory())

    it_was_deleted = rule_repository.delete(rule=rule)

    assert not it_was_deleted


def test_sql_rule_repository_returns_list_of_rules() -> None:
    rule = Rule(
        name="ALWAYS_APPLIES",
        condition=SimpleCondition(
            operator=ComparisonOperator.EQUALS,
            field=EventField.EVENT_TYPE,
            value="USER_CREATED",
        ),
        outcome=DecisionOutcome.APPROVED,
        priority=0,
    )
    session_factory = build_dev_session_factory()
    rule_repository = SqlRuleRepository(session=session_factory())
    rule_repository.save(rule=rule)

    rules = rule_repository.list_all()

    assert isinstance(rules, list)

    for r in rules:
        if r == rule:
            assert r.is_structurally_equal(other=rule)
