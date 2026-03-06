from typing import Iterable

from app.domain.domain_entity import DomainEntity

# functions
def assert_domain_entities_equal(
    a = DomainEntity, 
    b = DomainEntity
) -> bool:
    return tuple(not callable(getattr(a, slot)) for slot in type(a).__slots__) == tuple(not callable(getattr(b, slot)) for slot in type(b).__slots__)
