from uuid import UUID

from pydantic import BaseModel


class RegisterRuleHttpResponse(BaseModel):
    name: str
    outcome: str
    rule_id: UUID
