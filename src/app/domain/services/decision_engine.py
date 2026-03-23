from app.domain.entities.decision import Decision
from app.domain.entities.event import Event
from app.domain.entities.rule import Rule
from app.domain.value_objects.decision_outcome import DecisionOutcome


class DecisionEngine:
    def decide(self, event: Event, rules: list[Rule]) -> Decision:
        for rule in rules:
            if rule.applies_to(event):
                outcome = rule.outcome
                explanation = "Event <ID: " + str(event.id) + "> " + str(outcome.value)

                return Decision(
                    event_id=event.id,
                    rule_id=rule.id,
                    outcome=outcome,
                    explanation=explanation,
                )

        outcome = DecisionOutcome.NO_MATCH
        explanation = "Event <ID: " + str(event.id) + "> " + str(outcome.value)

        return Decision(
            event_id=event.id, rule_id=None, outcome=outcome, explanation=explanation
        )
