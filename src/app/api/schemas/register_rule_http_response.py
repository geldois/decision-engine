from pydantic import BaseModel
from uuid import UUID

class RegisterRuleHttpResponse(BaseModel):
    name: str
    outcome: str
    rule_id: UUID
    