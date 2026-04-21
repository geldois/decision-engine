from __future__ import annotations

from copy import deepcopy
from uuid import UUID

from app.domain.entities.decision import Decision
from app.domain.entities.event import Event
from app.domain.entities.rule import Rule


class InMemoryStorage:
    def __init__(self) -> None:
        self.decisions: dict[UUID, Decision] = {}
        self.events: dict[UUID, Event] = {}
        self.rules: dict[UUID, Rule] = {}

    def backup(self) -> InMemoryStorage:
        return deepcopy(self)

    def clear(self) -> None:
        self.decisions.clear()
        self.events.clear()
        self.rules.clear()

    def update(self, new_storage: InMemoryStorage) -> None:
        self.decisions.update(deepcopy(new_storage.decisions))
        self.events.update(deepcopy(new_storage.events))
        self.rules.update(deepcopy(new_storage.rules))
