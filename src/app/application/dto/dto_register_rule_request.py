from dataclasses import dataclass


@dataclass(frozen=True)
class DTORegisterRuleRequest:
    name: str
    condition_field: str
    condition_operator: str
    condition_value: int | str
    outcome: str
