from app.application.types.rule_operator import RuleOperator as DtoRuleOperator
from app.domain.entities.rules.rule import RuleOperator

# tests
def test_dto_rule_operator_values_are_valid_rule_operators():
    assert {member.name for member in DtoRuleOperator} == {member.name for member in RuleOperator}
    