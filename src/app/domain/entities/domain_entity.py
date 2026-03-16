from uuid import UUID, uuid4


class DomainEntity:
    __slots__: tuple[str, ...]

    def __init__(self, entity_id: UUID | None):
        self.id = entity_id if entity_id else uuid4()
