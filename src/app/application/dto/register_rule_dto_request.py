class RegisterRuleDtoRequest:
    __slots__ = (
        "condition_field", 
        "condition_operator", 
        "condition_value", 
        "name", 
        "outcome"
    )

    # initializer
    def __init__(
        self, 
        name: str, 
        condition_field: str, 
        condition_operator: str,
        condition_value: int | str, 
        outcome: str
    ):
        self.name = name
        self.condition_field = condition_field
        self.condition_operator = condition_operator
        self.condition_value = condition_value
        self.outcome = outcome
        