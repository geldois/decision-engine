from app.domain.entities.rule import Rule
from app.domain.value_objects.decision_outcome import DecisionOutcome
from app.domain.value_objects.event_field import EventField
from app.domain.value_objects.rule_operator import RuleOperator
from app.infrastructure.persistence.in_memory.repositories.in_memory_rule_repository import (
    InMemoryRuleRepository,
)
from app.infrastructure.persistence.in_memory.storage.in_memory_storage import (
    InMemoryStorage,
)


# ==========
# valid cases
# ==========
def test_in_memory_rule_repository_returns_saved_rule() -> None:
    rule = Rule(
        name="ALWAYS_APPLIES",
        condition_field=EventField.EVENT_TYPE,
        condition_operator=RuleOperator.EQUALS,
        condition_value="USER_CREATED",
        outcome=DecisionOutcome.APPROVED,
        priority=0,
    )
    rule_repository = InMemoryRuleRepository(in_memory_storage=InMemoryStorage())
    saved_rule = rule_repository.save(rule)

    assert saved_rule is rule


def test_in_memory_rule_repository_returns_rule_when_id_exists() -> None:
    rule = Rule(
        name="ALWAYS_APPLIES",
        condition_field=EventField.EVENT_TYPE,
        condition_operator=RuleOperator.EQUALS,
        condition_value="USER_CREATED",
        outcome=DecisionOutcome.APPROVED,
        priority=0,
    )
    rule_repository = InMemoryRuleRepository(in_memory_storage=InMemoryStorage())
    rule_repository.save(rule=rule)

    returned_rule = rule_repository.get_by_id(rule_id=rule.id)

    assert returned_rule is rule


def test_in_memory_rule_repository_returns_none_when_id_does_not_exist() -> None:
    rule = Rule(
        name="ALWAYS_APPLIES",
        condition_field=EventField.EVENT_TYPE,
        condition_operator=RuleOperator.EQUALS,
        condition_value="USER_CREATED",
        outcome=DecisionOutcome.APPROVED,
        priority=0,
    )
    rule_repository = InMemoryRuleRepository(in_memory_storage=InMemoryStorage())

    returned_rule = rule_repository.get_by_id(rule_id=rule.id)

    assert not returned_rule


def test_in_memory_rule_repository_returns_true_when_rule_is_deleted() -> None:
    rule = Rule(
        name="ALWAYS_APPLIES",
        condition_field=EventField.EVENT_TYPE,
        condition_operator=RuleOperator.EQUALS,
        condition_value="USER_CREATED",
        outcome=DecisionOutcome.APPROVED,
        priority=0,
    )
    rule_repository = InMemoryRuleRepository(in_memory_storage=InMemoryStorage())
    rule_repository.save(rule=rule)

    it_was_deleted = rule_repository.delete(rule=rule)

    returned_rule = rule_repository.get_by_id(rule_id=rule.id)

    assert it_was_deleted

    assert not returned_rule


def test_in_memory_rule_repository_returns_false_when_rule_is_not_deleted() -> None:
    rule = Rule(
        name="ALWAYS_APPLIES",
        condition_field=EventField.EVENT_TYPE,
        condition_operator=RuleOperator.EQUALS,
        condition_value="USER_CREATED",
        outcome=DecisionOutcome.APPROVED,
        priority=0,
    )
    rule_repository = InMemoryRuleRepository(in_memory_storage=InMemoryStorage())

    it_was_deleted = rule_repository.delete(rule=rule)

    assert not it_was_deleted


def test_in_memory_rule_repository_returns_list_of_rules() -> None:
    rule = Rule(
        name="ALWAYS_APPLIES",
        condition_field=EventField.EVENT_TYPE,
        condition_operator=RuleOperator.EQUALS,
        condition_value="USER_CREATED",
        outcome=DecisionOutcome.APPROVED,
        priority=0,
    )
    rule_repository = InMemoryRuleRepository(in_memory_storage=InMemoryStorage())
    rule_repository.save(rule=rule)

    rules = rule_repository.list_all()

    assert isinstance(rules, list)

    assert rule in rules
