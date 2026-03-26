from enum import Enum

from app.domain.exceptions.decisions.decision_exception import DecisionException
from app.domain.exceptions.events.event_exception import EventException
from app.domain.exceptions.rules.rule_exception import RuleException


class ApplicationError(Enum):
    # DecisionException
    DECISION_EXPLANATION_INVALID = DecisionException
    EVENT_INVALID = EventException
    RULE_INVALID = RuleException
