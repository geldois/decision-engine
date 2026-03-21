from uuid import UUID, uuid4


class DomainEntity:
    def __init__(self, entity_id: UUID | None) -> None:
        self.id = entity_id if entity_id else uuid4()
