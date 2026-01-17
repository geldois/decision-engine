from app.domain.events.event import Event
from app.domain.rules.rule import Rule
from app.domain.decisions.decision import Decision

class DecisionService:
    # methods
    def decide(
        self, 
        event: Event, 
        rules: list[Rule]
    ):
        for rule in rules:
            if rule.applies_to(event):
                outcome = rule.outcome
                explanation = "Rule applied to Event."

                return Decision(
                    event, 
                    rule, 
                    outcome, 
                    explanation
                )
        outcome = "rejected"
        explanation = "No Rule applied do Event."

        return Decision(
            event = event, 
            rule = None, 
            outcome = outcome, 
            explanation = explanation
        )
