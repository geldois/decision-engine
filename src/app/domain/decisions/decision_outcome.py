from enum import Enum

class DecisionOutcome(Enum):
    APPROVED = "approved"
    NO_MATCH = "no_match"
    REJECTED = "rejected"
    