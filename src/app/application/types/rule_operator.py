from enum import StrEnum

class RuleOperator(StrEnum):
    # enum members
    EQUALS = "=="
    NOT_EQUALS = "!="
    LESS_THAN = "<"
    GREATER_THAN = ">"
    