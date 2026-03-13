from app.application.types.rule_operator import RuleOperator as DtoRuleOperator
from app.domain.entities.rules.rule import RuleOperator

_MAPPING = {
    RuleOperator.EQUALS: DtoRuleOperator.EQUALS,
    RuleOperator.NOT_EQUALS: DtoRuleOperator.NOT_EQUALS,
    RuleOperator.LESS_THAN: DtoRuleOperator.LESS_THAN,
    RuleOperator.GREATER_THAN: DtoRuleOperator.GREATER_THAN,
}


def map_rule_operator_to_dto(rule_operator: RuleOperator) -> DtoRuleOperator:
    return _MAPPING[rule_operator]


def map_rule_operator_to_domain(rule_operator: DtoRuleOperator | str) -> RuleOperator:
    if isinstance(rule_operator, DtoRuleOperator):
        return RuleOperator(rule_operator.value)

    return RuleOperator(rule_operator)
