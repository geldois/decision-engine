from uuid import UUID


class ProduceDecisionDtoRequest:
    __slots__ = ("event_id",)

    def __init__(self, event_id: UUID):
        self.event_id = event_id
