from enum import StrEnum

class DecisionResult(StrEnum):
    # enum members
    APPROVED = "approved"
    NO_MATCH = "no_match"
    REJECTED = "rejected"
