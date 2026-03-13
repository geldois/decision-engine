from pydantic import BaseModel


class RegisterRuleHttpRequest(BaseModel):
    name: str
    condition_field: str
    condition_operator: str
    condition_value: int | str
    outcome: str
