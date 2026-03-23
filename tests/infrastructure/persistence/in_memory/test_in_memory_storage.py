from app.infrastructure.persistence.in_memory.storage.in_memory_storage import (
    InMemoryStorage,
)


# ==========
# valid cases
# ==========
def test_in_memory_storage_creates_empty_dicts() -> None:
    in_memory_storage = InMemoryStorage()

    assert not in_memory_storage.decisions

    assert not in_memory_storage.events

    assert not in_memory_storage.rules
