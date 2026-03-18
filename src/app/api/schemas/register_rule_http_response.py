from uuid import UUID

from app.api.contracts.schemas.http_contract import HttpContract


class RegisterRuleHttpResponse(HttpContract):
    name: str
    outcome: str
    rule_id: UUID
