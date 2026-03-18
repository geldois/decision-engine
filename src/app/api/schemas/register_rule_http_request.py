from app.api.contracts.schemas.http_contract import HttpContract


class RegisterRuleHttpRequest(HttpContract):
    name: str
    condition_field: str
    condition_operator: str
    condition_value: int | str
    outcome: str
