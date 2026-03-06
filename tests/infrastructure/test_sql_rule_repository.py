from app.domain.decisions.decision_outcome import DecisionOutcome
from app.domain.events.event import EventField
from app.domain.rules.rule import Rule, RuleOperator
from app.infrastructure.database.engine import SessionLocal
from app.infrastructure.database.models import RuleModel
from app.infrastructure.repositories.sql_rule_repository import SqlRuleRepository
from tests.utils.domain_entity_util import assert_domain_entities_equal

# tests
def test_sql_rule_repository_assigns_id_when_rule_is_saved():
    name = "ALWAYS_APPLIES"
    condition_field = EventField.EVENT_TYPE
    condition_operator = RuleOperator.EQUALS
    condition_value = "USER_CREATED"
    outcome = DecisionOutcome.APPROVED
    rule = Rule(
        name = name, 
        condition_field = condition_field, 
        condition_operator = condition_operator, 
        condition_value = condition_value, 
        outcome = outcome
    )
    session = SessionLocal()
    rule_repository = SqlRuleRepository(session)
    
    saved_rule = rule_repository.save(rule)

    assert saved_rule is rule

    assert saved_rule.rule_id is not None
    
    assert saved_rule.rule_id == rule.rule_id

def test_sql_rule_repository_returns_rule_when_id_exists():
    name = "ALWAYS_APPLIES"
    condition_field = EventField.EVENT_TYPE
    condition_operator = RuleOperator.EQUALS
    condition_value = "USER_CREATED"
    outcome = DecisionOutcome.APPROVED
    rule = Rule(
        name = name, 
        condition_field = condition_field, 
        condition_operator = condition_operator, 
        condition_value = condition_value, 
        outcome = outcome
    )
    session = SessionLocal()
    rule_repository = SqlRuleRepository(session)
    saved_rule = rule_repository.save(rule)

    returned_rule = rule_repository.get_by_id(saved_rule.rule_id)

    assert assert_domain_entities_equal(returned_rule, saved_rule)

def test_sql_rule_repository_returns_none_when_id_does_not_exist():
    name = "ALWAYS_APPLIES"
    condition_field = EventField.EVENT_TYPE
    condition_operator = RuleOperator.EQUALS
    condition_value = "USER_CREATED"
    outcome = DecisionOutcome.APPROVED
    rule = Rule(
        name = name, 
        condition_field = condition_field, 
        condition_operator = condition_operator, 
        condition_value = condition_value, 
        outcome = outcome
    )
    session = SessionLocal()
    rule_repository = SqlRuleRepository(session)

    returned_rule = rule_repository.get_by_id(rule.rule_id)

    assert returned_rule is None

def test_sql_rule_repository_returns_true_when_rule_is_deleted():
    name = "ALWAYS_APPLIES"
    condition_field = EventField.EVENT_TYPE
    condition_operator = RuleOperator.EQUALS
    condition_value = "USER_CREATED"
    outcome = DecisionOutcome.APPROVED
    rule = Rule(
        name = name, 
        condition_field = condition_field, 
        condition_operator = condition_operator, 
        condition_value = condition_value, 
        outcome = outcome
    )
    session = SessionLocal()
    rule_repository = SqlRuleRepository(session)
    saved_rule = rule_repository.save(rule)

    it_was_deleted = rule_repository.delete(saved_rule)

    returned_rule = rule_repository.get_by_id(saved_rule.rule_id)

    assert it_was_deleted is True

    assert returned_rule is None

def test_sql_rule_repository_returns_false_when_rule_is_not_deleted():
    name = "ALWAYS_APPLIES"
    condition_field = EventField.EVENT_TYPE
    condition_operator = RuleOperator.EQUALS
    condition_value = "USER_CREATED"
    outcome = DecisionOutcome.APPROVED
    rule = Rule(
        name = name, 
        condition_field = condition_field, 
        condition_operator = condition_operator, 
        condition_value = condition_value, 
        outcome = outcome
    )
    session = SessionLocal()
    rule_repository = SqlRuleRepository(session)

    it_was_deleted = rule_repository.delete(rule)

    assert it_was_deleted is False
