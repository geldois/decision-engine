from uuid import UUID

from pydantic import BaseModel


class HTTPRegisterRuleResponse(BaseModel):
    name: str
    condition: dict[str, object]
    outcome: str
    priority: int
    rule_id: UUID
