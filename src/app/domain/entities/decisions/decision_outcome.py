from enum import Enum

class DecisionOutcome(Enum):
    # enum members
    APPROVED = "approved"
    NO_MATCH = "no_match"
    REJECTED = "rejected"
    