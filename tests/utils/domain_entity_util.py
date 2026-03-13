from app.domain.entities.domain_entity import DomainEntity


def compare_domain_entities(a: DomainEntity, b: DomainEntity) -> bool:
    return a.__dict__ == b.__dict__
