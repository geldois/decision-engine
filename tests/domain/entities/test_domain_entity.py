from uuid import UUID, uuid4

from app.domain.entities.domain_entity import DomainEntity


# ==========
# valid cases
# ==========
def test_domain_entity_assigns_uuid_when_entity_id_is_none() -> None:
    domain_entity = DomainEntity(entity_id=None)

    assert domain_entity.id

    assert isinstance(domain_entity.id, UUID)


def test_domain_entity_assigns_same_uuid_when_entity_id_exists() -> None:
    uuid = uuid4()

    domain_entity = DomainEntity(entity_id=uuid)

    assert domain_entity.id == uuid
