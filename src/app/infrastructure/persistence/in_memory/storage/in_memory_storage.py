from uuid import UUID

from app.domain.entities.decision import Decision
from app.domain.entities.event import Event
from app.domain.entities.rule import Rule


class InMemoryStorage:
    def __init__(self) -> None:
        self.decisions: dict[UUID, Decision] = {}
        self.events: dict[UUID, Event] = {}
        self.rules: dict[UUID, Rule] = {}
