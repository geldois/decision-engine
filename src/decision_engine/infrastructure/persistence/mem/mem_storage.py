from __future__ import annotations

from copy import deepcopy
from uuid import UUID

from decision_engine.domain.entities.decision import Decision
from decision_engine.domain.entities.event import Event
from decision_engine.domain.entities.rule import Rule


class MemStorage:
    def __init__(self) -> None:
        self.decisions: dict[UUID, Decision] = {}
        self.events: dict[UUID, Event] = {}
        self.rules: dict[UUID, Rule] = {}

    def backup(self) -> MemStorage:
        return deepcopy(self)

    def clear(self) -> None:
        self.decisions.clear()
        self.events.clear()
        self.rules.clear()

    def update(self, new_storage: MemStorage) -> None:
        self.decisions.update(deepcopy(new_storage.decisions))
        self.events.update(deepcopy(new_storage.events))
        self.rules.update(deepcopy(new_storage.rules))
