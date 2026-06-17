from pydantic import BaseModel


class HTTPRegisterRuleRequest(BaseModel):
    name: str
    condition: dict[str, object]
    outcome: str
    priority: int
