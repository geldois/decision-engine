from uuid import UUID

from app.application.contracts.dto.dto_request import DtoRequest


class ProduceDecisionDtoRequest(DtoRequest):
    __slots__ = ("event_id",)

    def __init__(self, event_id: UUID):
        self.event_id = event_id
