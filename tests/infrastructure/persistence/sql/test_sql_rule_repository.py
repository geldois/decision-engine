from utils.domain_entity_util import compare_domain_entities

from app.bootstrap.bootstrap import build_dev_session_factory
from app.domain.entities.rule import Rule
from app.domain.value_objects.decision_outcome import DecisionOutcome
from app.domain.value_objects.event_field import EventField
from app.domain.value_objects.rule_operator import RuleOperator
from app.infrastructure.persistence.sql.repositories.sql_rule_repository import (
    SqlRuleRepository,
)


# ==========
# valid cases
# ==========
def test_sql_rule_repository_returns_saved_rule() -> None:
    rule = Rule(
        name="ALWAYS_APPLIES",
        condition_field=EventField.EVENT_TYPE,
        condition_operator=RuleOperator.EQUALS,
        condition_value="USER_CREATED",
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
        condition_field=EventField.EVENT_TYPE,
        condition_operator=RuleOperator.EQUALS,
        condition_value="USER_CREATED",
        outcome=DecisionOutcome.APPROVED,
        priority=0,
    )
    session_factory = build_dev_session_factory()
    rule_repository = SqlRuleRepository(session=session_factory())
    rule_repository.save(rule=rule)

    returned_rule = rule_repository.get_by_id(rule_id=rule.id)

    assert compare_domain_entities(a=returned_rule, b=rule)


def test_sql_rule_repository_returns_none_when_id_does_not_exist() -> None:
    rule = Rule(
        name="ALWAYS_APPLIES",
        condition_field=EventField.EVENT_TYPE,
        condition_operator=RuleOperator.EQUALS,
        condition_value="USER_CREATED",
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
        condition_field=EventField.EVENT_TYPE,
        condition_operator=RuleOperator.EQUALS,
        condition_value="USER_CREATED",
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
        condition_field=EventField.EVENT_TYPE,
        condition_operator=RuleOperator.EQUALS,
        condition_value="USER_CREATED",
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
        condition_field=EventField.EVENT_TYPE,
        condition_operator=RuleOperator.EQUALS,
        condition_value="USER_CREATED",
        outcome=DecisionOutcome.APPROVED,
        priority=0,
    )
    session_factory = build_dev_session_factory()
    rule_repository = SqlRuleRepository(session=session_factory())
    rule_repository.save(rule=rule)

    rules = rule_repository.list_all()

    assert isinstance(rules, list)

    for r in rules:
        if r.id == rule.id:
            assert compare_domain_entities(a=r, b=rule)
