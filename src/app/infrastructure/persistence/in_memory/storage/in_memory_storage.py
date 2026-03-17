from functools import partial
from typing import Dict
from uuid import UUID

from app.domain.entities.decisions.decision import Decision
from app.domain.entities.events.event import Event
from app.domain.entities.rules.rule import Rule


class InMemoryStorage:
    def __init__(
        self,
        decisions: Dict[UUID, Decision] | None = None,
        events: Dict[UUID, Event] | None = None,
        rules: Dict[UUID, Rule] | None = None,
    ):
        self.decisions: Dict[UUID, Decision] = {}
        self.events: Dict[UUID, Event] = {}
        self.rules: Dict[UUID, Rule] = {}


in_memory_storage_factory = partial(InMemoryStorage)
