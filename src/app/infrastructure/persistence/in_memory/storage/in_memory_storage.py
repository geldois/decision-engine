from typing import Dict
from uuid import UUID

from app.domain.entities.decisions.decision import Decision
from app.domain.entities.events.event import Event
from app.domain.entities.rules.rule import Rule


class InMemoryStorage:
    def __init__(self) -> None:
        self.decisions: Dict[UUID, Decision] = {}
        self.events: Dict[UUID, Event] = {}
        self.rules: Dict[UUID, Rule] = {}
