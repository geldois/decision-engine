from app.domain.decisions.decision_outcome import DecisionOutcome
from app.domain.events.event import EventField
from app.domain.rules.rule import Rule, RuleOperator
from app.infrastructure.repositories.in_memory_rule_repository import InMemoryRuleRepository

# tests
def test_in_memory_rule_repository_assigns_correct_id_when_rule_is_saved():
    rule = Rule(
        name = "ALWAYS_APPLIES", 
        condition_field = EventField.EVENT_TYPE, 
        condition_operator = RuleOperator.EQUALS, 
        condition_value = "USER_CREATED", 
        outcome = DecisionOutcome.APPROVED
    )
    rule_repository = InMemoryRuleRepository()
    saved_rule = rule_repository.save(rule)

    assert saved_rule is rule

    assert saved_rule._id

    assert saved_rule._id == rule._id

def test_in_memory_rule_repository_returns_rule_when_id_exists():
    rule = Rule(
        name = "ALWAYS_APPLIES", 
        condition_field = EventField.EVENT_TYPE, 
        condition_operator = RuleOperator.EQUALS, 
        condition_value = "USER_CREATED", 
        outcome = DecisionOutcome.APPROVED
    )
    rule_repository = InMemoryRuleRepository()
    saved_rule = rule_repository.save(rule = rule)

    returned_rule = rule_repository.get_by_id(rule_id = saved_rule._id)

    assert returned_rule is saved_rule

def test_in_memory_rule_repository_returns_none_when_id_does_not_exist():
    rule = Rule(
        name = "ALWAYS_APPLIES", 
        condition_field = EventField.EVENT_TYPE, 
        condition_operator = RuleOperator.EQUALS, 
        condition_value = "USER_CREATED", 
        outcome = DecisionOutcome.APPROVED
    )
    rule_repository = InMemoryRuleRepository()

    returned_rule = rule_repository.get_by_id(rule_id = rule._id)

    assert not returned_rule

def test_in_memory_rule_repository_returns_true_when_rule_is_deleted():
    rule = Rule(
        name = "ALWAYS_APPLIES", 
        condition_field = EventField.EVENT_TYPE, 
        condition_operator = RuleOperator.EQUALS, 
        condition_value = "USER_CREATED", 
        outcome = DecisionOutcome.APPROVED
    )
    rule_repository = InMemoryRuleRepository()
    saved_rule = rule_repository.save(rule = rule)

    it_was_deleted = rule_repository.delete(rule = saved_rule)

    returned_rule = rule_repository.get_by_id(rule_id = saved_rule._id)

    assert it_was_deleted

    assert not returned_rule

def test_in_memory_rule_repository_returns_false_when_rule_is_not_deleted():
    rule = Rule(
        name = "ALWAYS_APPLIES", 
        condition_field = EventField.EVENT_TYPE, 
        condition_operator = RuleOperator.EQUALS, 
        condition_value = "USER_CREATED", 
        outcome = DecisionOutcome.APPROVED
    )
    rule_repository = InMemoryRuleRepository()

    it_was_deleted = rule_repository.delete(rule = rule)

    assert not it_was_deleted

def test_in_memory_rule_repository_returns_list_of_rules():
    rule = Rule(
        name = "ALWAYS_APPLIES", 
        condition_field = EventField.EVENT_TYPE, 
        condition_operator = RuleOperator.EQUALS, 
        condition_value = "USER_CREATED", 
        outcome = DecisionOutcome.APPROVED
    )
    rule_repository = InMemoryRuleRepository()
    saved_rule = rule_repository.save(rule = rule)

    rules = rule_repository.list_all()

    assert rules

    assert isinstance(rules, list)

    assert saved_rule in rules
