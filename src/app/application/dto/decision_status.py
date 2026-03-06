from enum import StrEnum

class DecisionStatus(StrEnum):
    # enum members
    APPROVED = "approved"
    NO_MATCH = "no_match"
    REJECTED = "rejected"
