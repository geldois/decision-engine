from datetime import UTC, datetime
from uuid import UUID, uuid4


class DomainEntity:
    def __init__(self, created_at: datetime | None, entity_id: UUID | None) -> None:
        if created_at is None:
            self.created_at = datetime.now(UTC)
        elif created_at.tzinfo is None:
            self.created_at = created_at.replace(tzinfo=UTC)
        else:
            self.created_at = created_at

        self.id = entity_id if entity_id else uuid4()
