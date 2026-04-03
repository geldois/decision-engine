from datetime import UTC, datetime
from uuid import UUID, uuid4

from app.domain.entities.domain_entity import DomainEntity


# ==========
# valid cases
# ==========
def test_domain_entity_assigns_attributes_when_none_provided() -> None:
    domain_entity = DomainEntity(created_at=None, entity_id=None)

    assert domain_entity.created_at

    assert domain_entity.created_at.tzinfo

    assert isinstance(domain_entity.created_at, datetime)

    assert domain_entity.id

    assert isinstance(domain_entity.id, UUID)


def test_domain_entity_assigns_same_datetime_when_created_at_exists() -> None:
    created_at = datetime.now(UTC)

    domain_entity = DomainEntity(created_at=created_at, entity_id=None)

    assert domain_entity.created_at == created_at


def test_domain_entity_assigns_same_uuid_when_entity_id_exists() -> None:
    uuid = uuid4()

    domain_entity = DomainEntity(created_at=None, entity_id=uuid)

    assert domain_entity.id == uuid
