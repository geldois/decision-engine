from app.domain.decisions.decision import Decision
from app.domain.decisions.decision_outcome import DecisionOutcome
from app.domain.events.event import Event
from app.domain.rules.rule import Rule

class DecisionEngine:
    # methods
    def decide(
        self, 
        event: Event, 
        rules: list[Rule]
    ) -> Decision:
        for rule in rules:
            if rule.applies_to(event):
                outcome = rule.outcome
                explanation = "Rule applied to Event."

                return Decision(
                    event_id = event._id, 
                    rule_id = rule._id, 
                    outcome = outcome, 
                    explanation = explanation
                )
            
        outcome = DecisionOutcome.NO_MATCH
        explanation = "No Rule applied to Event."

        return Decision(
            event_id = event._id, 
            rule_id = None, 
            outcome = outcome, 
            explanation = explanation
        )
    
