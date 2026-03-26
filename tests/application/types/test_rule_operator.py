from app.application.types.rule_operator import RuleOperator as DtoRuleOperator
from app.domain.value_objects.rule_operator import RuleOperator


# ==========
# valid
# ==========
def test_dto_rule_operator_values_are_valid_rule_operators():
    assert {member.name for member in DtoRuleOperator} == {
        member.name for member in RuleOperator
    }
