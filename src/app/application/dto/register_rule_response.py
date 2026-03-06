from dataclasses import dataclass

from app.domain.decisions.decision_outcome import DecisionOutcome

@dataclass(frozen = True)
class RegisterRuleResponse:
    rule_id: int
    outcome: DecisionOutcome
    