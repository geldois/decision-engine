from typing import Dict
from uuid import UUID

from app.domain.entities.decisions.decision import Decision
from app.domain.entities.events.event import Event
from app.domain.entities.rules.rule import Rule


class InMemoryStorage:
    def __init__(
        self,
        _decisions: Dict[UUID, Decision],
        _events: Dict[UUID, Event],
        _rules: Dict[UUID, Rule],
    ):
        self._decisions = _decisions
        self._events = _events
        self._rules = _rules
