from app.application.mappers.rule_operator_mapper import (
    map_rule_operator_to_domain,
    map_rule_operator_to_dto,
)
from app.application.types.rule_operator import RuleOperator as DtoRuleOperator
from app.domain.value_objects.rule_operator import RuleOperator


# ==========
# valid
# ==========
def test_map_rule_operator_to_dto_returns_valid_dto_rule_operators():
    for member in RuleOperator:
        assert map_rule_operator_to_dto(member) is DtoRuleOperator[member.name]


def test_map_rule_operator_to_domain_returns_valid_domain_rule_operators():
    for member in DtoRuleOperator:
        assert map_rule_operator_to_domain(member) is RuleOperator(member.value)
