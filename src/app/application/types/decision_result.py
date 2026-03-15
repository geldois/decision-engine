from enum import StrEnum


class DecisionResult(StrEnum):
    APPROVED = "approved"
    NO_MATCH = "no_match"
    REJECTED = "rejected"
